import io
import sys
import logging
import platform
from requests import *
from os import *
from json import load
from playsound import playsound
from datetime import datetime
from PyQt6 import QtWidgets
from ui import Ui_MainWindow
from PyQt6.QtGui import QIcon
from clicker import ReviewClicker
from configparser import ConfigParser
from key_manager import KeyManager
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        logging.basicConfig(level=logging.INFO)
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.key_manager = KeyManager()
        self.setFixedSize(self.size())
        self.ui.label.setStyleSheet("color: red")
        self.set_icons()
        self.ui.searchButton.clicked.connect(self.run_clicker)
        self.ui.pushButton.clicked.connect(self.get_chrome_user_data)
        self.os = platform.system()
        self.chrome_user_data = self.check_default_path()
        self.chrome_profile = "Default"
        self.setWindowTitle("NearCrowd Review Clicker")
        self.profiles = self.load_profiles()
        self.ui.comboBox.currentIndexChanged.connect(self.set_chrome_profile)
        self.ui.pushButton_2.clicked.connect(
            lambda: self.key_manager.set_key(self.ui.lineEdit.text())
        )
        self.ui.pushButton_2.clicked.connect(self.invalid_key_dialog)

        self.url = "http://127.0.0.1:5000/api/keys"
        self.set_activation_status()
        self.set_line_edit_key()
        self.manage_key()

    def manage_key(self):
        if not self.key_manager.validate_key():
            self.set_line_edit_key()
            self.key_manager.reset_key()
            self.set_activation_status()

    def unlock_ui(self):
        self.ui.searchButton.setEnabled(True)
        self.ui.comboBox.setEnabled(True)

        self.ui.pushButton_2.setEnabled(False)
        self.ui.lineEdit.setEnabled(False)

    def lock_ui(self):
        self.ui.searchButton.setEnabled(False)
        self.ui.pushButton.setEnabled(False)
        self.ui.comboBox.setEnabled(False)

        self.ui.pushButton_2.setEnabled(True)
        self.ui.lineEdit.setEnabled(True)

    def set_activation_status(self):
        if not self.key_manager.key_is_activated():
            self.lock_ui()

        else:
            self.unlock_ui()

    def set_chrome_profile(self):
        for key, value in self.profiles.items():
            if value == self.ui.comboBox.currentText():
                self.chrome_profile = key
                print(key)
                break

    def set_icons(self):
        if platform.system() == "Windows":
            self.ui.pushButton.setIcon(QIcon(r"img\folder.png"))
            self.setWindowIcon(QIcon(r"img\nearcrowd.jpg"))
        elif platform.system() == "Linux":
            self.ui.pushButton.setIcon(QIcon("img/folder.png"))
            self.setWindowIcon(QIcon("img/nearcrowd.jpg"))

    def run_clicker(self):
        if self.check_empty_fields() and self.check_chrome_profile(
            self.ui.comboBox.currentText()
        ):
            print(self.chrome_profile)
            clicker = ReviewClicker(self.chrome_user_data, self.chrome_profile)
            clicker.load_page()
            clicker.find_review()
            playsound("sounds/sound.mp3")

    def set_line_edit_key(self):
        if self.config.has_option("Key", "key"):
            self.ui.lineEdit.setText(self.config["Key"]["key"])
        else:
            self.ui.lineEdit.setText("Enter your key here")

    def check_default_path(self):
        user = getlogin()

        if self.os == "Windows":
            default_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"
        elif self.os == "Linux":
            default_path = rf"/home/{user}/.config/google-chrome/"

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

                if self.os == "Windows":
                    chrome_profile_name_path = (
                        rf"{path}\{initial_profile_name}\Preferences"
                    )

                    real_profile_name = self.get_profile_name_from_file(
                        chrome_profile_name_path
                    )

                elif self.os == "Linux":
                    chrome_profile_name_path = (
                        rf"{path}/{initial_profile_name}/Preferences"
                    )

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

    def invalid_key_dialog(self):
        if not self.key_manager.key_exists() or not self.key_manager.key_outdated():
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon(r"img\not_found.png"))
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setText("The key is invalid!")
            msgBox.setWindowTitle("Warning!")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)

            msgBox.exec()

        else:
            self.set_activation_status()

    def expired_key_dialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(r"img\not_found.png"))
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("The key is expired!")
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
