"""
Renderizador gráfico interactivo de la partitura y la lección en tiempo real.
Muestra el pentagrama (Clave de Sol / Fa), las notas esperadas y el cursor de avance.
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QFont, QPen, QBrush

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
        self.setRenderHint(Qt.RenderHint.Antialiasing)

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

            # Calcular posición Y aproximada según nota MIDI (Sol4 = 80, Do4 = 122)
            # Sol4(67) -> y = 80; Do4(60) -> y = 122 (7 semitonos * 6px)
            note_offset = (67 - note.midi_note) * 6
            y = staff_y_start + note_offset

            is_current = (idx == self._current_step)
            is_past = (idx < self._current_step)

            if is_current:
                brush = QBrush(QColor("#38bdf8"))  # Azul brillante para nota actual
                pen = QPen(QColor("#0284c7"), 2)
                # Anillo de resaltado
                self._scene.addEllipse(x - 4, y - 4, 22, 22, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine))
            elif is_past:
                brush = QBrush(QColor("#22c55e"))  # Verde para completadas
                pen = QPen(QColor("#15803d"), 1)
            else:
                brush = QBrush(QColor("#475569"))  # Gris para futuras
                pen = QPen(QColor("#334155"), 1)

            # Cabeza de la nota
            self._scene.addEllipse(x, y, 14, 14, pen, brush)

            # Digitación recomendada arriba de la nota
            finger_text = self._scene.addText(str(note.finger), QFont("Consolas", 11, QFont.Weight.Bold))
            finger_text.setDefaultTextColor(QColor("#38bdf8") if is_current else QColor("#94a3b8"))
            finger_text.setPos(x - 2, y - 28)

            # Nombre / Lírica de la nota abajo
            name_str = note.lyric or midi_to_note_name(note.midi_note)
            lyric_text = self._scene.addText(name_str, QFont("Segoe UI", 9))
            lyric_text.setDefaultTextColor(QColor("#cbd5e1") if is_current else QColor("#64748b"))
            lyric_text.setPos(x - 4, y + 18)
