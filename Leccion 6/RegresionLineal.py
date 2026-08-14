import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Cargar directamente el dataset ya limpio
df_limpio = pd.read_csv('datos_limpios.csv')
print(f"Filas cargadas para el entrenamiento: {len(df_limpio)}")

# 2. Entrenar Modelo
X = df_limpio[['Tiempo_s']]
y = df_limpio['Temperatura_C']

modelo = LinearRegression()
modelo.fit(X, y)

# 3. Predicción del alumno
tiempo_usuario = float(
    input("Ingresa el tiempo en segundos para la predicción: ")
)
prediccion = modelo.predict(pd.DataFrame({'Tiempo_s': [tiempo_usuario]}))[0]

print(f"\n🔮 A los {tiempo_usuario}s la temperatura estimada es: {prediccion:.1f} °C")

# 4. Visualización con línea extendida adaptada
max_x = max(df_limpio['Tiempo_s'].max(), tiempo_usuario)
X_extendido = pd.DataFrame(
    {'Tiempo_s': np.linspace(df_limpio['Tiempo_s'].min(), max_x, 100)}
)
y_extendido = modelo.predict(X_extendido)

plt.figure(figsize=(9, 4.5))
plt.scatter(
    df_limpio['Tiempo_s'],
    df_limpio['Temperatura_C'],
    color='blue',
    alpha=0.6,
    label='Datos Reales (Validados)',
)
plt.plot(
    X_extendido['Tiempo_s'],
    y_extendido,
    color='red',
    linewidth=2,
    label='Línea de Regresión',
)
plt.scatter(
    [tiempo_usuario],
    [prediccion],
    color='green',
    s=150,
    zorder=5,
    marker='*',
    label=f'Tu Predicción ({tiempo_usuario}s, {prediccion:.1f}°C)',
)

plt.ylim(18, max(prediccion + 3, 32))
plt.xlabel('Tiempo (s)', fontweight='bold')
plt.ylabel('Temperatura (°C)', fontweight='bold')
plt.title(
    'Predicción Interactiva de Temperatura (Smart House)', fontweight='bold'
)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()