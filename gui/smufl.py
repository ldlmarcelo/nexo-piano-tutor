"""
Módulo de Soporte SMuFL (Standard Music Font Layout) para NEXO Piano Tutor.
Proporciona la carga de la fuente tipográfica vectorial Bravura (.otf) y
el mapeo de glifos musicales según el estándar internacional de Steinberg.
"""

import os
from PySide6.QtGui import QFontDatabase, QFont

# Constantes de Glifos SMuFL (Unicode Block U+E000..U+F8FF)
CLEF_TREBLE = "\uE050"      # Clave de Sol (gClef)
CLEF_BASS = "\uE062"        # Clave de Fa (fClef)

NOTEHEAD_BLACK = "\uE0A4"   # Cabeza de nota negra / corchea (noteheadBlack)
NOTEHEAD_HALF = "\uE0A3"    # Cabeza de nota blanca (noteheadHalf)
NOTEHEAD_WHOLE = "\uE0A2"   # Cabeza de nota redonda (noteheadWhole)

ACCIDENTAL_SHARP = "\uE260"   # Sostenido (accidentalSharp)
ACCIDENTAL_FLAT = "\uE262"    # Bemol (accidentalFlat)
ACCIDENTAL_NATURAL = "\uE261" # Becuadro (accidentalNatural)

REST_WHOLE = "\uE4E3"     # Silencio de redonda (restWhole)
REST_HALF = "\uE4E4"      # Silencio de blanca (restHalf)
REST_QUARTER = "\uE4E5"   # Silencio de negra (restQuarter)
REST_8TH = "\uE4E6"       # Silencio de corchea (rest8th)

# Corchetes (Flags) Individuales SMuFL
FLAG_8TH_UP = "\uE240"     # Corchete corchea plica arriba (flag8thUp)
FLAG_8TH_DOWN = "\uE241"   # Corchete corchea plica abajo (flag8thDown)
FLAG_16TH_UP = "\uE242"    # Corchete semicorchea plica arriba (flag16thUp)
FLAG_16TH_DOWN = "\uE243"  # Corchete semicorchea plica abajo (flag16thDown)

# Métrica de Compás SMuFL (timeSig0 .. timeSig9)
TIME_SIG_DIGITS = {
    "0": "\uE080",
    "1": "\uE081",
    "2": "\uE082",
    "3": "\uE083",
    "4": "\uE084",
    "5": "\uE085",
    "6": "\uE086",
    "7": "\uE087",
    "8": "\uE088",
    "9": "\uE089",
}

_SMUFL_FONT_FAMILY: str = None


def load_smufl_font() -> str:
    """
    Registra la fuente Bravura.otf en la base de datos de fuentes de Qt.
    Devuelve el nombre de la familia cargada ('Bravura') o None si falla.
    """
    global _SMUFL_FONT_FAMILY
    if _SMUFL_FONT_FAMILY is not None:
        return _SMUFL_FONT_FAMILY

    font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "Bravura.otf")
    font_path = os.path.abspath(font_path)

    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                _SMUFL_FONT_FAMILY = families[0]
                print(f"[SMuFL] Fuente vectorial '{_SMUFL_FONT_FAMILY}' cargada exitosamente.")
                return _SMUFL_FONT_FAMILY

    print("[SMuFL] ADVERTENCIA: No se pudo cargar 'Bravura.otf'. Usando fuentes de sistema de reserva (fallback).")
    _SMUFL_FONT_FAMILY = ""
    return _SMUFL_FONT_FAMILY


def get_smufl_font(point_size: int = 24, bold: bool = False) -> QFont:
    """
    Devuelve una instancia de QFont configurada con Bravura o fuente de reserva (Segoe UI Symbol / Arial).
    """
    family = load_smufl_font()
    if family:
        font = QFont(family, point_size)
    else:
        # Fallback a Segoe UI Symbol en Windows / DejaVu Sans en Linux
        font = QFont("Segoe UI Symbol", point_size)
    
    font.setBold(bold)
    return font
