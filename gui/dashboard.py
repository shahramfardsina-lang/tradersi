from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class InfoCard(QFrame):

    def __init__(self, title, value, color):
        super().__init__()

        self.setStyleSheet(f"""
        QFrame {{
            background:#2b2d31;
            border:2px solid {color};
            border-radius:12px;
        }}
        """)

        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            color:#aaaaaa;
            font-size:12px;
        """)

        self.value = QLabel(value)
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)

        self.setLayout(layout)

    def setValue(self, text):
        self.value.setText(text)