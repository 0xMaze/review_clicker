import io
import sys
import logging
from os import *
from json import load
from playsound import playsound
from PyQt6 import QtWidgets
from ui import Ui_MainWindow
from PyQt6.QtGui import QIcon
from clicker import ReviewClicker
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        logging.basicConfig(level=logging.INFO)
        self.setFixedSize(self.size())
        self.ui.label.setStyleSheet("color: red")
        self.ui.pushButton.setIcon(QIcon(r"img\folder.png"))
        self.ui.searchButton.clicked.connect(self.run_clicker)
        self.ui.pushButton.clicked.connect(self.get_chrome_user_data)
        self.chrome_user_data = self.check_default_path()
        self.chrome_profile = "Default"
        self.setWindowTitle("NearCrowd Review Clicker")
        self.setWindowIcon(QIcon(r"img\nearcrowd.jpg"))
        self.profiles = self.load_profiles()
        self.ui.comboBox.currentIndexChanged.connect(self.set_chrome_profile)

    def set_chrome_profile(self):
        for key, value in self.profiles.items():
            if value == self.ui.comboBox.currentText():
                self.chrome_profile = key
                print(key)
                break

    def run_clicker(self):
        if self.check_empty_fields() and self.check_chrome_profile(
            self.ui.comboBox.currentText()
        ):
            print(self.chrome_profile)
            clicker = ReviewClicker(self.chrome_user_data, self.chrome_profile)
            clicker.load_page()
            clicker.find_review()
            playsound("sound.mp3")

    def check_default_path(self):
        user = getlogin()
        default_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"

        if path.exists(default_path):
            self.ui.label.setText("Path found!")
            self.ui.label.setStyleSheet("color: green")
            self.ui.pushButton.setEnabled(False)

            return default_path
        else:
            self.show_not_found_path_dialog()
            return self.get_chrome_user_data()

    def check_chrome_profile(self, profile_name):
        for i in self.profiles:
            print(i)
            if self.profiles[i] == profile_name:
                return True
        return False

    def check_empty_fields(self):
        if self.chrome_user_data == "":
            self.show_empty_fields_dialog()
            return False
        else:
            return True

    def get_profile_name_from_file(self, file_path):
        with io.open(file_path, "r", encoding="utf-8") as f:
            data = load(f)

        return data["profile"]["name"]

    def load_profiles(self):
        path = self.chrome_user_data
        real_profile_name = ""

        profiles = dict()

        for f in scandir(path=path):
            if f.name.__contains__("Profile") or f.name.__contains__("Default"):

                if f.name == "Guest Profile" or f.name == "System Profile":
                    continue

                initial_profile_name = f.name
                chrome_profile_name_path = rf"{path}\{initial_profile_name}\Preferences"

                real_profile_name = self.get_profile_name_from_file(
                    chrome_profile_name_path
                )

                profiles[f.name] = real_profile_name
                self.ui.comboBox.addItem(real_profile_name)

        return profiles

    def show_empty_fields_dialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(r"img\not_found.png"))
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("Not all fields are filled in!")
        msgBox.setWindowTitle("Warning!")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        msgBox.exec()

    def show_incorrect_profile_dialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(r"img\not_found.png"))
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("Invalid chrome profile!")
        msgBox.setWindowTitle("Warning!")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        msgBox.exec()

    def show_not_found_path_dialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(r"img\not_found.png"))
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("Chrome user data directory not found!")
        msgBox.setWindowTitle("Warning!")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

        msgBox.exec()

    def get_chrome_user_data(self):
        chrome_user_data = QFileDialog.getExistingDirectory(
            self,
            "Open chrome user data directory",
            r"C:\Users\user\AppData\Local\Google\Chrome\User Data",
        )

        self.ui.label.setText("Path found!")
        self.ui.label.setStyleSheet("color: green")

        return chrome_user_data


def main():
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
