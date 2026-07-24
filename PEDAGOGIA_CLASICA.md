# NEXO Piano Tutor — FUNDAMENTACIÓN PEDAGÓGICA Y MANIFIESTO CIENTÍFICO

Este documento consolida la arquitectura pedagógica, científica y filosófica de **NEXO Piano Tutor**.

> **"La excelencia en el piano no emerge del automatismo pasivo, sino del desacoplamiento consciente de la carga cognitiva y el refinamiento del gesto motor."**

---

## 🏛️ 1. Declaración de Principios

`nexo-piano-tutor` nace con un propósito claro: **brindar una formación de piano clásico científicamente rigurosa para estudiantes de todas las edades (niños, jóvenes y adultos)**, distanciándose deliberadamente de las aplicaciones comerciales basadas en barras cayendo estilo arcade (*Guitar Hero*). 

Las interfaces tipo arcade generan adicción visual y reflejos oculares pasivos, pero **anulan la lectura de partitura real, destruyen la noción del pulso interno y no desarrollan memoria muscular ni control biomecánico**.

Nuestra propuesta se fundamenta en tres ciencias:
1. **Neurociencia del Aprendizaje Motor** (Mielenización y bucles de realimentación inmediata).
2. **Biomecánica Pianística** (Escuela Taubman y Suzuki: peso del brazo, libertad articular y digitación activa).
3. **Psicología Cognitiva de Sweller** (Teoría de la Carga Cognitiva).

---

## 🔬 2. Los 4 Pilares Neuro-Pedagógicos

### Pillar I: Desacoplamiento de Carga Cognitiva
Para evitar la saturación en el cerebro infantil, cada lección se aborda en tres fases secuenciales:

1. **Modo Lectura & Digitación (Cero Presión de Tiempo)**
   - El metrónomo está desactivado.
   - El cursor gráfico sobre la partitura **no avanza** hasta que el estudiante presione la tecla física correcta en el controlador MIDI.
   - Se entrena la asociación espacial: *Nota en Pentagrama ➔ Dedo Físico (1 al 5) ➔ Tecla en el Teclado*.

2. **Modo Tiempo y Pulso (Subdivisión Rítmica)**
   - Se activa el pulso de metrónomo.
   - Se evalúa exclusivamente el *timing* y la estabilidad rítmica.

3. **Modo Expresión & Examen (Integración)**
   - Se combinan Notación + Tiempo + Control de Dinámica (*Velocity*).

---

### Pillar II: Realimentación Inmediata de Ultra-Baja Latencia (<15ms)
El aprendizaje motor requiere que la corrección del error ocurra dentro de la ventana de asociación neuro-sináptica (<100ms).

El motor `RealtimeEvaluator` analiza cada evento `NOTE_ON`:
- **Precisión Tonal**: Coincidencia exacta del pitch MIDI.
- **Tolerancia Rítmica (Delta)**:
  - `±25ms`: **Perfecto**
  - `±60ms`: **Aceptable**
  - `>100ms`: **Desfase Rítmico**
- **Control de Dinámica (Velocity Meter)**: Detección de acentos involuntarios entre dedos adyacentes (desarrollo del control fino de pulgar y meñique).

---

### Pillar III: Aislamiento Atómico de Errores (Repetición Espaciada)
Cuando el estudiante falla en un pasaje:
1. El sistema **no reinicia la obra desde el principio** (evita el hábito frustrante de re-ensayar lo que ya sale bien).
2. El algoritmo aísla el **micro-compás problemático** (bucle de 2 a 4 notas).
3. Se reduce el tempo (BPM) automáticamente un 30% y se exige una racha de 3 ejecuciones limpias antes de retornar a la obra completa.

---

