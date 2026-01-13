import os
import subprocess
import sys
from app_paths import STARTUP_LOG
import re
import webbrowser
import time
import requests
import urllib.parse
from PIL import Image
from pathlib import Path

with open(STARTUP_LOG, "a", encoding="utf-8") as f:
    f.write(">>> deck_window import iniciado\n")


import traceback
import json
from PIL import Image
from background_controller import BackgroundController
from theme import get_stylesheet
from loading_dialog import LoadingDialog



from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton,
    QFileDialog, QMenu, QHBoxLayout, QSpacerItem,
    QSizePolicy, QInputDialog,QPushButton,QApplication, QLineEdit, QTabWidget

    ,QMessageBox
 
 )
from PyQt6.QtCore import Qt, QPropertyAnimation,QEasingCurve, QTimer, QUrl
from playback_window import PlaybackWindow
from PyQt6.QtGui import QFontMetrics, QColor
from PyQt6.QtCore import pyqtProperty
from PyQt6.QtGui import QIcon, QAction,QPainter, QPen
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLabel, QSpinBox
from PyQt6.QtGui import QPixmap, QGuiApplication, QImage
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtWidgets import QDialog, QCheckBox  










DECK_FILE = "deck_config.sdk"



# ===============================
# EXCEPTION HOOK (GLOBAL)
# ===============================






