from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QGridLayout, QListWidget
import requests
from dashboard.audio import Audio
from utils import generate_short_id
from dashboard.controller import Controller
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from dashboard.constants import URL
import os

class DashboardApp(QWidget):
    def __init__(self, access_token, refresh_token):
        super().__init__()
        self.setWindowTitle("Vox Controller")
        self.setGeometry(200, 200, 800, 600)
        self.access_token = access_token
        self.refresh_token = refresh_token
        layout = QGridLayout()
        layout.addWidget(QLabel("Welcome to the Vox Controller!"), 0, 0)


        self.record_button = QPushButton("Record Sound")
        self.record_button.setStyleSheet("background-color: #C9DDFF; border-radius: 5px")
        self.record_button.clicked.connect(self.record_sound)
        layout.addWidget(self.record_button, 2, 0)
        
        self.record_button = QPushButton("Get info")
        self.record_button.clicked.connect(self.get_info)
        layout.addWidget(self.record_button, 0, 1)


        self.info_list_widget = QListWidget()
        layout.addWidget(self.info_list_widget, 1, 1)
        self.command_result_label = QLabel("Command result will appear here")
        layout.addWidget(self.command_result_label, 2, 1)

        self.post_response_list_widget = QListWidget()
        layout.addWidget(self.post_response_list_widget, 3, 1)

        self.setLayout(layout)
        
    def get_info(self):
        url = f"{URL}/home/get_info"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.display_info(data)
                else:
                    QMessageBox.warning(self, "Error", "Received data is not a list.")
            else:
                QMessageBox.warning(self, "Error", f"Failed to retrieve user info. Status Code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Unable to connect to the server.\n{e}")


    def display_info(self, info_list):
        self.info_list_widget.clear()

        for item in info_list:
            id = item.get('id', 'Unknown')
            name = item.get('name', 'Unknown')
            status = item.get('status', 'Unknown')
            running = item.get('runtime', '')

            if status == "stopped":
                display_text = f"{id} - {name}: {status}"
            else:
                display_text = f"{id} - {name}: {status} - {running}"
            
            list_item = QListWidgetItem(display_text)

            font = QFont()
            font.setPointSize(16)
            list_item.setFont(font)
            label = QLabel(display_text)
        
            if status.lower() == 'stopped':
                label.setAlignment(Qt.AlignRight)
                list_item.setBackground(QColor('#DE6C83'))
            elif status.lower() == 'running':
                list_item.setBackground(QColor('#2CF6B3'))

            self.info_list_widget.addItem(list_item)
            

    def record_sound(self):
        controller = Controller()
        print("Record for 5 seconds")
        uuid = generate_short_id()
        audio = Audio(uuid=uuid)
        audio.record()
        print("Recognizing your voice ...")
        recognized_text = audio.recognize_audio()
        
        result = controller.run_command(recognized_text)
        self.command_result_label.setText(f"{result[1]}")
        if result[0]:
            self.send_post_request(result[0])
        print(result[0])

    
    def send_post_request(self, command: dict):
        url = f"{URL}/home/execute"

        payload = {
            "action": command["action"],
            "modifier": command['modifier'],
            "id": command["id"]
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                print("Command executed successfully!")
                response_text = response.json()["message"]
                
                self.append_to_post_response_list(f"{response.status_code} - {response_text}")
            else:
                error_text = f"{response.status_code} - {response.json()["message"]}"
                self.append_to_post_response_list(error_text)
        except requests.exceptions.RequestException as e:
            error_text = f"500 - {e}"
            self.append_to_post_response_list(error_text)

    def append_to_post_response_list(self, message):
        list_item = QListWidgetItem(message)
        font = QFont()
        font.setPointSize(12)
        list_item.setFont(font)
        if message.startswith("500"):
            list_item.setBackground(QColor("#DE6C83"))
        elif message.startswith("200"):
            list_item.setBackground(QColor('#2CF6B3'))

        self.post_response_list_widget.addItem(list_item)