#George Huang
from __future__ import annotations
from typing import List, Tuple, Dict
from collections import defaultdict
from datetime import datetime

import requests

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ForecastClient:
   
    FCST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._cache: Dict[str, dict] = {}

    def _url(self, city: str) -> str:
        return f"{self.FCST_URL}?q={city}&appid={self.api_key}&units=imperial"

    def _fetch(self, city: str) -> dict:
        if city in self._cache:
            return self._cache[city]
        r = requests.get(self._url(city), timeout=12)
        if r.status_code == 200:
            data = r.json()
            self._cache[city] = data
            return data
        return {}

    def highs_lows_by_day(self, city: str) -> Tuple[List[str], List[float], List[float]]:
        
        data = self._fetch(city)
        if not data or "list" not in data:
            return [], [], []

        highs = defaultdict(lambda: float("-inf"))
        lows  = defaultdict(lambda: float("inf"))

        # preserve first-seen day order
        day_order: List[str] = []

        for entry in data["list"]:  # each is a 3-hour forecast point
            ts = datetime.fromtimestamp(entry["dt"])
            day = ts.strftime("%a")  # Mon, Tue, ...
            if not day_order or day_order[-1] != day:
                if day not in day_order:
                    day_order.append(day)

            temp = float(entry["main"]["temp"])
            highs[day] = max(highs[day], temp)
            lows[day]  = min(lows[day], temp)

        days = day_order
        return days, [highs[d] for d in days], [lows[d] for d in days]


class TemperatureTrendView(QWidget):
   
    def __init__(self, api_key: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # data client (no impact on your original WeatherAPI)
        self.client = ForecastClient(api_key)

        # matplotlib figure
        self._fig = Figure(figsize=(6, 4))
        self._ax = self._fig.add_subplot(111)
        self._canvas = FigureCanvas(self._fig)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._canvas)

        # initial empty state
        self._ax.set_title("Temperature Trend")
        self._ax.set_xlabel("Day")
        self._ax.set_ylabel("°F")
        self._ax.grid(True, linestyle="--", alpha=0.4)
        self._canvas.draw_idle()

    # ---------- public API ----------

    def plot_city(self, city: str):
        
        days, highs, lows = self.client.highs_lows_by_day(city)
        if not days:
            self._clear_with_message(f"No forecast data for '{city}'")
            return
        self.plot_series(days, highs, lows, title=f"{city} Temperature Trend")

    def compare_cities(self, cities: List[str]):
        
        self._ax.clear()
        any_data = False
        for city in cities:
            days, highs, lows = self.client.highs_lows_by_day(city)
            if not days:
                continue
            any_data = True
            self._ax.plot(days, highs, marker="o", label=f"{city} Highs")
        if not any_data:
            self._clear_with_message("No forecast data for selected cities")
            return
        self._ax.set_title("City Comparison: High Temperatures")
        self._style_axes()
        self._canvas.draw_idle()

    def plot_series(self, days: List[str], highs: List[float], lows: List[float], title: str = "Temperature Trend"):
        
        self._ax.clear()
        self._ax.plot(days, highs, marker="o", label="Highs")
        self._ax.plot(days, lows,  marker="o", label="Lows")
        self._ax.set_title(title)
        self._style_axes()
        self._canvas.draw_idle()

   

    def _style_axes(self):
        self._ax.set_xlabel("Day")
        self._ax.set_ylabel("°F")
        self._ax.grid(True, linestyle="--", alpha=0.4)
        self._ax.legend()

    def _clear_with_message(self, msg: str):
        self._ax.clear()
        self._ax.text(0.5, 0.5, msg, ha="center", va="center", transform=self._ax.transAxes)
        self._ax.set_axis_off()
        self._canvas.draw_idle()

