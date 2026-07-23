"""
Punto de entrada principal para NEXO Piano Tutor (PySide6).
Tutor pedagógico científico de piano clásico para niños.
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Asegurar que el directorio raíz esté en sys.path
CARPETA_RAIZ = os.path.dirname(os.path.abspath(__file__))
if CARPETA_RAIZ not in sys.path:
    sys.path.insert(0, CARPETA_RAIZ)

from gui.main_window import MainWindow
from gui.theme import TUTOR_THEME
from gui.smufl import load_smufl_font


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("NEXO Piano Tutor")
    app.setOrganizationName("NEXO")

    # Cargar tipografía musical SMuFL (Bravura.otf)
    load_smufl_font()

    # Aplicar Dark Theme de Partitura
    app.setStyleSheet(TUTOR_THEME)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
