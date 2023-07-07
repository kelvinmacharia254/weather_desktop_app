import sys ,requests, logging, threading, pprint
from datetime import*
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from weatherApi import *

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        threading.Thread( target = self.keepRunning, daemon = True ).start()


        self.cityOrId()
        self.ui.pushButton_Search.clicked.connect(self.cityOrId)

    def keepRunning(self):
        while True:
            if self.ui.lineEdit_NameorID.text().strip() == '':
                self.ui.pushButton_Search.setEnabled(False)
                #logging.debug("'pushButton_Search' disable.")
            else:
                self.ui.pushButton_Search.setEnabled(True)
                #logging.debug("'pushButton_Search' enabled.")

    def cityOrId(self): #determine whether to search by ID or City's Name
        # a38eb4269ce410a9f48c7453beec1ca1
            try:
                cityId = self.ui.lineEdit_NameorID.text().strip()
                int(cityId)
                url = "http://api.openweathermap.org/data/2.5/weather?id=" \
                        +str(cityId)+"&appid=237ec7ebf9e55cae7d76169e622669ea"
                logging.debug("Searching '"+url+"' by ID.")
                self.search(url)
            except ValueError:
                cityName = self.ui.lineEdit_NameorID.text().strip()
                url = "http://api.openweathermap.org/data/2.5/weather?q=" \
                  + cityName + "&appid=237ec7ebf9e55cae7d76169e622669ea"
                logging.debug("Searching '" + url + "' by Name.")
                self.search(url)

    def search(self, url):
        try:
            weatherApiResponse = requests.get(url)
            weather_dic = weatherApiResponse.json()

            if weatherApiResponse.status_code == 200:
                logging.debug("Your request was successful.\n")
                self.display_weather(weather_dic)
                self.ui.statusbar.showMessage("Displaying weather info for "+weather_dic["name"]+".")
            else: #handles error 404 i.e unavailability of the requested info.
                #QMessageBox.information(self, "Weather api","Error " + weather_dic["cod"] + ": " + weather_dic["message"]+". Please enter a valid city name or ISO ID.")
                self.ui.statusbar.showMessage(weather_dic["message"]+".Enter valid city name or ISO ID.")
        except Exception as error:
            logging.debug("Error: %s" %(error))
            QMessageBox.information(self, "Weather api", "Bad connection, check your internet connectivity.")

    def display_weather(self, weather_dic):

        date = datetime.fromtimestamp(weather_dic["dt"]).strftime("%a %d %b,%Y %I:%M %p" )
        whereLocation = str(weather_dic["name"]) + ", " + str(weather_dic["sys"]["country"])
        geoLocation = "(Latitude: " + str(weather_dic["coord"]["lat"]) + ", Longitude: " + str(weather_dic["coord"]["lon"])+")"

        humidity = str(weather_dic["main"]["humidity"])+ "%"
        pressure = str(weather_dic["main"]["pressure"])+" hPa"
        temp = str(round(float(weather_dic["main"]["temp"]) - 273))+"\u00b0C"
        temp_feels_like = str(round(float(weather_dic["main"]["feels_like"]) - 273)) + "\u00b0C"
        tempMax = str(round(float(weather_dic["main"]["temp_max"]) - 273))+"\u00b0C"
        tempMin = str(round(float(weather_dic["main"]["temp_min"]) - 273))+"\u00b0C"


        self.ui.label_whereLocation.setText(whereLocation+"  "+date)
        self.ui.label_humidity.setText(humidity)
        self.ui.label_pressure.setText(pressure)
        self.ui.label_temp_feeling_like.setText("Feels like "+temp_feels_like)
        self.ui.label_temp.setText(temp)
        self.ui.label_temp_2.setText(tempMin+" / "+tempMax)

        pprint.pprint(weather_dic)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
