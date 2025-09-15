from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QTabWidget
from PySide6.QtCore import QSize, Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        dayColor = "#000000"  # Default color for day tab text
        # Date and Location
        dateLocation = QWidget() #date and location widget
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
        todayTab.setStyleSheet("background-color: #e0f7fa; border: none;")  # Remove border, fill background
        todayTabLayout = QHBoxLayout()
        todayTab.setLayout(todayTabLayout)
        todayStatsLayout = QVBoxLayout()
        todayTabLayout.addLayout(todayStatsLayout)
        
        def setDayColors(dayColor):
            color = todayTab.styleSheet()
            todayTemp.setStyleSheet("color: "+dayColor+";")
            todayWindSpeed.setStyleSheet("color: "+dayColor+";")
            todayWindDirection.setStyleSheet("color: "+dayColor+";")
            todayHumidity.setStyleSheet("color: "+dayColor+";")
            todayPrecipitation.setStyleSheet("color: "+dayColor+";")
            return color # returning the old color, incase you want to revert back
        
        def setNightColors(nightColor):
            color = tonightTab.styleSheet()
            tonightTemp.setStyleSheet("color: "+nightColor+";")
            tonightWindSpeed.setStyleSheet("color: "+nightColor+";")
            tonightWindDirection.setStyleSheet("color: "+nightColor+";")
            tonightHumidity.setStyleSheet("color: "+nightColor+";")
            tonightPrecipitation.setStyleSheet("color: "+nightColor+";")
            return color # returning the old color, incase you want to revert back

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

        # Image support is possible
        # todayimg = QPixmap()
        # todayimg.load("weather_app/assets/sunny.png")
        # todayimg = todayimg.scaled(QSize(100,100), Qt.KeepAspectRatio) #scaling the image to fit the label
        # todayTabLayout.addWidget(QLabel(pixmap=todayimg)) #adding the image to the layout

        # night tab content
        tonightTab = QWidget()
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

        # Tabs setting
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.addTab(todayTab, "Today")
        tabs.addTab(tonightTab, "Tonight")

        # Main Widget
        main = QWidget()
        mainLayout = QVBoxLayout() # creating a layout
        main.setLayout(mainLayout) #setting the layout to the main widget. IDK why it has to be done this way but
        mainLayout.addWidget(dateLocation)
        mainLayout.addWidget(tabs)

        self.setCentralWidget(main)

wgui = QApplication(sys.argv)
window = MainWindow()
window.show()
