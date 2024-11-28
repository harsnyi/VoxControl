from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
import requests
from dashboard.dashboard import DashboardApp
from dashboard.constants import URL

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QGridLayout()

        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label, 0, 0)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 0, 1)

        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, 1, 1)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button, 2, 0, 1, 2)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        payload = {"username": username, "password": password}

        try:
            response = requests.post(f"{URL}/user/authenticate", json=payload)

            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                refresh_token = data.get('refresh_token')

                QMessageBox.information(self, "Success", f"Logged in successfully!")

                self.open_dashboard(access_token, refresh_token)

            elif response.status_code == 401:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
            else:
                QMessageBox.warning(self, "Error", f"Unexpected Error: {response.json()}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Unable to connect to the server.\n{e}")

    def open_dashboard(self, access_token, refresh_token):
        self.close()
        self.dashboard = DashboardApp(access_token, refresh_token)
        self.dashboard.show()
