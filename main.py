# main.py
# IY499 - Introduction to Programming — Practical Assignment
# Weather Prediction Application
# Fetches real weather data, stores it locally, analyses trends,
# and predicts future temperatures using linear regression.

import fetch
import storage
import analysis
import visualise


# ==============================================================================
# MENU HELPERS
# ==============================================================================

def print_header():
    """Print the application banner."""
    print("\n" + "=" * 50)
    print("        🌤  WEATHER PREDICTION APP  🌤")
    print("=" * 50)


def print_menu():
    """Display the main menu."""
    print("\n  [1]  Fetch latest weather data")
    print("  [2]  View saved data")
    print("  [3]  Search records by date")
    print("  [4]  Find hottest / coldest day")
    print("  [5]  Predict next 24 hours")
    print("  [6]  Plot charts")
    print("  [0]  Exit")
    print("-" * 50)


def print_chart_menu():
    """Display the chart sub-menu."""
    print("\n  [1]  Temperature over time")
    print("  [2]  Precipitation over time")
    print("  [3]  Wind speed over time")
    print("  [4]  Full dashboard (all three)")
    print("  [0]  Back")
    print("-" * 50)


def get_int_input(prompt, valid_range):
    """
    Prompt the user for an integer within a valid range.
    Loops until valid input is given — robust against strings, floats, blanks.

    Time Complexity: O(1) per valid input
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if value in valid_range:
                return value
            print(f"  Please enter one of: {list(valid_range)}")
        except ValueError:
            print("  Invalid input — please enter a number.")


# ==============================================================================
# MENU ACTIONS
# ==============================================================================

def action_fetch():
    """Fetch live weather data and save it to CSV."""
    print("\n  Fetching weather data for Leeds, UK...")
    data = fetch.get_weather()
    if data:
        storage.save_to_csv(data)
    else:
        print("  Could not retrieve data. Saved data (if any) is unchanged.")


def action_view():
    """Display the first and last 5 saved records."""
    records = storage.load_from_csv()
    if not records:
        return

    print(f"\n  {len(records)} records loaded.\n")
    print(f"  {'Time':<22} {'Temp (°C)':>10} {'Precip (mm)':>12} {'Wind (km/h)':>12}")
    print("  " + "-" * 58)

    # Show first 5 and last 5 to handle large datasets cleanly
    display = records[:5] + (records[-5:] if len(records) > 10 else [])
    if len(records) > 10:
        for r in records[:5]:
            print(f"  {r['time']:<22} {r['temperature']:>10} {r['precipitation']:>12} {r['windspeed']:>12}")
        print(f"  {'... ' + str(len(records) - 10) + ' records hidden ...':<58}")
        for r in records[-5:]:
            print(f"  {r['time']:<22} {r['temperature']:>10} {r['precipitation']:>12} {r['windspeed']:>12}")
    else:
        for r in display:
            print(f"  {r['time']:<22} {r['temperature']:>10} {r['precipitation']:>12} {r['windspeed']:>12}")


def action_search():
    """Search saved records for a specific date using binary search."""
    records = storage.load_from_csv()
    if not records:
        return

    date_str = input("\n  Enter a date to search (YYYY-MM-DD): ").strip()

    # Validate date format before searching
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("  Invalid date format. Please use YYYY-MM-DD (e.g. 2026-04-14).")
        return

    # Records must be sorted by time for binary search to work — O(n log n)
    sorted_records = analysis.merge_sort(records, key="time")

    # Binary search is O(log n)
    matches = analysis.binary_search_by_date(sorted_records, date_str)

    if not matches:
        print(f"  No records found for {date_str}.")
        return

    print(f"\n  {len(matches)} records found for {date_str}:\n")
    print(f"  {'Time':<22} {'Temp (°C)':>10} {'Precip (mm)':>12} {'Wind (km/h)':>12}")
    print("  " + "-" * 58)
    for r in matches:
        print(f"  {r['time']:<22} {r['temperature']:>10} {r['precipitation']:>12} {r['windspeed']:>12}")


def action_extremes():
    """Find and display the hottest and coldest recorded entries."""
    records = storage.load_from_csv()
    if not records:
        return
    print()
    analysis.find_extremes(records)


def action_predict():
    """Run linear regression and display 24-hour temperature forecast."""
    records = storage.load_from_csv()
    if not records:
        return

    print("\n  Running linear regression on saved data...")
    try:
        predictions = analysis.predict_next_hours(records, hours_ahead=24)
    except ValueError as e:
        print(f"  Prediction error: {e}")
        return

    if not predictions:
        return

    print(f"\n  {'Hours Ahead':>12}  {'Predicted Temp (°C)':>20}")
    print("  " + "-" * 36)
    for p in predictions:
        print(f"  {p['hours_ahead']:>12}  {p['predicted_temperature']:>20}")

    # Offer to plot the forecast
    show_plot = input("\n  Plot the forecast? (y/n): ").strip().lower()
    if show_plot == "y":
        visualise.plot_prediction(records, predictions)


def action_charts():
    """Show chart sub-menu and render the chosen visualisation."""
    records = storage.load_from_csv()
    if not records:
        return

    print_chart_menu()
    choice = get_int_input("  Choose a chart: ", range(5))

    if choice == 0:
        return
    elif choice == 1:
        visualise.plot_temperatures(records)
    elif choice == 2:
        visualise.plot_precipitation(records)
    elif choice == 3:
        visualise.plot_windspeed(records)
    elif choice == 4:
        visualise.plot_summary_dashboard(records)


# ==============================================================================
# MAIN LOOP
# ==============================================================================

def main():
    """
    Main application loop.
    Displays menu, routes user input to the correct action, handles all errors.
    Runs until the user selects Exit (0).
    """
    print_header()
    print("  Real-time weather data powered by Open-Meteo API.")
    print("  Data is cached locally and predictions use linear regression.")

    actions = {
        1: action_fetch,
        2: action_view,
        3: action_search,
        4: action_extremes,
        5: action_predict,
        6: action_charts,
    }

    while True:
        print_menu()
        choice = get_int_input("  Enter choice: ", range(7))

        if choice == 0:
            print("\n  Goodbye!\n")
            break

        try:
            actions[choice]()
        except KeyboardInterrupt:
            # Ctrl+C mid-action returns to menu rather than crashing
            print("\n  Action cancelled. Returning to menu.")
        except Exception as e:
            # Catch-all so an unexpected bug never crashes the whole program
            print(f"\n  Unexpected error: {e}")
            print("  Returning to menu. Your saved data has not been affected.")


if __name__ == "__main__":
    main()