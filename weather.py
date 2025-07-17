import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,
QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("icon.jpg"))

        self.city_label=QLabel("Enter city name: ",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Check Weather",self)
        self.temprature_label=QLabel(self)
        self.wind_speed_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.emoje_label=QLabel("",self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather")

        vbox=QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.wind_speed_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.emoje_label)
    
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        # self.wind_speed_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        # self.emoje_label.setAlignment(Qt.AlignCenter)

        self.city_input.setObjectName("city_input")
        self.city_label.setObjectName("city_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temprature_label.setObjectName("temprature_label")
        # self.wind_speed_label.setObjectName("wind_speed_label")
        self.emoji_label.setObjectName("emoji_label")
        # self.emoje_label.setObjectName("emoje_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family: georgia;
                           }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
                           }
            QLineEdit#city_input{
                font-size: 40px;
                           }
            QPushButton#get_weather_button{
                font-size: 40px;
                font-weight: bold;           
                           }
            QLabel#temprature_label{
                font-size: 80px; 
                           }           
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
                           }
            QLabel#description_label{
                font-size: 40px;           
                           }
            # QLabel#wind_speed_label{
            #     font-size: 80px;           
            #                }
            # QLabel#emoje_label{
            #     font-size: 100px;
            #     font-family: Segoe UI emoji
            #                }

        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)


    def get_weather(self):
        api_key="2462c492fd050d5a704ff332c9dc0c96"
        city= self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response=requests.get(url)
            data = response.json()
            response.raise_for_status()
            if data["cod"]==200:
                self.show_weather(data)
            
        except requests.exceptions.HTTPError as http_errror:
            match response.status_code :
                case 400:
                    self.show_error("Bad request:\nPlease check your input")
                case 401:
                    self.show_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.show_error("Forbidden:\nAccess is denied")
                case 404:
                    self.show_error("Not found:\nCity not Found")
                case 500:
                    self.show_error("Internal server error:\nPlease try again later")
                case 502:
                    self.show_error("Bad gateway:\nInvalid response from the server")
                case 503:
                    self.show_error("Service Unavailable:\nServer is down ")
                case 504:
                    self.show_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.show_error(f"HTTP error occured:\n{http_errror}")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.show_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.show_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.show_error(f"Request Error:\n{req_error}")


    def show_error(self,message):
        self.temprature_label.setStyleSheet("font-size:30px;")
        self.temprature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        # self.wind_speed_label.clear()
        # self.emoje_label.clear()
        

    def show_weather(self, data):
        self.temprature_label.setStyleSheet("font-size:80px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id=data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        

        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.temprature_label.setText(f"{temperature_c:.0f}°C")
        self.description_label.setText(f"{weather_description}")
    
    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id >= 200 and weather_id <=232:
            return "⛈️"
        elif weather_id >= 300 and weather_id <=321:
            return "🌦️"
        elif weather_id >= 500 and weather_id <=531:
            return "🌧️"
        elif weather_id >= 600 and weather_id <=622:
            return "❄️"
        elif weather_id >= 701 and weather_id <=741:
            return "🌫️"
        elif weather_id == 751 and weather_id ==761:
            return ".･:･"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id >= 801 and weather_id <=804:
            return "☁️"
        else:
            return " "
        

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
