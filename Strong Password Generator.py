import sys
import random
import string
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QGroupBox, QCheckBox, QLabel, QSlider, QAction,
    QMenuBar, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QPen, QBrush

def create_modern_icon(size=256):
    COLOR_BACKGROUND = Qt.transparent
    COLOR_LOCK_BODY = QColor("#3E3E3E")
    COLOR_SHACKLE = QColor("#EAEAEA")
    COLOR_ACCENT = QColor("#007ACC")
    COLOR_OUTLINE = QColor("#000000")

    pixmap = QPixmap(size, size)
    pixmap.fill(COLOR_BACKGROUND)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    arc_rect = QRect(
        int(size * 0.28), int(size * 0.10),
        int(size * 0.44), int(size * 0.44)
    )

    outline_pen = QPen(COLOR_OUTLINE)
    outline_pen.setWidth(int(size * 0.15))
    outline_pen.setCapStyle(Qt.RoundCap)
    painter.setPen(outline_pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawArc(arc_rect, 0 * 16, 180 * 16)

    shackle_pen = QPen(COLOR_SHACKLE)
    shackle_pen.setWidth(int(size * 0.11))
    shackle_pen.setCapStyle(Qt.RoundCap)
    painter.setPen(shackle_pen)
    painter.drawArc(arc_rect, 0 * 16, 180 * 16)

    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(COLOR_LOCK_BODY))
    body_rect = QRect(
        int(size * 0.18), int(size * 0.43),
        int(size * 0.64), int(size * 0.47)
    )
    painter.drawRoundedRect(body_rect, int(size * 0.06), int(size * 0.06))

    painter.setBrush(QBrush(COLOR_ACCENT))
    center_point = QPoint(int(size / 2), int(size * 0.66))
    radius = int(size * 0.08)
    painter.drawEllipse(center_point, radius, radius)
    
    painter.end()

    return QIcon(pixmap)

DARK_STYLESHEET = """
    QWidget {
        background-color: #121212; 
        color: #EAEAEA;
        font-family: Segoe UI, sans-serif; 
        font-size: 11pt;
    }
    QMenuBar {
        background-color: #2D2D2D;
        color: #EAEAEA;
    }
    QMenuBar::item:selected {
        background-color: #007ACC;
        color: white;
    }
    QMenu {
        background-color: #2D2D2D;
        border: 1px solid #777777;
    }
    QMenu::item:selected {
        background-color: #007ACC;
        color: white;
    }
    QGroupBox {
        border: 1px solid #777777;
        margin-top: 10px;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 10px;
    }
    QLineEdit {
        background-color: #2D2D2D;
        border: 1px solid #777777;
        padding: 8px;
        font-size: 14pt;
        font-weight: bold;
    }
    QPushButton {
        background-color: #3E3E3E;
        border: 1px solid #777777;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: #505050;
    }
    QPushButton:pressed {
        background-color: #606060;
    }
    QPushButton#GenerateButton {
        background-color: #007ACC;
        color: white;
        font-weight: bold;
        border: 1px solid #007ACC;
    }
    QPushButton#GenerateButton:hover {
        background-color: #008CFF;
    }
    QPushButton#GenerateButton:pressed {
        background-color: #006AB3;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
    QSlider::groove:horizontal {
        border: 1px solid #777777;
        height: 4px;
        background: #3E3E3E;
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #007ACC;
        border: 1px solid #007ACC;
        width: 18px;
        margin: -7px 0;
    }
    QLabel#FeedbackLabel {
        color: #00C853;
        font-weight: bold;
    }
"""

