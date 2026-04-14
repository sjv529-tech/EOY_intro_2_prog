# fetch.py
# Handles API calls with streaming support, retries, and caching
# Designed to handle intermittent connections gracefully

import requests
import json
import os
import time
from datetime import datetime

CACHE_FILE = "weather_cache.json"
CACHE_EXPIRY_SECONDS = 3600  # 1 hour — avoid hammering the API


def _is_cache_valid():
    """
    Check if a local cache file exists and is still fresh.
    Time Complexity: O(1)
    """
    if not os.path.exists(CACHE_FILE):
        return False
    cache_age = time.time() - os.path.getmtime(CACHE_FILE)
    return cache_age < CACHE_EXPIRY_SECONDS


def _load_cache():
    """Load cached API response from disk. Returns None if file is corrupt."""
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  Warning: Cache file unreadable ({e}). Will re-fetch.")
        return None


def _save_cache(data):
    """
    Write API response to cache file atomically.
    Uses a temp file + rename to prevent corruption if the program crashes mid-write.
    """
    temp_path = CACHE_FILE + ".tmp"
    try:
        with open(temp_path, "w") as f:
            json.dump(data, f)
        os.replace(temp_path, CACHE_FILE)  # atomic on all major OS
    except OSError as e:
        print(f"  Warning: Could not save cache ({e}).")


def get_weather(latitude=53.8, longitude=-1.55, retries=3, backoff=2):
    """
    Fetch 7 days of hourly weather data with retry logic and caching.

    Strategy:
      1. Return valid cache if fresh (avoids unnecessary API calls)
      2. Attempt live fetch with exponential backoff on failure
      3. Fall back to stale cache if all retries fail (no data loss)

    Time Complexity: O(1) — single API call, fixed-size response
    Space Complexity: O(n) — n = number of hourly data points returned

    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        retries (int): Max number of retry attempts
        backoff (int): Seconds between retries (doubles each attempt)
    Returns:
        dict or None: Hourly weather data, or None if totally unreachable
    """
    # Step 1: Serve from cache if still fresh
    if _is_cache_valid():
        print("  Using cached data (less than 1 hour old).")
        return _load_cache()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "past_days": 7
    }

    # Step 2: Attempt live fetch with exponential backoff
    wait = backoff
    for attempt in range(1, retries + 1):
        try:
            print(f"  Fetching live data (attempt {attempt}/{retries})...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()["hourly"]
            _save_cache(data)
            print("  Success.")
            return data

        except requests.exceptions.ConnectionError:
            print(f"  No connection. Retrying in {wait}s...")
        except requests.exceptions.Timeout:
            print(f"  Request timed out. Retrying in {wait}s...")
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error {e}. Retrying in {wait}s...")

        time.sleep(wait)
        wait *= 2  # exponential backoff: 2s, 4s, 8s...

    # Step 3: All retries failed — fall back to stale cache rather than losing data
    print("\n  All retries failed. Attempting to load stale cache as fallback...")
    stale = _load_cache()
    if stale:
        print("  Warning: Using stale cached data. Results may be outdated.")
        return stale

    print("  Error: No data available. Check your internet connection.")
    return None