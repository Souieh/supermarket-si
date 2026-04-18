import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import InfoBar, InfoBarPosition
from src.modules.database import Database
from src.ui.config_dialog import ConfigDialog
from src.ui.launcher_window import LauncherWindow
from src.ui.admin_window import AdminWindow
from src.ui.login_window import LoginWindow


class SupermarketApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.set_global_font()
        self.login = None
        self.launcher = None
        self.admin_win = None
        self.cashier_win = None

    def set_global_font(self):
        # Choose a UI-friendly font
        font = QFont("Segoe UI", 10)
        if not QFont(font).exactMatch():
            font = QFont("DejaVu Sans", 10)
        self.app.setFont(font)

    def start(self):
        self.show_launcher()
        sys.exit(self.app.exec())

    def center_window(self, window):
        frame = window.frameGeometry()
        center_point = self.app.primaryScreen().availableGeometry().center()
        frame.moveCenter(center_point)
        window.move(frame.topLeft())

    def show_launcher(self):
        if self.admin_win:
            self.admin_win.close()
        if self.cashier_win:
            self.cashier_win.close()
        self.launcher = LauncherWindow()
        # Connect cards directly
        self.launcher.adminCard.clicked.connect(self.open_admin)
        self.launcher.cashierCard.clicked.connect(self.open_cashier)
        self.launcher.settingsCard.clicked.connect(self.open_settings)
        self.center_window(self.launcher)
        self.launcher.show()

    def open_admin(self):
        db = Database()
        success, _ = db.connect()
        if not success:
            self.open_settings()
            return

        self.login = LoginWindow(target_role="admin", title="دخول الإدارة")
        self.login.loginSuccess.connect(self._do_open_admin)
        self.center_window(self.login)
        self.login.show()
        if self.launcher:
            self.launcher.hide()

    def _do_open_admin(self, role):
        if self.login:
            self.login.close()
        if self.cashier_win:
            self.cashier_win.close()
        self.admin_win = AdminWindow()
        self.admin_win.switchToCashier.connect(self.open_cashier)
        self.admin_win.returnToLauncher.connect(self.show_launcher)
        self.center_window(self.admin_win)
        self.admin_win.show()

    def open_cashier(self):
        db = Database()
        success, _ = db.connect()
        if not success:
            self.open_settings()
            return

        self.login = LoginWindow(target_role="cashier", title="دخول الكاشير")
        self.login.loginSuccess.connect(self._do_open_cashier)
        self.center_window(self.login)
        self.login.show()
        if self.launcher:
            self.launcher.hide()
        if self.admin_win:
            self.admin_win.hide()

    def _do_open_cashier(self, role):
        if self.login:
            self.login.close()
        # Show Coming Soon message and do not open the window
        InfoBar.info(
            title="قريباً",
            content="واجهة الكاشير قيد التطوير حالياً.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=None
        )
        self.show_launcher()

    def open_settings(self):
        dialog = ConfigDialog()
        if dialog.exec():
            host, port, db_name, user, password = dialog.get_config()
            Database().save_config(host, port, db_name, user, password)
            if self.launcher:
                self.launcher.check_connection()


def main():
    app = SupermarketApp()
    app.start()


if __name__ == "__main__":
    main()