### Pillar IV: Notación Musical Interactiva en Pentagrama Real (Estándar SMuFL)
- Partitura real en **Clave de Sol** (mano derecha) y **Clave de Fa** (mano izquierda).
- Renderizado de glifos con la fuente vectorial **Bravura.otf** (W3C SMuFL Standard).
- Indicación clara de digitación recomendada (dedos 1-Pulgar al 5-Meñique).
- Renderizado adaptativo que responde iluminando las notas a medida que se ejecutan.

---

## 📚 3. Curriculum Clásico de Dominio Público (Programa Completo)

### Capítulo I: Los Fundamentos de Beyer (Opus 101) — *Completado (Lecciones 1 a 10)*
1. `beyer_op101_01.json`: Posición Fija de Do Mayor — Mano Derecha (Clave de Sol).
2. `beyer_op101_02.json`: Posición Fija de Do Mayor — Mano Izquierda (Clave de Fa).
3. `beyer_op101_03.json`: Saltos de Terceras (3as) — Mano Derecha.
4. `beyer_op101_04.json`: Saltos de Terceras (3as) — Mano Izquierda.
5. `beyer_op101_05.json`: Escala de Do Mayor Completa (El Paso del Pulgar).
6. `beyer_op101_06.json`: Alternancia y Diálogo en Clave de Fa (MI).
7. `beyer_op101_07.json`: Escala de Do Mayor en Mano Izquierda con paso de pulgar.
8. `beyer_op101_08.json`: Saltos de Terceras en Mano Izquierda.
9. `beyer_op101_09.json`: Primer Unísono Bimanual Simultáneo (Manos Juntas a Octava).
10. `beyer_op101_10.json`: Saltos de Cuartas y Articulación interdigital.

### Capítulo II: Polifonía e Independencia Barroca (J. S. Bach) — *Completado (Lecciones 11 a 20)*
11. `bach_anh126_11.json`: La Musette en Re Mayor (BWV Anh. 126) — Bajo continuo de gaita y timbre de Clavecín.
12. `bach_anh114a_12.json`: Minueto en Sol Mayor (BWV Anh. 114) — Parte A (Independencia rítmica en 3/4).
13. `bach_anh114b_13.json`: Minueto en Sol Mayor (BWV Anh. 114) — Parte B (Imitación melódica).
14. `bach_anh115_14.json`: Minueto en Sol Menor (BWV Anh. 115) — Tonalidad menor y armadura de clave (2 bemoles).
15. `bach_anh122_15.json`: Marcha en Re Mayor (BWV Anh. 122 - C. P. E. Bach) — Legato vs. Staccato.
16. `bach_anh121_16.json`: Minueto en Do Menor (BWV Anh. 121) — Walking bass en mano izquierda.
17. `bach_anh132_17.json`: Aria en Re Menor (BWV Anh. 132) — Canto barroco expressivo.
18. `bach_anh119_18.json`: Polonesa en Sol Menor (BWV Anh. 119) — Síncopa y danza.
19. `bach_bwv939_19.json`: Preludio en Do Mayor (BWV 939 - Pequeños Preludios) — Arpegiado contrapuntístico.
20. `bach_bwv924_20.json`: Pequeño Preludio N° 1 en Do Mayor (BWV 924) — Obra cumbre barroca.

### Capítulo III: Claridad y Agilidad Clásica (Muzio Clementi & Béla Bartók) — *Completado (Lecciones 21 a 30)*
21. `clementi_op36_21.json`: Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 1 'Allegro' con Bajo Alberti).
22. `beyer_op101_22.json`: Escala de Sol Mayor completa con alteración fija (Fa#) y paso de pulgar.
23. `clementi_op36_23.json`: Muzio Clementi — Agilidad en Staccato de muñeca.
24. `bartok_mikro1_24.json`: Béla Bartók — Mikrokosmos N° 1 (Estudio Modal de 6 notas a manos en espejo).
25. `bartok_mikro12_25.json`: Béla Bartók — Mikrokosmos N° 12 (Acompañamiento reflejado y ritmo asimétrico).
26. `clementi_op36_26.json`: Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 2 'Andante') y contraste dinámico (Forte vs. Piano).
27. `beyer_op101_27.json`: Escala de Fa Mayor completa con armadura de 1 bemol (Si♭).
28. `bartok_mikro22_28.json`: Béla Bartók — Mikrokosmos N° 22 (Canon a la Octava).
29. `clementi_op36_29.json`: Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 3 'Vivace' en 3/8).
30. `bartok_mikro32_30.json`: Béla Bartók — Mikrokosmos N° 32 (Ritmo Búlgaro) / Finale de Maestría Clásica.

