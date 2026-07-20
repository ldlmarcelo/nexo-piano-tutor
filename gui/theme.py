"""
Dark theme QSS para NEXO Piano Tutor.
Estética elegante con alto contraste para lectura clara de partituras.
"""

TUTOR_THEME = """
/* ── Base ─────────────────────────────────────── */
QMainWindow, QWidget {
    background-color: #121826;
    color: #e0e6ed;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

/* ── Grupos ───────────────────────────────────── */
QGroupBox {
    background-color: #1a2332;
    border: 1px solid #2d3b54;
    border-radius: 8px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: bold;
    font-size: 12px;
    color: #8fa0bd;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    color: #8fa0bd;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Headings ─────────────────────────────────── */
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #6366f1;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #64748b;
}

QLabel#feedbackLabel {
    font-size: 18px;
    font-weight: bold;
    font-family: "Consolas", monospace;
    qproperty-alignment: AlignCenter;
}

QLabel#fingerLabel {
    font-size: 32px;
    font-weight: bold;
    color: #38bdf8;
    font-family: "Consolas", monospace;
    qproperty-alignment: AlignCenter;
}

/* ── Partitura / Area de Render ──────────────── */
QGraphicsView#sheetView {
    background-color: #0f172a;
    border: 2px solid #1e293b;
    border-radius: 8px;
}

/* ── Botones ──────────────────────────────────── */
QPushButton {
    background-color: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: bold;
    font-size: 13px;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #818cf8;
}

QPushButton:pressed {
    background-color: #4f46e5;
}

QPushButton#resetBtn {
    background-color: #334155;
    color: #94a3b8;
}

QPushButton#resetBtn:hover {
    background-color: #475569;
    color: #ffffff;
}

/* ── Combos ───────────────────────────────────── */
QComboBox {
    background-color: #0f172a;
    border: 1px solid #2d3b54;
    border-radius: 6px;
    padding: 6px 12px;
    color: #e0e6ed;
    min-height: 28px;
}

QComboBox:hover {
    border-color: #6366f1;
}
"""
