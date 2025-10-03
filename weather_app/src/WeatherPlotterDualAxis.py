from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class WeatherPlotterDualAxis(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        self.data = {}
        # theme defaults (text color, background color)
        self._text_color = "#000000"
        self._bg_color = "#FFFFFF"

    def set_theme_colors(self, text_color: str, bg_color: str):
        """
        Set colors used by the plot for text (labels/lines/legend) and background.

        :param text_color: hex color string for text and lines (e.g. '#000000')
        :param bg_color: hex color string for figure/axes background (e.g. '#FFFFFF')
        """
        self._text_color = text_color
        self._bg_color = bg_color
        # Apply immediately to the Qt widget (canvas) so the area behind the figure isn't white
        try:
            # FigureCanvasQTAgg inherits QWidget; style via Qt stylesheet
            self.setStyleSheet(f"background-color: {self._bg_color};")
        except Exception:
            pass
        # Also ensure matplotlib figure facecolor is set so saved images also have correct bg
        try:
            self.fig.patch.set_facecolor(self._bg_color)
        except Exception:
            pass

    def _hex_to_rgb(self, hexstr: str):
        h = hexstr.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % tuple(max(0, min(255, int(x))) for x in rgb)

    def _tint_color(self, hexstr: str, factor: float = 0.6):
        """Return a color between the given hex color and white.
        factor=0 -> original color, factor=1 -> white
        """
        r, g, b = self._hex_to_rgb(hexstr)
        r = r + (255 - r) * factor
        g = g + (255 - g) * factor
        b = b + (255 - b) * factor
        return self._rgb_to_hex((r, g, b))

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

        # create primary axis
        ax1 = self.fig.add_subplot(111)
        # create a single secondary axis (shared for all precipitation series)
        ax2 = ax1.twinx()

        # apply background colors to figure and axes
        try:
            self.fig.patch.set_facecolor(self._bg_color)
        except Exception:
            pass
        ax1.set_facecolor(self._bg_color)
        ax2.set_facecolor('none')  # keep second axis transparent so grid shows through

        # derive unified colors
        temp_color = self._text_color
        precip_color = self._tint_color(self._text_color, factor=0.35)  # lighter tint for precipitation

        # store plotted handles for legend
        all_lines = []
        all_labels = []

        # color cycle can be used or fixed colors per measurement
        for city, values in self.data.items():
            times = values["times"]

            # Temperature line (left Y-axis)
            temp_line, = ax1.plot(
                times,
                values["temps"],
                marker="o",
                linestyle="-",
                color=temp_color,
                label=f"{city} Temperature"
            )
            all_lines.append(temp_line)
            all_labels.append(f"{city} Temperature")

            # Precipitation line (right Y-axis)
            precip_line, = ax2.plot(
                times,
                values["precipitation"],
                marker="s",
                linestyle="--",
                color=precip_color,
                label=f"{city} Precipitation"
            )
            all_lines.append(precip_line)
            all_labels.append(f"{city} Precipitation")

        # Axis labels and title colored to match theme
        ax1.set_xlabel("Time", color=self._text_color)
        ax1.set_ylabel("Temperature (°F)", color=self._text_color)
        ax2.set_ylabel("Precipitation (mm)", color=self._text_color)

        # ticks color
        ax1.tick_params(axis='x', colors=self._text_color)
        ax1.tick_params(axis='y', colors=self._text_color)
        ax2.tick_params(axis='y', colors=self._text_color)

        # title
        ax1.set_title("Temperature and Precipitation Dual Axis Chart", color=self._text_color)

        # grid - draw on primary axis
        ax1.grid(True, color=self._text_color, alpha=0.15)

        # Legend - place on primary axis and color text
        legend = ax1.legend(all_lines, all_labels, loc="upper left")
        for text in legend.get_texts():
            text.set_color(self._text_color)

        # adjust layout so labels don't overlap
        self.fig.tight_layout()

        # Ensure the canvas widget background matches the figure
        try:
            self.setStyleSheet(f"background-color: {self._bg_color};")
        except Exception:
            pass

        self.draw()  # Refresh the plot