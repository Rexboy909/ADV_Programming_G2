from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class WeatherPlotterDualAxis(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        self.data = {}

    def add_city_data(self, city: str, times: list, temps: list, precipitation: list):
        """
        Store the city's time, temperature, and precipitation data.
        
        :param city: City name
        :param times: List of time labels
        :param temps: List of temperature values
        :param precipitation: List of precipitation values
        """
        self.data[city] = {
            "times": times,
            "temps": temps,
            "precipitation": precipitation
        }

    def plot(self):
        self.fig.clear()

        if not self.data:
            return

        ax1 = self.fig.add_subplot(111)

        for city, values in self.data.items():
            times = values["times"]

            # Temperature line (left Y-axis)
            ax1.plot(
                times,
                values["temps"],
                marker="o",
                linestyle="-",
                color="red",
                label=f"{city} Temperature"
            )
            ax1.set_xlabel("Time")
            ax1.set_ylabel("Temperature (°F)", color="red")
            ax1.tick_params(axis='y', labelcolor="red")

            # Precipitation line (right Y-axis)
            ax2 = ax1.twinx()
            ax2.plot(
                times,
                values["precipitation"],
                marker="s",
                linestyle="--",
                color="blue",
                label=f"{city} Precipitation"
            )
            ax2.set_ylabel("Precipitation (mm)", color="blue")
            ax2.tick_params(axis='y', labelcolor="blue")

        ax1.grid(True)
        ax1.set_title("Temperature and Precipitation Dual Axis Chart")

        # Merge legends
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper left")

        self.draw()  # Refresh the plot
