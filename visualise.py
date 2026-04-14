# visualise.py
# Handles all data visualisation using matplotlib

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


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