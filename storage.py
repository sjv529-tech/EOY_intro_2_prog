# storage.py
# Handles reading and writing weather data to CSV
# Uses atomic writes and backups to prevent data loss

import csv
import os
import shutil
from datetime import datetime

FILENAME = "weather_data.csv"
BACKUP_FILE = "weather_data_backup.csv"
FIELDNAMES = ["time", "temperature", "precipitation", "windspeed"]


def save_to_csv(data):
    """
    Save fetched weather data to CSV using atomic write pattern.

    Atomic write strategy:
      1. Write to a .tmp file first
      2. Back up existing data before overwriting
      3. Replace original with .tmp only after successful write
      → If the program crashes mid-write, the original file is never corrupted.

    Time Complexity: O(n) — writes each of the n records once
    """
    if not data:
        print("  No data to save.")
        return

    temp_path = FILENAME + ".tmp"

    try:
        # Write new data to temp file first
        with open(temp_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for i in range(len(data["time"])):
                writer.writerow({
                    "time": data["time"][i],
                    "temperature": data["temperature_2m"][i],
                    "precipitation": data["precipitation"][i],
                    "windspeed": data["windspeed_10m"][i]
                })

        # Back up existing file before replacing
        if os.path.exists(FILENAME):
            shutil.copy2(FILENAME, BACKUP_FILE)

        # Atomic replace — safe even if program crashes here
        os.replace(temp_path, FILENAME)
        print(f"  Data saved to {FILENAME} ({len(data['time'])} records).")

    except OSError as e:
        print(f"  Error saving data: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)


def load_from_csv():
    """
    Load weather records from CSV with automatic backup recovery.

    Recovery strategy:
      1. Try loading main file
      2. If corrupt or missing, attempt to restore from backup
      3. Validate each row — skip and warn on bad data rather than crashing

    Time Complexity: O(n) — reads each record once
    Returns:
        list of dict: Validated weather records, empty list if nothing recoverable
    """
    for filepath in [FILENAME, BACKUP_FILE]:
        if not os.path.exists(filepath):
            continue

        label = "main file" if filepath == FILENAME else "backup"
        try:
            records = []
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)

                # Validate expected columns are present
                if not reader.fieldnames or not all(
                    col in reader.fieldnames for col in FIELDNAMES
                ):
                    print(f"  Warning: {filepath} has unexpected columns. Skipping.")
                    continue

                for line_num, row in enumerate(reader, start=2):
                    try:
                        # Validate each field can be parsed correctly
                        float(row["temperature"])
                        float(row["precipitation"])
                        float(row["windspeed"])
                        datetime.fromisoformat(row["time"])
                        records.append(row)
                    except (ValueError, KeyError):
                        print(f"  Warning: Skipping corrupt row {line_num} in {filepath}.")

            if records:
                if filepath == BACKUP_FILE:
                    print("  Recovered data from backup file.")
                return records

        except OSError as e:
            print(f"  Could not read {label}: {e}")

    print("  No valid data found. Please fetch new data.")
    return []