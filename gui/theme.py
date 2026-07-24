"""
Dark theme QSS para NEXO Piano Tutor (v1.2.0).
Estética elegante con alto contraste, bordes traslúcidos glassmorphic y botones icónicos.
"""

TUTOR_THEME = """
/* ── Base ─────────────────────────────────────── */
QMainWindow, QWidget {
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: "Segoe UI", "Inter", -apple-system, sans-serif;
    font-size: 13px;
}

/* ── Grupos ───────────────────────────────────── */
QGroupBox {
    background-color: #111827;
    border: 1px solid #1f293d;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px 10px 8px 10px;
    font-weight: bold;
    font-size: 11px;
    color: #94a3b8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    color: #38bdf8;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Headings ─────────────────────────────────── */
QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #38bdf8;
}

QLabel#subtitleLabel {
    font-size: 11px;
    color: #64748b;
}

QLabel#feedbackLabel {
    font-size: 16px;
    font-weight: bold;
    font-family: "Segoe UI", sans-serif;
    qproperty-alignment: AlignCenter;
}

QLabel#fingerLabel {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
    font-family: "Consolas", monospace;
    qproperty-alignment: AlignCenter;
}

/* ── Partitura / Area de Render ──────────────── */
QGraphicsView#sheetView {
    background-color: #080d1a;
    border: 1px solid #1e293b;
    border-radius: 8px;
}

/* ── Botones Genéricos y Icónicos ─────────────── */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 10px;
    font-weight: bold;
    font-size: 12px;
    min-height: 28px;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #0284c7;
}

QPushButton:pressed {
    background-color: #0f172a;
}

/* Botones de Transporte Icónicos (Play, Pause, Stop, Reset) */
QPushButton#transportPlayBtn {
    background-color: #0284c7;
    color: #ffffff;
    font-size: 15px;
    border: none;
    min-width: 44px;
    max-width: 44px;
    min-height: 32px;
}
QPushButton#transportPlayBtn:hover {
    background-color: #0369a1;
}

QPushButton#transportPauseBtn {
    background-color: #d97706;
    color: #ffffff;
    font-size: 15px;
    border: none;
    min-width: 44px;
    max-width: 44px;
    min-height: 32px;
}
QPushButton#transportPauseBtn:hover {
    background-color: #b45309;
}

QPushButton#transportStopBtn {
    background-color: #dc2626;
    color: #ffffff;
    font-size: 15px;
    border: none;
    min-width: 44px;
    max-width: 44px;
    min-height: 32px;
}
QPushButton#transportStopBtn:hover {
    background-color: #b91c1c;
}

QPushButton#transportIconBtn {
    background-color: #1e293b;
    color: #cbd5e1;
    font-size: 14px;
    border: 1px solid #334155;
    min-width: 40px;
    max-width: 40px;
    min-height: 32px;
}
QPushButton#transportIconBtn:hover {
    background-color: #334155;
    color: #ffffff;
    border-color: #0284c7;
}

/* ── Combos ───────────────────────────────────── */
QComboBox {
    background-color: #0f172a;
    border: 1px solid #2d3b54;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e0e6ed;
    min-height: 26px;
}

QComboBox:hover {
    border-color: #0284c7;
}

QSpinBox {
    background-color: #0f172a;
    color: #00e676;
    font-weight: bold;
    border: 1px solid #2d3b54;
    border-radius: 4px;
    padding: 2px 4px;
}
"""
