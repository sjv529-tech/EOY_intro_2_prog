import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_prediction(records, predictions):
    """
    Plot historical temperatures with a forecast line extending from the last record.

    Time Complexity: O(n + k) where n = historical records, k = predictions
    """
    if not records or not predictions:
        print("No data to plot.")
        return

    times, temperatures, _, _ = _parse_records(records)

    # Build future x-axis points by extending from the last historical timestamp
    from datetime import timedelta
    last_time = times[-1]
    future_times = [last_time + timedelta(hours=p["hours_ahead"]) for p in predictions]
    future_temps = [p["predicted_temperature"] for p in predictions]

    fig, ax = plt.subplots(figsize=(13, 5))

    # Historical data
    ax.plot(times, temperatures, color="tomato", linewidth=1.5, label="Historical Temp (°C)")
    ax.fill_between(times, temperatures, alpha=0.1, color="tomato")

    # Prediction line — starts from last historical point for a clean join
    ax.plot(
        [times[-1]] + future_times,
        [temperatures[-1]] + future_temps,
        color="royalblue",
        linewidth=1.5,
        linestyle="--",
        label="Predicted Temp (°C)"
    )
    ax.fill_between(
        [times[-1]] + future_times,
        [temperatures[-1]] + future_temps,
        alpha=0.1,
        color="royalblue"
    )

    # Vertical marker at the forecast boundary
    ax.axvline(x=times[-1], color="grey", linestyle=":", linewidth=1, label="Forecast start")

    ax.set_title("Temperature History + 24-Hour Forecast", fontsize=14)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Temperature (°C)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
    fig.autofmt_xdate()
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()

def _parse_records(records):
    """Convert CSV string records into typed Python values."""
    times = [datetime.fromisoformat(r["time"]) for r in records]
    temperatures = [float(r["temperature"]) for r in records]
    precipitation = [float(r["precipitation"]) for r in records]
    windspeeds = [float(r["windspeed"]) for r in records]
    return times, temperatures, precipitation, windspeeds


def plot_temperatures(records):
    """Plot hourly temperature over time as a line chart."""
    if not records:
        print("No data to plot.")
        return

    times, temperatures, _, _ = _parse_records(records)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(times, temperatures, color="tomato", linewidth=1.5, label="Temperature (°C)")
    ax.fill_between(times, temperatures, alpha=0.1, color="tomato")

    ax.set_title("Temperature Over Time", fontsize=14)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Temperature (°C)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
    fig.autofmt_xdate()
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_precipitation(records):
    """Plot hourly precipitation as a bar chart."""
    if not records:
        print("No data to plot.")
        return

    times, _, precipitation, _ = _parse_records(records)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(times, precipitation, width=0.03, color="steelblue", label="Precipitation (mm)")

    ax.set_title("Precipitation Over Time", fontsize=14)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Precipitation (mm)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    fig.autofmt_xdate()
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5, axis="y")

    plt.tight_layout()
    plt.show()


def plot_windspeed(records):
    """Plot hourly wind speed over time as a line chart."""
    if not records:
        print("No data to plot.")
        return

    times, _, _, windspeeds = _parse_records(records)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(times, windspeeds, color="mediumseagreen", linewidth=1.5, label="Wind Speed (km/h)")
    ax.fill_between(times, windspeeds, alpha=0.1, color="mediumseagreen")

    ax.set_title("Wind Speed Over Time", fontsize=14)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Wind Speed (km/h)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
    fig.autofmt_xdate()
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_summary_dashboard(records):
    """Show all three charts stacked in a single dashboard view."""
    if not records:
        print("No data to plot.")
        return

    times, temperatures, precipitation, windspeeds = _parse_records(records)

    fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True)
    fig.suptitle("Weather Summary Dashboard", fontsize=16, fontweight="bold")

    # --- Temperature ---
    axes[0].plot(times, temperatures, color="tomato", linewidth=1.5)
    axes[0].fill_between(times, temperatures, alpha=0.1, color="tomato")
    axes[0].set_ylabel("Temp (°C)")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].set_title("Temperature")

    # --- Precipitation ---
    axes[1].bar(times, precipitation, width=0.03, color="steelblue")
    axes[1].set_ylabel("Precip (mm)")
    axes[1].grid(True, linestyle="--", alpha=0.5, axis="y")
    axes[1].set_title("Precipitation")

    # --- Wind Speed ---
    axes[2].plot(times, windspeeds, color="mediumseagreen", linewidth=1.5)
    axes[2].fill_between(times, windspeeds, alpha=0.1, color="mediumseagreen")
    axes[2].set_ylabel("Wind (km/h)")
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].set_title("Wind Speed")

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()