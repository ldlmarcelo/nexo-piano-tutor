# nexo-piano-tutor (v1.0.0)

Tutor pedagógico científico, analítico y riguroso de piano clásico para estudiantes de todas las edades (niños, jóvenes y adultos).

> **Pedagogía científica de precisión.** Sin barras cayendo estilo arcade. Basado en notación de pentagrama real (Clave de Sol y Fa), desacoplamiento de carga cognitiva (Lectura, Tiempo, Expresión), evaluación MIDI en tiempo real (<15ms), bucles de repetición adaptativos y perfiles soberanos de estudiantes.

---

## 🏛️ Curriculum Clásico (Estado de Avance)

### Capítulo I: Los Fundamentos de Beyer (Opus 101) — *Completado (Lecciones 1 a 10)*
- **Lección 1 (`beyer_op101_01.json`):** Ejercicio N° 1 (Posición Fija de Do4 a Sol4, Mano Derecha, Clave de Sol).
- **Lección 2 (`beyer_op101_02.json`):** Ejercicio N° 2 (Mano Izquierda, Clave de Fa, Do3 a Sol3, meñique a pulgar).
- **Lección 3 (`beyer_op101_03.json`):** Saltos de terceras en Mano Derecha (dedos 1, 3, 5).
- **Lección 4 (`beyer_op101_04.json`):** Saltos de terceras en Mano Izquierda (dedos 5, 3, 1).
- **Lección 5 (`beyer_op101_05.json`):** Escala de Do Mayor completa (8 notas) e introducción al **paso del pulgar** (paso por debajo del dedo 3 en Fa4).
- **Lección 6 (`beyer_op101_06.json`):** Ejercicio N° 6 (Alternancia de Manos - Diálogo Armónico en Clave de Fa).
- **Lección 7 (`beyer_op101_07.json`):** Ejercicio N° 7 (Escala de Do Mayor completa en Mano Izquierda, Clave de Fa).
- **Lección 8 (`beyer_op101_08.json`):** Ejercicio N° 8 (Estudio de Corcheas e Independencia Rítmica).
- **Lección 9 (`beyer_op101_09.json`):** Ejercicio N° 9 (Vals en Métrica de 3/4).
- **Lección 10 (`beyer_op101_10.json`):** Ejercicio N° 10 (Saltos de Cuartas y Articulación).

### Capítulo II: Polifonía e Independencia (J. S. Bach) — *En Roadmap*
- Piezas del *Libro de Clavecin de Anna Magdalena Bach*.
- Contrapunto inicial bimanual simultáneo.

### Capítulo III: Claridad y Técnica (Muzio Clementi - Op. 36 & Béla Bartók - Mikrokosmos) — *En Roadmap*
- Escalas, arpegios y fraseo articulado (*legato* / *staccato*).

---

## 🧪 Pilares Pedagógicos y Funcionalidades

1. **Desacoplamiento de Carga Cognitiva**:
   - *Modo Lectura*: Evaluación de notas/dedos a ritmo del alumno (sin metrónomo).
   - *Modo Tiempo*: Evaluación con metrónomo y **cuenta regresiva previa de 4 pulsos** con indicación sonora de compás.
   - *Modo Expresión*: Integración completa de tempo y dinámica.
2. **Evaluación en Tiempo Real y Análisis Rítmico Espacial (Estilo Drum Tutor)**:
   - Captura aislada vía `python-rtmidi` acoplada a audio sintético `pyfluidsynth` (driver MIDI IN desactivado en C para evitar conflictos WinMM en Windows).
   - **Evaluación Rítmica Espacial**: Marcación de notas impecables con Círculo Verde (`✓`), errores de tono con Cruz Roja (`✗`), y desfases rítmicos con desplazamiento espacial: **`🡠 ✗`** (adelantado) a la izquierda y **`✗ 🡢`** (retrasado) a la derecha.
   - Metrónomo dedicado en Canal 9 GM Percussion (Woodblock 76/77).
3. **Perfiles de Estudiantes & Bitácora de Sesión (`UserManager` / `DashboardDialog`)**:
   - Registro de estudiantes con PIN opcional y guardado local en `users.json`.
   - Medición de precisión acumulada (%), series completadas, total de notas ejecutadas e historial cronológico de sesiones (`SessionLog`).
4. **Sistema de Repetición Adaptativa (Bucles xN)**:
   - Modos `1x`, `3x`, `5x` e `♾️ Bucle Infinito` con reinicio automático de series y evaluación final de desempeño.
5. **Partitura Vectorial Responsiva y Teclado Activo (`SheetView` / `PianoKeyboard`)**:
   - Auto-seguimiento centrado (`centerOn`) de la nota activa en partitura con trazado de alto contraste (2px) para notas caladas (blancas y redondas) y destellos de error en rojo sobre el teclado virtual.
6. **Tarjetas Teóricas & "La Biblioteca de la Fragua" (`TheoryDialog` / `LibraryDialog`)**:
   - Popups de teoría emergente por lección y glosario integral de notación y técnica.

---

## Stack Técnico

- **Lenguaje**: Python 3.10+
- **Interfaz**: PySide6 (Qt6) — Layout adaptativo 16:9
- **Audio & MIDI**: `python-rtmidi` + `pyfluidsynth` (vía `nexo-midi-synth` y SoundFont `FluidR3_GM_GS.sf2`)
- **Partitura**: Renderizador vectorial interactivo en `QGraphicsScene` (`SheetView`) + Teclado Virtual 48 teclas (`PianoKeyboard`)
- **Persistencia**: Perfiles en JSON (`users.json`), extensible a SQLite (`progress.db`)

---

## Instalación y Uso

```bash
git clone https://github.com/ldlmarcelo/nexo-piano-tutor.git
cd nexo-piano-tutor
pip install -r requirements.txt
python main.py
```

---

## Origen

Módulo federado del ecosistema NEXO, diseñado para la formación musical clásica de los hijos de Marcelo.

## 🔄 Protocolo de Desarrollo Cross-Platform (NUC ➔ Windows)

> ⚠️ **IMPERATIVO DE COMMIT Y PUSH**: Dado que el código se escribe y refacciona en el host Linux (NUC) pero **la aplicación real con hardware MIDI (Samson Carbon 49) se ejecuta y prueba físicamente en Windows**, **es obligatorio realizar `git commit` y `git push` tras cada implementación o ajuste completado**, garantizando que la máquina Windows pueda sincronizar (`git pull`) y verificar inmediatamente los cambios en caliente.

---

## Licencia

MIT
