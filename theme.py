# ===============================
# TEMA MODERNO UNIFICADO
# ===============================

MODERN_STYLESHEET = """
    QWidget {
        background-color: #1e1e2e;
        color: #ffffff;
        font-family: 'Segoe UI';
    }

    /* CHECKBOXES */
    QCheckBox {
        spacing: 8px;
        padding: 4px;
        color: #ffffff;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 3px;
        border: 2px solid #404060;
        background-color: #2a2a3e;
    }

    QCheckBox::indicator:hover {
        border: 2px solid #6c63ff;
        background-color: #3a3a4e;
    }

    QCheckBox::indicator:checked {
        background-color: #6c63ff;
        border: 2px solid #6c63ff;
        image: url(none);
    }

    QCheckBox::indicator:checked:hover {
        background-color: #7c73ff;
    }

    /* INPUT FIELDS */
    QLineEdit {
        padding: 8px 12px;
        border: 2px solid #404060;
        border-radius: 6px;
        background-color: #2a2a3e;
        color: #ffffff;
        selection-background-color: #6c63ff;
    }

    QLineEdit:focus {
        border: 2px solid #6c63ff;
        background-color: #323245;
    }

    QLineEdit::placeholder {
        color: #777788;
    }

    /* BOTÕES PRINCIPAIS */
    QPushButton {
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        color: #ffffff;
        background-color: #6c63ff;
    }

    QPushButton:hover {
        background-color: #7c73ff;
    }

    QPushButton:pressed {
        background-color: #5c53ef;
    }

    /* BOTÕES ESPECÍFICOS - GRID */
    QPushButton#gridBtn {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #3a3a4e,
            stop:1 #1f1f2e
        );
        border: 2px solid #404060;
        border-bottom: 4px solid #1a1a2e;
        border-right: 4px solid #1a1a2e;
        padding: 8px;
        color: #f5f5f5;
        font-weight: 600;
        font-size: 11px;
        border-radius: 8px;
    }

    QPushButton#gridBtn:hover {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #6c63ff,
            stop:1 #5c53ef
        );
        border: 2px solid #6c63ff;
        border-bottom: 4px solid #4c43df;
        border-right: 4px solid #4c43df;
    }

    QPushButton#gridBtn:pressed {
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #1f1f2e,
            stop:1 #3a3a4e
        );
        border: 2px solid #5c53ef;
        border-bottom: 2px solid #404060;
        border-right: 2px solid #404060;
        padding: 10px 6px 6px 10px;
    }

    /* BOTÃO PAUSE - ROXO */
    QPushButton#pauseBtn {
        background-color: #7b68ee;
        border: 2px solid #6c63ff;
        font-weight: bold;
    }

    QPushButton#pauseBtn:hover {
        background-color: #8b78ff;
    }

    QPushButton#pauseBtn:pressed {
        background-color: #6b58de;
    }

    /* BOTÃO LAST - VERDE */
    QPushButton#lastBtn {
        background-color: #2ecc71;
        border: 2px solid #27ae60;
        font-weight: bold;
    }

    QPushButton#lastBtn:hover {
        background-color: #3ed87d;
    }

    QPushButton#lastBtn:pressed {
        background-color: #27ae60;
    }

    /* BOTÃO CLOSE - VERMELHO */
    QPushButton#closeBtn {
        background-color: #e74c3c;
        border: 2px solid #c0392b;
        font-weight: bold;
    }

    QPushButton#closeBtn:hover {
        background-color: #ec7063;
    }

    QPushButton#closeBtn:pressed {
        background-color: #c0392b;
    }

    /* BOTÃO BACKGROUND - AZUL */
    QPushButton#bgBtn {
        background-color: #3498db;
        border: 2px solid #2980b9;
        font-weight: bold;
    }

    QPushButton#bgBtn:hover {
        background-color: #5dade2;
    }

    QPushButton#bgBtn:pressed {
        background-color: #2980b9;
    }

    /* BOTÃO START - VERDE */
    #start_btn {
        background-color: #2ecc71;
    }

    #start_btn:hover {
        background-color: #3ed87d;
    }

    #start_btn:pressed {
        background-color: #27ae60;
    }

    /* BOTÃO STOP - VERMELHO */
    #stop_btn {
        background-color: #e74c3c;
    }

    #stop_btn:hover {
        background-color: #ec7063;
    }

    #stop_btn:pressed {
        background-color: #c0392b;
    }

    /* BOTÃO SELECT - AZUL */
    #select_media_btn {
        background-color: #3498db;
    }

    #select_media_btn:hover {
        background-color: #5dade2;
    }

    #select_media_btn:pressed {
        background-color: #2980b9;
    }

    /* LISTAS */
    QListWidget {
        background-color: #2a2a3e;
        border: 2px solid #404060;
        border-radius: 6px;
        padding: 4px;
        outline: none;
    }

    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
        margin: 2px;
        background-color: #323245;
    }

    QListWidget::item:hover {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #3a3a4e,
            stop:1 #454560
        );
        border: 1px solid #6c63ff;
    }

    QListWidget::item:selected {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #6c63ff,
            stop:1 #7c73ff
        );
        color: #ffffff;
        border: 1px solid #5c53ef;
    }

    QListWidget::item:selected:hover {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #7c73ff,
            stop:1 #8c83ff
        );
    }

    /* Scrollbar */
    QListWidget::vertical {
        border-right: 2px solid #404060;
    }

    QScrollBar:vertical {
        background-color: #2a2a3e;
        width: 12px;
        border: none;
    }

    QScrollBar::handle:vertical {
        background-color: #6c63ff;
        border-radius: 6px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #7c73ff;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    /* LABELS */
    QLabel {
        color: #ffffff;
    }
"""

def get_stylesheet():
    """Retorna o stylesheet moderno unificado"""
    return MODERN_STYLESHEET
