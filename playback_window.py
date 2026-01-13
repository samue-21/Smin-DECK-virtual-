import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl, QTimer, pyqtSignal, QRect
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtMultimedia import QMediaPlayer


# ===============================
# EDITOR DE LOGO (INTERATIVO)
# ===============================
class LogoEditorOverlay(QWidget):
    """Widget overlay para editar logo em tempo real (tipo vMix)"""
    logo_updated = pyqtSignal(dict)  # Emite config atualizada
    
    def __init__(self, parent, pixmap, config):
        super().__init__(parent)
        self.pixmap = pixmap
        self.config = config.copy()
        
        # Posição e tamanho iniciais
        self.logo_x = config.get("x", 10)
        self.logo_y = config.get("y", parent.height() - config.get("logo_size", 150) - 10)
        self.logo_width = pixmap.width()
        self.logo_height = pixmap.height()
        self.opacity = config.get("logo_opacity", 0.8)
        
        # Estado de edição
        self.dragging = False
        self.resizing = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # NÃO usar WA_TransparentForMouseEvents - precisa receber eventos!
        self.setStyleSheet("background: rgba(0, 0, 0, 50);")  # Semi-transparente para visualizar
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()
        
        print("✅ Editor de logo ativado - clique e arraste para mover")
    
    def paintEvent(self, event):
        """Desenha logo com handles para edição"""
        try:
            painter = QPainter(self)
            
            # Desenhar logo
            painter.setOpacity(self.opacity)
            painter.drawPixmap(self.logo_x, self.logo_y, self.logo_width, self.logo_height)
            
            # Desenhar handles (pequenos quadrados nos cantos e bordas)
            painter.setOpacity(1.0)
            painter.setPen(Qt.GlobalColor.white)
            painter.setBrush(QColor(0, 150, 255, 200))
            
            handle_size = 10
            # Canto superior esquerdo
            painter.drawRect(self.logo_x - handle_size//2, self.logo_y - handle_size//2, handle_size, handle_size)
            # Canto inferior direito
            painter.drawRect(self.logo_x + self.logo_width - handle_size//2, 
                            self.logo_y + self.logo_height - handle_size//2, handle_size, handle_size)
            
            # Info text
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(self.logo_x, self.logo_y - 20, 
                            f"Posição: ({self.logo_x}, {self.logo_y}) | Tamanho: {self.logo_width}x{self.logo_height}")
            painter.drawText(self.logo_x, self.height() - 20,
                            "Arrastar=Mover | Shift+Arrastar=Redimensionar | ENTER=Salvar | ESC=Cancelar")
            
            painter.end()
        except Exception as e:
            print(f"⚠️ Erro em paintEvent: {e}")
    
    def mousePressEvent(self, event):
        """Detecta clique na logo"""
        if self._is_on_logo(event.pos()):
            self.dragging = True
            self.drag_start_x = event.pos().x()
            self.drag_start_y = event.pos().y()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
    
    def mouseMoveEvent(self, event):
        """Move ou redimensiona a logo"""
        if self.dragging:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Redimensionar
                dx = event.pos().x() - self.drag_start_x
                dy = event.pos().y() - self.drag_start_y
                self.logo_width = max(50, self.logo_width + dx)
                self.logo_height = max(50, self.logo_height + dy)
                self.drag_start_x = event.pos().x()
                self.drag_start_y = event.pos().y()
            else:
                # Mover
                dx = event.pos().x() - self.drag_start_x
                dy = event.pos().y() - self.drag_start_y
                self.logo_x += dx
                self.logo_y += dy
                self.drag_start_x = event.pos().x()
                self.drag_start_y = event.pos().y()
            
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Libera edição"""
        self.dragging = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)
    
    def _is_on_logo(self, pos):
        """Verifica se clicou na logo"""
        return (self.logo_x <= pos.x() <= self.logo_x + self.logo_width and
                self.logo_y <= pos.y() <= self.logo_y + self.logo_height)
    
    def get_config(self):
        """Retorna config atualizada"""
        return {
            "logo_path": self.config.get("logo_path"),
            "logo_size": max(50, int(self.logo_height)),  # Usar altura como tamanho base
            "logo_opacity": self.opacity,
            "x": self.logo_x,
            "y": self.logo_y
        }


# ===============================
# LOGO OVERLAY WIDGET (SIMPLES - SEM EDIÇÃO)
# ===============================
class LogoOverlay(QWidget):
    """Widget overlay para renderizar a logo acima de tudo"""
    def __init__(self, parent, pixmap, x, y, opacity):
        super().__init__(parent)
        self.pixmap = pixmap
        self.x = x
        self.y = y
        self.opacity = opacity
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("background: transparent;")
    
    def paintEvent(self, event):
        try:
            if self.pixmap:
                painter = QPainter(self)
                painter.setOpacity(self.opacity)
                painter.drawPixmap(self.x, self.y, self.pixmap)
                painter.end()
        except Exception as e:
            print(f"⚠️ Erro em LogoOverlay.paintEvent: {e}")






class PlaybackWindow(QWidget):
    finished = pyqtSignal()  # 🔔 sinal de término (ON AIR / crossfade)

    def __init__(
        self,
        media_path,
        screen_index=1,
        fade_in_ms=800,
        fade_out_ms=600,
        loop=False,
        crossfade_ms=0,
        player_config=None
    ):
        super().__init__()

        self.setWindowTitle("Playback")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setStyleSheet("background-color: black;")
        
        # Fullscreen sem bordas
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.media_path = media_path
        self.ext = os.path.splitext(media_path)[1].lower()
        
        # Configurações do player (logo, etc)
        self.player_config = player_config or {}

        self.player = None
        self.audio = None

        self._is_closing = False
        self._fade_timer = None
        self._finished_emitted = False  # 🛡️ proteção
        self._force_close = False

        self.fade_in_ms = fade_in_ms
        self.fade_out_ms = fade_out_ms
        self.loop = bool(loop)
        self.crossfade_ms = int(crossfade_ms)
        self._crossfade_started = False
        self._crossfade_timer = None
        self._crossfade_steps = 20

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._overlay_label = QLabel(self)
        self._overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._overlay_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._overlay_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                font-size: 48px;
                font-weight: bold;
            }
        """)
        self._overlay_label.hide()
        
        # LOGO - NÃO será adicionada ao layout, será posicionada com move/resize
        self._logo_label = QLabel("", self)
        self._logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._logo_label.setStyleSheet("background: transparent;")
        self._logo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._logo_label.hide()  # Oculta até ser configurada

        # ===============================
        # MONITOR
        # ===============================
        screens = QApplication.screens()
        if 0 <= screen_index < len(screens):
            # Usa availableGeometry para pegar tamanho total da tela (sem barra de tarefas)
            # Depois sobrescreve com geometry para cobrir TUDO incluindo barra
            screen_geometry = screens[screen_index].geometry()
            self.setGeometry(
                screen_geometry.x(),
                screen_geometry.y(), 
                screen_geometry.width(),
                screen_geometry.height()
            )
        
        # ===============================
        # LOGO DO PLAYER (criar label sem adicioná-lo ao layout)
        # ===============================
        # Não adicionar ao layout - será posicionada manualmente com move/resize
        self._logo_label = QLabel(self)
        self._logo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self._logo_label.setStyleSheet("background: transparent;")
        # Importante: NÃO chamar self.layout.addWidget(self._logo_label)

        # ===============================
        # VÍDEO
        # ===============================
        if self.ext in (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"):
            self._init_video()

        # ===============================
        # ÁUDIO
        # ===============================
        elif self.ext in (".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma"):
            self._init_audio()

        # ===============================
        # IMAGEM
        # ===============================
        elif self.ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif", ".svg"):
            self._init_image()

        # ===============================
        # NÃO SUPORTADO
        # ===============================
        else:
            label = QLabel("Formato não suportado", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white; font-size: 22px;")
            self.layout.addWidget(label)

        self.showFullScreen()
        # Força raise após show para garantir visibilidade
        self.raise_()
        
        # Carregar logo DEPOIS que fullscreen é ativado
        self._load_player_logo()

    def _load_player_logo(self):
        """Carrega logo via editor interativo (apenas armazena configuração)
        
        A exibição da logo no fullscreen é limitada em PyQt6.
        Use o editor interativo para configurar posição e tamanho.
        """
        if not (self.player_config and self.player_config.get("logo_path")):
            if hasattr(self, '_logo_label'):
                self._logo_label.clear()
                self._logo_label.hide()
            return
        
        # Logo configuration is managed by the interactive editor
        # This method is kept for future enhancement or alternative display methods
    
    def keyPressEvent(self, event):
        """Detecta teclas - L abre modo editor de logo"""
        if event.isAutoRepeat():
            return
        
        if event.key() == Qt.Key.Key_L:
            self._enter_logo_editor_mode()
        elif event.key() == Qt.Key.Key_Return and hasattr(self, '_logo_editor') and self._logo_editor:
            config = self._logo_editor.get_config()
            self.player_config.update(config)
            self._logo_editor.deleteLater()
            self._logo_editor = None
        elif event.key() == Qt.Key.Key_Escape:
            if hasattr(self, '_logo_editor') and self._logo_editor:
                self._logo_editor.deleteLater()
                self._logo_editor = None
            else:
                self.close()
        else:
            super().keyPressEvent(event)
    
    def _enter_logo_editor_mode(self):
        """Abre editor de logo em janela flutuante separada"""
        if not (self.player_config and self.player_config.get("logo_path")):
            print("⚠️ Nenhuma logo configurada")
            return
        
        logo_path = self.player_config["logo_path"]
        if not os.path.exists(logo_path):
            print(f"⚠️ Logo não encontrada: {logo_path}")
            return
        
        try:
            logo_size = self.player_config.get("logo_size", 150)
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                print("⚠️ Logo inválida")
                return
            
            pixmap = pixmap.scaledToHeight(logo_size, Qt.TransformationMode.SmoothTransformation)
            
            # Importar a janela do editor
            from logo_editor_window import LogoEditorWindow
            
            # Criar e mostrar editor
            self._logo_editor_window = LogoEditorWindow(pixmap, self.player_config, parent=None)
            self._logo_editor_window.config_changed.connect(self._on_logo_config_changed)
            self._logo_editor_window.show()
            
            print("✅ Editor de logo aberto em janela flutuante")
            
        except Exception as e:
            print(f"⚠️ Erro ao abrir editor de logo: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_logo_config_changed(self, config):
        """Callback quando usuário salva config da logo"""
        self.player_config.update(config)
        print(f"✅ Config da logo atualizada: {config}")

    # ===============================
    # INIT VIDEO
    # ===============================
    def _init_video(self):

        from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)

        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)

        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)

        # If loop requested, use QMediaPlaylist for seamless looping
        if getattr(self, 'loop', False):
            try:
                from PyQt6.QtMultimedia import QMediaPlaylist
                playlist = QMediaPlaylist(self)
                playlist.addMedia(QUrl.fromLocalFile(self.media_path))
                playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
                try:
                    self.player.setPlaylist(playlist)
                except Exception:
                    # some PyQt builds may not expose setPlaylist; fallback
                    self.player.setSource(QUrl.fromLocalFile(self.media_path))
            except Exception:
                # fallback to direct source when QMediaPlaylist unavailable
                self.player.setSource(QUrl.fromLocalFile(self.media_path))
        else:
            self.player.setSource(QUrl.fromLocalFile(self.media_path))

        self.player.mediaStatusChanged.connect(self._on_media_status)
        # positionChanged loop handling not needed when using playlist
        self.player.positionChanged.connect(self._check_loop_position)
        self.player.durationChanged.connect(self._on_duration_changed)

        self._duration_ms = 0
        self._loop_guard = False
        # keep existing self.loop value (set from constructor)

        self.audio.setVolume(0.0)
        self.player.play()
        self.fade_in(self.fade_in_ms)

    # ===============================
    # INIT AUDIO
    # ===============================
    def _init_audio(self):

        from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
        label = QLabel("🎵 Reproduzindo áudio", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 26px;")
        self.layout.addWidget(label)

        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)

        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile(self.media_path))
        self.player.mediaStatusChanged.connect(self._on_media_status)

        self.audio.setVolume(0.0)
        self.player.play()
        self.fade_in(self.fade_in_ms)

    # ===============================
    # INIT IMAGE
    # ===============================
    def _init_image(self):
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.pixmap = QPixmap(self.media_path)
        self._update_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "pixmap"):
            self._update_image()

    def _update_image(self):
        self.image_label.setPixmap(
            self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    # ===============================
    # TEXTO OVERLAY
    # ===============================
    def set_overlay_text(self, text: str):
        if text:
            self._overlay_label.setText(text)
            self._overlay_label.show()
            self._overlay_label.raise_()
        else:
            self._overlay_label.hide()

    def set_black_background(self):
        self.setStyleSheet("background-color: black;")

    # ===============================
    # CONTROLES
    # ===============================
    def pause(self):
        if self.player:
            self.player.pause()

    def close_playback(self):
        self.fade_out_and_close(self.fade_out_ms)

    def stop_playback_smooth(self):
        """Para a reprodução e esconde a janela suavemente (sem fechar)"""
        if self.player:
            try:
                self.player.stop()
            except Exception:
                pass
        self.hide()

    def crossfade_out(self, duration_ms=600):
        """Faz fade out de opacidade da janela"""
        from PyQt6.QtCore import QPropertyAnimation
        self._opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self._opacity_anim.setDuration(duration_ms)
        self._opacity_anim.setStartValue(1.0)
        self._opacity_anim.setEndValue(0.0)
        self._opacity_anim.finished.connect(self.hide)
        self._opacity_anim.start()

    def crossfade_in(self, duration_ms=600):
        """Faz fade in de opacidade da janela"""
        from PyQt6.QtCore import QPropertyAnimation
        self.setWindowOpacity(0.0)
        self._opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self._opacity_anim.setDuration(duration_ms)
        self._opacity_anim.setStartValue(0.0)
        self._opacity_anim.setEndValue(1.0)
        self._opacity_anim.start()

    # ===============================
    # FADE IN
    # ===============================
    def fade_in(self, duration_ms=800, target_volume=1.0):
        if not self.audio:
            return

        steps = 20
        interval = max(10, duration_ms // steps)
        delta = target_volume / steps

        if self._fade_timer:
            self._fade_timer.stop()

        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(
            lambda: self._fade_in_step(delta, target_volume)
        )
        self._fade_timer.start(interval)

    def _fade_in_step(self, delta, target):
        vol = self.audio.volume() + delta
        if vol >= target:
            self.audio.setVolume(target)
            self._fade_timer.stop()
            return
        self.audio.setVolume(vol)

    # ===============================
    # FADE OUT
    # ===============================
    def fade_out_and_close(self, duration_ms=600):
        if self._is_closing:
            return

        self._is_closing = True

        if not self.audio:
            self._final_close()
            return

        steps = 20
        interval = max(10, duration_ms // steps)
        delta = self.audio.volume() / steps

        if self._fade_timer:
            self._fade_timer.stop()

        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(
            lambda: self._fade_out_step(delta)
        )
        self._fade_timer.start(interval)

    def _fade_out_step(self, delta):
        vol = self.audio.volume() - delta
        if vol <= 0.01:
            self.audio.setVolume(0.0)
            self._fade_timer.stop()
            self._final_close()
            return
        self.audio.setVolume(vol)

    # ===============================
    # FINAL CLOSE
    # ===============================
    def _final_close(self):
        # If loop is active and not being force-closed, ignore final close
        if self.loop and not getattr(self, '_force_close', False):
            return

        if self._finished_emitted:
            return

        self._finished_emitted = True

        if self.player:
            try:
                self.player.stop()
            except Exception:
                pass

        try:
            self.finished.emit()
        except Exception:
            pass

        try:
            self.hide()
        except Exception:
            pass

        try:
            self.deleteLater()
        except Exception:
            pass

        # reset force flag
        self._force_close = False

    def closeEvent(self, event):
        # Prevent accidental window close when in loop mode unless forced
        if self.loop and not getattr(self, '_force_close', False):
            event.ignore()
            return
        super().closeEvent(event)

    # ===============================
    # FIM NATURAL DA MÍDIA
    # ===============================
    def _on_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # If loop is enabled but crossfade wasn't started for some reason,
            # restart playback normally. If not looping, close.
            if self.loop and not getattr(self, '_crossfade_started', False):
                try:
                    self.player.setPosition(0)
                    self.player.play()
                except Exception:
                    pass
            elif not self.loop:
                self.close()

    def _on_duration_changed(self, duration):
        self._duration_ms = duration

    def _check_loop_position(self, position):
        if not self.loop:
            return
        if self._duration_ms <= 0:
            return

        # If we are within crossfade window, start crossfade once
        if (getattr(self, 'crossfade_ms', 0) > 0 and
                position >= self._duration_ms - getattr(self, 'crossfade_ms', 0) and
                not getattr(self, '_crossfade_started', False)):
            self._crossfade_started = True
            self._start_crossfade()

        # Legacy loop guard fallback (short gap)
        if position >= self._duration_ms - 80 and not self._loop_guard and not getattr(self, '_crossfade_started', False):
            self._loop_guard = True
            try:
                # seek a few milliseconds into the file to reduce black-frame on some backends
                self.player.setPosition(10)
                self.player.play()
            except Exception:
                pass
            QTimer.singleShot(100, self._reset_loop_guard)

    def _reset_loop_guard(self):
        self._loop_guard = False

    # ===============================
    # CROSSFADE
    # ===============================
    def _start_crossfade(self):
        try:
            if not self.player or getattr(self, '_duration_ms', 0) <= 0:
                self._crossfade_started = False
                return

            # create next player and audio
            from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
            from PyQt6.QtMultimediaWidgets import QVideoWidget

            self._next_video_widget = None
            if hasattr(self, 'video_widget'):
                self._next_video_widget = QVideoWidget(self)
                # match geometry
                self._next_video_widget.setGeometry(self.video_widget.geometry())
                self._next_video_widget.show()
                self._next_video_widget.raise_()
                # apply opacity effects
                self._next_opacity = QGraphicsOpacityEffect(self._next_video_widget)
                self._next_opacity.setOpacity(0.0)
                self._next_video_widget.setGraphicsEffect(self._next_opacity)

                # ensure current has opacity effect
                if not hasattr(self, '_curr_opacity'):
                    self._curr_opacity = QGraphicsOpacityEffect(self.video_widget)
                    self._curr_opacity.setOpacity(1.0)
                    self.video_widget.setGraphicsEffect(self._curr_opacity)

            self._next_player = QMediaPlayer(self)
            self._next_audio = QAudioOutput(self)
            self._next_player.setAudioOutput(self._next_audio)

            if self._next_video_widget:
                self._next_player.setVideoOutput(self._next_video_widget)

            self._next_player.setSource(QUrl.fromLocalFile(self.media_path))
            self._next_audio.setVolume(0.0)
            self._next_player.play()

            # prepare crossfade timing
            steps = max(6, getattr(self, '_crossfade_steps', 20))
            interval = max(10, int(getattr(self, 'crossfade_ms', 600) // steps))
            self._crossfade_step_index = 0
            self._crossfade_steps = steps
            self._crossfade_interval = interval

            # store original target volume
            target_vol = 1.0

            # start timer
            if getattr(self, '_crossfade_timer', None):
                try:
                    self._crossfade_timer.stop()
                except Exception:
                    pass

            self._crossfade_timer = QTimer(self)
            self._crossfade_timer.timeout.connect(lambda: self._crossfade_step(target_vol))
            self._crossfade_timer.start(self._crossfade_interval)

        except Exception as e:
            print("Erro no crossfade:", e)
            self._crossfade_started = False

    def _crossfade_step(self, target_vol):
        try:
            i = getattr(self, '_crossfade_step_index', 0)
            steps = getattr(self, '_crossfade_steps', 20)

            # calc volumes
            next_vol = (i + 1) / steps * target_vol
            curr_vol = max(0.0, (1.0 - (i + 1) / steps) * target_vol)

            if hasattr(self, '_next_audio') and self._next_audio:
                try:
                    self._next_audio.setVolume(next_vol)
                except Exception:
                    pass

            if hasattr(self, 'audio') and self.audio:
                try:
                    self.audio.setVolume(curr_vol)
                except Exception:
                    pass

            # update opacities for video crossfade
            if hasattr(self, '_next_opacity') and getattr(self, '_next_opacity', None) and hasattr(self, '_curr_opacity') and getattr(self, '_curr_opacity', None):
                try:
                    self._next_opacity.setOpacity((i + 1) / steps)
                    self._curr_opacity.setOpacity(max(0.0, 1.0 - (i + 1) / steps))
                except Exception:
                    pass

            self._crossfade_step_index = i + 1

            if self._crossfade_step_index >= steps:
                # finish crossfade: stop old player and swap
                try:
                    if self.player:
                        self.player.stop()
                except Exception:
                    pass

                # remove old video widget visually (hide) but don't force delete
                try:
                    if hasattr(self, 'video_widget') and self.video_widget:
                        try:
                            self.video_widget.hide()
                        except Exception:
                            pass
                except Exception:
                    pass

                # promote next to current
                try:
                    self.player = self._next_player
                    self.audio = self._next_audio
                    if hasattr(self, '_next_video_widget') and self._next_video_widget:
                        self.video_widget = self._next_video_widget
                    # reconnect signals
                    try:
                        self.player.mediaStatusChanged.connect(self._on_media_status)
                        self.player.positionChanged.connect(self._check_loop_position)
                        self.player.durationChanged.connect(self._on_duration_changed)
                    except Exception:
                        pass
                except Exception:
                    pass

                # cleanup
                try:
                    if getattr(self, '_crossfade_timer', None):
                        self._crossfade_timer.stop()
                except Exception:
                    pass

                self._crossfade_started = False
                self._crossfade_timer = None
                self._crossfade_step_index = 0
        except Exception as e:
            print("Erro no passo do crossfade:", e)
