"""
Renderizador gráfico interactivo de la partitura y la lección en tiempo real.
Muestra el pentagrama (Clave de Sol / Fa), las notas esperadas y el cursor de avance.
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainter

from core.lesson import Lesson, TargetNote

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(note: int) -> str:
    octave = (note // 12) - 1
    name = NOTE_NAMES[note % 12]
    return f"{name}{octave}"


class SheetView(QGraphicsView):
    """Vista gráfica interactiva de la lección y pentagrama."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sheetView")
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._lesson: Lesson = None
        self._current_step: int = 0

    def load_lesson(self, lesson: Lesson, step: int = 0):
        self._lesson = lesson
        self._current_step = step
        self.redraw()

    def set_step(self, step: int):
        self._current_step = step
        self.redraw()

    def redraw(self):
        self._scene.clear()
        if not self._lesson:
            return

        # Dibujar líneas del pentagrama (5 líneas)
        staff_y_start = 80
        line_spacing = 14
        width = max(500, len(self._lesson.notes) * 60 + 100)
        self._scene.setSceneRect(0, 0, width, 220)

        pen_staff = QPen(QColor("#334155"), 2)
        for i in range(5):
            y = staff_y_start + i * line_spacing
            self._scene.addLine(20, y, width - 20, y, pen_staff)

        # Clave / Título de la lección
        clef_text = self._scene.addText("🎼 Clave de Sol (Mano Derecha)", QFont("Segoe UI", 10, QFont.Weight.Bold))
        clef_text.setDefaultTextColor(QColor("#64748b"))
        clef_text.setPos(25, 20)

        # Dibujar notas de la lección
        x_start = 70
        x_step = 50

        for idx, note in enumerate(self._lesson.notes):
            x = x_start + idx * x_step

# Tabla diatónica: mapeo de nota MIDI a paso diatónico relativo a C4 (MIDI 60 = paso 0)
SEMITONE_TO_DIATONIC_STEP = {
    60: 0,   # C4 (Do) - Línea adicional inferior
    61: 0,   # C#4
    62: 1,   # D4 (Re) - Espacio bajo Línea 1
    63: 1,   # D#4
    64: 2,   # E4 (Mi) - Línea 1 (Inferior)
    65: 3,   # F4 (Fa) - Espacio 1
    66: 3,   # F#4
    67: 4,   # G4 (Sol) - Línea 2
    68: 4,   # G#4
    69: 5,   # A4 (La) - Espacio 2
    70: 5,   # A#4
    71: 6,   # B4 (Si) - Línea 3 (Central)
    72: 7,   # C5 (Do) - Espacio 3
    73: 7,   # C#5
    74: 8,   # D5 (Re) - Línea 4
    75: 8,   # D#5
    76: 9,   # E5 (Mi) - Espacio 4
    77: 10,  # F5 (Fa) - Línea 5 (Superior)
    78: 10,  # F#5
    79: 11,  # G5 (Sol) - Espacio sobre Línea 5
}


class SheetView(QGraphicsView):
    """Vista gráfica interactiva de la lección y pentagrama."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sheetView")
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._lesson: Lesson = None
        self._current_step: int = 0

    def load_lesson(self, lesson: Lesson, step: int = 0):
        self._lesson = lesson
        self._current_step = step
        self.redraw()

    def set_step(self, step: int):
        self._current_step = step
        self.redraw()

    def redraw(self):
        self._scene.clear()
        if not self._lesson:
            return

        # Dibujar líneas del pentagrama (5 líneas)
        # Línea 5 (F5) = 80, Línea 4 (D5) = 94, Línea 3 (B4) = 108, Línea 2 (G4) = 122, Línea 1 (E4) = 136
        staff_y_start = 80
        line_spacing = 14
        width = max(520, len(self._lesson.notes) * 55 + 110)
        self._scene.setSceneRect(0, 0, width, 220)

        pen_staff = QPen(QColor("#334155"), 2)
        for i in range(5):
            y = staff_y_start + i * line_spacing
            self._scene.addLine(20, y, width - 20, y, pen_staff)

        # Clave / Título de la lección
        clef_symbol = "🎼 Clave de Sol" if self._lesson.clef == "treble" else "𝄢 Clave de Fa"
        clef_text = self._scene.addText(f"{clef_symbol} — {self._lesson.title}", QFont("Segoe UI", 10, QFont.Weight.Bold))
        clef_text.setDefaultTextColor(QColor("#94a3b8"))
        clef_text.setPos(25, 18)

        # Dibujar notas de la lección
        x_start = 75
        x_step = 48

        # C4 está a Y = 150 (paso 0). Cada paso sube 7px (medio espacio)
        y_c4 = 150
        step_px = 7

        for idx, note in enumerate(self._lesson.notes):
            x = x_start + idx * x_step

            # Calcular posición Y diatónica exacta
            step_val = SEMITONE_TO_DIATONIC_STEP.get(note.midi_note, 0)
            y_note_center = y_c4 - (step_val * step_px)
            y_oval = y_note_center - 7  # Centrar el óvalo de 14px

            is_current = (idx == self._current_step)
            is_past = (idx < self._current_step)

            if is_current:
                brush = QBrush(QColor("#38bdf8"))  # Azul brillante para nota actual
                pen = QPen(QColor("#0284c7"), 2)
                # Anillo de resaltado
                self._scene.addEllipse(x - 4, y_oval - 4, 22, 22, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine))
            elif is_past:
                brush = QBrush(QColor("#22c55e"))  # Verde para completadas
                pen = QPen(QColor("#15803d"), 1)
            else:
                brush = QBrush(QColor("#475569"))  # Gris para futuras
                pen = QPen(QColor("#334155"), 1)

            # Dibujar línea adicional (Ledger Line) para Do4 (C4)
            if note.midi_note in (60, 61):
                pen_ledger = QPen(QColor("#64748b") if not is_current else QColor("#38bdf8"), 2)
                self._scene.addLine(x - 4, y_c4, x + 18, y_c4, pen_ledger)

            # Cabeza de la nota (óvalo estilizado de 14x14)
            self._scene.addEllipse(x, y_oval, 14, 14, pen, brush)

            # Digitación recomendada (1-5) arriba de la nota
            finger_text = self._scene.addText(str(note.finger), QFont("Consolas", 11, QFont.Weight.Bold))
            finger_text.setDefaultTextColor(QColor("#38bdf8") if is_current else QColor("#94a3b8"))
            finger_text.setPos(x - 2, y_oval - 28)

            # Nombre / Lírica de la nota abajo del pentagrama
            name_str = note.lyric or midi_to_note_name(note.midi_note)
            lyric_text = self._scene.addText(name_str, QFont("Segoe UI", 9, QFont.Weight.Bold if is_current else QFont.Weight.Normal))
            lyric_text.setDefaultTextColor(QColor("#38bdf8") if is_current else QColor("#64748b"))
            lyric_text.setPos(x - 4, 168)

