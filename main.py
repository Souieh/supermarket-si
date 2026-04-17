import sys
from PyQt6.QtWidgets import QApplication
from src.modules.database import Database
from src.ui.config_dialog import ConfigDialog
from src.ui.launcher_window import LauncherWindow
from src.ui.admin_window import AdminWindow
from src.ui.cashier_window import CashierWindow

class SupermarketApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.launcher = None
        self.admin_win = None
        self.cashier_win = None

    def start(self):
        self.show_launcher()
        sys.exit(self.app.exec())

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
        self.launcher.show()

    def open_admin(self):
        db = Database()
        success, _ = db.connect()
        if not success:
            self.open_settings()
            return
        if self.cashier_win:
            self.cashier_win.close()
        self.admin_win = AdminWindow()
        self.admin_win.switchToCashier.connect(self.open_cashier)
        self.admin_win.returnToLauncher.connect(self.show_launcher)
        self.admin_win.show()
        self.launcher.hide()

    def open_cashier(self):
        db = Database()
        success, _ = db.connect()
        if not success:
            self.open_settings()
            return
        if self.admin_win:
            self.admin_win.close()
        self.cashier_win = CashierWindow()
        self.cashier_win.switchToAdmin.connect(self.open_admin)
        self.cashier_win.returnToLauncher.connect(self.show_launcher)
        self.cashier_win.show()
        self.launcher.hide()

    def open_settings(self):
        dialog = ConfigDialog()
        if dialog.exec():
            host, port, db_name = dialog.get_config()
            Database().save_config(host, port, db_name)
            if self.launcher:
                self.launcher.check_connection()

def main():
    app = SupermarketApp()
    app.start()

if __name__ == "__main__":
    main()
