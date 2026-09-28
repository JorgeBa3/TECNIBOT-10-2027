LECCIÓN 8. Clustering y clasificación en tu SmartHouse

Descripción: Con este programa vas a recolectar temperatura y luz en tres situaciones de la casa (día, tarde y noche) sin guardar el nombre del modo. Todo corre en la ESP32: K-means (K = 3) descubre los grupos y nombra según la luz del centroide. Las luces LED responden: verde = DÍA, amarillo = TARDE, rojo = NOCHE. Si temperatura y luz están las dos altas (por encima de 80), suena el buzzer y las 3 LEDs se encienden en secuencia: es el camino de salida. El CSV sale de TUS sensores (potenciómetro y LDR de la lección 5).

Electrónica:

Materiales:
ESP32
Protoboard
Potenciómetro (simula temperatura)
LDR / fotorresistencia (luz)
LED verde
LED amarillo
LED rojo
Resistencias 220 Ω (3)
Buzzer
Cables jumper

Paso 1: Coloca el potenciómetro y la LDR en el protoboard, igual que en la lección 5.
Potenciómetro (temperatura) → GPIO 34
LDR (luz) → GPIO 35
GND y 3V3 a la riel del protoboard.

Paso 2: En el mismo protoboard conecta las luces de la casa (3 LEDs) y el buzzer. Luego conecta la ESP32 a la computadora.
LED verde (DÍA): GPIO 2 → 220 Ω → pata larga (+), pata corta → GND
LED amarillo (TARDE): GPIO 4 → 220 Ω → pata larga (+), pata corta → GND
LED rojo (NOCHE): GPIO 5 → 220 Ω → pata larga (+), pata corta → GND
Buzzer: GPIO 25 → (+), (−) → GND
En emergencia las tres LEDs se encienden una tras otra (camino de salida) y suena el buzzer.

Programación:
Sube a la ESP32 el archivo main.py.

Importar librerías y configurar pines:
Importa Pin, PWM, ADC, sleep y math. Potenciómetro GPIO 34, LDR GPIO 35, LED verde GPIO 2, amarillo GPIO 4, rojo GPIO 5, buzzer GPIO 25. Los tres modos de recolección son DIA, TARDE y NOCHE. El CSV solo guarda Temperatura_C y Luz, sin etiquetas.

Definir funciones:
leer() convierte el ADC a temperatura y luz (0–100). dist() es la distancia euclidiana. kmeans() busca 3 centros a mano. aplicar() enciende verde (DÍA), amarillo (TARDE) o rojo (NOCHE). camino_salida() hace sonar el buzzer y recorre las 3 LEDs.

# 1) Recolectar en la ESP32. Cuando la consola pida cada modo, simula la casa así:
DIA: luz alta y potenciómetro medio-alto (no al máximo).
TARDE: luz media y potenciómetro a la mitad.
NOCHE: tapa la LDR y baja el potenciómetro.
8 muestras de cada uno. No se guarda el nombre del modo.

# 2) Leer el CSV y entrenar K-means a mano (K = 3) en la misma ESP32. Elige 3 centros, asigna cada punto al más cercano y recalcula. Nombra los grupos: menos luz → NOCHE, en medio → TARDE, más luz → DÍA.

# 3) En vivo, cada lectura nueva va al centro más cercano. Luces: verde = DÍA, amarillo = TARDE, rojo = NOCHE. Si temperatura y luz superan 80 (pot al máximo y LDR descubierta), es EMERGENCIA: buzzer y las 3 LEDs marcan el camino de salida. Así respondes: ¿cómo una casa agrupa sola día y noche, y avisa si algo está demasiado alto?

https://github.com/JorgeBa3/MaterialApoyo-TK/tree/main/TB10/Leccion%208
