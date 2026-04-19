import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import fetch
import storage
import analysis
import visualise
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Prediction App")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set color scheme
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.warning_color = "#f39c12"
        self.error_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="WEATHER PREDICTION APP",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Leeds, UK | 7-day forecast | Linear regression predictions",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - Buttons
        button_frame = tk.Frame(content_frame, bg=self.bg_color, width=200)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        button_frame.pack_propagate(False)
        
        buttons = [
            ("1. Fetch Weather Data", self.fetch_data),
            ("2. View Saved Data", self.view_data),
            ("3. Search by Date", self.search_data),
            ("4. Hottest / Coldest", self.show_extremes),
            ("5. Predict 24 Hours", self.predict),
            ("6. Plot Charts", self.show_chart_menu),
            ("7. Full Dashboard", self.show_dashboard)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 11),
                bg=self.accent_color,
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief=tk.FLAT,
                pady=8
            )
            btn.pack(fill=tk.X, pady=5)
        
        # Exit button
        exit_btn = tk.Button(
            button_frame,
            text="0. Exit",
            command=self.root.quit,
            font=("Arial", 11, "bold"),
            bg=self.error_color,
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.FLAT,
            pady=8
        )
        exit_btn.pack(fill=tk.X, pady=(20, 5))
        
        # Right side - Output area
        output_frame = tk.Frame(content_frame, bg=self.bg_color)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Scrolled text for output
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            height=25
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, padx=10, pady=5)
        
    def log(self, message, color="normal"):
        """Add message to output area with optional color"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def fetch_data(self):
        """Fetch weather data from API"""
        self.clear_output()
        self.log("=" * 50)
        self.log("FETCHING WEATHER DATA")
        self.log("=" * 50)
        self.update_status("Fetching data from Open-Meteo API...")
        
        # Run in thread to avoid freezing GUI
        def fetch_thread():
            try:
                data = fetch.get_weather()
                if data:
                    storage.save_to_csv(data)
                    self.log("\n[SUCCESS] Data fetched and saved!")
                    self.update_status("Data fetched successfully")
                else:
                    self.log("\n[ERROR] Could not retrieve data")
                    self.update_status("Fetch failed")
            except Exception as e:
                self.log(f"\n[ERROR] {e}")
                self.update_status("Error occurred")
        
        threading.Thread(target=fetch_thread, daemon=True).start()
        
    def view_data(self):
        """Display saved records"""
        self.clear_output()
        self.log("=" * 50)
        self.log("SAVED WEATHER DATA")
        self.log("=" * 50)
        
        records = storage.load_from_csv()
        if not records:
            self.log("No data found. Please fetch data first (option 1).")
            return
            
        self.log(f"\nTotal records: {len(records)}\n")
        self.log(f"{'Time':<22} {'Temp(C)':>10} {'Precip(mm)':>12} {'Wind(km/h)':>12}")
        self.log("-" * 58)
        
        # Show first 10 records
        for r in records[:10]:
            self.log(f"{r['time']:<22} {float(r['temperature']):>10.1f} "
                    f"{float(r['precipitation']):>12.1f} {float(r['windspeed']):>12.1f}")
        
        if len(records) > 10:
            self.log(f"\n... and {len(records) - 10} more records")
            self.log("(Use search option for specific dates)")
            
        self.update_status(f"Loaded {len(records)} records")
        
    def search_data(self):
        """Search for records by date"""
        # Create search dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Search by Date")
        dialog.geometry("300x150")
        dialog.configure(bg=self.bg_color)
        
        tk.Label(
            dialog,
            text="Enter date (YYYY-MM-DD):",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=20)
        
        date_entry = tk.Entry(dialog, font=("Arial", 11), width=15)
        date_entry.pack(pady=5)
        
        def do_search():
            date_str = date_entry.get().strip()
            if len(date_str) != 10:
                messagebox.showerror("Error", "Use format YYYY-MM-DD")
                return
                
            records = storage.load_from_csv()
            if not records:
                messagebox.showinfo("Info", "No data found. Fetch data first.")
                dialog.destroy()
                return
                
            sorted_records = analysis.merge_sort(records, key="time")
            matches = analysis.binary_search_by_date(sorted_records, date_str)
            
            self.clear_output()
            self.log("=" * 50)
            self.log(f"SEARCH RESULTS: {date_str}")
            self.log("=" * 50)
            
            if not matches:
                self.log(f"\nNo records found for {date_str}")
            else:
                self.log(f"\nFound {len(matches)} records:\n")
                self.log(f"{'Time':<22} {'Temp(C)':>10} {'Precip(mm)':>12} {'Wind(km/h)':>12}")
                self.log("-" * 58)
                for r in matches:
                    self.log(f"{r['time']:<22} {float(r['temperature']):>10.1f} "
                            f"{float(r['precipitation']):>12.1f} {float(r['windspeed']):>12.1f}")
                    
            dialog.destroy()
            self.update_status(f"Searched for {date_str}")
            
        tk.Button(
            dialog,
            text="Search",
            command=do_search,
            bg=self.accent_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=5
        ).pack(pady=10)
        
    def show_extremes(self):
        """Display hottest and coldest temperatures"""
        self.clear_output()
        self.log("=" * 50)
        self.log("TEMPERATURE EXTREMES")
        self.log("=" * 50)
        
        records = storage.load_from_csv()
        if not records:
            self.log("No data found. Please fetch data first (option 1).")
            return
            
        sorted_records = analysis.merge_sort(records, key="temperature")
        coldest = sorted_records[0]
        hottest = sorted_records[-1]
        
        self.log(f"\n🔥 HOTTEST: {hottest['time']}  →  {hottest['temperature']}°C")
        self.log(f"❄️ COLDEST: {coldest['time']}  →  {coldest['temperature']}°C")
        
        self.update_status("Extremes calculated")
        
    def predict(self):
        """Generate temperature predictions"""
        self.clear_output()
        self.log("=" * 50)
        self.log("24-HOUR TEMPERATURE FORECAST")
        self.log("=" * 50)
        
        records = storage.load_from_csv()
        if not records:
            self.log("No data found. Please fetch data first (option 1).")
            return
            
        self.log("\nRunning linear regression on historical data...\n")
        
        try:
            predictions = analysis.predict_next_hours(records, hours_ahead=24)
        except ValueError as e:
            self.log(f"Prediction error: {e}")
            return
            
        if not predictions:
            return
            
        self.log(f"{'Hours Ahead':>12}  {'Predicted Temp (C)':>20}")
        self.log("-" * 35)
        for p in predictions[:12]:  # Show first 12 hours
            self.log(f"{p['hours_ahead']:>12}  {p['predicted_temperature']:>20.1f}")
        
        if len(predictions) > 12:
            self.log(f"\n... and {len(predictions) - 12} more hours")
            
        # Ask if user wants to see plot
        if messagebox.askyesno("Plot Forecast", "Would you like to see the forecast plot?"):
            visualise.plot_prediction(records, predictions)
            
        self.update_status("Prediction complete")
        
    def show_chart_menu(self):
        """Show chart options dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Chart Options")
        dialog.geometry("300x250")
        dialog.configure(bg=self.bg_color)
        
        tk.Label(
            dialog,
            text="Select Chart Type:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=15)
        
        records = storage.load_from_csv()
        if not records:
            tk.Label(
                dialog,
                text="No data available",
                bg=self.bg_color,
                fg=self.warning_color
            ).pack()
            return
            
        def plot_temp():
            visualise.plot_temperatures(records)
            dialog.destroy()
            
        def plot_precip():
            visualise.plot_precipitation(records)
            dialog.destroy()
            
        def plot_wind():
            visualise.plot_windspeed(records)
            dialog.destroy()
            
        buttons = [
            ("Temperature Over Time", plot_temp),
            ("Precipitation Over Time", plot_precip),
            ("Wind Speed Over Time", plot_wind)
        ]
        
        for text, command in buttons:
            tk.Button(
                dialog,
                text=text,
                command=command,
                bg=self.accent_color,
                fg="white",
                relief=tk.FLAT,
                width=25,
                pady=5
            ).pack(pady=5)
            
    def show_dashboard(self):
        """Show complete dashboard with all charts"""
        records = storage.load_from_csv()
        if not records:
            messagebox.showinfo("Info", "No data found. Fetch data first.")
            return
        visualise.plot_summary_dashboard(records)
        self.update_status("Dashboard displayed")


def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()