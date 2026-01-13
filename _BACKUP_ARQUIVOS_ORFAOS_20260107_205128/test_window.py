from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)

w = QWidget()
w.setWindowTitle("Teste OK")
w.resize(400, 300)
w.show()

sys.exit(app.exec())
