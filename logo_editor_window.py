"""
Editor de Logo em Janela Flutuante (tipo vMix)
Janela separada que fica por cima do player fullscreen
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QSpinBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen


class LogoPreviewWidget(QWidget):
    """Preview simples da logo com edição interativa"""
    logo_moved = pyqtSignal(int, int)  # x, y
    logo_resized = pyqtSignal(int)  # size
    
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.logo_x = 10
        self.logo_y = 10
        self.logo_size = 150
        self.opacity = 0.8
        
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setStyleSheet("border: 2px solid #00ff00; background: #1a1a1a;")
        self.setMinimumSize(600, 350)
        
        print(f"✅ LogoPreviewWidget criado com pixmap: {pixmap.width()}x{pixmap.height()}")
    
    def paintEvent(self, event):
        """Renderiza preview da logo"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Background cinzento
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # Grid (linhas de referência)
        painter.setPen(QColor(60, 60, 60))
        for i in range(0, self.width(), 50):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height(), 50):
            painter.drawLine(0, i, self.width(), i)
        
        # Desenhar logo se existir
        if self.pixmap:
            # Redimensionar pixmap mantendo proporção
            scaled = self.pixmap.scaledToHeight(
                self.logo_size,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Desenhar com opacidade
            painter.setOpacity(self.opacity)
            painter.drawPixmap(self.logo_x, self.logo_y, scaled)
            
            # Desenhar borda e handles (sem opacidade)
            painter.setOpacity(1.0)
            painter.setPen(QPen(QColor(0, 255, 200), 2))
            painter.drawRect(self.logo_x, self.logo_y, scaled.width(), scaled.height())
            
            # Desenhar handles nos cantos
            handle_size = 8
            painter.fillRect(
                self.logo_x - handle_size//2, 
                self.logo_y - handle_size//2, 
                handle_size, handle_size, 
                QColor(0, 255, 0)
            )
            painter.fillRect(
                self.logo_x + scaled.width() - handle_size//2, 
                self.logo_y + scaled.height() - handle_size//2, 
                handle_size, handle_size, 
                QColor(255, 0, 0)
            )
            
            # Info
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(
                self.logo_x, 
                self.logo_y - 25, 
                f"Posição: ({self.logo_x}, {self.logo_y}) | Tamanho: {scaled.width()}x{scaled.height()}"
            )
        
        painter.end()
    
    def mousePressEvent(self, event):
        """Detecta clique na logo"""
        if self.pixmap and self._is_on_logo(event.pos()):
            self.dragging = True
            self.drag_start_x = event.pos().x()
            self.drag_start_y = event.pos().y()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
    
    def mouseMoveEvent(self, event):
        """Move ou redimensiona a logo"""
        if self.dragging and self.pixmap:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Redimensionar (Shift + Arrastar)
                dx = event.pos().x() - self.drag_start_x
                self.logo_size = max(50, self.logo_size + dx)
                self.drag_start_x = event.pos().x()
                self.logo_resized.emit(self.logo_size)
            else:
                # Mover (Arrastar simples)
                dx = event.pos().x() - self.drag_start_x
                dy = event.pos().y() - self.drag_start_y
                self.logo_x += dx
                self.logo_y += dy
                self.drag_start_x = event.pos().x()
                self.drag_start_y = event.pos().y()
                self.logo_moved.emit(self.logo_x, self.logo_y)
            
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Libera edição"""
        self.dragging = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)
    
    def _is_on_logo(self, pos):
        """Verifica se clicou na logo"""
        if not self.pixmap:
            return False
        
        scaled = self.pixmap.scaledToHeight(
            self.logo_size,
            Qt.TransformationMode.SmoothTransformation
        )
        return (self.logo_x <= pos.x() <= self.logo_x + scaled.width() and
                self.logo_y <= pos.y() <= self.logo_y + scaled.height())


class LogoEditorWindow(QMainWindow):
    """Janela flutuante para editar logo (fica por cima do player)"""
    config_changed = pyqtSignal(dict)
    
    def __init__(self, pixmap, config, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.config = config.copy()
        
        self.setWindowTitle("📐 Editor de Logo")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Preview
        self.preview = LogoPreviewWidget(pixmap)
        self.preview.logo_x = config.get("x", 10)
        self.preview.logo_y = config.get("y", 10)
        self.preview.logo_size = config.get("logo_size", 150)
        self.preview.opacity = config.get("logo_opacity", 0.8)
        self.preview.logo_moved.connect(self._on_logo_moved)
        self.preview.logo_resized.connect(self._on_logo_resized)
        layout.addWidget(self.preview)
        
        # Controls
        controls = QHBoxLayout()
        
        # Posição X
        controls.addWidget(QLabel("X:"))
        self.spin_x = QSpinBox()
        self.spin_x.setMinimum(0)
        self.spin_x.setMaximum(3840)
        self.spin_x.setValue(self.preview.logo_x)
        self.spin_x.valueChanged.connect(lambda v: setattr(self.preview, 'logo_x', v) or self.preview.update())
        controls.addWidget(self.spin_x)
        
        # Posição Y
        controls.addWidget(QLabel("Y:"))
        self.spin_y = QSpinBox()
        self.spin_y.setMinimum(0)
        self.spin_y.setMaximum(2160)
        self.spin_y.setValue(self.preview.logo_y)
        self.spin_y.valueChanged.connect(lambda v: setattr(self.preview, 'logo_y', v) or self.preview.update())
        controls.addWidget(self.spin_y)
        
        # Tamanho
        controls.addWidget(QLabel("Tamanho:"))
        self.spin_size = QSpinBox()
        self.spin_size.setMinimum(50)
        self.spin_size.setMaximum(400)
        self.spin_size.setValue(self.preview.logo_size)
        self.spin_size.valueChanged.connect(lambda v: setattr(self.preview, 'logo_size', v) or self.preview.update())
        controls.addWidget(self.spin_size)
        
        # Opacidade
        controls.addWidget(QLabel("Opacidade:"))
        self.slider_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_opacity.setMinimum(10)
        self.slider_opacity.setMaximum(100)
        self.slider_opacity.setValue(int(self.preview.opacity * 100))
        self.slider_opacity.valueChanged.connect(lambda v: setattr(self.preview, 'opacity', v / 100) or self.preview.update())
        controls.addWidget(self.slider_opacity)
        
        # Botões
        btn_save = QPushButton("✅ Salvar")
        btn_save.clicked.connect(self._on_save)
        controls.addWidget(btn_save)
        
        btn_cancel = QPushButton("❌ Cancelar")
        btn_cancel.clicked.connect(self.close)
        controls.addWidget(btn_cancel)
        
        layout.addLayout(controls)
    
    def _on_logo_moved(self, x, y):
        self.spin_x.setValue(x)
        self.spin_y.setValue(y)
    
    def _on_logo_resized(self, size):
        self.spin_size.setValue(size)
    
    def _on_save(self):
        config = {
            "logo_path": self.config.get("logo_path"),
            "x": self.preview.logo_x,
            "y": self.preview.logo_y,
            "logo_size": self.preview.logo_size,
            "logo_opacity": self.preview.opacity
        }
        self.config_changed.emit(config)
        print(f"✅ Logo salva: {config}")
        self.close()
