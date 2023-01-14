import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtGui import QMovie, QPainter, QPixmap
from game.client.UI.menuUI import Ui_MainWindow
from game.client.app_state import AppState
from game.client.main import main


class MainWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_dialog = QFileDialog(self)
        self.OnlineConnectionButton.clicked.connect(self.handle_connection)
        self.ExitButton.clicked.connect(self.handle_exit)
        self.SettingsButton.clicked.connect(self.settings_menu)
        self.ToMenuButton.clicked.connect(self.handle_to_menu)
        self.VolumeButton.clicked.connect(self.edit_volume)
        self.SizeButton.clicked.connect(self.edit_size)
        self.VolumeButton.hide()
        self.SizeButton.hide()
        self.ToMenuButton.hide()
        self.movie = QMovie(".gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def handle_connection(self):
        server_ip, ok_pressed = QInputDialog.getText(self, 'Подключение к серверу', 'Введите ip сервера')

        if ok_pressed:
            main(server_ip, 2023)

    def settings_menu(self):
        self.VolumeButton.show()
        self.SizeButton.show()
        self.ToMenuButton.show()
        self.OnlineConnectionButton.hide()
        self.ExitButton.hide()
        self.SettingsButton.hide()

    def handle_exit(self):
        sys.exit()

    def handle_to_menu(self):
        self.VolumeButton.hide()
        self.SizeButton.hide()
        self.ToMenuButton.hide()
        self.OnlineConnectionButton.show()
        self.ExitButton.show()
        self.SettingsButton.show()

    def edit_volume(self):
        pass

    def edit_size(self):
        width, ok_pressed = QInputDialog.getInt(
            self, "Введите ширину", "Введите ширину окна",
            1920, 1, 10000, 1)
        if ok_pressed:
            height, ok_pressed = QInputDialog.getInt(
                self, "Введите высоту", "Введите высоту окна",
                1080, 1, 7000, 1)
            if ok_pressed:
                self.setGeometry(0, 0, width, height)

        AppState.set_screen_resolution(self.size().width(), self.size().height())


def menu():
    app = QApplication(sys.argv)
    app.setStyleSheet('')
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())
