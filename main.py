from PyQt5.QtWidgets import QApplication
import sys
from dashboard.login import LoginApp

def main():
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
