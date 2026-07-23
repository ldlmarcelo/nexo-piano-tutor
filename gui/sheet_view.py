"""
Renderizador gráfico interactivo de la partitura y la lección en tiempo real.
Muestra el pentagrama (Clave de Sol / Fa), signo de clave, métrica de compás (4/4, 3/4),
figuras rítmicas (redondas, blancas, negras, corchetes), plicas, líneas divisoras de compás,
digitación (1-5 por mano) y cursor de avance en tiempo real.
"""

from typing import Any, Dict
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
    """Vista gráfica interactiva de la lección con notación musical rítmica completa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sheetView")
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Desactivar barras de desplazamiento manuales (Auto-seguimiento dinámico)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self._lesson: Lesson = None
        self._current_step: int = 0
        self._range_start: int = 0
        self._range_end: int = -1
        self._error_steps: set[int] = set()
        self._note_results: dict[int, Any] = {}

    def set_error_steps(self, error_steps: set[int]):
        self._error_steps = set(error_steps)
        self.redraw()

    def set_note_results(self, note_results: dict[int, Any]):
        self._note_results = dict(note_results)
        self.redraw()

    def load_lesson(self, lesson: Lesson, step: int = 0):
        self._lesson = lesson
        self._current_step = step
        self._range_start = 0
        self._range_end = len(lesson.notes) - 1 if lesson and lesson.notes else -1
        self._error_steps.clear()
        self._note_results.clear()
        self.redraw()
        self.center_on_active_step()

    def set_range(self, start_step: int, end_step: int):
        self._range_start = start_step
        self._range_end = end_step
        self.redraw()
        self.center_on_active_step()

    def set_step(self, step: int):
        self._current_step = step
        self.redraw()
        self.center_on_active_step()

    def center_on_active_step(self):
        """Centra automáticamente la vista sobre la nota activa para evitar scroll manual."""
        if not self._lesson or not self._lesson.notes:
            return
        x_start = 135
        x_step = 54
        x_active = x_start + self._current_step * x_step
        self.centerOn(x_active, 110)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.center_on_active_step()

    def redraw(self):
        self._scene.clear()
        if not self._lesson:
            return

        # Geometría del pentagrama (5 líneas)
        # Línea 5 (80), Línea 4 (94), Línea 3 (108 - centro), Línea 2 (122), Línea 1 (136)
        staff_y_start = 80
        line_spacing = 14
        staff_y_end = staff_y_start + 4 * line_spacing  # 136
        half_spacing = line_spacing / 2  # 7px por paso diatónico

        # Métrica / Compás (ej: "4/4" -> 4 tiempos de negra por compás)
        ts_str = getattr(self._lesson, "time_signature", "4/4")
        try:
            ts_num, ts_den = map(int, ts_str.split("/"))
        except Exception:
            ts_num, ts_den = 4, 4

        beats_per_measure = float(ts_num)

        # Ancho adaptable de escena
        x_start = 135  # Espacio tras clave + métrica
        x_step = 54
        width = max(600, len(self._lesson.notes) * x_step + x_start + 60)
        self._scene.setSceneRect(0, 0, width, 220)

        # 1. Dibujar las 5 líneas principales del pentagrama
        pen_staff = QPen(QColor("#475569"), 2)
        for i in range(5):
            y = staff_y_start + i * line_spacing
            self._scene.addLine(20, y, width - 20, y, pen_staff)

        # 2. Dibujar el Signo de Clave sobre el pentagrama
        is_treble = (self._lesson.clef == "treble")
        clef_symbol = "𝄞" if is_treble else "𝄢"
        clef_font = QFont("Segoe UI Symbol", 36 if is_treble else 30, QFont.Weight.Bold)
        clef_item = self._scene.addText(clef_symbol, clef_font)
        clef_item.setDefaultTextColor(QColor("#38bdf8"))
        clef_item.setPos(22, 60 if is_treble else 70)

        # 3. Dibujar la Métrica de Compás (Time Signature e.g. 4/4, 3/4)
        ts_font = QFont("Segoe UI", 13, QFont.Weight.Bold)
        
        num_item = self._scene.addText(str(ts_num), ts_font)
        num_item.setDefaultTextColor(QColor("#0284c7"))
        num_item.setPos(72, 75)

        den_item = self._scene.addText(str(ts_den), ts_font)
        den_item.setDefaultTextColor(QColor("#0284c7"))
        den_item.setPos(72, 103)

        # Título de la lección y clave
        clef_title = "Clave de Sol (Mano Derecha)" if is_treble else "Clave de Fa (Mano Izquierda)"
        title_text = self._scene.addText(f"{clef_title} — {self._lesson.title} [{ts_str}]", QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_text.setDefaultTextColor(QColor("#94a3b8"))
        title_text.setPos(75, 18)

        # Dibujar Cuadro Traslúcido de Rango Seleccionado A-B
        total_notes = len(self._lesson.notes)
        if 0 <= self._range_start <= self._range_end < total_notes:
            if not (self._range_start == 0 and self._range_end == total_notes - 1):
                x_a = x_start + self._range_start * x_step - 8
                x_b = x_start + self._range_end * x_step + 22
                w_box = x_b - x_a
                self._scene.addRect(x_a, 40, w_box, 140, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine), QBrush(QColor(56, 189, 248, 30)))
                t_a = self._scene.addText("[A]", QFont("Consolas", 10, QFont.Weight.Bold))
                t_a.setDefaultTextColor(QColor("#38bdf8"))
                t_a.setPos(x_a - 4, 38)
                t_b = self._scene.addText("[B]", QFont("Consolas", 10, QFont.Weight.Bold))
                t_b.setDefaultTextColor(QColor("#38bdf8"))
                t_b.setPos(x_b - 16, 38)

        # 4. Dibujar notas musicales y líneas divisoras de compás
        cumulative_beats = 0.0
        pen_barline = QPen(QColor("#64748b"), 2)

        for idx, note in enumerate(self._lesson.notes):
            x = x_start + idx * x_step
            diatonic_val = midi_to_diatonic_step(note.midi_note)

            # En Clave de Sol: Sol4 (67, diatónico 32) en Línea 2 (y = 122)
            # En Clave de Fa: Fa3 (53, diatónico 24) en Línea 4 (y = 94)
            if is_treble:
                y_center = 122 - (diatonic_val - 32) * half_spacing
            else:
                y_center = 94 - (diatonic_val - 24) * half_spacing

            y_oval = y_center - 7  # Centrar óvalo de 14px

            is_current = (idx == self._current_step)
            is_past = (idx < self._current_step)

            has_error = (idx in self._error_steps)
            note_res = self._note_results.get(idx)
            status_key = getattr(note_res, "status", None) if note_res else None

            # Colores e indicadores de estado rítmico/tonal
            if status_key == "EARLY":
                color_note = QColor("#ef4444")  # Rojo carmesí para golpe adelantado
                pen_note = QPen(QColor("#b91c1c"), 2)
                # Flecha + X a la izquierda indicando que tocó antes del pulso
                badge = self._scene.addText("🡠 ✗", QFont("Segoe UI", 9, QFont.Weight.Bold))
                badge.setDefaultTextColor(QColor("#ef4444"))
                badge.setPos(x - 14, 24)
            elif status_key == "LATE":
                color_note = QColor("#ef4444")  # Rojo carmesí para golpe retrasado
                pen_note = QPen(QColor("#b91c1c"), 2)
                # X + Flecha a la derecha indicando que tocó después del pulso
                badge = self._scene.addText("✗ 🡢", QFont("Segoe UI", 9, QFont.Weight.Bold))
                badge.setDefaultTextColor(QColor("#ef4444"))
                badge.setPos(x + 10, 24)
            elif status_key == "WRONG_NOTE" or (is_current and has_error):
                color_note = QColor("#ef4444")  # Rojo carmesí para nota equivocada
                pen_note = QPen(QColor("#b91c1c"), 2)
                if is_current:
                    self._scene.addEllipse(x - 5, y_oval - 5, 24, 24, QPen(QColor("#ef4444"), 2, Qt.PenStyle.DashLine), QBrush(QColor(239, 68, 68, 50)))
                cross_item = self._scene.addText("✗", QFont("Segoe UI", 10, QFont.Weight.Bold))
                cross_item.setDefaultTextColor(QColor("#ef4444"))
                cross_item.setPos(x, 24)
            elif is_current:
                color_note = QColor("#38bdf8")  # Azul cian brillante para nota activa
                pen_note = QPen(QColor("#0284c7"), 2)
                self._scene.addEllipse(x - 5, y_oval - 5, 24, 24, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine), QBrush(QColor(56, 189, 248, 40)))
            elif is_past:
                if has_error:
                    color_note = QColor("#f59e0b")  # Ámbar para notas corregidas tras error
                    pen_note = QPen(QColor("#d97706"), 2)
                    check_item = self._scene.addText("✓", QFont("Segoe UI", 9, QFont.Weight.Bold))
                    check_item.setDefaultTextColor(QColor("#f59e0b"))
                    check_item.setPos(x, 26)
                else:
                    color_note = QColor("#22c55e")  # Verde esmeralda para completadas impecables
                    pen_note = QPen(QColor("#16a34a"), 2)
                    check_item = self._scene.addText("✓", QFont("Segoe UI", 9, QFont.Weight.Bold))
                    check_item.setDefaultTextColor(QColor("#22c55e"))
                    check_item.setPos(x, 26)
            else:
                color_note = QColor("#94a3b8")  # Gris claro para futuras
                pen_note = QPen(QColor("#475569"), 1)

            # Relleno y trazo de cabeza de nota según duración (Redonda/Blanca = contorno nítido 2px)
            duration = getattr(note, "duration_quarter", 1.0)
            is_hollow = (duration >= 2.0)
            if is_hollow:
                if is_past:
                    pen_note = QPen(QColor("#22c55e") if not has_error else QColor("#f59e0b"), 2)
                    brush_note = QBrush(QColor(34, 197, 94, 120) if not has_error else QColor(245, 158, 11, 120))
                elif is_current:
                    pen_note = QPen(QColor("#ef4444") if has_error else QColor("#38bdf8"), 2)
                    brush_note = QBrush(QColor(239, 68, 68, 120) if has_error else QColor(56, 189, 248, 120))
                else:
                    pen_note = QPen(QColor("#e2e8f0"), 2)  # Contorno nítido gris plateado de 2px
                    brush_note = QBrush(QColor("#0f172a"))  # Fondo oscuro para contraste impecable
            else:
                brush_note = QBrush(color_note)

            # A. Líneas Adicionales (Ledger Lines)
            if y_center >= 150:
                y_ledger = 150
                while y_ledger <= y_center:
                    pen_ledger = QPen(QColor("#38bdf8") if is_current else (QColor("#22c55e") if is_past else QColor("#64748b")), 2)
                    self._scene.addLine(x - 5, y_ledger, x + 19, y_ledger, pen_ledger)
                    y_ledger += 14
            elif y_center <= 66:
                y_ledger = 66
                while y_ledger >= y_center:
                    pen_ledger = QPen(QColor("#38bdf8") if is_current else (QColor("#22c55e") if is_past else QColor("#64748b")), 2)
                    self._scene.addLine(x - 5, y_ledger, x + 19, y_ledger, pen_ledger)
                    y_ledger -= 14

            # B. Cabeza de la nota (Óvalo nítido 15x13 para blanca, 16x12 para redonda, 14x14 para negra)
            if duration >= 4.0:
                self._scene.addEllipse(x - 1, y_oval + 1, 16, 12, pen_note, brush_note)
            else:
                self._scene.addEllipse(x, y_oval, 14, 14, pen_note, brush_note)

            # C. Plica (Stem) y Corchete (Flag)
            # Redonda (>= 4.0 tiempos) no lleva plica
            if duration < 4.0:
                # Dirección de plica: Hacia arriba si nota está abajo de Línea 3 (y > 108), abajo si y <= 108
                stem_up = (y_center > 108)
                pen_stem = QPen(color_note, 2)

                if stem_up:
                    stem_x = x + 13
                    stem_y1 = y_center
                    stem_y2 = y_center - 32
                    self._scene.addLine(stem_x, stem_y1, stem_x, stem_y2, pen_stem)
                    # Corchete para corcheas (0.5)
                    if duration <= 0.5:
                        self._scene.addLine(stem_x, stem_y2, stem_x + 8, stem_y2 + 10, pen_stem)
                else:
                    stem_x = x + 1
                    stem_y1 = y_center
                    stem_y2 = y_center + 32
                    self._scene.addLine(stem_x, stem_y1, stem_x, stem_y2, pen_stem)
                    # Corchete para corcheas (0.5)
                    if duration <= 0.5:
                        self._scene.addLine(stem_x, stem_y2, stem_x + 8, stem_y2 - 10, pen_stem)

            # D. Digitación (1 al 5)
            if is_current:
                finger_color = QColor("#38bdf8")
            elif is_past:
                finger_color = QColor("#22c55e")
            else:
                is_right_hand = (getattr(note, "hand", "R").upper() == "R")
                finger_color = QColor("#38bdf8") if is_right_hand else QColor("#22c55e")

            finger_text = self._scene.addText(str(note.finger), QFont("Consolas", 11, QFont.Weight.Bold))
            finger_text.setDefaultTextColor(finger_color)
            # Posicionar digitación sobre o debajo de la nota para no colisionar con plica
            finger_y = y_oval - 28 if (y_center > 108 or duration >= 4.0) else y_oval + 18
            finger_text.setPos(x - 2, finger_y)

            # E. Nombre / Lírica debajo del pentagrama
            name_str = note.lyric or midi_to_note_name(note.midi_note)
            if is_current:
                lyric_color = QColor("#38bdf8")
                lyric_weight = QFont.Weight.Bold
            elif is_past:
                lyric_color = QColor("#22c55e")
                lyric_weight = QFont.Weight.Bold
            else:
                lyric_color = QColor("#64748b")
                lyric_weight = QFont.Weight.Normal

            lyric_text = self._scene.addText(name_str, QFont("Segoe UI", 9, lyric_weight))
            lyric_text.setDefaultTextColor(lyric_color)
            lyric_text.setPos(x - 4, 172)

            # F. Acumular tiempos y dibujar Línea Divisora de Compás
            cumulative_beats += duration
            if cumulative_beats >= beats_per_measure and idx < len(self._lesson.notes) - 1:
                x_bar = x + (x_step / 2) + 6
                self._scene.addLine(x_bar, staff_y_start, x_bar, staff_y_end, pen_barline)
                cumulative_beats = 0.0

        # Línea final de cierre del pentagrama (Doble barra de compás final)
        x_final = x_start + len(self._lesson.notes) * x_step - 15
        self._scene.addLine(x_final - 4, staff_y_start, x_final - 4, staff_y_end, QPen(QColor("#64748b"), 1))
        self._scene.addLine(x_final, staff_y_start, x_final, staff_y_end, QPen(QColor("#cbd5e1"), 3))
