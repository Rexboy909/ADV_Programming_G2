# Created by Rex
# Other contributors:
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QTabWidget, QToolBar, QMessageBox, QColorDialog, QMenu, QToolButton
from PySide6.QtGui import QAction, QColor, QCursor
from PySide6.QtCore import QSize, Qt
import sys
import requests  


from trend_view import TemperatureTrendView

import sys, weatherData, weatherPlotterDualAxis
API_KEY = "04b2c70f5678cb788cb9d62c0325ef32"  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        # Date and Location
        dateLocation = QWidget()  # date and location widget
        dateLocation.setAttribute(Qt.WA_StyledBackground, True)
        dateLocationLayout = QHBoxLayout()
        dateLocation.setLayout(dateLocationLayout)

        locationLabel = QLabel("Location")
        locationLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        dateLocationLayout.addWidget(locationLabel)

        location = QLineEdit()
        location.setPlaceholderText("Enter Location (e.g., Salt Lake City or Paris,FR)")
        dateLocationLayout.addWidget(location)

        dateLabel = QLabel("Date:")
        dateLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)
        dateLocationLayout.addWidget(dateLabel)

        date = QDateTimeEdit()
        date.setCalendarPopup(True)
        date.setDateTime(date.dateTime().currentDateTime())
        dateLocationLayout.addWidget(date)

        
        todayTab = QWidget()
        todayTab.setAttribute(Qt.WA_StyledBackground, True)
        todayTabLayout = QHBoxLayout()
        todayTab.setLayout(todayTabLayout)
        todayStatsLayout = QVBoxLayout()
        todayTabLayout.addLayout(todayStatsLayout)

        todayTemp = QLabel("Temperature: ")
        todayWindSpeed = QLabel("Wind Speed: ")
        todayWindDirection = QLabel("Wind Direction: ")
        todayHumidity = QLabel("Humidity: ")
        todayPrecipitation = QLabel("Precipitation: ")
        todayStatsLayout.addWidget(todayTemp)
        todayStatsLayout.addWidget(todayWindSpeed)
        todayStatsLayout.addWidget(todayWindDirection)
        todayStatsLayout.addWidget(todayHumidity)
        todayStatsLayout.addWidget(todayPrecipitation)

        # night tab content
        tonightTab = QWidget()
        tonightTab.setAttribute(Qt.WA_StyledBackground, True)
        tonightTabLayout = QHBoxLayout()
        tonightTab.setLayout(tonightTabLayout)
        tonightStatsLayout = QVBoxLayout()
        tonightTabLayout.addLayout(tonightStatsLayout)

        tonightTemp = QLabel("Temperature: ")
        tonightWindSpeed = QLabel("Wind Speed: ")
        tonightWindDirection = QLabel("Wind Direction: ")
        tonightHumidity = QLabel("Humidity: ")
        tonightPrecipitation = QLabel("Precipitation: ")
        tonightStatsLayout.addWidget(tonightTemp)
        tonightStatsLayout.addWidget(tonightWindSpeed)
        tonightStatsLayout.addWidget(tonightWindDirection)
        tonightStatsLayout.addWidget(tonightHumidity)
        tonightStatsLayout.addWidget(tonightPrecipitation)

    
        trendTab = QWidget()
        trendTab.setAttribute(Qt.WA_StyledBackground, True)
        trendLayout = QVBoxLayout(trendTab)
        self.trend_widget = TemperatureTrendView(api_key=API_KEY)
        trendLayout.addWidget(self.trend_widget)

        # Tabs
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.addTab(todayTab, "Today")
        tabs.addTab(tonightTab, "Tonight")
        tabs.addTab(trendTab, "Trend")

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setObjectName("mainToolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Theme state
        self._is_night = False
        self._day_colors = ("#000000", "#818181")
        self._night_colors = ("#FFFFFF", "#2C3E50")

        # Theme actions
        def toggle_theme():
            if getattr(self, "_is_night", False):
                setColors(*self._day_colors); self._is_night = False
            else:
                setColors(*self._night_colors); self._is_night = True

        def pick_day_colors():
            txt = QColorDialog.getColor(QColor(self._day_colors[0]), self, "Day text color")
            if not txt.isValid(): return
            bg = QColorDialog.getColor(QColor(self._day_colors[1]), self, "Day background color")
            if not bg.isValid(): return
            self._day_colors = (txt.name(), bg.name()); setColors(*self._day_colors)

        def pick_night_colors():
            txt = QColorDialog.getColor(QColor(self._night_colors[0]), self, "Night text color")
            if not txt.isValid(): return
            bg = QColorDialog.getColor(QColor(self._night_colors[1]), self, "Night background color")
            if not bg.isValid(): return
            self._night_colors = (txt.name(), bg.name()); setColors(*self._night_colors)

        toggle_action = QAction("Toggle Theme", self); toggle_action.triggered.connect(toggle_theme); toolbar.addAction(toggle_action)
        day_color_action = QAction("Day Colors...", self); day_color_action.triggered.connect(pick_day_colors); toolbar.addAction(day_color_action)
        night_color_action = QAction("Night Colors...", self); night_color_action.triggered.connect(pick_night_colors); toolbar.addAction(night_color_action)
        about_action = QAction("About", self); about_action.triggered.connect(lambda: QMessageBox.information(self, "About", "Weather App")); toolbar.addAction(about_action)

        # Main container
        main = QWidget()
        main.setAttribute(Qt.WA_StyledBackground, True)
        mainLayout = QVBoxLayout()
        main.setLayout(mainLayout)
        mainLayout.addWidget(dateLocation)
        mainLayout.addWidget(tabs)
        self.setCentralWidget(main)

       
        def setColors(dayColorTxt, dayColorBG):
            def _to_name(val, fallback):
                if isinstance(val, QColor): return val.name() if val.isValid() else fallback
                if isinstance(val, str) and val: return val
                return fallback
            txt = _to_name(dayColorTxt, "#000000"); bg = _to_name(dayColorBG, "#CCEAFF")
            self.setStyleSheet(f"background-color: {bg};")
            dateLocation.setStyleSheet(f"background-color: {bg}; border: none;")
            todayTab.setStyleSheet(f"background-color: {bg}; border: none;")
            tonightTab.setStyleSheet(f"background-color: {bg}; border: none;")
            locationLabel.setStyleSheet(f"color: {txt};")
            location.setStyleSheet(f"color: {txt}; background: transparent; border: 1px solid {txt}; border-radius: 4px; padding: 4px;")
            date.setStyleSheet(f"QDateTimeEdit, QDateTimeEdit::drop-down, QDateTimeEdit QAbstractSpinBox, QDateTimeEdit QLineEdit {{ color: {txt}; background: transparent; border: none; }}")
            dateLabel.setStyleSheet(f"color: {txt};")
            todayTemp.setStyleSheet(f"color: {txt};")
            todayWindSpeed.setStyleSheet(f"color: {txt};")
            todayWindDirection.setStyleSheet(f"color: {txt};")
            todayHumidity.setStyleSheet(f"color: {txt};")
            todayPrecipitation.setStyleSheet(f"color: {txt};")
            tonightTemp.setStyleSheet(f"color: {txt};")
            tonightWindSpeed.setStyleSheet(f"color: {txt};")
            tonightWindDirection.setStyleSheet(f"color: {txt};")
            tonightHumidity.setStyleSheet(f"color: {txt};")
            tonightPrecipitation.setStyleSheet(f"color: {txt};")
            try:
                toolbar.setStyleSheet(f"""
                QToolBar {{
                    background-color: {bg};
                    border: 1px solid {txt};
                }}
                QToolButton {{
                    color: {txt};
                    background: transparent;
                    border: none;
                    padding: 4px 8px;
                }}
                QToolButton:hover {{ background: rgba(0,0,0,0.04); }}
                """)
            except NameError:
                pass
            tab_style = f'''
            QTabWidget::pane {{ background-color: {bg}; border: 1px solid {txt}; top: -1px; }}
            QTabBar::tab {{ color: {txt}; background: transparent; padding: 6px 12px; margin: 2px;
                             border: 1px solid {txt}; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; }}
            QTabBar::tab:selected {{ background: {bg}; margin-bottom: 0; font-weight: bold; }}
            QTabBar::tab:hover {{ background: rgba(0,0,0,0.03); }}
            QTabBar::tab:focus {{ outline: none; }}
            '''
            tabs.setStyleSheet(tab_style)
            # Try to update the plotter theme if the plotter has been created
            try:
                dataPlotter.set_theme_colors(txt, bg)
                dataPlotter.plot()
            except NameError:
                # dataPlotter not created yet; it'll be initialized later
                pass
            except Exception:
                # ignore plotting errors to avoid breaking the UI theme change
                pass
            return txt, bg  # return the applied colors
        # Tabs setting
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.addTab(todayTab, "Today")
        tabs.addTab(tonightTab, "Tonight")

        # --- Add toolbar here ---
        toolbar = QToolBar("Main Toolbar")
        toolbar.setObjectName("mainToolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # store theme colors so toggle works reliably
        self._is_night = False
        self._day_colors = ("#000000", "#818181")
        self._night_colors = ("#FFFFFF", "#2C3E50")
        # remember the original defaults so we can reset later
        self._default_day_colors = self._day_colors
        self._default_night_colors = self._night_colors

        def toggle_theme():
            if getattr(self, "_is_night", False):
                setColors(*self._day_colors)
                self._is_night = False
            else:
                setColors(*self._night_colors)
                self._is_night = True

        def pick_day_colors():
            txt = QColorDialog.getColor(QColor(self._day_colors[0]), self, "Day text color")
            if not txt.isValid():
                return
            bg = QColorDialog.getColor(QColor(self._day_colors[1]), self, "Day background color")
            if not bg.isValid():
                return
            self._day_colors = (txt.name(), bg.name())
            setColors(*self._day_colors)

        def pick_night_colors():
            txt = QColorDialog.getColor(QColor(self._night_colors[0]), self, "Night text color")
            if not txt.isValid():
                return
            bg = QColorDialog.getColor(QColor(self._night_colors[1]), self, "Night background color")
            if not bg.isValid():
                return
            self._night_colors = (txt.name(), bg.name())
            setColors(*self._night_colors)

        def reset_colors():
            # restore the stored defaults and apply them
            self._day_colors = self._default_day_colors
            self._night_colors = self._default_night_colors
            setColors(*self._day_colors)

        toggle_action = QAction("Toggle Theme", self)
        toggle_action.triggered.connect(toggle_theme)
        toolbar.addAction(toggle_action)

        settings_menu = QMenu("Settings", self)

        day_color_action = QAction("Day Colors...", self)
        day_color_action.triggered.connect(pick_day_colors)
        settings_menu.addAction(day_color_action)

        night_color_action = QAction("Night Colors...", self)
        night_color_action.triggered.connect(pick_night_colors)
        settings_menu.addAction(night_color_action)

        reset_colors_action = QAction("Reset Colors", self)
        reset_colors_action.triggered.connect(reset_colors)
        settings_menu.addAction(reset_colors_action)

        # Create a tool button that shows the settings menu when clicked
        settings_button = QToolButton(self)
        settings_button.setText("Settings")
        settings_button.setMenu(settings_menu)
        settings_button.setPopupMode(QToolButton.InstantPopup)
        toolbar.addWidget(settings_button)

        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "About", "Weather App"))
        toolbar.addAction(about_action)
        # --- end toolbar insertion ---

        dataPlotter = weatherPlotterDualAxis.WeatherPlotterDualAxis(parent=tabs)
        dataPlotter.add_city_data("CityA", ["08:00","12:00","16:00"], [60,72,68], [0.0, 1.2, 0.3])
        dataPlotter.add_city_data("CityB", ["08:00","12:00","16:00"], [55,70,66], [0.0, 0.5, 0.0])
        dataPlotter.plot()
        tabs.addTab(dataPlotter, "Data Plot")
        dataPlotter.set_theme_colors(*self._day_colors)
        # Main Widget
        main = QWidget()
        main.setAttribute(Qt.WA_StyledBackground, True)
        mainLayout = QVBoxLayout() # creating a layout
        main.setLayout(mainLayout) #setting the layout to the main widget. IDK why it has to be done this way but
        mainLayout.addWidget(dateLocation)
        mainLayout.addWidget(tabs)
        
        self.setCentralWidget(main)

        # apply initial theme now that toolbar, tabs and widgets exist
        setColors(*self._day_colors)


        def update_today_tonight(city: str):
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
                r = requests.get(url, timeout=10)
                if r.status_code != 200:
                    todayTemp.setText("Temperature: (no data)")
                    todayWindSpeed.setText("Wind Speed: (no data)")
                    todayWindDirection.setText("Wind Direction: (no data)")
                    todayHumidity.setText("Humidity: (no data)")
                    todayPrecipitation.setText("Precipitation: (no data)")
                    tonightTemp.setText("Temperature: (no data)")
                    tonightWindSpeed.setText("Wind Speed: (no data)")
                    tonightWindDirection.setText("Wind Direction: (no data)")
                    tonightHumidity.setText("Humidity: (no data)")
                    tonightPrecipitation.setText("Precipitation: (no data)")
                    return

                data = r.json()
                main = data.get("main", {})
                wind = data.get("wind", {})
                desc = (data.get("weather") or [{}])[0].get("description", "")
                t = main.get("temp"); h = main.get("humidity")
                ws = wind.get("speed"); wd = wind.get("deg")

                dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
                wd_text = "N/A" if wd is None else dirs[int((wd + 11.25) // 22.5) % 16]

                todayTemp.setText(f"Temperature: {t} °F  {desc}")
                todayWindSpeed.setText(f"Wind Speed: {ws} mph")
                todayWindDirection.setText(f"Wind Direction: {wd_text}")
                todayHumidity.setText(f"Humidity: {h}%")

                precip = 0.0
                if "rain" in data and "1h" in data["rain"]:
                    precip = float(data["rain"]["1h"])
                elif "snow" in data and "1h" in data["snow"]:
                    precip = float(data["snow"]["1h"])
                todayPrecipitation.setText(f"Precipitation: {precip} mm (last 1h)")

                # Mirror to Tonight
                tonightTemp.setText(f"Temperature: {t} °F")
                tonightWindSpeed.setText(f"Wind Speed: {ws} mph")
                tonightWindDirection.setText(f"Wind Direction: {wd_text}")
                tonightHumidity.setText(f"Humidity: {h}%")
                tonightPrecipitation.setText(f"Precipitation: {precip} mm (last 1h)")
            except Exception:
                # Show safe error text without crashing UI
                todayTemp.setText("Temperature: (error)")
                todayWindSpeed.setText("Wind Speed: (error)")
                todayWindDirection.setText("Wind Direction: (error)")
                todayHumidity.setText("Humidity: (error)")
                todayPrecipitation.setText("Precipitation: (error)")
                tonightTemp.setText("Temperature: (error)")
                tonightWindSpeed.setText("Wind Speed: (error)")
                tonightWindDirection.setText("Wind Direction: (error)")
                tonightHumidity.setText("Humidity: (error)")
                tonightPrecipitation.setText("Precipitation: (error)")

      
        location.returnPressed.connect(lambda: (
            update_today_tonight((location.text() or "Salt Lake City").strip()),
            self.trend_widget.plot_city((location.text() or "Salt Lake City").strip())
        ))

   
        default_city = "Salt Lake City"
        location.setText(default_city)
        update_today_tonight(default_city)
        self.trend_widget.plot_city(default_city)

wgui = QApplication(sys.argv)
window = MainWindow()
window.show()
