import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import (
    Qt,
    QTimer
)

from PyQt6.QtGui import QPixmap

from playback_window import PlaybackWindow


# ======================================================
# ARQUIVOS COMPARTILHADOS
# ======================================================
from app_paths import BG_TEXT_FILE, BG_MODE_FILE, BG_LOOP_FILE
with open(BG_TEXT_FILE, "a", encoding="utf-8") as f:
    f.write(">>> background import iniciado\n")



# ======================================================
# JANELA DE TEXTO
# ======================================================
class TextBackgroundWindow(QWidget):
    def __init__(self, screen_index):
        super().__init__()

        screens = QApplication.screens()
        self.screen = screens[screen_index]

        self.setScreen(self.screen)
        self.setGeometry(self.screen.geometry())

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            "color:white;font-size:48px;font-weight:bold;"
        )

        layout.addWidget(self.label)
        self.showFullScreen()

    def set_text(self, text):
        self.label.setText(text)


# ======================================================
# JANELA DE RELÓGIO
# ======================================================
class ClockBackgroundWindow(QWidget):
    def __init__(self, screen_index, logo_path=None, logo_scale=1.0):
        super().__init__()

        # Armazena caminho da logo e escala
        self.logo_path = logo_path
        self.logo_scale = logo_scale

        screens = QApplication.screens()
        self.screen = screens[screen_index]

        self.setScreen(self.screen)
        self.setGeometry(self.screen.geometry())

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Fundo preto
        self.setStyleSheet("background-color: #0a0a0a;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        layout.addStretch()

        # ===============================
        # LOGO (opcional, acima do relógio)
        # ===============================
        self.logo_label = QLabel("", self)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("padding-bottom: 10px;")
        layout.addWidget(self.logo_label)

        # ===============================
        # RELÓGIO - HORA PRINCIPAL (7-SEGMENT)
        # ===============================
        self.time_label = QLabel("10:39:42", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            color: #ff0000;
            font-size: 200px;
            font-weight: bold;
            font-family: '7 Segment', 'Courier New', monospace;
            letter-spacing: 15px;
            line-height: 1.0;
        """)
        layout.addWidget(self.time_label)

        # ===============================
        # INFORMAÇÕES (DATA, DIA, ANO, TEMP)
        # ===============================
        self.info_label = QLabel("13 DATA │ SEG 20 │ ANO TEMP 24°C", self)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            color: #ff0000;
            font-size: 32px;
            font-weight: bold;
            font-family: '7 Segment', 'Courier New', monospace;
            letter-spacing: 4px;
        """)
        layout.addWidget(self.info_label)

        layout.addStretch()
        self.showFullScreen()

        # Timer para atualizar a cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        
        # Atualiza logo de início
        self._update_clock()
        self._set_logo(logo_path)

    def _set_logo(self, logo_path):
        if not logo_path or not os.path.exists(logo_path):
            self.logo_label.clear()
            return
        try:
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                self.logo_label.clear()
                return
            # escala configurável mantendo proporção; evita sobrepor o relógio
            target_width = min(self.width() - 120, 600) * self.logo_scale
            scaled = pixmap.scaledToWidth(int(max(target_width, 80)), Qt.TransformationMode.SmoothTransformation)
            max_height = int(160 * self.logo_scale)
            if scaled.height() > max_height:
                scaled = pixmap.scaledToHeight(max(max_height, 60), Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled)
        except Exception:
            self.logo_label.clear()
    
    def set_logo_scale(self, scale: float):
        """Atualiza a escala do logo e reaplica o redimensionamento."""
        try:
            self.logo_scale = max(0.1, float(scale))
        except Exception:
            return
        # Reaplica a logo com a nova escala usando o caminho original
        self._set_logo(self.logo_path)

    def _update_clock(self):
        from datetime import datetime
        
        now = datetime.now()
        
        # Hora formatada HH:MM:SS
        time_str = now.strftime("%H:%M:%S")
        self.time_label.setText(time_str)
        
        # Dias da semana em Português
        day_names = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
        month_names = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", 
                      "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
        
        date_str = now.strftime("%d")
        day_str = day_names[now.weekday()]
        month_str = month_names[now.month - 1]
        year_str = now.strftime("%Y")
        
        info_text = f"{date_str} {day_str}   │   {month_str}   │   {year_str}   │   TEMP 24°C"
        self.info_label.setText(info_text)

    def closeEvent(self, event):
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()


# ======================================================
# HELPERS
# ======================================================

def run_background(media, screens):
        print("Background iniciado")
        print("Media:", media)
        print("Screens:", screens)

        while True:
            pass  # aqui entra sua lógica real
def parse_screens(arg):
    return [int(p) for p in arg.split(",") if p.isdigit()] or [0]


def read_bg_text():
    try:
        return open(BG_TEXT_FILE, "r", encoding="utf-8").read().strip()
    except:
        return ""
    



# ======================================================
# MAIN
# ======================================================
def main():
    app = QApplication(sys.argv)

    file_path = sys.argv[1]
    screens = parse_screens(sys.argv[2])

    windows = []

    # TEXT / VIDEO
    for s in screens:
        if file_path != "__TEXT_ONLY__" and os.path.exists(file_path):
            win = PlaybackWindow(file_path, s)
        else:
            win = TextBackgroundWindow(s)
        windows.append(win)

    def update_text():
        text = read_bg_text()
        for w in windows:
            if isinstance(w, TextBackgroundWindow):
                w.set_text(text)

    timer = QTimer()
    timer.timeout.connect(update_text)
    timer.start(300)

    sys.exit(app.exec())


    # background.py



