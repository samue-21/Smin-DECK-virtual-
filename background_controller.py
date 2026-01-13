import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QLineEdit,
    QApplication, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QThread, pyqtSignal
from playback_window import PlaybackWindow
from background import TextBackgroundWindow, ClockBackgroundWindow
from theme import get_stylesheet


class BackgroundThread(QThread):
    show_screen = pyqtSignal(str, int)

    def __init__(self, media, screens):
        super().__init__()
        self.media = media
        self.screens = screens

    def run(self):
        # Emit a signal for each selected screen so the GUI thread can open playback windows
        media_arg = self.media if self.media else "__TEXT_ONLY__"
        print(f"📡 BackgroundThread enviando mídia: {media_arg}")
        for s in self.screens:
            print(f"   → Tela {s}")
            self.show_screen.emit(media_arg, s)


class BackgroundController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Background Controller")
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(440, 680)

        self.bg_process = None
        self.media_path = None
        self.logo_path = None
        self.logo_scale = 1.0  # Escala inicial da logo

        self.bg_script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "background.py"
        )

        # Aplicar stylesheet moderno unificado
        self.setStyleSheet(get_stylesheet())

        # ===============================
        # LAYOUT PRINCIPAL
        # ===============================
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("🎬 BACKGROUND CONTROL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
        layout.addWidget(title)

        # ===============================
        # LOOP
        # ===============================
        self.loop_checkbox = QCheckBox("🔄 Loop infinito")
        self.loop_checkbox.setChecked(True)
        self.loop_checkbox.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.loop_checkbox)
        self.loop_checkbox.toggled.connect(self._on_loop_toggled)

        # ===============================
        # RELÓGIO
        # ===============================
        self.clock_checkbox = QCheckBox("⏰ Exibir relógio no palco")
        self.clock_checkbox.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.clock_checkbox)

        # ===============================
        # LOGO DO RELÓGIO
        # ===============================
        logo_label_title = QLabel("🖼️ Logo do relógio (PNG):")
        logo_label_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(logo_label_title)

        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(8)

        self.select_logo_btn = QPushButton("🖼️ Selecionar logo")
        self.select_logo_btn.setFont(QFont("Segoe UI", 9))
        self.select_logo_btn.setMinimumHeight(32)
        self.select_logo_btn.clicked.connect(self.select_logo)

        self.logo_status_label = QLabel("Nenhum logo selecionado")
        self.logo_status_label.setStyleSheet("color: #9e9e9e; font-size: 10px;")
        self.logo_status_label.setFont(QFont("Segoe UI", 9))

        # Botões + e - para controlar tamanho da logo
        self.btn_decrease_logo = QPushButton("-")
        self.btn_decrease_logo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.btn_decrease_logo.setFixedSize(45, 35)
        self.btn_decrease_logo.setToolTip("Diminuir tamanho da logo")
        self.btn_decrease_logo.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a4e,
                    stop:1 #2a2a3e
                );
                color: #ffffff;
                border: 2px solid #404060;
                border-radius: 6px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c63ff,
                    stop:1 #5c53ef
                );
                border: 2px solid #6c63ff;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #5c53ef;
                border: 2px solid #5c53ef;
                color: #ffffff;
            }
        """)
        self.btn_decrease_logo.clicked.connect(self.decrease_logo_size)
        
        self.btn_increase_logo = QPushButton("+")
        self.btn_increase_logo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.btn_increase_logo.setFixedSize(45, 35)
        self.btn_increase_logo.setToolTip("Aumentar tamanho da logo")
        self.btn_increase_logo.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a4e,
                    stop:1 #2a2a3e
                );
                color: #ffffff;
                border: 2px solid #404060;
                border-radius: 6px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c63ff,
                    stop:1 #5c53ef
                );
                border: 2px solid #6c63ff;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #5c53ef;
                border: 2px solid #5c53ef;
                color: #ffffff;
            }
        """)
        self.btn_increase_logo.clicked.connect(self.increase_logo_size)

        logo_layout.addWidget(self.select_logo_btn, 0)
        logo_layout.addWidget(self.logo_status_label, 1)
        logo_layout.addWidget(self.btn_decrease_logo)
        logo_layout.addWidget(self.btn_increase_logo)

        layout.addLayout(logo_layout)

        # ===============================
        # TEXTO
        # ===============================
        self.text_checkbox = QCheckBox("📝 Exibir texto no palco")
        self.text_checkbox.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.text_checkbox)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Digite o texto para o palco...")
        self.text_input.setFont(QFont("Segoe UI", 10))
        self.text_input.setMinimumHeight(35)
        layout.addWidget(self.text_input)
        self.text_input.textChanged.connect(self._update_text_windows)

        # ===============================
        # SELEÇÃO DE MÍDIA
        # ===============================
        media_label = QLabel("📁 Selecionar Mídia:")
        media_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(media_label)

        media_layout = QHBoxLayout()
        media_layout.setSpacing(8)

        self.select_media_btn = QPushButton("📂 Procurar")
        self.select_media_btn.setObjectName("select_media_btn")
        self.select_media_btn.setFont(QFont("Segoe UI", 9))
        self.select_media_btn.setMinimumHeight(35)
        self.select_media_btn.clicked.connect(self.select_media)

        self.media_label = QLabel("Nenhuma mídia selecionada")
        self.media_label.setStyleSheet("color: #9e9e9e; font-size: 10px;")
        self.media_label.setFont(QFont("Segoe UI", 9))

        media_layout.addWidget(self.select_media_btn, 0)
        media_layout.addWidget(self.media_label, 1)

        layout.addLayout(media_layout)

        # ===============================
        # TELAS
        # ===============================
        screens_label = QLabel("📺 Telas de Saída:")
        screens_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        screens_label.setStyleSheet("color: #ffffff; margin-top: 8px;")
        layout.addWidget(screens_label)

        self.screens_list = QListWidget()
        self.screens_list.setFont(QFont("Segoe UI", 10))
        self.screens_list.setMinimumHeight(110)
        self.screens_list.setMaximumHeight(150)
        self.screens_list.setSpacing(2)
        for i in range(len(QApplication.screens())):
            item = QListWidgetItem(f"📺 Tela {i}")
            item.setCheckState(
                Qt.CheckState.Checked if i == 0 else Qt.CheckState.Unchecked
            )
            item.setFont(QFont("Segoe UI", 10))
            self.screens_list.addItem(item)

        layout.addWidget(self.screens_list)

        # ===============================
        # BOTÕES
        # ===============================
        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        self.start_btn = QPushButton("▶ ATIVAR BG")
        self.stop_btn = QPushButton("⛔ PARAR BG")

        self.start_btn.setObjectName("start_btn")
        self.stop_btn.setObjectName("stop_btn")

        self.start_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.stop_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        self.start_btn.setMinimumHeight(40)
        self.stop_btn.setMinimumHeight(40)

        self.start_btn.clicked.connect(self.start_background)
        self.stop_btn.clicked.connect(self.stop_background)

        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.stop_btn)

        layout.addLayout(buttons)

    # ===============================
    # BACKGROUND
    # ===============================
    def get_selected_screens(self):
        screens = []
        for i in range(self.screens_list.count()):
            if self.screens_list.item(i).checkState() == Qt.CheckState.Checked:
                screens.append(i)
        return screens if screens else [0]

    def start_background(self):
        screens = self.get_selected_screens()
        
        # Se o checkbox de relógio está ativado, usa __CLOCK__
        if self.clock_checkbox.isChecked():
            media = "__CLOCK__"
            print("🕐 Modo RELÓGIO ativado")
        # Se o checkbox de texto está ativado, usa __TEXT_ONLY__
        elif self.text_checkbox.isChecked():
            media = "__TEXT_ONLY__"
            print("📝 Modo TEXTO ativado")
        else:
            media = self.media_path
            # Valida se o arquivo de mídia existe
            if not media or not os.path.exists(media):
                print("⚠️ Erro: Nenhuma mídia selecionada ou arquivo não encontrado")
                return
            print(f"🎬 Reproduzindo vídeo: {os.path.basename(media)}")

        bg = getattr(self, "bg_thread", None)
        if bg and getattr(bg, 'isRunning', lambda: False)():
            print("🔁 BG já ativo")
            return

        self.bg_thread = BackgroundThread(media, screens)
        self.bg_thread.show_screen.connect(self.open_playback)
        self.bg_thread.start()
        print("🟢 Background iniciado")

    def stop_background(self):
        bg = getattr(self, "bg_thread", None)
        if bg is not None:
            try:
                if bg.isRunning():
                    bg.terminate()
            except Exception:
                pass
        # Force-close and fully release any active playback windows created by this controller
        try:
            for w in list(getattr(self, 'playback_windows', [])):
                try:
                    # stop any running timers on the playback window
                    if getattr(w, '_crossfade_timer', None):
                        try:
                            w._crossfade_timer.stop()
                        except Exception:
                            pass
                    if getattr(w, '_fade_timer', None):
                        try:
                            w._fade_timer.stop()
                        except Exception:
                            pass

                    # mark force close so PlaybackWindow allows final close
                    try:
                        w._force_close = True
                    except Exception:
                        pass

                    # stop media playback and lower volume
                    if getattr(w, 'player', None):
                        try:
                            w.player.stop()
                        except Exception:
                            pass
                    if getattr(w, 'audio', None):
                        try:
                            w.audio.setVolume(0.0)
                        except Exception:
                            pass

                    # hide and schedule deletion
                    try:
                        w.hide()
                    except Exception:
                        pass
                    try:
                        w.deleteLater()
                    except Exception:
                        pass

                except Exception:
                    pass

            # clear list
            self.playback_windows = []

            # Também fecha as janelas de texto
            for w in list(getattr(self, 'text_windows', [])):
                try:
                    w.hide()
                    w.deleteLater()
                except Exception:
                    pass
            self.text_windows = []

            # Também fecha as janelas de relógio
            for w in list(getattr(self, 'clock_windows', [])):
                try:
                    w.hide()
                    w.deleteLater()
                except Exception:
                    pass
            self.clock_windows = []

            # allow Qt to process pending deletions
            try:
                from PyQt6.QtWidgets import QApplication
                QApplication.processEvents()
            except Exception:
                pass
        except Exception:
            pass

        self.bg_thread = None
        print("⛔ Background parado")


    def select_logo(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar logo do relógio",
            "",
            "Imagens PNG (*.png);;Imagens (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        self.logo_path = file_path
        self.logo_status_label.setText(os.path.basename(file_path))

    def select_media(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar mídia de Background",
            "",
            "Mídia (*.mp4 *.avi *.mov *.mp3 *.wav *.jpg *.png)"
        )

        if not file_path:
            return

        self.media_path = file_path
        self.media_label.setText(os.path.basename(file_path))

    def open_playback(self, media, screen_index):
        try:
            # Se é modo relógio
            if media == "__CLOCK__":
                win = ClockBackgroundWindow(screen_index, logo_path=self.logo_path, logo_scale=self.logo_scale)
                if not hasattr(self, 'clock_windows'):
                    self.clock_windows = []
                self.clock_windows.append(win)
                print(f"✅ Janela de relógio aberta na tela {screen_index}")
            # Se é modo texto
            elif media == "__TEXT_ONLY__":
                win = TextBackgroundWindow(screen_index)
                # Conecta o sinal de mudança de texto
                if not hasattr(self, 'text_windows'):
                    self.text_windows = []
                self.text_windows.append(win)
                # Define o texto inicial
                self._update_text_windows()
                print(f"✅ Janela de texto aberta na tela {screen_index}")
            else:
                # Valida se o arquivo existe
                if not os.path.exists(media):
                    print(f"❌ Arquivo não encontrado: {media}")
                    return
                    
                # Modo normal com mídia (vídeo/áudio/imagem)
                win = PlaybackWindow(media, screen_index, loop=bool(self.loop_checkbox.isChecked()))
                win.finished.connect(lambda w=win: self._on_playback_finished(w))
                
                if not hasattr(self, 'playback_windows'):
                    self.playback_windows = []
                self.playback_windows.append(win)
                print(f"✅ Reprodução iniciada na tela {screen_index}: {os.path.basename(media)}")

            win.show()
        except Exception as e:
            print(f"❌ Erro ao abrir PlaybackWindow: {e}")
            import traceback
            traceback.print_exc()

    def _on_playback_finished(self, win):
        try:
            if hasattr(self, 'playback_windows') and win in self.playback_windows:
                self.playback_windows.remove(win)
        except Exception:
            pass

    def _on_loop_toggled(self, checked: bool):
        # Update loop state on all active playback windows
        if not hasattr(self, 'playback_windows'):
            return
        for w in list(self.playback_windows):
            try:
                w.loop = bool(checked)
            except Exception:
                pass

    def _update_text_windows(self):
        # Atualiza o texto em todas as janelas de texto abertas
        if not hasattr(self, 'text_windows'):
            return
        text = self.text_input.text()
        for w in list(self.text_windows):
            try:
                w.set_text(text)
            except Exception as e:
                print(f"Erro ao atualizar texto na janela: {e}")
    
    def increase_logo_size(self):
        """Aumenta o tamanho da logo em 10%."""
        self.logo_scale += 0.1
        self._update_logo_scale()
        print(f"🔺 Logo aumentada: {self.logo_scale:.1f}x")
    
    def decrease_logo_size(self):
        """Diminui o tamanho da logo em 10%."""
        self.logo_scale = max(0.1, self.logo_scale - 0.1)
        self._update_logo_scale()
        print(f"🔻 Logo diminuída: {self.logo_scale:.1f}x")
    
    def _update_logo_scale(self):
        """Atualiza a escala da logo em todas as janelas de relógio abertas."""
        if not hasattr(self, 'clock_windows'):
            return
        for w in list(self.clock_windows):
            try:
                w.set_logo_scale(self.logo_scale)
            except Exception as e:
                print(f"Erro ao atualizar escala da logo: {e}")

    def closeEvent(self, event):
        self.stop_background()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BackgroundController()
    win.show()
    sys.exit(app.exec())
