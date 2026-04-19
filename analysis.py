import csv
import os

FILENAME = "weather_data.csv"

# SORTING & SEARCHING

def merge_sort(records, key):
    """
    Sort records using merge sort algorithm.

    Time Complexity:  O(n log n) — divides list in half recursively, merges in linear time
    Space Complexity: O(n)       — creates temporary sublists during merge

    Chosen over bubble sort (O(n²)) for better performance on large datasets.
    """
    if len(records) <= 1:
        return records

    mid = len(records) // 2
    left = merge_sort(records[:mid], key)
    right = merge_sort(records[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    """Merge two sorted sublists into one sorted list. O(n)."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Convert to float only for numeric keys, compare directly for string keys
        if key == "time":
            left_val = left[i][key]
            right_val = right[j][key]
        else:
            left_val = float(left[i][key])
            right_val = float(right[j][key])
            
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search_by_date(records, target_date):
    """
    Search for a record matching a target date prefix using binary search.
    Records must be sorted by time before calling this.

    Time Complexity:  O(log n) — halves search space each iteration
    Space Complexity: O(1)     — no extra memory needed

    Much faster than linear search O(n) on large datasets.

    Args:
        records (list): List of dicts sorted by 'time' key
        target_date (str): Date string prefix e.g. '2026-04-14'
    Returns:
        list: All matching records for that date
    """
    if not records:
        return []
        
    lo, hi = 0, len(records) - 1
    matches = []

    # Find any record matching the date
    while lo <= hi:
        mid = (lo + hi) // 2
        record_date = records[mid]["time"][:10]  # take YYYY-MM-DD portion

        if record_date == target_date:
            # Found one match — expand outward to find all matches for that day
            left = mid
            while left > 0 and records[left - 1]["time"][:10] == target_date:
                left -= 1
            right = mid
            while right < len(records) - 1 and records[right + 1]["time"][:10] == target_date:
                right += 1
            matches = records[left:right + 1]
            break
        elif record_date < target_date:
            lo = mid + 1
        else:
            hi = mid - 1

    return matches


def find_extremes(records):
    """
    Find and display the hottest and coldest recorded entries using merge sort.
    Time Complexity: O(n log n) due to merge sort.
    """
    if not records:
        print("No data to analyse.")
        return

    # Make a copy to avoid modifying original
    records_copy = records.copy()
    sorted_records = merge_sort(records_copy, key="temperature")
    
    # Check if we have valid temperature data
    if not sorted_records:
        print("No valid temperature data found.")
        return
        
    coldest = sorted_records[0]
    hottest = sorted_records[-1]

    print(f"\n  Hottest: {hottest['time']}  →  {hottest['temperature']}°C")
    print(f"  Coldest: {coldest['time']}  →  {coldest['temperature']}°C")

# PREDICTION ALGORITHM — Linear Regression (implemented from scratch)

def _mean(values):
    """Calculate arithmetic mean. O(n)."""
    if not values:
        return 0
    return sum(values) / len(values)


def linear_regression(x_vals, y_vals):
    """
    Compute slope (m) and intercept (b) for y = mx + b using Ordinary Least Squares.

    Formula:
        m = Σ((x - x̄)(y - ȳ)) / Σ((x - x̄)²)
        b = ȳ - m * x̄

    Time Complexity:  O(n) — single pass through data after computing means
    Space Complexity: O(1) — accumulates into scalar variables

    Args:
        x_vals (list of float): Independent variable (e.g. time index)
        y_vals (list of float): Dependent variable (e.g. temperature)
    Returns:
        tuple: (slope m, intercept b)
    """
    if len(x_vals) != len(y_vals) or len(x_vals) < 2:
        raise ValueError("Need at least 2 matching data points for regression.")

    x_mean = _mean(x_vals)
    y_mean = _mean(y_vals)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)

    if denominator == 0:
        raise ValueError("All x values are identical — cannot compute regression.")

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept


def predict_next_hours(records, hours_ahead=24):
    """
    Use linear regression on recent temperature data to predict future values.

    Time Complexity: O(n) for regression + O(k) for predictions = O(n)
    where n = number of historical records, k = hours_ahead

    Args:
        records (list): Weather records loaded from CSV
        hours_ahead (int): How many hours into the future to predict
    Returns:
        list of dict: Predicted records with 'time' and 'temperature' keys,
                      or empty list on failure
    """
    if len(records) < 2:
        print("Not enough data to make a prediction.")
        return []

    # Filter out any records with invalid temperature data
    valid_records = []
    for r in records:
        try:
            temp = float(r["temperature"])
            valid_records.append(r)
        except (ValueError, KeyError, TypeError):
            print(f"  Warning: Skipping record with invalid temperature: {r.get('time', 'unknown time')}")
            continue
    
    if len(valid_records) < 2:
        print("Not enough valid temperature data for prediction.")
        return []

    # Use index as x (time proxy) and temperature as y
    x = list(range(len(valid_records)))
    y = [float(r["temperature"]) for r in valid_records]

    try:
        slope, intercept = linear_regression(x, y)
    except ValueError as e:
        print(f"  Prediction error: {e}")
        return []

    predictions = []
    for i in range(1, hours_ahead + 1):
        future_x = len(valid_records) + i
        predicted_temp = slope * future_x + intercept
        predictions.append({
            "hours_ahead": i,
            "predicted_temperature": round(predicted_temp, 2)
        })

    return predictions