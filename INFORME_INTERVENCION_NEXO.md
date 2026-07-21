# 🎼 INFORME DE INTERVENCIÓN ARQUITECTÓNICA Y SOLUCIÓN MIDI

**Para:** Agente NEXO / Equipo de Desarrollo  
**De:** Antigravity (Google DeepMind - Advanced Agentic Coding)  
**Proyecto:** `nexo-piano-tutor`  
**Fecha:** 21 de Julio, 2026  

---

## 📌 1. Resumen Ejecutivo del Problema Diagnostico

### Síntoma Reportado
Al conectar el controlador MIDI **Samson Carbon 49**, la pulsación de teclas generaba sonido de piano en el equipo, pero la interfaz gráfica de la aplicación (PySide6) **no capturaba las notas ni avanzaba el pentagrama**.

### Evaluación de la Propuesta Previa de Nexo
*Propuesta de Nexo:* "Implementar captura MIDI aislada en proceso secundario (Worker Process IPC vía multiprocessing)".

* **Diagnóstico de la propuesta:** **Incorrecta para este escenario.**
* **Razón Técnica:** En Windows (API Multimedia WinMM), la restricción sobre handles de entrada MIDI es **exclusiva a nivel de dispositivo en todo el Sistema Operativo**, no a nivel de proceso. Si FluidSynth en el proceso principal mantenía abierto el puerto `winmidi` del Samson Carbon 49, un proceso secundario (`Worker Process`) hubiera recibido exactamente el mismo error de kernel: `MMSYSERR_ALLOCATED` *(Error 4: Dispositivo en uso)*. Además, la comunicación inter-proceso (IPC) introducía latencia innecesaria superando la meta de <15ms.

---

## 🔬 2. Causa Raíz Identificada

El problema radicaba en el comportamiento por defecto de `pyfluidsynth` en Windows:
1. En `core/sound_engine.py`, la inicialización llamaba a `self._fluidsynth.start(driver=driver, midi_driver=None)`.
2. En la implementación interna de `pyfluidsynth`, pasar `midi_driver=None` provoca un fallback implícito al ajuste predeterminado del sistema, que en Windows es `"winmidi"`.
3. FluidSynth abría el puerto MIDI IN en C, adueñándose de forma exclusiva del handle WinMM del Samson Carbon 49.
4. **Consecuencia:** FluidSynth procesaba las notas internamente en C generando sonido directo, pero **secuestraba el puerto impidiendo que `rtmidi` (Python) pudiera registrar la entrada**. Por ende, PySide nunca recibía señales `note_played` y la partitura permanecía estática.

---

## 🛠️ 3. Solución Arquitectónica Implementada

Se aplicó una solución quirúrgica en 2 capas para desacoplar responsabilidades:

1. **Configuración Estricta de FluidSynth como Motor de Salida Exclusivo (`core/sound_engine.py`):**
   ```python
   # Forzar a FluidSynth a NO abrir ningún driver de entrada MIDI
   self._fluidsynth.setting("midi.driver", "none")
   self._fluidsynth.start(driver=driver, midi_driver="none")
   ```
2. **Flujo de Eventos Unidireccional y Sincrónico:**
   ```
   [ Samson Carbon 49 (Hardware) ]
                 │
                 ▼ (MIDI IN)
       [ rtmidi.MidiIn (Python) ]
                 │
                 ▼ (Señal Qt note_played)
      [ RealtimeEvaluator & SheetView ] ──► (Avanza Pentagrama y Evaluación)
                 │
                 ▼ (play_note)
       [ SoundEngine / FluidSynth ] ──► (Genera Audio por DSound)
   ```

---

## 📊 4. Verificación

Se ejecutó el script de verificación `diagnose_midi.py`, validando lo siguiente:
* ✅ **SoundEngine:** FluidSynth arranca su síntesis de audio correctamente.
* ✅ **MidiInputHandler:** `rtmidi` abre el puerto `[0] SAMSON Carbon49 0` sin errores de WinMM.
* ✅ **Sincronización:** Eventos de notas capturados en tiempo real mientras el motor de audio reproduce el SoundFont de piano de cola (`FluidR3_GM_GS.sf2`).

---

## 💡 5. Recomendaciones y Consejos para el Futuro Desarrollo con Nexo

Para continuar expandiendo **NEXO Piano Tutor** manteniendo los estándares neuro-pedagógicos y la solidez técnica, se recomiendan las siguientes pautas:

### A. Arquitectura y Rendimiento (<15ms)
* **Evitar hilos innecesarios para MIDI:** `python-rtmidi` opera internamente con callbacks nativos en C++. El manejo mediante señales Qt (`Signal`/`Slot`) en el hilo principal GUI es extremadamente eficiente y suficiente para latencias sub-15ms. No migrar a `multiprocessing` a menos que se trate de análisis de audio por DSP en tiempo real.
* **Fallback de Audio:** Mantener y pulir la cascada de drivers en `SoundEngine`: FluidSynth (`.sf2`) ➔ Windows Native WINMM (`ctypes.windll.winmm`) ➔ `rtmidi.MidiOut`.

### B. Notación de Partitura (`SheetView`) y Escalabilidad Pedagogica
* **Evolución del Renderizador:** Para el *Capítulo I (Beyer Op. 101)* la vista actual basada en `QGraphicsScene` funciona excelentemente. Al avanzar al *Capítulo II (J. S. Bach)* con polifonía bimanual y voces cruzadas, evaluar integrar un motor de notación dinámico como `verovio` o notación SVG/MusicXML integrada.
* **Desacoplamiento de Carga Cognitiva:** Implementar los modificadores visuales según el modo seleccionado (ej. en *Modo Lectura*, ocultar la barra de tiempo y pausar la evaluación de métrica; en *Modo Tiempo*, mostrar indicación de pulso visual).

### C. Persistencia y Algoritmo de Repetición Espaciada (SRS)
* **Métricas SQLite (`progress.db`):** Al guardar el progreso del alumno, registrar:
  1. `jitter_ms`: Desvío temporal relativo al pulso recomendado.
  2. `velocity_map`: Mapa de fuerza/dinámica para corregir pulsación demasiado débil o descompensada entre dedos.
  3. `first_attempt_accuracy`: Porcentaje de notas correctas al primer intento.
* Usar estas métricas para alimentar la curva de repetición adaptativa en pasajes problemáticos.

---
*Informe generado para el ecosistema NEXO por Antigravity.*
