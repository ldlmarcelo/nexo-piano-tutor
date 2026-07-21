"""
Renderizador gráfico interactivo de la partitura y la lección en tiempo real.
Muestra el pentagrama (Clave de Sol / Fa), el signo de clave estándar,
las notas en sus posiciones diatónicas exactas y el cursor de avance.
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainter

from core.lesson import Lesson

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Mapeo de semitono (0..11) a paso diatónico en la octava (C=0, D=1, E=2, F=3, G=4, A=5, B=6)
SEMITONE_TO_DIATONIC_IN_OCTAVE = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]


def midi_to_note_name(note: int) -> str:
    octave = (note // 12) - 1
    name = NOTE_NAMES[note % 12]
    return f"{name}{octave}"


def midi_to_diatonic_step(note: int) -> int:
    """Devuelve el índice diatónico absoluto de una nota MIDI (C0 = paso 0, C4 = paso 28)."""
    octave = (note // 12) - 1
    semitone = note % 12
    diatonic_in_octave = SEMITONE_TO_DIATONIC_IN_OCTAVE[semitone]
    return octave * 7 + diatonic_in_octave


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

        # Geometría del pentagrama
        # 5 líneas: Línea 5 (80), Línea 4 (94), Línea 3 (108), Línea 2 (122), Línea 1 (136)
        staff_y_start = 80
        line_spacing = 14
        half_spacing = line_spacing / 2  # 7px por paso diatónico

        width = max(560, len(self._lesson.notes) * 52 + 130)
        self._scene.setSceneRect(0, 0, width, 220)

        # 1. Dibujar las 5 líneas principales del pentagrama
        pen_staff = QPen(QColor("#475569"), 2)
        for i in range(5):
            y = staff_y_start + i * line_spacing
            self._scene.addLine(20, y, width - 20, y, pen_staff)

        # 2. Dibujar el Signo de Clave sobre el pentagrama
        is_treble = (self._lesson.clef == "treble")
        clef_symbol = "𝄞" if is_treble else "𝄢"
        
        # Intentar renderizar la clave musical con fuente rica
        clef_font = QFont("Segoe UI Symbol", 36 if is_treble else 30, QFont.Weight.Bold)
        clef_item = self._scene.addText(clef_symbol, clef_font)
        clef_item.setDefaultTextColor(QColor("#38bdf8"))
        
        # Ajuste Físico de Posición de Clave en el Pentagrama:
        # Clave de Sol rodea Línea 2 (y=122). Clave de Fa los puntos rodean Línea 4 (y=94).
        if is_treble:
            clef_item.setPos(22, 60)
        else:
            clef_item.setPos(22, 70)

        # Título de la lección y clave
        clef_title = "Clave de Sol (Mano Derecha)" if is_treble else "Clave de Fa (Mano Izquierda)"
        title_text = self._scene.addText(f"{clef_title} — {self._lesson.title}", QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_text.setDefaultTextColor(QColor("#94a3b8"))
        title_text.setPos(75, 18)

        # 3. Dibujar notas musicales de la lección
        x_start = 95
        x_step = 48

        for idx, note in enumerate(self._lesson.notes):
            x = x_start + idx * x_step
            diatonic_val = midi_to_diatonic_step(note.midi_note)

            # Cálculo de Y según la Clave:
            # En Clave de Sol: Sol4 (67, diatónico 32) está en Línea 2 (y = 122)
            # En Clave de Fa: Fa3 (53, diatónico 24) está en Línea 4 (y = 94)
            if is_treble:
                y_center = 122 - (diatonic_val - 32) * half_spacing
            else:
                y_center = 94 - (diatonic_val - 24) * half_spacing

            y_oval = y_center - 7  # Centrar óvalo de 14px

            is_current = (idx == self._current_step)
            is_past = (idx < self._current_step)

            if is_current:
                brush = QBrush(QColor("#38bdf8"))  # Azul cian brillante para nota activa
                pen = QPen(QColor("#0284c7"), 2)
                # Anillo pulsante alrededor de la nota activa
                self._scene.addEllipse(x - 4, y_oval - 4, 22, 22, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine))
            elif is_past:
                brush = QBrush(QColor("#22c55e"))  # Verde para completadas
                pen = QPen(QColor("#15803d"), 1)
            else:
                brush = QBrush(QColor("#64748b"))  # Gris para futuras
                pen = QPen(QColor("#334155"), 1)

            # 4. Líneas Adicionales (Ledger Lines)
            # Línea 1 inferior = 136. Si y_center >= 150, se requiere línea adicional inferior.
            # Línea 5 superior = 80. Si y_center <= 66, se requiere línea adicional superior.
            if y_center >= 150:
                # Líneas adicionales inferiores (ej. Do4 en Clave de Sol a y=150)
                y_ledger = 150
                while y_ledger <= y_center:
                    pen_ledger = QPen(QColor("#38bdf8") if is_current else QColor("#64748b"), 2)
                    self._scene.addLine(x - 5, y_ledger, x + 19, y_ledger, pen_ledger)
                    y_ledger += 14
            elif y_center <= 66:
                # Líneas adicionales superiores (ej. Do4 en Clave de Fa a y=66)
                y_ledger = 66
                while y_ledger >= y_center:
                    pen_ledger = QPen(QColor("#38bdf8") if is_current else QColor("#64748b"), 2)
                    self._scene.addLine(x - 5, y_ledger, x + 19, y_ledger, pen_ledger)
                    y_ledger -= 14

            # Cabeza de la nota (óvalo estilizado 14x14)
            self._scene.addEllipse(x, y_oval, 14, 14, pen, brush)

            # Digitación (1 al 5) arriba de la nota
            finger_text = self._scene.addText(str(note.finger), QFont("Consolas", 11, QFont.Weight.Bold))
            finger_text.setDefaultTextColor(QColor("#38bdf8") if is_current else QColor("#94a3b8"))
            finger_text.setPos(x - 2, y_oval - 28)

            # Nombre / Lírica abajo de la partitura
            name_str = note.lyric or midi_to_note_name(note.midi_note)
            lyric_text = self._scene.addText(name_str, QFont("Segoe UI", 9, QFont.Weight.Bold if is_current else QFont.Weight.Normal))
            lyric_text.setDefaultTextColor(QColor("#38bdf8") if is_current else QColor("#64748b"))
            lyric_text.setPos(x - 4, 172)
