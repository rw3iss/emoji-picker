import sys
import keyboard
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QAction, QIcon, QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Emoji Picker")
        self.initLayout()

    def initLayout(self):
        self.setCentralWidget(QWidget(self))
        self.resize(200, 400)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.vbox.addWidget(QLabel("Emoji Picker"))

        self.emojiLayout = QGridLayout()
        self.emojiLayout.addWidget(QLabel("👌"), 0, 0)
        self.emojiLayout.addWidget(QLabel("👍🏻"), 0, 1)
        self.emojiLayout.addWidget(QLabel("🙏🏻"), 1, 0)
        self.emojiLayout.addWidget(QLabel("😬"), 1, 1)
        self.emojiLayout.addWidget(QLabel("🥁"), 2, 0)
        self.emojiLayout.addWidget(QLabel("❤️"), 2, 1)

        self.vbox.addLayout(self.emojiLayout)

        self.centralWidget().setLayout(self.vbox)
        self.centralWidget().setStyleSheet(
            # ("* {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"
            #                "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 blue);}");
            "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 blue); color: white; text-align: center; border-radius: 5px; padding: 10px; font-size: 20pt; width: 200px; height: 400px; border: 2px solid #55aa88;")


class KeyBoardManager(QObject):
    ShortcutSignal = pyqtSignal()
    QuitSignal = pyqtSignal()

    def start(self):
        keyboard.add_hotkey("F1", self.ShortcutSignal.emit, suppress=True)
        keyboard.add_hotkey("F2", self.QuitSignal.emit, suppress=True)


class SystemTrayApp(QSystemTrayIcon):
    def __init__(self):  # , icon, parent=None):
        super().__init__()  # icon, parent)

        self.mainWindow = MainWindow()

        self.setIcon(QIcon("./resources/trayIcon.ico"))
        self.setToolTip("Emoji Picker")

        self.initMenu()

        # self.activated.connect(self.onTrayIconActivated)
        self.quitAction.triggered.connect(QApplication.instance().quit)
        self.testAction.triggered.connect(self.onTestAction)

        manager = KeyBoardManager(self)
        manager.ShortcutSignal.connect(self.onPopupActivated)
        manager.QuitSignal.connect(QApplication.instance().quit)
        manager.start()

        self.setVisible(True)
        self.show()

    def initMenu(self):
        self.menu = QMenu(parent=None)  # parent)
        self.quitAction = QAction("Quit")  # , parent)
        self.menu.addAction(self.quitAction)
        self.testAction = QAction('Test Action')  # , parent)
        self.menu.addAction(self.testAction)
        self.setContextMenu(self.menu)

    def onPopupActivated(self):
        print("Popup activated.")
        cursorPos = QCursor().pos()
        POPUP_X_OFFSET = -20
        POPUP_Y_OFFSET = -5
        cursorPos.setX(cursorPos.x() + POPUP_X_OFFSET)
        cursorPos.setY(cursorPos.y() + POPUP_Y_OFFSET)
        self.mainWindow.move(cursorPos)
        self.mainWindow.show()

    def onTestAction(self, s):
        print("TEST")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trayApp = SystemTrayApp()

    # app.installEventFilter(tray)
    app.setQuitOnLastWindowClosed(False)

    # shortcut = QShortcut(QKeySequence("Ctrl+B"), tray)
    # shortcut.activated.connect(tray.onShortcutActivated)

    sys.exit(app.exec())