def excepthook(exc_type, exc_value, exc_tb):
    print("🔥 EXCEPTION:")
    traceback.print_exception(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # 🔹 texto base (ESSENCIAL)
        self.setAcceptDrops(True)
        self._enabled_overlay = True
        self._allow_hover = True
        self._screens_count = 1


        self.base_text = text
        self._is_on_air = False
        self._glow_intensity = 0  # Para controlar o pulsante (0-100)

        # 🔄 Cria animação do pulsante
        self._pulse_anim = QPropertyAnimation(self, b"glowIntensity", self)
        self._pulse_anim.setDuration(1500)
        self._pulse_anim.setStartValue(10)
        self._pulse_anim.setEndValue(40)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    
    @pyqtProperty(int)
    def glowIntensity(self):
        return self._glow_intensity
    
    @glowIntensity.setter
    def glowIntensity(self, value):
        self._glow_intensity = value
        self.update()  # Força repaint a cada mudança
        
    # ===============================
    # HOVER
    # ===============================

    def enterEvent(self, event):
        if self._is_on_air:
            return

        super().enterEvent(event)


    def leaveEvent(self, event):
        super().leaveEvent(event)



    # ===============================
    # ON AIR
    # ===============================
    def start_on_air(self):
        self._is_on_air = True
        # Reset da animação para garantir que começa do zero
        if self._pulse_anim.state() == 1:  # QAbstractAnimation.Running = 1
            self._pulse_anim.stop()
        self._glow_intensity = 10  # Inicia com valor inicial
        # Inicia a animação do pulsante
        self._pulse_anim.start()

    def stop_on_air(self):
        self._is_on_air = False
        # Para a animação
        self._pulse_anim.stop()
        self._glow_intensity = 0
        self.update()



    def reset(self):
        self._is_on_air = False
        self.setText(self.base_text)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()


    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            return

        urls = event.mimeData().urls()
        if not urls:
            return

        file_path = urls[0].toLocalFile()

        # notifica o DeckWindow
        if self.parent():
            try:
                self.parent().on_file_dropped(self, file_path)
            except AttributeError:
                pass

    def set_enabled_overlay(self, enabled: bool):
        self._enabled_overlay = enabled
        self.update()

    def set_fade_enabled(self, enabled: bool):
        self._fade_enabled = enabled
        self.update()

    def set_screens_count(self, count: int):
        self._screens_count = count
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 🔴 ON AIR - Desenhar border pulsante vermelho
        if self._is_on_air:
            painter.setPen(QPen(QColor(220, 50, 50), int(self._glow_intensity / 5) + 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # Desenha um retângulo arredondado como border
            painter.drawRoundedRect(
                1, 1,
                self.width() - 2,
                self.height() - 2,
                8, 8
            )

    def reset_visual(self):
        """Reset visual"""
        self._is_on_air = False
        self._pulse_anim.stop()
        self._glow_intensity = 0
        self.update()








class ScreenSelectDialog(QDialog):
    
    def __init__(self, selected_screens=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Selecionar telas")
        self.setMinimumWidth(420)

        if selected_screens is None:
            selected_screens = []

        self.checkboxes = []

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        info = QLabel("Selecione as telas onde o conteúdo será exibido:")
        layout.addWidget(info)

        screens = QGuiApplication.screens()

        for index, screen in enumerate(screens):
            geo = screen.geometry()
            text = (
                f"Tela {index}  •  "
                f"{screen.name()}  •  "
                f"{geo.width()}x{geo.height()}"
            )

            cb = QCheckBox(text)
            cb.setChecked(index in selected_screens)

            self.checkboxes.append((index, cb))
            layout.addWidget(cb)

        # botões
        btn_layout = QHBoxLayout()

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("cancelBtn")

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("okBtn")

        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)

        layout.addLayout(btn_layout)

        self.apply_style()


    def apply_style(self):
        self.setStyleSheet("""
        QDialog {
            background-color: #1e1e2e;
            color: #ffffff;
            font-family: 'Segoe UI';
            font-size: 13px;
        }

        QLabel {
            color: #ffffff;
            font-weight: 600;
            padding-bottom: 6px;
        }

        QCheckBox {
            padding: 12px;
            border-radius: 8px;
            background-color: #2a2a3e;
            margin-bottom: 8px;
            spacing: 10px;
            color: #ffffff;
        }

        QCheckBox:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #3a3a4e,
                stop:1 #454560
            );
            border: 1px solid #6c63ff;
        }

        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }

        QCheckBox::indicator:unchecked {
            border: 2px solid #404060;
            background-color: #2a2a3e;
            border-radius: 4px;
        }

        QCheckBox::indicator:unchecked:hover {
            border: 2px solid #6c63ff;
            background-color: #323245;
        }

        QCheckBox::indicator:checked {
            border: 2px solid #6c63ff;
            background-color: #6c63ff;
            border-radius: 4px;
        }

        QCheckBox::indicator:checked:hover {
            background-color: #7c73ff;
        }

        QPushButton {
            background-color: #6c63ff;
            border: 2px solid #5c53ef;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            color: #ffffff;
            min-width: 80px;
        }

        QPushButton:hover {
            background-color: #7c73ff;
            border: 2px solid #6c63ff;
        }

        QPushButton:pressed {
            background-color: #5c53ef;
        }

        QPushButton#okBtn {
            background-color: #2ecc71;
            border: 2px solid #27ae60;
        }

        QPushButton#okBtn:hover {
            background-color: #3ed87d;
            border: 2px solid #2ecc71;
        }

        QPushButton#okBtn:pressed {
            background-color: #27ae60;
        }

        QPushButton#cancelBtn {
            background-color: #95a5a6;
            border: 2px solid #7f8c8d;
        }

        QPushButton#cancelBtn:hover {
            background-color: #bdc3c7;
            border: 2px solid #95a5a6;
        }

        QPushButton#cancelBtn:pressed {
            background-color: #7f8c8d;
        }
        """)

    def selected_indexes(self):
        """
        Retorna uma lista com os índices das telas selecionadas
        """
        return [
            index
            for index, checkbox in self.checkboxes
            if checkbox.isChecked()
    ]




class FadeConfigDialog(QDialog):
    def __init__(self, fade_enabled=True, fade_in=800, fade_out=600, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configurar Fade")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Configuração de Fade")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.enable_cb = QCheckBox("Ativar Fade")
        self.enable_cb.setChecked(fade_enabled)
        layout.addWidget(self.enable_cb)

        # Fade IN
        fade_in_layout = QHBoxLayout()
        fade_in_label = QLabel("Fade IN (ms)")
        self.fade_in_spin = QSpinBox()
        self.fade_in_spin.setRange(0, 10000)
        self.fade_in_spin.setSingleStep(100)
        self.fade_in_spin.setValue(fade_in)

        fade_in_layout.addWidget(fade_in_label)
        fade_in_layout.addStretch()
        fade_in_layout.addWidget(self.fade_in_spin)
        layout.addLayout(fade_in_layout)

        # Fade OUT
        fade_out_layout = QHBoxLayout()
        fade_out_label = QLabel("Fade OUT (ms)")
        self.fade_out_spin = QSpinBox()
        self.fade_out_spin.setRange(0, 10000)
        self.fade_out_spin.setSingleStep(100)
        self.fade_out_spin.setValue(fade_out)

        fade_out_layout.addWidget(fade_out_label)
        fade_out_layout.addStretch()
        fade_out_layout.addWidget(self.fade_out_spin)
        layout.addLayout(fade_out_layout)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancelar")
        btn_ok = QPushButton("OK")

        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        # comportamento
        self.enable_cb.toggled.connect(self._update_state)
        self._update_state(self.enable_cb.isChecked())

        self.apply_style()

    def _update_state(self, enabled):
        self.fade_in_spin.setEnabled(enabled)
        self.fade_out_spin.setEnabled(enabled)

    def get_values(self):
        return {
            "fade_enabled": self.enable_cb.isChecked(),
            "fade_in": self.fade_in_spin.value(),
            "fade_out": self.fade_out_spin.value()
        }

    def apply_style(self):
        self.setStyleSheet("""
        QDialog {
            background-color: #1b1b1b;
            color: #eaeaea;
            font-family: Segoe UI;
        }

        QLabel {
            color: #eaeaea;
        }

        QCheckBox {
            padding: 6px;
            font-weight: 600;
        }

        QSpinBox {
            min-width: 100px;
            background-color: #242424;
            border-radius: 6px;
            padding: 4px;
        }

        QPushButton {
            background-color: #3a3a3a;
            border-radius: 8px;
            padding: 6px 14px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #4a4a4a;
        }
        """)



    def selected_indexes(self):
        return [
            index for index, cb in self.checkboxes
            if cb.isChecked()
        ]

    def apply_style(self):
        self.setStyleSheet("""
        QDialog {
            background-color: #1b1b1b;
            color: #eaeaea;
            font-family: Segoe UI;
            font-size: 13px;
        }

        QLabel {
            color: #eaeaea;
            font-weight: 600;
            padding-bottom: 8px;
        }

        QCheckBox {
            padding: 10px;
            border-radius: 10px;
            background-color: #242424;
            margin-bottom: 6px;
        }

        QCheckBox:hover {
            background-color: #2d2d2d;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }

        QCheckBox::indicator:unchecked {
            border: 2px solid #666;
            background-color: #1b1b1b;
            border-radius: 4px;
        }

        QCheckBox::indicator:checked {
            border: 2px solid #4caf50;
            background-color: #4caf50;
            border-radius: 4px;
        }

        QPushButton {
            background-color: #3a3a3a;
            border-radius: 10px;
            padding: 8px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #4a4a4a;
        }

        QPushButton#okBtn {
            background-color: #2e7d32;
        }

        QPushButton#okBtn:hover {
            background-color: #388e3c;
        }

        QPushButton#cancelBtn {
            background-color: #5d4037;
        }

        QPushButton#cancelBtn:hover {
            background-color: #6d4c41;
        }
        """)


class MediaSelectDialog(QDialog):
    def __init__(self, enabled=True, file_path=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Selecionar mídia")
        self.setMinimumWidth(480)

        self.file_path = file_path
        self.is_youtube_url = False

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Configuração de mídia")
        title.setStyleSheet("font-size:14px; font-weight:bold;")
        layout.addWidget(title)

        self.enable_cb = QCheckBox("Ativar mídia neste botão")
        self.enable_cb.setChecked(enabled)
        layout.addWidget(self.enable_cb)

        # Abas para arquivo ou URL
        self.tabs = QTabWidget()
        
        # Aba 1: Arquivo local
        tab_file = QWidget()
        tab_file_layout = QVBoxLayout(tab_file)
        
        # preview
        self.preview = QLabel("Nenhum arquivo selecionado")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(120)
        self.preview.setStyleSheet("""
            QLabel {
                background-color: #242424;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        tab_file_layout.addWidget(self.preview)

        # botão de seleção de arquivo
        btn_select = QPushButton("Selecionar arquivo")
        btn_select.setObjectName("selectBtn")
        btn_select.clicked.connect(self.open_file_dialog)
        tab_file_layout.addWidget(btn_select)
        
        self.tabs.addTab(tab_file, "📁 Arquivo Local")
        
        # Aba 2: YouTube
        tab_youtube = QWidget()
        tab_youtube_layout = QVBoxLayout(tab_youtube)
        
        youtube_info = QLabel("Cole a URL do YouTube:")
        youtube_info.setStyleSheet("color: #eaeaea; font-weight: 600;")
        tab_youtube_layout.addWidget(youtube_info)
        
        self.youtube_input = QLineEdit()
        self.youtube_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.youtube_input.setStyleSheet("""
            QLineEdit {
                background-color: #242424;
                color: #eaeaea;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        if file_path and self._is_youtube_url(file_path):
            self.youtube_input.setText(file_path)
            self.is_youtube_url = True
        
        self.youtube_input.textChanged.connect(self._on_youtube_url_changed)
        tab_youtube_layout.addWidget(self.youtube_input)
        
        self.youtube_preview = QLabel("Cole uma URL válida do YouTube")
        self.youtube_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.youtube_preview.setMinimumHeight(80)
        self.youtube_preview.setStyleSheet("""
            QLabel {
                background-color: #242424;
                border-radius: 12px;
                padding: 10px;
                color: #999;
            }
        """)
        tab_youtube_layout.addWidget(self.youtube_preview)
        
        tab_youtube_layout.addStretch()
        self.tabs.addTab(tab_youtube, "📺 YouTube")
        
        layout.addWidget(self.tabs)

        if file_path:
            if self._is_youtube_url(file_path):
                self.tabs.setCurrentIndex(1)
                self.is_youtube_url = True
            else:
                self.tabs.setCurrentIndex(0)
                self.set_preview(file_path)

        # OK / Cancel
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("cancelBtn")

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("okBtn")

        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        self.apply_style()

    def _is_youtube_url(self, url_string):
        """Verifica se a string é uma URL válida do YouTube"""
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        return bool(re.match(youtube_regex, url_string))

    def _on_youtube_url_changed(self):
        """Atualiza preview quando a URL do YouTube muda"""
        url = self.youtube_input.text().strip()
        if url and self._is_youtube_url(url):
            self.youtube_preview.setText(f"✅ URL válida:\n{url[:60]}...")
            self.youtube_preview.setStyleSheet("""
                QLabel {
                    background-color: #1a3a1a;
                    border-radius: 12px;
                    padding: 10px;
                    color: #4caf50;
                    font-weight: bold;
                }
            """)
            self.file_path = url
            self.is_youtube_url = True
        elif url:
            self.youtube_preview.setText("❌ URL inválida do YouTube")
            self.youtube_preview.setStyleSheet("""
                QLabel {
                    background-color: #3a1a1a;
                    border-radius: 12px;
                    padding: 10px;
                    color: #ff6b6b;
                    font-weight: bold;
                }
            """)
            self.file_path = None
            self.is_youtube_url = False
        else:
            self.youtube_preview.setText("Cole uma URL válida do YouTube")
            self.youtube_preview.setStyleSheet("""
                QLabel {
                    background-color: #242424;
                    border-radius: 12px;
                    padding: 10px;
                    color: #999;
                }
            """)
            self.file_path = None
            self.is_youtube_url = False

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar mídia",
            "",
            "Mídia (*.mp4 *.avi *.mov *.mp3 *.wav *.jpg *.png)"
        )
        if path:
            self.file_path = path
            self.is_youtube_url = False
            self.set_preview(path)

    def set_preview(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".bmp"):
            pix = QPixmap(path).scaled(
                200, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview.setPixmap(pix)
        else:
            self.preview.setText(os.path.basename(path))

    def get_values(self):
        return {
            "enabled": self.enable_cb.isChecked(),
            "file_path": self.file_path,
            "is_youtube_url": self.is_youtube_url
        }

    def apply_style(self):
        self.setStyleSheet("""
        QDialog {
            background-color: #1b1b1b;
            color: #eaeaea;
            font-family: Segoe UI;
        }

        QLabel {
            color: #eaeaea;
        }

        QCheckBox {
            font-weight: 600;
            padding: 6px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }

        QCheckBox::indicator:unchecked {
            border: 2px solid #666;
            background-color: #1b1b1b;
            border-radius: 4px;
        }

        QCheckBox::indicator:checked {
            border: 2px solid #4caf50;
            background-color: #4caf50;
            border-radius: 4px;
        }

        QTabWidget::pane {
            border: 1px solid #444;
        }

        QTabBar::tab {
            background-color: #242424;
            color: #aaa;
            padding: 8px 16px;
            margin-right: 2px;
            border-radius: 6px 6px 0 0;
        }

        QTabBar::tab:selected {
            background-color: #3a3a3a;
            color: #fff;
            border-bottom: 2px solid #1976d2;
        }

        QTabBar::tab:hover {
            background-color: #2d2d2d;
        }

        QPushButton {
            border-radius: 10px;
            padding: 8px 14px;
            font-weight: 600;
            background-color: #3a3a3a;
        }

        QPushButton:hover {
            background-color: #4a4a4a;
        }

        /* Botão Selecionar Arquivo */
        QPushButton#selectBtn {
            background-color: #1976d2;
        }

        QPushButton#selectBtn:hover {
            background-color: #1e88e5;
        }

        /* Botão OK */
        QPushButton#okBtn {
            background-color: #2e7d32;
        }

        QPushButton#okBtn:hover {
            background-color: #388e3c;
        }

        QPushButton#cancelBtn {
            background-color: #2f2f2f;
            color: #cccccc;
        }

        QPushButton#cancelBtn:hover {
            background-color: #3a3a3a;
        }
        """)

# ===============================
# YOUTUBE PREVIEW WINDOW
# ===============================
class YouTubePreviewWindow(QWidget):
    """Janela flutuante com preview do YouTube e controles"""
    def __init__(self, button_index, screen_index, close_callback):
        super().__init__()
        
        self.button_index = button_index
        self.screen_index = screen_index
        self.close_callback = close_callback
        self.running = True
        self._mss_missing_warned = False
        self._monitor_geo = None
        
        self.setWindowTitle(f"Preview YouTube - Botão {button_index + 1}")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                border: 3px solid #6c63ff;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label para mostrar o preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(400, 260)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #000000;")
        self.preview_label.setMouseTracking(True)
        self.preview_label.mousePressEvent = self._on_preview_click
        layout.addWidget(self.preview_label)
        
        # Botão de fullscreen
        self.fullscreen_btn = QPushButton("🖥️ FULLSCREEN")
        self.fullscreen_btn.setFixedHeight(40)
        self.fullscreen_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c63ff;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7c73ff;
            }
        """)
        self.fullscreen_btn.clicked.connect(self._send_fullscreen)
        layout.addWidget(self.fullscreen_btn)
        
        # Posicionar no monitor 1
        self.move(50, 50)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # Timer para capturar tela
        self.capture_timer = QTimer()
        self.capture_timer.timeout.connect(self._update_preview)
        self.capture_timer.start(100)  # Atualizar a cada 100ms

    def _click_screen_point(self, x, y):
        """Clica em (x,y) absoluto na tela e restaura o cursor."""
        try:
            import ctypes

            # Tentar melhorar mapeamento de coordenadas em Windows com DPI scaling
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

            GetCursorPos = ctypes.windll.user32.GetCursorPos
            SetCursorPos = ctypes.windll.user32.SetCursorPos
            mouse_event = ctypes.windll.user32.mouse_event

            MOUSEEVENTF_LEFTDOWN = 0x0002
            MOUSEEVENTF_LEFTUP = 0x0004

            original = POINT()
            GetCursorPos(ctypes.byref(original))

            SetCursorPos(int(x), int(y))
            time.sleep(0.02)
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            time.sleep(0.02)
            SetCursorPos(int(original.x), int(original.y))
        except Exception:
            pass

    def _on_preview_click(self, event):
        """Encaminha clique do preview para o monitor do vídeo."""
        try:
            if not self._monitor_geo:
                return

            preview_w = self.preview_label.width()
            preview_h = self.preview_label.height()
            if preview_w <= 0 or preview_h <= 0:
                return

            local_x = max(0, min(event.position().x(), preview_w - 1))
            local_y = max(0, min(event.position().y(), preview_h - 1))

            geo = self._monitor_geo
            # Mapear clique do preview (400x260) para coordenadas reais do monitor
            target_x = geo.x() + int((local_x / preview_w) * geo.width())
            target_y = geo.y() + int((local_y / preview_h) * geo.height())

            self._click_screen_point(target_x, target_y)
        except Exception:
            pass
    
    def _update_preview(self):
        """Capturar e atualizar o preview do navegador"""
        try:
            try:
                import mss
                has_mss = True
            except ImportError:
                has_mss = False
                if not self._mss_missing_warned:
                    try:
                        import sys
                        exe = sys.executable
                    except Exception:
                        exe = "(desconhecido)"
                    print(f"⚠️ mss não instalado no Python do SminDeck ({exe}). Usando captura alternativa do Qt.")
                    self._mss_missing_warned = True
            
            screens = QApplication.screens()
            if self.screen_index >= len(screens):
                return
            
            # Obter geometria do monitor
            screen = screens[self.screen_index]
            geo = screen.geometry()
            self._monitor_geo = geo

            if not has_mss:
                try:
                    pixmap = screen.grabWindow(0)
                    if pixmap.isNull():
                        return
                    pixmap = pixmap.scaled(
                        400,
                        260,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    self.preview_label.setPixmap(pixmap)
                except Exception:
                    return
                return
            
            # Capturar a tela
            with mss.mss() as sct:
                # Ajustar para o monitor correto (mss usa índice 1+)
                monitor = sct.monitors[self.screen_index + 1] if self.screen_index + 1 < len(sct.monitors) else sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Converter para QImage
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Redimensionar para caber na janela (400x260)
                img_resized = img.resize((400, 260), Image.Resampling.LANCZOS)
                
                # Converter para QPixmap
                data = img_resized.tobytes()
                qimg = QImage(data, 400, 260, 1200, QImage.Format.Format_RGB888).copy()
                pixmap = QPixmap.fromImage(qimg)
                
                # Mostrar no label
                self.preview_label.setPixmap(pixmap)
        except Exception as e:
            # Silenciar erros de captura para não poluir o console
            pass
    
    def _send_fullscreen(self):
        """Enviar tecla F para fullscreen"""
        try:
            if self._monitor_geo:
                geo = self._monitor_geo
                # 1) focar o navegador sem pausar o vídeo:
                # clicar no topo (barra do navegador), evitando o centro do player (toggle play/pause).
                safe_x = geo.x() + min(80, max(10, geo.width() // 10))
                safe_y = geo.y() + 10
                self._click_screen_point(safe_x, safe_y)
                time.sleep(0.05)

            import ctypes
            VK_F = 0x46  # tecla 'F'
            KEYEVENTF_KEYUP = 0x0002

            ctypes.windll.user32.keybd_event(VK_F, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.keybd_event(VK_F, 0, KEYEVENTF_KEYUP, 0)
        except Exception:
            pass
    
    def closeEvent(self, event):
        """Limpar quando fechar a janela"""
        self.running = False
        self.capture_timer.stop()
        
        # ✅ SALVAR CONFIGURAÇÃO ANTES DE FECHAR
        self.save_to_json()
        
        # Importante: fechar o preview NÃO deve fechar o navegador/vídeo.
        # O fechamento do playback é responsabilidade do botão STOP/fechar no Deck.
        super().closeEvent(event)













class ClickableLogoLabel(QLabel):
    """Label que detecta cliques para easter egg de DEV"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.click_count = 0
        self.click_timer = None
    
    def mousePressEvent(self, event):
        if self.parent_window is None:
            return
        
        self.click_count += 1
        
        # Reset timer se existir
        if self.click_timer:
            self.click_timer.stop()
        
        # Se chegou em 5 cliques, abrir dialog DEV
        if self.click_count >= 5:
            self.click_count = 0
            self.open_dev_dialog()
        else:
            # Resetar contador após 2 segundos sem clicar
            self.click_timer = QTimer()
            self.click_timer.singleShot(2000, lambda: setattr(self, 'click_count', 0))
    
    def open_dev_dialog(self):
        """Abre o dialog de DEV"""
        try:
            from dev_reset_dialog import DevResetDialog
            dialog = DevResetDialog(self.parent_window)
            dialog.exec()
        except ImportError:
            print("❌ dev_reset_dialog não disponível")
        except Exception as e:
            print(f"❌ Erro ao abrir DEV dialog: {e}")


class DeckWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # ===============================
        # LOADING DIALOG - SINCRONIZAR BD
        # ===============================
        from database_client import DatabaseClient
        db_client = DatabaseClient()
        tem_updates = db_client.tem_atualizacoes_pendentes()
        
        if tem_updates:
            loading = LoadingDialog(self, mostrar=True)
            loading.exec()
        
        self.setWindowTitle("Stream_DECK Virtual")
        self.resize(600, 400)
        
        # ===============================
        # AVISO DE TESTE - Primeira Vez
        # ===============================
        self.show_beta_warning_if_needed()

        
         # ===============================
        # ESTADO
        # ===============================
        self.active_index = None
        self.button_files = {}
        self.buttons = []
        self.playback_windows = []
        # Removido: self._pending_play (não mais necessário)
        self.bg_process = None
        self.bg_controller = None
        self.clock = None
        self.youtube_processes = {}  # Guardar processos do YouTube por botão
        self.youtube_profile_dirs = {}  # user-data-dir temporário por botão (evita "Restaurar páginas")
        self.yt_preview_window = None  # Janela de preview do YouTube
        
        # 🔧 DEV MODE - Easter egg: clique 5x na logo pra resetar chaves
        self.dev_click_count = 0
        self.dev_click_timer = None
        
        # ===============================
        # BOT DISCORD INTEGRATION
        # ===============================
        self.bot_connection_key = None
        self.bot_api_url = "http://72.60.244.240:8000"  # URL do bot no VPS
        self.bot_sync_timer = QTimer()
        self.bot_sync_timer.timeout.connect(self.sync_with_bot)
        self.bot_sync_timer.start(10000)  # Sincronizar a cada 10 segundos

        # 🔄 TIMER DE SINCRONIZAÇÃO DE ATUALIZAÇÕES (Tempo Real)
        self.update_sync_timer = QTimer()
        self.update_sync_timer.timeout.connect(self.sincronizar_atualizacoes)
        self.update_sync_timer.start(5000)  # Sincronizar atualizações a cada 5 segundos


        # ===============================
        # GRID
        # ===============================
        self.TOTAL_BUTTONS = 12
        self.GRID_ROWS = 3
        self.GRID_COLS = 4

        self.button_config = {
            i: {
                "fade_enabled": True,
                "fade_in": 800,
                "fade_out": 600,
                "screens": [0]
            }
            for i in range(self.TOTAL_BUTTONS)
        }
        
        # ===============================
        # CONFIGURAÇÕES GLOBAIS DO PLAYER
        # ===============================
        self.player_config = {
            "logo_path": None,  # Caminho da logo
            "logo_opacity": 0.8,  # Opacidade da logo (0-1)
            "logo_size": 150  # Tamanho da logo em pixels
        }

        # ===============================
        # LAYOUT
        # ===============================
        root_layout = QVBoxLayout(self)

        def _get_version_text() -> str:
            try:
                if getattr(sys, 'frozen', False):
                    version_path = Path(sys.executable).with_name('version.json')
                else:
                    version_path = Path(__file__).with_name('version.json')

                if version_path.exists():
                    with version_path.open('r', encoding='utf-8') as f:
                        data = json.load(f)
                    build = data.get('build')
                    if build:
                        return str(build)
            except Exception:
                pass

            return "Build 1.0.0  |  Versão: Beta test"

        grid = QGridLayout()
        grid.setSpacing(10)

        index = 0
        for r in range(self.GRID_ROWS):
            for c in range(self.GRID_COLS):
                if index >= self.TOTAL_BUTTONS:
                    break

                btn = AnimatedButton(f"BTN {index + 1}")
                btn.setObjectName("gridBtn")
                btn.setFixedSize(120, 90)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

                btn.clicked.connect(lambda _, i=index: self.on_button_clicked(i))
                btn.customContextMenuRequested.connect(self.show_context_menu)

                grid.addWidget(btn, r, c)
                self.buttons.append(btn)
                index += 1

        root_layout.addLayout(grid)

        # ===============================
        # BOTÃO FADE MODE
        # ===============================
        self.fade_mode_enabled = False
        
        fade_control_layout = QHBoxLayout()
        fade_control_layout.addStretch()
        
        self.fade_btn = QPushButton("FADE: OFF")
        self.fade_btn.setObjectName("fadeBtn")
        self.fade_btn.setFixedSize(95, 30)
        self.fade_btn.setCheckable(True)
        self.fade_btn.setChecked(False)
        self.fade_btn.clicked.connect(self._toggle_fade_mode)
        
        fade_control_layout.addWidget(self.fade_btn)
        fade_control_layout.addSpacing(10)
        fade_control_layout.addStretch()
        
        root_layout.addLayout(fade_control_layout)

        root_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.load_from_json()
        # ===============================
        # BARRA INFERIOR
        # ===============================
        bottom_bar = QHBoxLayout()

        self.pause_btn = QPushButton("PAUSE")
        self.pause_btn.setObjectName("pauseBtn")
        self.pause_btn.clicked.connect(self.pause_playback)

        self.last_btn = QPushButton("ÚLTIMO")
        self.last_btn.setObjectName("lastBtn")
        self.last_btn.clicked.connect(self.load_last_deck)

        self.close_btn = QPushButton("STOP")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.clicked.connect(self.close_playback_window)

        # 🔁 agora é só um launcher
        self.bg_btn = QPushButton("BACKGROUND")
        self.bg_btn.setObjectName("bgBtn")
        self.bg_btn.clicked.connect(self.open_background_window)

        # 🤖 Bot Discord
        self.bot_btn = QPushButton("🤖 BOT")
        self.bot_btn.setObjectName("botBtn")
        self.bot_btn.clicked.connect(self.manage_bot_keys)

        for b in (self.pause_btn, self.last_btn, self.close_btn, self.bg_btn, self.bot_btn):
            b.setFixedSize(140, 40)
            bottom_bar.addWidget(b)

        root_layout.addLayout(bottom_bar)

        # ===============================
        # LOGO
        # ===============================
       # ===============================
# RODAPÉ COM LOGO + BUILD
# ===============================
        # ===============================
# RODAPÉ COM BUILD (SEM LOGO)
# ===============================
        self.header = QHBoxLayout()
        self.header.setContentsMargins(10, 0, 10, 2)

        build_label = QLabel(_get_version_text())
        build_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        build_label.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 11px;
                padding-bottom: 2px;
            }
        """)

        self.header.addStretch()
        self.header.addWidget(build_label)

        root_layout.addLayout(self.header)

        # Inicializar visibilidade do botão BOT
        self.update_bot_button_visibility()

        self.apply_style()


    # ===============================
    # PLAY
    # ===============================

    
    def _toggle_fade_mode(self):
        """Alterna o modo de fade de transição"""
        self.fade_mode_enabled = not self.fade_mode_enabled
        if self.fade_mode_enabled:
            self.fade_btn.setText("FADE: ON")
            self.fade_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff6b6b;
                    color: white;
                    border: 2px solid #ff0000;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background-color: #ff5252;
                }
            """)
        else:
            self.fade_btn.setText("FADE: OFF")
            self.fade_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d44;
                    color: #aaa;
                    border: 2px solid #555;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background-color: #3d3d54;
                }
            """)

    def _is_youtube_url(self, url_string):
        """Verifica se a string é uma URL válida do YouTube"""
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        return bool(re.match(youtube_regex, url_string))

    def _open_youtube_fullscreen(self, youtube_url, cfg, button_index=None):
        """Abre o vídeo do YouTube em navegador externo no monitor selecionado"""
        try:
            # Extrai o video ID da URL
            video_id = self._extract_youtube_id(youtube_url)
            
            if not video_id:
                print("❌ Não foi possível extrair o ID do YouTube")
                return
            
            # URL do YouTube com autoplay e mute
            fullscreen_url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1&mute=1"
            
            # Obter o monitor selecionado
            screens = cfg.get("screens", [0])
            screen_index = screens[0] if screens else 0
            
            # Fechar YouTube anterior se existir
            if button_index is not None:
                self._close_youtube_for_button(button_index)
            
            # Abrir no navegador no monitor selecionado
            if button_index is not None:
                self._open_browser_on_screen(fullscreen_url, screen_index, button_index)
            else:
                self._open_browser_on_screen(fullscreen_url, screen_index)
            
            print(f"✅ YouTube aberto: {video_id} (Tela {screen_index})")
            
        except Exception as e:
            print(f"❌ Erro ao abrir YouTube: {e}")
            import traceback
            traceback.print_exc()

    def _open_browser_on_screen(self, url, screen_index=0, button_index=None):
        """Abre navegador no monitor especificado"""
        try:
            screens = QApplication.screens()
            
            # Validar índice
            if not (0 <= screen_index < len(screens)):
                print(f"⚠️ Tela {screen_index} não existe, usando 0")
                screen_index = 0
            
            # Obter geometria
            target_screen = screens[screen_index]
            geometry = target_screen.geometry()
            
            print(f"📺 Abrindo YouTube na Tela {screen_index}")
            
            # Encontrar navegador
            browser_path = self._find_browser_path()
            
            if not browser_path:
                print("⚠️ Navegador não encontrado, usando webbrowser padrão")
                webbrowser.open(url)
                return

            # Flags para reduzir pop-ups (ex: "restaurar páginas") e isolar sessão
            common_flags = [
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-session-crashed-bubble",
            ]

            # Perfil temporário por execução: evita que o Chrome reaproveite uma sessão "crashada"
            # (que gera o pop-up "Restaurar páginas?") quando o processo é encerrado à força.
            if button_index is not None:
                try:
                    import tempfile
                    import shutil

                    old_dir = self.youtube_profile_dirs.get(button_index)
                    if old_dir:
                        try:
                            shutil.rmtree(old_dir, ignore_errors=True)
                        except Exception:
                            pass

                    profile_dir = tempfile.mkdtemp(prefix=f"smindeck_browser_{button_index}_")
                    self.youtube_profile_dirs[button_index] = profile_dir
                    common_flags.append(f"--user-data-dir={profile_dir}")
                except Exception:
                    pass
            
            # Argumentos para Chrome/Edge
            if "chrome" in browser_path.lower():
                args = [
                    browser_path,
                    *common_flags,
                    f"--window-position={geometry.x()},{geometry.y()}",
                    f"--window-size={geometry.width()},{geometry.height()}",
                    url
                ]
            elif "edge" in browser_path.lower():
                args = [
                    browser_path,
                    *common_flags,
                    f"--window-position={geometry.x()},{geometry.y()}",
                    f"--window-size={geometry.width()},{geometry.height()}",
                    url
                ]
            else:
                args = [browser_path, url]
            
            # Abrir navegador
            proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Navegador aberto no monitor {screen_index} (PID: {proc.pid})")
            
            # Guardar processo se for YouTube
            if button_index is not None:
                self.youtube_processes[button_index] = proc
                
                # Abrir janela de preview no monitor 1
                self.yt_preview_window = YouTubePreviewWindow(button_index, screen_index, self._close_youtube_for_button)
                self.yt_preview_window.show()
            
            # Agendar envio de tecla F para fullscreen após carregar
            QTimer.singleShot(12000, lambda: self._send_fullscreen_key_windows())
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            webbrowser.open(url)

    def _find_browser_path(self):
        """Encontra o caminho do navegador no Windows"""
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None

    def _send_fullscreen_key_windows(self):
        """Ativa fullscreen do YouTube enviando a tecla F"""
        try:
            print("⏳ Ativando fullscreen...")
            
            # Importar keyboard
            import keyboard
            
            # Enviar tecla F de forma mais confiável
            keyboard.press('f')
            keyboard.release('f')
            
            print("✅ Fullscreen ativado (tecla F enviada)")
            
        except Exception as e:
            print(f"⚠️ Erro ao ativar fullscreen: {e}")
            # Se keyboard não funcionar, tenta o método antigo
            try:
                import ctypes
                keybd_event = ctypes.windll.user32.keybd_event
                keybd_event(0x46, 0, 0, 0)
                time.sleep(0.1)
                keybd_event(0x46, 0, 2, 0)
                print("✅ Fullscreen ativado (método alternativo)")
            except:
                pass

    def _close_youtube_for_button(self, button_index):
        """Fecha o navegador do YouTube aberto para um botão específico"""
        print(f"🔍 Tentando fechar YouTube do botão {button_index}")
        
        if button_index in self.youtube_processes:
            proc = self.youtube_processes[button_index]
            print(f"✅ Processo encontrado: {proc.pid}")
            
            try:
                # Tentar enviar ESC para sair do fullscreen
                import ctypes
                ctypes.windll.user32.keybd_event(0x1B, 0, 0, 0)  # ESC key down
                ctypes.windll.user32.keybd_event(0x1B, 0, 2, 0)  # ESC key up
                time.sleep(0.5)
            except Exception:
                pass
            
            try:
                proc.terminate()
                proc.wait(timeout=2)
                print(f"✅ Navegador YouTube fechado (botão {button_index})")
            except subprocess.TimeoutExpired:
                try:
                    proc.kill()
                    proc.wait(timeout=1)
                    print(f"✅ Navegador YouTube terminado à força (botão {button_index})")
                except Exception as e:
                    print(f"⚠️ Erro ao fechar YouTube: {e}")
            except Exception as e:
                print(f"⚠️ Erro ao fechar YouTube: {e}")
            finally:
                if button_index in self.youtube_processes:
                    del self.youtube_processes[button_index]
                # Limpar perfil temporário do navegador
                try:
                    import shutil
                    profile_dir = self.youtube_profile_dirs.pop(button_index, None)
                    if profile_dir:
                        shutil.rmtree(profile_dir, ignore_errors=True)
                except Exception:
                    pass
        else:
            print(f"⚠️ Nenhum processo YouTube encontrado para botão {button_index}")

    def _send_fullscreen_command(self):
        """Fullscreen é ativado via argumentos do navegador"""
        pass

    def _extract_youtube_id(self, url):
        """Extrai o ID do vídeo da URL do YouTube"""
        try:
            # Padrão para youtube.com/watch?v=ID
            match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)', url)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"❌ Erro ao extrair ID do YouTube: {e}")
        return None

    # ===============================
    # DISCORD BOT INTEGRATION
    # ===============================

    def sync_with_bot(self):
        """Sincroniza URLs do Discord Bot"""
        if not self.bot_connection_key:
            return False
        
        # O bot Discord não fornece API HTTP, sincronização desativada
        # Os URLs são gerenciados através dos comandos Discord
        return True

    def sincronizar_atualizacoes(self):
        """Sincroniza atualizacoes em tempo real (a cada 5 segundos)
        
        IMPORTANTE: Aplica mudancas DIRETAMENTE NA MEMORIA, nao no arquivo JSON.
        O arquivo JSON so eh salvo quando o app fecha (closeEvent).
        LOG: SO MOSTRA SUCESSOS!
        """
        try:
            from sincronizador import AtualizadorDeck
            
            atualizador = AtualizadorDeck()
            mudancas = atualizador.processar_atualizacoes()
            
            if mudancas:
                # Aplicar cada mudanca diretamente na memoria
                for mudanca in mudancas:
                    idx = mudanca['botao_idx']
                    file_path = mudanca['file']
                    is_youtube = mudanca['is_youtube']
                    tipo = mudanca['tipo']
                    nome_arquivo = mudanca.get('nome_arquivo')  # Para deletar depois
                    nome_botao = mudanca.get('nome_botao')  # Nome customizado do botao
                    
                    # Se for arquivo, tentar abrir (para validar)
                    if tipo in ('video', 'imagem'):
                        if not os.path.exists(file_path):
                            continue
                        # Se chegou aqui, arquivo existe e foi validado
                        # Usar nome customizado se disponivel, senao usar nome do arquivo
                        if nome_botao:
                            conteudo_visual = nome_botao
                        else:
                            conteudo_visual = os.path.basename(file_path)[:15]
                    else:
                        # Para links, usar nome customizado se disponivel
                        conteudo_visual = nome_botao if nome_botao else file_path[:50]
                    
                    # Atualizar na memoria (self.button_files e self.button_config)
                    self.button_files[idx] = file_path
                    self.button_config[idx]['is_youtube'] = is_youtube
                    self.button_config[idx]['nome_botao'] = nome_botao  # Armazenar nome customizado
                    
                    # Atualizar visual do botao com nome customizado
                    btn = self.buttons[idx]
                    btn.setText(conteudo_visual)
                    print(f"[ATUALIZACAO OK] Botao {idx+1}: {conteudo_visual}")
                    
                    # Agendar delecao do arquivo do VPS apos 30 minutos
                    # Da tempo suficiente para o app baixar e sincronizar
                    if tipo in ('video', 'imagem') and nome_arquivo:
                        QTimer.singleShot(1800000, lambda n=nome_arquivo: self._deletar_arquivo_vps(n))  # 30 minutos
                    
        except Exception as e:
            # Silenciar erros de conexao durante sincronizacao continua
            if "Connection refused" not in str(e) and "timeout" not in str(e).lower():
                print(f"[ERRO] Sincronizacao: {e}")
    
    def _deletar_arquivo_vps(self, filename: str):
        """Deleta arquivo do VPS apos consumo (SILENCIOSO)"""
        try:
            from sincronizador import AtualizadorDeck
            atualizador = AtualizadorDeck()
            atualizador.deletar_arquivo_vps(filename)
        except Exception:
            # Silencioso: erro ao deletar, ignorar
            pass

    def setup_bot_connection(self):
        """Solicita chave de conexão do Discord Bot"""
        dialog = QInputDialog()
        dialog.setWindowTitle("Conexão com Discord Bot")
        dialog.setLabelText("Cole sua chave de conexão (obtida com /setup no Discord):")
        
        if dialog.exec() == QInputDialog.DialogCode.Accepted:
            key = dialog.textValue().strip().upper()
            if key:
                self.bot_connection_key = key
                self.save_config()
                
                # Tentar sincronizar imediatamente
                if self.sync_with_bot():
                    print(f"✅ Conexão estabelecida com sucesso!")
                    return True
                else:
                    print(f"❌ Não foi possível conectar ao bot. Verifique se a chave está correta e o bot está rodando.")
        
        return False

    def manage_bot_keys(self):
        """Abre dialog para gerenciar chaves do bot - Discord opcional"""
        try:
            from bot_connector import connector
            from bot_key_ui import BotKeyDialog, BotKeysListDialog
            from PyQt6.QtWidgets import QMessageBox
            
            # Verificar se há chaves conectadas
            keys = connector.list_keys()
            
            if not keys:
                # Fluxo automático simples: perguntar se quer integrar Discord
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("🤖 Conectar com Discord Bot?")
                msg_box.setText("Deseja integrar seu servidor Discord com SminDeck?\n\n"
                    "Vamos adicionar o bot ao seu servidor em poucos cliques!\n\n"
                    "Você precisa ter um servidor Discord.")
                
                # Adicionar três botões
                btn_sim = msg_box.addButton("Sim", QMessageBox.ButtonRole.YesRole)
                btn_tenho_chave = msg_box.addButton("Tenho chave", QMessageBox.ButtonRole.ActionRole)
                btn_nao = msg_box.addButton("Não", QMessageBox.ButtonRole.NoRole)
                
                msg_box.setDefaultButton(btn_sim)
                msg_box.exec()
                
                reply = msg_box.clickedButton()
                
                if reply == btn_sim:
                    # Abrir Discord automaticamente com convite
                    import webbrowser
                    
                    # URL de convite com o ID real do bot
                    invite_url = "https://discord.com/api/oauth2/authorize?client_id=1457841504893538385&scope=bot&permissions=8"
                    webbrowser.open(invite_url)
                    
                    QMessageBox.information(
                        self,
                        "✅ Adicione o Bot",
                        "Discord abriu no seu navegador!\n\n"
                        "1. Clique em 'Selecionar um servidor'\n"
                        "2. Escolha seu servidor\n"
                        "3. Clique em 'Autorizar'\n"
                        "4. Clique em 'OK' aqui quando terminar\n\n"
                        "O bot enviará uma CHAVE via DM para você!"
                    )
                    
                    # Aguardar a chave via DM
                    QMessageBox.information(
                        self,
                        "🔑 Receba sua Chave",
                        "Verifique suas mensagens diretas no Discord.\n\n"
                        "O bot enviou uma CHAVE para você.\n\n"
                        "Clique em 'OK' e cole a chave na próxima tela."
                    )
                    
                    # Abrir dialog para colar a chave
                    dialog = BotKeyDialog(connector, self)
                    if dialog.exec():
                        keys = connector.list_keys()
                        if keys:
                            first_key = list(keys.keys())[0]
                            self.bot_connection_key = first_key
                            self.save_config()
                            self.update_bot_button_visibility()
                            self.sync_with_bot()
                elif reply == btn_tenho_chave:
                    # Usuário já tem uma chave do Discord Bot
                    dialog = BotKeyDialog(connector, self)
                    if dialog.exec():
                        keys = connector.list_keys()
                        if keys:
                            first_key = list(keys.keys())[0]
                            self.bot_connection_key = first_key
                            self.save_config()
                            self.update_bot_button_visibility()
                            self.sync_with_bot()
            else:
                # Se há chaves, mostrar lista para gerenciar
                list_dialog = BotKeysListDialog(connector, self)
                list_dialog.exec()
        except ImportError:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Aviso",
                "Discord não está configurado.\n\n"
                "O app funciona normalmente, mas você pode integrar Discord quando quiser."
            )

    def update_bot_button_visibility(self):
        """Mostra/oculta o botão BOT baseado na presença de chave ativada"""
        # Verificar se o botão foi criado
        if not hasattr(self, 'bot_btn'):
            return
        
        if self.bot_connection_key:
            # Se há chave ativada, ocultar o botão
            self.bot_btn.hide()
        else:
            # Se não há chave, mostrar o botão
            self.bot_btn.show()

    def on_button_clicked(self, index):
        file_path = self.button_files.get(index)

        
        if not self.button_config[index].get("enabled", True):
            return

        if not file_path:
            return

        cfg = self.button_config[index]

        # Verificar se é URL do YouTube
        if cfg.get("is_youtube", False) and self._is_youtube_url(file_path):
            self._open_youtube_fullscreen(file_path, cfg, index)
            return

        if self.fade_mode_enabled:
            # 🎬 Com FADE: Inicia a nova reprodução (opaca, sem fade in)
            self._start_play(index, file_path, cfg)
            # ⏱️ Aguarda 100ms para garantir que a nova está renderizada
            # Então faz fade out da anterior
            QTimer.singleShot(100, self._hide_previous_playback)
        else:
            # ⚡ Sem FADE: Fecha completamente a anterior antes de iniciar a nova
            self._force_close_all_playbacks()
            QTimer.singleShot(50, lambda: self._start_play(index, file_path, cfg))

    def _hide_previous_playback(self):
        """Faz crossfade da reprodução anterior (mantém apenas a última ativa)"""
        if len(self.playback_windows) > 1:
            # Garante que a nova janela (última) está visível primeiro
            self.playback_windows[-1].raise_()
            
            # Depois faz fade out das anteriores
            for win in self.playback_windows[:-1]:  # Todas EXCETO a última
                if win:
                    try:
                        # Faz fade out de opacidade (600ms)
                        win.crossfade_out(600)
                    except Exception:
                        pass

    def _force_close_all_playbacks(self):
        """Força o fechamento imediato de todas as reproduções (destroi as janelas) e YouTubes"""
        for win in self.playback_windows[:]:
            if win:
                try:
                    win.close()
                    win.deleteLater()
                except Exception as e:
                    print(f"❌ Erro ao fechar playback: {e}")
        self.playback_windows.clear()
        
        # Fechar todos os YouTubes abertos
        for button_index in list(self.youtube_processes.keys()):
            self._close_youtube_for_button(button_index)

    def _close_all_playbacks_fade(self):
        """Para e esconde todas as reproduções ativas suavemente"""
        if len(self.playback_windows) > 1:
            for win in self.playback_windows[:-1]:  # Todas EXCETO a última
                if win and hasattr(win, 'stop_playback_smooth'):
                    win.stop_playback_smooth()

    def _close_all_playbacks(self):
        """Fecha todas as reproduções ativas com fade out"""
        for win in self.playback_windows[:]:  # Cópia da lista
            if win and hasattr(win, 'fade_out_and_close'):
                # Usa fade out da janela de reprodução
                win.fade_out_and_close()
        # NÃO limpa a lista - deixa que as janelas se removam via _on_playback_finished

    def _start_play(self, index, file_path, cfg):
        self.clear_on_air()
        self.set_button_active(index)

        fade_enabled = cfg.get("fade_enabled", True)
        fade_in = cfg.get("fade_in", 800) if fade_enabled else 0
        fade_out = cfg.get("fade_out", 600) if fade_enabled else 0


        screens = cfg.get("screens", [0])

        for screen_index in screens:
            print(f"\n{'='*60}")
            print(f"[DEBUG] self.player_config = {self.player_config}")
            print(f"[DEBUG] player_config não vazio? {bool(self.player_config)}")
            if self.player_config:
                print(f"[DEBUG] logo_path = {self.player_config.get('logo_path')}")
                print(f"[DEBUG] logo_size = {self.player_config.get('logo_size')}")
                print(f"[DEBUG] logo_opacity = {self.player_config.get('logo_opacity')}")
            print(f"[DEBUG] Abrindo PlaybackWindow com player_config: {self.player_config}")
            print(f"{'='*60}\n")
            win = PlaybackWindow(
                file_path,
                screen_index=screen_index,
                fade_in_ms=cfg.get("fade_in", 800),
                fade_out_ms=cfg.get("fade_out", 600),
                player_config=self.player_config  # Passar configurações do player
            )

            self.playback_windows.append(win)
            win.finished.connect(lambda w=win: self._on_playback_finished(w))

    def configure_player_logo(self):
        """Abre dialog para configurar logo do player"""
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Configurações do Player")
        dialog.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # Botão para selecionar logo
        logo_label = QLabel("Logo (canto inferior esquerdo):")
        layout.addWidget(logo_label)
        
        logo_btn = QPushButton("Selecionar Logo...")
        logo_current = QLabel()
        
        if self.player_config.get("logo_path"):
            logo_current.setText(f"Logo atual: {os.path.basename(self.player_config['logo_path'])}")
        else:
            logo_current.setText("Nenhuma logo selecionada")
        
        def select_logo():
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(
                self,
                "Selecionar Logo",
                "",
                "Imagens (*.png *.jpg *.jpeg *.bmp *.gif);;Todos os arquivos (*)"
            )
            if file_path:
                self.player_config["logo_path"] = file_path
                print(f"[DEBUG] Logo selecionada: {file_path}")
                logo_current.setText(f"Logo atual: {os.path.basename(file_path)}")
        
        logo_btn.clicked.connect(select_logo)
        layout.addWidget(logo_btn)
        layout.addWidget(logo_current)
        
        # Opacidade
        layout.addWidget(QLabel("Opacidade da Logo:"))
        opacity_spin = QSpinBox()
        opacity_spin.setMinimum(10)
        opacity_spin.setMaximum(100)
        opacity_spin.setValue(int(self.player_config.get("logo_opacity", 0.8) * 100))
        opacity_spin.setSuffix("%")
        layout.addWidget(opacity_spin)
        
        # Tamanho
        layout.addWidget(QLabel("Tamanho da Logo (pixels):"))
        size_spin = QSpinBox()
        size_spin.setMinimum(50)
        size_spin.setMaximum(400)
        size_spin.setValue(self.player_config.get("logo_size", 150))
        layout.addWidget(size_spin)
        
        # Botões OK/Cancel
        layout.addStretch()
        button_layout = QHBoxLayout()
        
        btn_ok = QPushButton("✅ OK")
        btn_cancel = QPushButton("❌ Cancelar")
        
        def on_ok():
            self.player_config["logo_opacity"] = opacity_spin.value() / 100.0
            self.player_config["logo_size"] = size_spin.value()
            print(f"[DEBUG] player_config salvo: {self.player_config}")
            self.save_config()
            dialog.accept()
        
        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def open_logo_editor_window(self):
        """Abre editor de logo em janela flutuante durante reprodução"""
        if not self.playback_windows:
            print("⚠️ Nenhuma reprodução ativa")
            return
        
        if not (self.player_config and self.player_config.get("logo_path")):
            print("⚠️ Nenhuma logo configurada")
            return
        
        logo_path = self.player_config["logo_path"]
        if not os.path.exists(logo_path):
            print(f"⚠️ Logo não encontrada: {logo_path}")
            return
        
        try:
            from PyQt6.QtGui import QPixmap
            from logo_editor_window import LogoEditorWindow
            
            logo_size = self.player_config.get("logo_size", 150)
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                print("⚠️ Logo inválida")
                return
            
            # Criar janela do editor
            self._logo_editor_window = LogoEditorWindow(pixmap, self.player_config, parent=None)
            self._logo_editor_window.config_changed.connect(self._on_logo_config_changed)
            self._logo_editor_window.show()
            
            print("✅ Editor de logo aberto")
        except Exception as e:
            print(f"⚠️ Erro ao abrir editor de logo: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_logo_config_changed(self, config):
        """Callback quando usuário salva a posição da logo"""
        self.player_config.update(config)
        # Atualizar também no playback window se estiver tocando
        for window in self.playback_windows:
            if hasattr(window, 'player_config'):
                window.player_config.update(config)
            # Recarregar a logo para atualizar display
            if hasattr(window, '_load_player_logo'):
                window._load_player_logo()
                window.update()  # Forçar repaint
        print(f"✅ Posição da logo atualizada: x={config.get('x')}, y={config.get('y')}")

    def show_context_menu(self, pos):
        button = self.sender()
        index = self.buttons.index(button)

        menu = QMenu(button)
        menu.setStyleSheet(self.context_menu_style())

        # ===============================
        # CHECKBOXES (ESTADO)
        # ===============================
        action_enabled = QAction(self.svg_icon("enable.svg"), "✅ Botão ativo", self)
        action_enabled.setCheckable(True)
        action_enabled.setChecked(
            self.button_config[index].get("enabled", True)
        )

        action_fade_toggle = QAction(self.svg_icon("fade.svg"), "✨ Fade ativado", self)
        action_fade_toggle.setCheckable(True)
        action_fade_toggle.setChecked(
            self.button_config[index].get("fade_enabled", True)
        )

        menu.addAction(action_enabled)
        menu.addAction(action_fade_toggle)
        menu.addSeparator()

        action_media = QAction(self.svg_icon("media.svg"), "📁 Selecionar mídia…", self)
        action_fade_cfg = QAction(self.svg_icon("fade.svg"), "⚙️ Configurar fade…", self)
        action_screen = QAction(self.svg_icon("screen.svg"), "📺 Opção de tela…", self)
        action_icon = QAction(self.svg_icon("media.svg"), "🖼️ Personalizar ícone…", self)
        action_edit_logo = QAction(self.svg_icon("media.svg"), "✏️ Editar posição da logo…", self)
        action_clear = QAction(self.svg_icon("media.svg"), "🗑️ Limpar botão", self)
        action_stop = QAction(self.svg_icon("media.svg"), "⛔ Parar reprodução", self)

        menu.addAction(action_media)
        menu.addAction(action_fade_cfg)
        menu.addAction(action_screen)
        menu.addSeparator()
        if self.playback_windows:  # Mostrar só se estiver reproduzindo
            menu.addAction(action_edit_logo)
        menu.addSeparator()
        menu.addAction(action_stop)
        menu.addSeparator()
        menu.addAction(action_icon)
        menu.addAction(action_clear)
        
        # ===============================
        # DISCORD BOT INTEGRATION
        # ===============================
        menu.addSeparator()
        
        # Só mostrar opção de conectar se ainda não tiver chave
        if not self.bot_connection_key:
            action_bot_connect = QAction(self.svg_icon("media.svg"), "🤖 Conectar Discord Bot", self)
            menu.addAction(action_bot_connect)
        else:
            action_bot_connect = None  # Não vai mostrar


        # ===============================
        # EXECUÇÃO
        # ===============================
        action = menu.exec(button.mapToGlobal(pos))

        if action is None:
            return

        # ===============================
        # TRATAMENTO
        # ===============================
        if action == action_enabled:
            enabled = action_enabled.isChecked()
            self.button_config[index]["enabled"] = enabled
            self.update_button_enabled_state(index)

        elif action == action_fade_toggle:
            enabled = action_fade_toggle.isChecked()
            self.button_config[index]["fade_enabled"] = enabled

        elif action == action_media:
            self.select_file_for_button(index, button)

        elif action == action_fade_cfg:
            self.configure_fade(index)

        elif action == action_screen:
            self.configure_screens(index)
        
        elif action == action_edit_logo:
            self.open_logo_editor_window()
        
        elif action == action_icon:
            self.customize_button_icon(index, button)
        
        elif action == action_clear:
            self.clear_button(index, button)

        elif action == action_stop:
            self._force_close_all_playbacks()
        
        elif action_bot_connect and action == action_bot_connect:
            self.setup_bot_connection()
        
        elif action == action_bot_sync:
            if self.sync_with_bot():
                print("✅ Sincronização concluída!")
            else:
                print("❌ Falha na sincronização")

        elif action == action_bot_install:
            self.open_discord_bot_installer()


    def open_discord_bot_installer(self):
        """Abre o instalador do bot (se estiver incluído na instalação do SminDeck)."""
        try:
            if getattr(sys, "frozen", False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))

            candidates = [
                # Instalado (padrão): {app}\bot_installer\SminDeckBot-Setup.exe
                os.path.join(base_dir, "bot_installer", "SminDeckBot-Setup.exe"),
                # Alternativa: instalador ao lado do exe
                os.path.join(base_dir, "SminDeckBot-Setup.exe"),
                # Dev/teste: se estiver rodando de dist\SminDeck.exe, procura também na raiz do projeto
                os.path.normpath(os.path.join(base_dir, "..", "bot_installer", "SminDeckBot-Setup.exe")),
                # Busca ampla: qualquer SminDeckBot-Setup.exe na pasta do SminDeck ou subpastas
                os.path.join(base_dir, "bot_installer", "SminDeckBot-Setup.exe"),
            ]
            
            # Log de debug
            print(f"🔍 Procurando instalador do bot em: {base_dir}")

            installer_path = next((p for p in candidates if os.path.exists(p)), None)
            if not installer_path:
                QMessageBox.information(
                    self,
                    "Bot Discord",
                    "Instalador do bot não encontrado nesta instalação.\n\n"
                    "Se você quer oferecer o modo remoto para o cliente, inclua o arquivo:\n"
                    "SminDeckBot-Setup.exe\n"
                    "na pasta de instalação do SminDeck (ao lado do SminDeck.exe ou em uma subpasta).\n\n"
                    "Pasta atual: " + base_dir + "\n\n"
                    "Caminhos verificados:\n- "
                    + "\n- ".join(candidates),
                )
                return

            print(f"✅ Encontrado instalador do bot: {installer_path}")
            subprocess.Popen([installer_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            try:
                QMessageBox.warning(self, "Bot Discord", f"Não consegui abrir o instalador: {e}")
            except Exception:
                pass


    def context_menu_style(self):
        return """
        QMenu {
            background-color: #1e1e2e;
            color: #ffffff;
            border: 2px solid #404060;
            border-radius: 8px;
            padding: 8px;
        }

        QMenu::item {
            padding: 10px 16px;
            border-radius: 6px;
            margin: 2px 2px;
        }

        QMenu::item:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6c63ff,
                stop:1 #5c53ef
            );
            color: #ffffff;
        }

        QMenu::item:selected {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6c63ff,
                stop:1 #5c53ef
            );
            color: #ffffff;
        }

        QMenu::indicator {
            width: 18px;
            height: 18px;
            margin-right: 10px;
        }

        QMenu::indicator:unchecked {
            border: 2px solid #404060;
            border-radius: 4px;
            background-color: #2a2a3e;
        }

        QMenu::indicator:unchecked:hover {
            border: 2px solid #6c63ff;
            background-color: #323245;
        }

        QMenu::indicator:checked {
            border: 2px solid #6c63ff;
            background-color: #6c63ff;
            border-radius: 4px;
        }

        QMenu::separator {
            height: 1px;
            background: #404060;
            margin: 8px 4px;
        }

        QMenu::icon {
            padding-left: 8px;
        }
        """

    def svg_icon(self, name):
        path = os.path.join("assets", "icons", name)
        if os.path.exists(path):
            return QIcon(path)
        return QIcon()

    
    def update_button_enabled_state(self, index):
        btn = self.buttons[index]
        enabled = self.button_config[index].get("enabled", True)

        # ⚠️ botão SEMPRE habilitado (para menu funcionar)
        btn.setEnabled(True)

        if enabled:
            btn.setStyleSheet("")
        else:
            btn.stop_on_air()
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: #777;
                }
            """)

        # atualiza overlay
        btn.set_enabled_overlay(enabled)


        




    # ===============================
    # ON AIR (CORRIGIDO)
    # ===============================
    def set_button_active(self, index):
        print(f"📍 set_button_active({index}) chamado")
        if self.active_index is not None:
            print(f"📍 Parando botão anterior: {self.active_index}")
            self.buttons[self.active_index].stop_on_air()

        print(f"📍 Ativando botão: {index}")
        self.buttons[index].start_on_air()
        self.active_index = index

    def clear_on_air(self):
        for btn in self.buttons:
            btn.stop_on_air()
        self.active_index = None

    def _on_playback_finished(self, win):
        if win in self.playback_windows:
            self.playback_windows.remove(win)

        # Limpa janelas ocultas antigas para não acumular
        self.playback_windows = [w for w in self.playback_windows if w and w.isVisible()]

        if not self.playback_windows and self.active_index is not None:
            self.buttons[self.active_index].reset_visual()
            self.active_index = None


    def save_to_json(self, path=DECK_FILE):
        if not self.has_any_media() and not self.bot_connection_key:
            print("ℹ️ Nenhuma mídia no deck — não salvando .sdk")
            return

        data = {
            "__metadata__": {
                "bot_connection_key": self.bot_connection_key,
                "player_config": self.player_config  # Salvar configurações do player
            }
        }
        
        print(f"[SAVE] Salvando player_config: {self.player_config}")

        for i in range(len(self.buttons)):
            data[str(i)] = {
                "file": self.button_files.get(i),
                "fade_enabled": self.button_config[i].get("fade_enabled", True),
                "fade_in": self.button_config[i].get("fade_in", 800),
                "fade_out": self.button_config[i].get("fade_out", 600),
                "screens": self.button_config[i].get("screens", [0]),
                "icon_path": self.button_config[i].get("icon_path"),
                "is_youtube": self.button_config[i].get("is_youtube", False),
                "nome_botao": self.button_config[i].get("nome_botao")  # Salvar nome customizado
            }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("💾 Configuração salva em .sdk")

    def load_from_json(self, path=DECK_FILE):
        if not os.path.exists(path):
            print("ℹ️ Nenhum arquivo .sdk encontrado")
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Carregar metadados (incluindo chave do bot)
        metadata = data.get("__metadata__", {})
        if metadata.get("bot_connection_key"):
            self.bot_connection_key = metadata.get("bot_connection_key")
            print(f"✅ Chave do Discord Bot carregada: {self.bot_connection_key[:4]}***")
            self.update_bot_button_visibility()
            # Tentar sincronizar com o bot na inicialização
            QTimer.singleShot(1000, self.sync_with_bot)
        
        # Carregar configurações do player
        if metadata.get("player_config"):
            self.player_config.update(metadata.get("player_config"))
            print(f"[STARTUP] player_config carregado do JSON: {self.player_config}")
            print(f"✅ Configurações do player carregadas")
            if self.player_config.get("logo_path"):
                print(f"   📺 Logo: {self.player_config['logo_path']}")
        else:
            print(f"[STARTUP] Nenhum player_config no JSON")

        for key, cfg in data.items():
            try:
                index = int(key)
            except ValueError:
                continue

            if index < 0 or index >= len(self.buttons):
                continue

            file_path = cfg.get("file")
            if file_path:
                self.button_files[index] = file_path
                print(f"📝 Carregando Botão {index}: {file_path}")
                
                # Verifica se é URL do YouTube
                is_youtube = cfg.get("is_youtube", False)
                self.button_config[index]["is_youtube"] = is_youtube
                
                if is_youtube and self._is_youtube_url(file_path):
                    self.buttons[index].setText(f"BTN {index + 1}\n📺 YouTube")
                    print(f"✅ Botão {index} atualizado como YouTube")
                else:
                    text = self.format_button_text(index, file_path)
                    self.buttons[index].setText(text)
                    print(f"✅ Botão {index} atualizado com: {text}")

            btn = self.buttons[index]

            btn.set_enabled_overlay(
                self.button_config[index].get("enabled", True)
            )

            btn.set_fade_enabled(
                self.button_config[index].get("fade_enabled", True)
            )

            self.button_config[index]["screens"] = cfg.get("screens", [0])
            
            # Restaurar nome customizado se existir
            nome_botao = cfg.get("nome_botao")
            if nome_botao:
                self.button_config[index]["nome_botao"] = nome_botao
                # IMPORTANTE: Atualizar o texto do botão também!
                self.buttons[index].setText(nome_botao)
                print(f"✅ Botão {index} restaurado com nome customizado: {nome_botao}")
            
            # Carregar ícone personalizado se existir
            icon_path = cfg.get("icon_path")
            if icon_path and os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                # Redimensiona a imagem para preencher quase todo o botão (deixa pequeno padding)
                icon_size = QSize(btn.width() - 8, btn.height() - 8)
                btn.setIconSize(icon_size)
                # Remove o texto se houver ícone
                btn.setText("")
                self.button_config[index]["icon_path"] = icon_path

        print("📂 Configuração carregada do .sdk")

    def reload_deck_config(self):
        """
        Recarrega a configuração do deck após sincronização
        Atualiza todos os botões com dados novos do arquivo
        """
        try:
            print("🔄 Recarregando configuração do deck...")
            
            # Limpar dados anteriores completamente
            self.button_files.clear()
            for i in range(len(self.buttons)):
                self.buttons[i].setText(f"BTN {i + 1}")
                self.buttons[i].setIcon(QIcon())  # Limpar ícone
                self.button_config[i]["icon_path"] = None
            
            # Recarregar configuração do arquivo
            self.load_from_json()
            
            print("✅ Configuração recarregada com sucesso!")
            return True
        except Exception as e:
            print(f"⚠️ Erro ao recarregar configuração: {e}")
            import traceback
            traceback.print_exc()
            return False

    def save_config(self):
        """Alias para save_to_json - salva a configuração"""
        self.save_to_json()

    def closeEvent(self, event):
        self.save_to_json()
        event.accept()
        print("🔥 closeEvent chamado")

    def has_any_media(self):
        """
        Retorna True se houver pelo menos um botão com mídia associada
        """
        return any(self.button_files.values())
    
    def configure_fade(self, index):
        cfg = self.button_config[index]

        dialog = FadeConfigDialog(
            fade_enabled=cfg.get("fade_enabled", True),
            fade_in=cfg.get("fade_in", 800),
            fade_out=cfg.get("fade_out", 600),
            parent=self
        )

        if dialog.exec():
            values = dialog.get_values()

            cfg["fade_enabled"] = values["fade_enabled"]
            cfg["fade_in"] = values["fade_in"]
            cfg["fade_out"] = values["fade_out"]

            print(
                f"🎚️ BTN {index + 1} | "
                f"Fade {'ON' if values['fade_enabled'] else 'OFF'} | "
                f"IN={values['fade_in']} / OUT={values['fade_out']}"
        )





    def format_button_text(self, index, file_path):
        """
        Formata o texto do botão com índice + nome do arquivo
        (método usado por load_from_json e select_file_for_button)
        """
        name = os.path.basename(file_path)
        name_no_ext = os.path.splitext(name)[0]

        btn = self.buttons[index]
        font = btn.font()
        metrics = QFontMetrics(font)

        available_width = btn.width() - 16

        elided = metrics.elidedText(
            name_no_ext,
            Qt.TextElideMode.ElideRight,
            available_width
        )

        return f"BTN {index + 1}\n{elided}"
    
    def configure_screens(self, index):
        current = self.button_config[index].get("screens", [0])

        dialog = ScreenSelectDialog(
            selected_screens=current,
            parent=self
        )

        if dialog.exec():
            selected = dialog.selected_indexes()
            if not selected:
                selected = [0]  # fallback de segurança

            self.button_config[index]["screens"] = selected
            
            # Salvar imediatamente
            self.save_to_json()

            print(f"🎯 Botão {index + 1} → telas {selected}")
    
    def customize_button_icon(self, index, button):
        """Personalizar ícone/imagem do botão"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar ícone/imagem para o botão",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.svg)"
        )
        
        if not file_path:
            return
        
        # Armazenar a imagem na configuração
        self.button_config[index]["icon_path"] = file_path
        
        # Aplicar o ícone no botão com tamanho que preencha a área
        button.setIcon(QIcon(file_path))
        # Redimensiona a imagem para preencher quase todo o botão (deixa pequeno padding)
        icon_size = QSize(button.width() - 8, button.height() - 8)
        button.setIconSize(icon_size)
        # Remove o texto para dar espaço à imagem
        button.setText("")
        
        print(f"🖼️ Ícone personalizado do BTN {index + 1}: {os.path.basename(file_path)}")
    
    def clear_button(self, index, button):
        """Limpar o botão (remover ícone e mídia, voltando ao padrão)"""
        # Remover ícone
        button.setIcon(QIcon())
        
        # Remover caminho do ícone da configuração
        if "icon_path" in self.button_config[index]:
            del self.button_config[index]["icon_path"]
        
        # Remover arquivo de mídia associado
        if index in self.button_files:
            del self.button_files[index]
        
        # Limpar a configuração "enabled"
        self.button_config[index]["enabled"] = True
        button.set_enabled_overlay(True)
        
        # ✅ LIMPAR NOME CUSTOMIZADO
        if "nome_botao" in self.button_config[index]:
            self.button_config[index]["nome_botao"] = None
        
        # Restaurar texto padrão
        button.setText(f"BTN {index + 1}")
        
        # ✅ SALVAR CONFIGURAÇÃO IMEDIATAMENTE
        self.save_to_json()
        
        print(f"🗑️ Botão {index + 1} completamente limpo (ícone + mídia + nome)")

    def on_file_dropped(self, button, file_path):
        if not os.path.isfile(file_path):
            return

        index = self.buttons.index(button)

        # reaproveita a lógica existente
        self.button_files[index] = file_path

        ext = os.path.splitext(file_path)[1].lower()

        if ext in (".jpg", ".jpeg", ".png", ".bmp"):
            button.setIcon(QIcon(file_path))
            # Redimensiona a imagem para preencher quase todo o botão (deixa pequeno padding)
            icon_size = QSize(button.width() - 8, button.height() - 8)
            button.setIconSize(icon_size)
            button.setText("")
        elif ext in (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"):
            # Vídeo detectado - capturar thumbnail automaticamente
            thumbnail_path = self.extract_video_thumbnail(file_path, index)
            if thumbnail_path:
                self.button_config[index]["icon_path"] = thumbnail_path
                button.setIcon(QIcon(thumbnail_path))
                icon_size = QSize(button.width() - 8, button.height() - 8)
                button.setIconSize(icon_size)
                button.setText("")
                print(f"🎬 Thumbnail extraído do vídeo (drop) para BTN {index + 1}")
            else:
                button.setIcon(QIcon())
                button.setText(self.format_button_text(index, file_path))
        else:
            button.setIcon(QIcon())
            button.setText(self.format_button_text(index, file_path))

        print(f"🧲 Arquivo associado ao BTN {index + 1}: {file_path}")

    def select_file_for_button(self, index, button):
        cfg = self.button_config[index]

        dialog = MediaSelectDialog(
            enabled=cfg.get("enabled", True),
            file_path=self.button_files.get(index),
            parent=self
        )

        if not dialog.exec():
            return

        values = dialog.get_values()

        cfg["enabled"] = values["enabled"]
        cfg["is_youtube"] = values.get("is_youtube_url", False)

        if not values["file_path"]:
            return

        file_path = values["file_path"]
        self.button_files[index] = file_path

        # Se é URL do YouTube
        if values.get("is_youtube_url", False):
            button.setIcon(QIcon())
            button.setText(f"BTN {index + 1}\n📺 YouTube")
            print(f"🎬 URL do YouTube associada ao BTN {index + 1}: {file_path}")
            self.update_button_enabled_state(index)
            return

        ext = os.path.splitext(file_path)[1].lower()

        if ext in (".jpg", ".jpeg", ".png", ".bmp"):
            button.setIcon(QIcon(file_path))
            button.setIconSize(
                QSize(button.width() - 16, button.height() - 16)
            )
            button.setText("")
        elif ext in (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"):
            # Vídeo detectado - capturar thumbnail automaticamente
            thumbnail_path = self.extract_video_thumbnail(file_path, index)
            if thumbnail_path:
                self.button_config[index]["icon_path"] = thumbnail_path
                button.setIcon(QIcon(thumbnail_path))
                icon_size = QSize(button.width() - 8, button.height() - 8)
                button.setIconSize(icon_size)
                button.setText("")
                print(f"🎬 Thumbnail extraído do vídeo para BTN {index + 1}")
            else:
                button.setIcon(QIcon())
                button.setText(self.format_button_text(index, file_path))
        else:
            button.setIcon(QIcon())
            button.setText(self.format_button_text(index, file_path))

        self.update_button_enabled_state(index)

    def extract_video_thumbnail(self, video_path, button_index):
        """Extrair thumbnail do vídeo usando ffmpeg"""
        try:
            import tempfile
            
            # Criar arquivo temporário para a thumbnail
            temp_dir = tempfile.gettempdir()
            thumbnail_filename = f"btn_{button_index}_thumbnail.jpg"
            thumbnail_path = os.path.join(temp_dir, thumbnail_filename)
            
            # Comando ffmpeg para extrair o primeiro frame útil
            # Usa seek=1 para pular o primeiro frame (às vezes preto) e pega aos 1 segundo
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-ss", "1",  # Começa em 1 segundo
                "-vframes", "1",  # Pega apenas 1 frame
                "-vf", "scale=200:150",  # Redimensiona para 200x150
                "-y",  # Overwrite sem perguntar
                thumbnail_path
            ]
            
            # Executar ffmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0 and os.path.exists(thumbnail_path):
                print(f"✅ Thumbnail extraída com sucesso: {thumbnail_path}")
                return thumbnail_path
            else:
                print(f"⚠️ Erro ao extrair thumbnail: {result.stderr.decode()}")
                return None
                
        except FileNotFoundError:
            print("❌ ffmpeg não encontrado. Instale ffmpeg para usar esta funcionalidade.")
            return None
        except Exception as e:
            print(f"❌ Erro ao extrair thumbnail: {e}")
            return None

    # ===============================
    # CONTROLES
    # ===============================




    # ===============================
    # CONTROLES
    # ===============================
    def pause_playback(self):
        for pw in getattr(self, "playback_windows", []):
            pw.pause()

        if self.active_index is not None:
            self.buttons[self.active_index].reset_visual()
            self.active_index = None

    def close_playback_window(self):
        for pw in getattr(self, "playback_windows", []):
            pw.close_playback()

        self.playback_windows = []

        if self.active_index is not None:
            self.buttons[self.active_index].reset_visual()
            self.active_index = None


    def load_last_deck(self):
        self.close_playback_window()
        self.load_from_json()

    def apply_style(self):
        self.setStyleSheet(get_stylesheet())


    # ===============================
    # BACKGROUND (SEPARADO)
    # ===============================
    def open_background_window(self):
        try:
            if hasattr(self, "bg_controller") and self.bg_controller is not None:
                self.bg_controller.show()
                try:
                    # bring to front if possible
                    self.bg_controller.raise_()
                except Exception:
                    pass
                return

            self.bg_controller = BackgroundController(self)
            self.bg_controller.show()
        except Exception as e:
            print("Erro ao abrir BackgroundController:", e)

    def handle_dev_reset(self, state):
        """Reseta chaves quando checkbox é marcado (DEV only)"""
        if state == 2:  # Qt.CheckState.Checked
            reply = QMessageBox.question(
                self,
                "🔧 Resetar Chaves",
                "Deseja resetar as chaves (Local + VPS)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import os
                    
                    # 1. Limpar BD local
                    db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
                    if os.path.exists(db_path):
                        os.remove(db_path)
                        print("✅ BD local deletado")
                    
                    # 2. Limpar VPS
                    try:
                        try:
                            from vps_config import VPS_CONFIG
                            import paramiko
                        except ImportError:
                            print("⚠️ Paramiko não instalado, pulando limpeza VPS")
                            return
                        
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(
                            VPS_CONFIG['host'],
                            port=VPS_CONFIG['port'],
                            username=VPS_CONFIG['user'],
                            password=VPS_CONFIG['password'],
                            timeout=10
                        )
                        
                        cmd = "rm -f /root/.smindeckbot/smindeckbot.db 2>/dev/null; mkdir -p /root/.smindeckbot"
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        stdout.read()
                        ssh.close()
                        print("✅ BD VPS deletado")
                        
                    except Exception as e:
                        print(f"⚠️  Erro ao resetar VPS: {e}")
                    
                    QMessageBox.information(self, "Sucesso", "✅ Chaves resetadas!\n\nLocal + VPS limpos")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"❌ Erro ao resetar:\n{str(e)}")
                finally:
                    # Desmarcar checkbox após operação
                    self.dev_reset_checkbox.blockSignals(True)
                    self.dev_reset_checkbox.setChecked(False)
                    self.dev_reset_checkbox.blockSignals(False)
            else:
                # Desmarcar se cancelar
                self.dev_reset_checkbox.blockSignals(True)
                self.dev_reset_checkbox.setChecked(False)
                self.dev_reset_checkbox.blockSignals(False)

    def show_beta_warning_if_needed(self):
        """Mostra aviso de teste usando QMessageBox padrão"""
        import os
        import json
        
        config_file = "deck_config.sdk"
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            beta_warning_disabled = config.get("beta_warning_disabled", False)
            
            if not beta_warning_disabled:
                from PyQt6.QtWidgets import QMessageBox
                
                msg = QMessageBox(self)
                msg.setWindowTitle("Versão em Teste")
                msg.setText("Este software está em fase de testes (Beta).\n\n"
                           "Podem ocorrer instabilidades.\n"
                           "Faça backup de suas configurações regularmente.")
                msg.setIcon(QMessageBox.Icon.NoIcon)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.setDefaultButton(QMessageBox.StandardButton.Ok)
                
                # Checkbox "Não mostrar novamente"
                checkbox = msg.findChild(type(None))  # Dummy para encontrar elemento
                from PyQt6.QtWidgets import QCheckBox
                checkbox = QCheckBox("Não mostrar novamente")
                msg.setCheckBox(checkbox)
                
                msg.exec()
                
                if checkbox.isChecked():
                    config["beta_warning_disabled"] = True
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"[ERRO] Aviso Beta: {e}")


    def open_playback(self, media, screen_index):
        win = PlaybackWindow(media, screen_index, player_config=self.player_config)
        win.show()










  