---

## 🚀 4. El Horizonte de Expansión Futuro (Roadmap de NEXO Piano Tutor)

1. **Módulo A: Capítulo IV — *La Tempestad Romántica y el Expresionismo***
   - *Obras master:* Frédéric Chopin (*Preludio Op. 28 N° 4 en Mi menor*), Robert Schumann (*Álbum para la Juventud Op. 68*), Pyotr I. Tchaikovsky (*Álbum de la Juventud Op. 39*).
   - *Física motor:* Control del **Pedal de Resonancia** (Sustain CC64), el tiempo *Rubato* y la polirritmia ($3 \text{ contra } 2$).
2. **Módulo B: "La Fragua Abierta" (Motor Importer Soberano MusicXML / MIDI)**
   - Motor de arrastrar y soltar que convierte cualquier archivo `.musicxml` o `.mid` de cualquier compositor en una lección interactiva vectorial con digitación y evaluación en vivo.
3. **Módulo C: "El Maestro Socrático de la Fragua" (Mente DeepSeek API)**
   - Integración de IA socrática a demanda que analiza los logs de errores rítmicos y de octava, devolviendo un consejo pedagógico en tono humano y biomecánico.

---

## 🎭 5. Gamificación y Rigor Narrativo

1. **Viaje Timbrico Histórico**:
   - Las piezas de Beyer y Clementi/Bartók suenan a **Piano de Cola de Concierto** (`Program GM 0`).
   - Las piezas de Bach suenan automáticamente a **Clavecín Barroco** (`Program GM 6`) u **Órgano de Catedral** (`Program GM 19`).
2. **Contexto Histórico Dramático**:
   - Tarjetas breves antes de cada obra narrando la historia humana detrás del compositor.
3. **Capítulos Épicos**:
   - Capítulo I: *Los Fundamentos de Beyer*
   - Capítulo II: *Los Secretos del Barroco (J. S. Bach)*
   - Capítulo III: *La Claridad Clásica y la Agilidad (Clementi & Bartók)*

---

## 🔐 6. Blueprint de Autenticación y Gestión de Perfiles Soberanos

### 6.1. Fundamentación y Ley de Universalidad Semántica
El diseño del sistema de perfiles se rige de forma estricta por la **Ley de Universalidad Semántica (Ley VI de NEXO)**:

> **"El código opera sobre abstracciones de sistema (User, Session, Progress, Auth), nunca sobre nombres customizados o constantes mágicas hardcodeadas."**

---

## 📈 7. Blueprint de Evaluación Realista, Tarjetas Teóricas y Bitácora

### 7.1. Evaluación Realista e Inmunidad a las Felicitaciones Ciegas
- **Cálculo de Precisión (%)**: $(N_{correctas} / N_{totales}) \times 100$.
- **Criterio de Maestría por Tramo**:
  - **90% – 100%**: 🌟 *Ejecución Impecable* (Desbloquea la lección y suma insignia).
  - **75% – 89%**: 👍 *Buena Técnica* (Consejo: "Notas logradas. Realizá una serie de repeticiones x3 para afinar la fluidez").
  - **< 75%**: 💡 *Revisión Requerida* (Sin felicitaciones vacías).

---

*Documento de diseño pedagógico consolidado y actualizado el 2026-07-23 en el Terroir de Marcelo y NEXO.*