class PasswordGenerator(QWidget):
    def __init__(self, app_icon):
        super().__init__()
        self.app_icon = app_icon
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Strong Password Generator")
        self.setFixedSize(450, 400)
        self.setWindowIcon(self.app_icon)
        self.setStyleSheet(DARK_STYLESHEET)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        menu_bar = QMenuBar(self)
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        main_layout.setMenuBar(menu_bar)

        display_layout = QHBoxLayout()
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignCenter)
        self.password_display.setFont(QFont("Consolas", 14, QFont.Bold))
        
        self.copy_button = QPushButton("Copy")
        self.copy_button.setFixedWidth(100)
        self.copy_button.clicked.connect(self.copy_password)

        display_layout.addWidget(self.password_display)
        display_layout.addWidget(self.copy_button)
        
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(15)

        length_layout = QHBoxLayout()
        self.length_label = QLabel("Length: 16")
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(2)
        self.length_slider.setMaximum(64)
        self.length_slider.setValue(16)
        self.length_slider.setTickInterval(1)
        self.length_slider.valueChanged.connect(self.update_length_label)
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_slider)
        
        checkbox_layout = QVBoxLayout()
        self.cb_upper = QCheckBox("Uppercase (A-Z)")
        self.cb_lower = QCheckBox("Lowercase (a-z)")
        self.cb_digits = QCheckBox("Numbers (0-9)")
        self.cb_symbols = QCheckBox("Symbols (!@#$%^)")

        self.cb_upper.setChecked(True)
        self.cb_lower.setChecked(True)
        self.cb_digits.setChecked(True)
        self.cb_symbols.setChecked(True)
        
        for cb in [self.cb_upper, self.cb_lower, self.cb_digits, self.cb_symbols]:
            cb.toggled.connect(self.ensure_one_checkbox_is_checked)
        
        checkbox_layout.addWidget(self.cb_upper)
        checkbox_layout.addWidget(self.cb_lower)
        checkbox_layout.addWidget(self.cb_digits)
        checkbox_layout.addWidget(self.cb_symbols)

        options_layout.addLayout(length_layout)
        options_layout.addLayout(checkbox_layout)

        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("FeedbackLabel")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFixedHeight(20)

        self.generate_button = QPushButton("Generate New Password")
        self.generate_button.setObjectName("GenerateButton")
        self.generate_button.setMinimumHeight(45)
        self.generate_button.clicked.connect(self.generate_password)

        main_layout.addLayout(display_layout)
        main_layout.addWidget(options_group)
        main_layout.addWidget(self.feedback_label)
        main_layout.addStretch()
        main_layout.addWidget(self.generate_button)

        self.generate_password()

    def show_about_dialog(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About Strong Password Generator")
        about_dialog.setWindowIcon(self.app_icon)
        
        about_text = """
            <h3>Strong Password Generator</h3>
            <p>Version 1.0</p>
            <p>This application was designed by MetaSister to generate secure passwords.</p>
            <p>For more information and source code, you can visit the project's GitHub page:</p>
            <a href='https://github.com/MetaSister/Strong-Password-Generator'>https://github.com/MetaSister/Strong-Password-Generator</a>
        """
        
        about_dialog.setText(about_text)
        about_dialog.setTextFormat(Qt.RichText)
        about_dialog.setStandardButtons(QMessageBox.Ok)
        about_dialog.exec_()

    def generate_password(self):
        char_pool = ""
        password_must_contain = []
        
        if self.cb_upper.isChecked():
            char_pool += string.ascii_uppercase
            password_must_contain.append(random.choice(string.ascii_uppercase))
        if self.cb_lower.isChecked():
            char_pool += string.ascii_lowercase
            password_must_contain.append(random.choice(string.ascii_lowercase))
        if self.cb_digits.isChecked():
            char_pool += string.digits
            password_must_contain.append(random.choice(string.digits))
        if self.cb_symbols.isChecked():
            char_pool += string.punctuation
            password_must_contain.append(random.choice(string.punctuation))
        
        if not char_pool:
            self.password_display.setText("Select a Character Set!")
            return

        length = self.length_slider.value()
        
        remaining_length = length - len(password_must_contain)
        if remaining_length < 0: remaining_length = 0
        
        password_rest = random.choices(char_pool, k=remaining_length)
        
        password_list = password_must_contain + password_rest
        random.shuffle(password_list)
        
        password = "".join(password_list)
        self.password_display.setText(password)

    def update_length_label(self, value):
        self.length_label.setText(f"Length: {value}")

    def copy_password(self):
        password_text = self.password_display.text()
        if password_text and "Select a Character Set!" not in password_text:
            QApplication.clipboard().setText(password_text)
            self.feedback_label.setText("Copied to clipboard!")
            QTimer.singleShot(2000, lambda: self.feedback_label.setText(""))

    def ensure_one_checkbox_is_checked(self):
        checked_count = sum([
            self.cb_upper.isChecked(),
            self.cb_lower.isChecked(),
            self.cb_digits.isChecked(),
            self.cb_symbols.isChecked()
        ])
        if checked_count == 0:
            self.sender().setChecked(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_icon = create_modern_icon()

    app.setWindowIcon(app_icon)

    myappid = 'mycompany.passwordgenerator.final'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    window = PasswordGenerator(app_icon=app_icon)
    window.show()
    sys.exit(app.exec_())