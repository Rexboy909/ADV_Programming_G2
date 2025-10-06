# Created by Rex
# Other contributors:
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QTabWidget, QToolBar, QMessageBox, QColorDialog, QMenu, QToolButton
from PySide6.QtGui import QAction, QColor, QCursor
from PySide6.QtCore import QSize, Qt

import sys, weatherData, weatherPlotterDualAxis, trend_view

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

       
        # Date and Location
        dateLocation = QWidget() #date and location widget
        dateLocation.setAttribute(Qt.WA_StyledBackground, True)  # allow styling background
        dateLocationLayout = QHBoxLayout() #setting a horizontal layout
        dateLocation.setLayout(dateLocationLayout) #setting the layout to the date and location widget


        locationLabel = QLabel("Location")
        locationLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop) # aligning the label to the left

        dateLocationLayout.addWidget(locationLabel) #adding the label to the layout

        location = QLineEdit()
        location.setPlaceholderText("Enter Location") 

        dateLocationLayout.addWidget(location) #adding the input field to the layout

        dateLabel = QLabel("Date:") 
        dateLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)

        dateLocationLayout.addWidget(dateLabel) #adding the date label to the layout

        date = QDateTimeEdit() 
        date.setCalendarPopup(True)
        date.setDateTime(date.dateTime().currentDateTime()) #setting the current date and time as default
        dateLocationLayout.addWidget(date) #adding the date input field to the layout
        
        # day tab content
        todayTab = QWidget()
        todayTab.setAttribute(Qt.WA_StyledBackground, True)  # Ensure background is styled
        todayTabLayout = QHBoxLayout()
        todayTab.setLayout(todayTabLayout)
        todayStatsLayout = QVBoxLayout()
        todayTabLayout.addLayout(todayStatsLayout)
        
        todayTemp = QLabel("Temperature: " + str(weatherData.temp)+"°F")
        todayWindSpeed = QLabel("Wind Speed: "+ str(weatherData.windSpeed)+" m/s")
        todayWindDirection = QLabel("Wind Direction: " + str(weatherData.windDir)+"°")
        todayHumidity = QLabel("Humidity: " + str(weatherData.humidity)+"%")
        todayPrecipitation = QLabel("Precipitation: "+ weatherData.precipitation)
        todayStatsLayout.addWidget(todayTemp)
        todayStatsLayout.addWidget(todayWindSpeed)
        todayStatsLayout.addWidget(todayWindDirection)
        todayStatsLayout.addWidget(todayHumidity)
        todayStatsLayout.addWidget(todayPrecipitation)

        # Image support is possible
        # todayimg = QPixmap()
        # todayimg.load("weather_app/assets/sunny.png")
        # todayimg = todayimg.scaled(QSize(100,100), Qt.KeepAspectRatio) #scaling the image to fit the label
        # todayTabLayout.addWidget(QLabel(pixmap=todayimg)) #adding the image to the layout

        # night tab content
        tonightTab = QWidget()
        tonightTab.setAttribute(Qt.WA_StyledBackground, True)  # Ensure background is styled
        tonightTabLayout = QHBoxLayout()
        tonightTab.setLayout(tonightTabLayout)
        tonightStatsLayout = QVBoxLayout()
        tonightTabLayout.addLayout(tonightStatsLayout)

        # initialize tonight labels from weatherData module variables
        tonightTemp = QLabel(f"Min/Max: {weatherData.tempMin} / {weatherData.tempMax}")
        tonightWindSpeed = QLabel("Wind Speed: " + str(weatherData.windSpeed))
        tonightWindDirection = QLabel("Wind Direction: " + str(weatherData.windDir))
        tonightHumidity = QLabel("Humidity: " + str(weatherData.humidity) + "%")
        tonightPrecipitation = QLabel("Precipitation: " + str(weatherData.precipitation))
        tonightStatsLayout.addWidget(tonightTemp)
        tonightStatsLayout.addWidget(tonightWindSpeed)
        tonightStatsLayout.addWidget(tonightWindDirection)
        tonightStatsLayout.addWidget(tonightHumidity)
        tonightStatsLayout.addWidget(tonightPrecipitation)
        
        def setColors(dayColorTxt, dayColorBG):
            # Accept either QColor or string; fall back to defaults if invalid
            def _to_name(val, fallback):
                if isinstance(val, QColor):
                    return val.name() if val.isValid() else fallback
                if isinstance(val, str) and val:
                    return val
                return fallback

            txt = _to_name(dayColorTxt, "#000000")
            bg = _to_name(dayColorBG, "#CCEAFF")

            # main/background containers
            self.setStyleSheet(f"background-color: {bg};")
            dateLocation.setStyleSheet(f"background-color: {bg}; border: none;")
            todayTab.setStyleSheet(f"background-color: {bg}; border: none;")
            tonightTab.setStyleSheet(f"background-color: {bg}; border: none;")
            # inline widgets
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
            # toolbar styling (toolbar variable created after setColors definition; safe because setColors is called later)
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
                QToolButton:hover {{
                    background: rgba(0,0,0,0.04);
                }}
                """)
            except NameError:
                # toolbar not created yet; styling will be applied when setColors is called later
                pass

            # tabs: pane (page) and tab outlines / text color via QSS
            tab_style = f'''
            QTabWidget::pane {{
                background-color: {bg};
                border: 1px solid {txt};
                top: -1px;
            }}
            QTabBar::tab {{
                color: {txt};
                background: transparent;
                padding: 6px 12px;
                margin: 2px;
                border: 1px solid {txt};
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background: {bg};
                margin-bottom: 0;
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background: rgba(0,0,0,0.03);
            }}
            QTabBar::tab:focus {{
                outline: none;
            }}
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
        # Fetch action: request new API data for the entered location and update UI
        def fetch_for_location():
            # Use weatherData.fetch_for_city so UI stays free of API logic
            city = location.text().strip()
            if not city:
                QMessageBox.warning(self, "No Location", "Please enter a location before fetching data.")
                return
            try:
                import weatherData
                vals = weatherData.fetch_for_city(city)
                new_temp = vals.get('temp', 'N/A')
                new_wind = vals.get('windSpeed', 'N/A')
                new_wind_dir = vals.get('windDir', 'N/A')
                new_humidity = vals.get('humidity', 'N/A')

                todayTemp.setText(f"Temperature: {new_temp}°F" if new_temp != "N/A" else "Temperature: N/A")
                todayWindSpeed.setText(f"Wind Speed: {new_wind} m/s" if new_wind != "N/A" else "Wind Speed: N/A")
                todayWindDirection.setText(f"Wind Direction: {new_wind_dir}°" if new_wind_dir != "N/A" else "Wind Direction: N/A")
                todayHumidity.setText(f"Humidity: {new_humidity}%" if new_humidity != "N/A" else "Humidity: N/A")

                # update tonight tab info (min/max, same wind/humidity/precip if available)
                tonightTemp.setText(f"Min/Max: {vals.get('tempMin','N/A')} / {vals.get('tempMax','N/A')}")
                tonightWindSpeed.setText(f"Wind Speed: {vals.get('windSpeed','N/A')} m/s")
                tonightWindDirection.setText(f"Wind Direction: {vals.get('windDir','N/A')}°")
                tonightHumidity.setText(f"Humidity: {vals.get('humidity','N/A')}%")
                tonightPrecipitation.setText(f"Precipitation: {vals.get('precipitation','N/A')}")

                # refresh plotter if available
                try:
                    dp = None
                    try:
                        dp = dataPlotter
                    except NameError:
                        try:
                            dp = getattr(self, 'dataPlotter')
                        except Exception:
                            dp = None
                    if dp:
                        x = ["Now"]
                        y = [new_temp if isinstance(new_temp, (int, float)) else 0]
                        precip = [0.0]
                        try:
                            dp.add_city_data(city, x, y, precip)
                            dp.plot()
                        except Exception:
                            pass
                except Exception:
                    pass

            except Exception as e:
                QMessageBox.critical(self, "Fetch Error", f"Failed to fetch weather for {city}: {e}")

        fetch_action = QAction("Fetch", self)
        fetch_action.setToolTip("Fetch weather for the entered location")
        fetch_action.triggered.connect(fetch_for_location)
        toolbar.addAction(fetch_action)
        # --- end toolbar insertion ---

        dataPlotter = weatherPlotterDualAxis.WeatherPlotterDualAxis(parent=tabs)
        dataPlotter.add_city_data("CityA", ["08:00","12:00","16:00"], [60,72,68], [0.0, 1.2, 0.3])
        dataPlotter.add_city_data("CityB", ["08:00","12:00","16:00"], [55,70,66], [0.0, 0.5, 0.0])
        dataPlotter.plot()
        tabs.addTab(dataPlotter, "Data Plot")
        dataPlotter.set_theme_colors(*self._day_colors)
        
        trendView = trend_view.TemperatureTrendView("04b2c70f5678cb788cb9d62c0325ef32",parent=tabs)
        tabs.addTab(trendView, "Trends")
        
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
wgui = QApplication(sys.argv)
window = MainWindow()
window.show()
