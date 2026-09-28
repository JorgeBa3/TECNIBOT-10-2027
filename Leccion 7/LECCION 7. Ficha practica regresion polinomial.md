LECCIÓN 7. Ficha práctica: regresión polinomial

Descripción: hoy vas a limpiar datos raros (outliers) directamente en la ESP32 y a entrenar a mano —sin librerías de Python para computadora— un modelo de regresión que ya no traza una línea recta, sino una curva que se ajusta mejor al comportamiento real de la temperatura. Todo el programa (recolección, limpieza, entrenamiento y predicción) corre dentro de la ESP32 con MicroPython; la computadora solo se usa para ver la consola de Thonny.

Electrónica:

Materiales: ESP32, protoboard, potenciómetro (ya armado desde la lección 5/6, hace de "sensor de temperatura"), cables jumper.
No hay hardware nuevo: se reutiliza el mismo potenciómetro en GPIO 34 de las lecciones anteriores.

Programación:

Paso 1: Sube a la ESP32 los archivos `limpieza.py` y `RegresionPolinomial.py`. Ejecuta primero `limpieza.py`: importa `ADC` y `Pin` de `machine` para leer el potenciómetro (temperatura), y `sleep`/`time` de `utime` para tomar una lectura por segundo.

Paso 2: Recolecta los datos moviendo el potenciómetro: de vez en cuando llévalo al tope o al mínimo para generar lecturas "raras" a propósito. Cada muestra (tiempo, temperatura) se guarda en la memoria de la ESP32, en el archivo `datos_sensores_l7.csv`.

Paso 3: Limpieza: en la propia ESP32 se filtran los valores atípicos, conservando solo las temperaturas lógicas de un hogar (entre 0°C y 50°C). El programa imprime cuántas muestras había, cuántas quedaron y cuántos outliers se eliminaron.

Paso 4: Comparación visual antes/después: como la ESP32 no tiene matplotlib, la comparación se dibuja como un gráfico de texto (ASCII) directamente en la consola de Thonny, una barra por cada muestra, antes y después de limpiar.

Paso 5: `limpieza.py` guarda el resultado limpio en `datos_limpios.csv`, dentro de la misma ESP32, listo para entrenar el modelo.

Paso 6: Ejecuta `RegresionPolinomial.py`. Carga `datos_limpios.csv` desde la memoria de la ESP32 y calcula, a mano, las sumatorias del sistema de ecuaciones normales de una regresión polinomial de grado 2 (`temp = a + b·t + c·t²`).

Paso 7: El sistema de 3 ecuaciones se resuelve por eliminación gaussiana escrita en puro MicroPython (sin numpy ni scikit-learn), obteniendo los coeficientes `a`, `b` y `c` del modelo.

Paso 8: El programa te pide un tiempo en segundos, calcula la predicción con la curva ajustada y la imprime en la consola. Después dibuja, también en ASCII, la curva del modelo completa y marca en qué punto cae tu predicción.

¿Cómo respondes con esto? ¿Por qué un cambio que acelera o desacelera no puede ser representado bien por una línea recta?

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB10/Leccion%207
