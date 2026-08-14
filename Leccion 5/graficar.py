import matplotlib.pyplot as plt
import pandas as pd

# 1. Cargar los datos guardados desde el archivo CSV
df = pd.read_csv('datos_sensores.csv')

# 2. Crear la figura y el primer eje (Temperatura en el eje izquierdo)
fig, ax_temp = plt.subplots(figsize=(10, 5))

# Graficar Temperatura (Línea roja)
line1 = ax_temp.plot(
    df['Muestra'],
    df['Temperatura_C'],
    color='#d9534f',
    linewidth=2,
    label='Temperatura (°C)',
)
ax_temp.set_xlabel('Muestra (Número de lectura)', fontsize=11, fontweight='bold')
ax_temp.set_ylabel(
    'Temperatura (°C)', color='#d9534f', fontsize=11, fontweight='bold'
)
ax_temp.tick_params(axis='y', labelcolor='#d9534f')
ax_temp.grid(True, linestyle='--', alpha=0.5)

# 3. Crear el segundo eje que comparte el mismo eje X (Luz en el eje derecho)
ax_luz = ax_temp.twinx()

# Graficar Luz (Línea azul punteada)
line2 = ax_luz.plot(
    df['Muestra'],
    df['Luz_Porcentaje'],
    color='#0275d8',
    linewidth=2,
    linestyle='--',
    label='Luz (%)',
)
ax_luz.set_ylabel(
    'Intensidad de Luz (%)', color='#0275d8', fontsize=11, fontweight='bold'
)
ax_luz.tick_params(axis='y', labelcolor='#0275d8')

# 4. Título y Leyenda unificada
plt.title(
    'Lectura de Sensores ESP32 (100 Muestras)',
    fontsize=13,
    fontweight='bold',
    pad=12,
)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax_temp.legend(lines, labels, loc='upper right')

# Ajustar márgenes y mostrar la gráfica
plt.tight_layout()
plt.show()