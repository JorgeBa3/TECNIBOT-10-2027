import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 1. Cargar datos crudos
df = pd.read_csv('datos_sensores_l7.csv')

# 2. LIMPIEZA L7: Borrar nulos Y filtrar valores atípicos
df_limpio = df.dropna()
# Conservar solo temperaturas lógicas de un hogar (entre 0°C y 50°C)
df_limpio = df_limpio[(df_limpio['Temperatura_C'] >= 0) & (df_limpio['Temperatura_C'] <= 50)]

# 3. COMPARACIÓN VISUAL: ANTES VS DESPUÉS DE LIMPIAR
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
# Gráfica 1: Sucia
ax1.scatter(df['Tiempo_s'], df['Temperatura_C'], color='purple', alpha=0.7)
ax1.set_title('Antes de Limpiar (Con Outliers)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.grid(True, linestyle='--', alpha=0.5)

# Gráfica 2: Limpia
ax2.scatter(df_limpio['Tiempo_s'], df_limpio['Temperatura_C'], color='blue', alpha=0.7)
ax2.set_title('Después de Limpiar (Filtrado 0°C a 50°C)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Temperatura (°C)')
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# 4. ENTRENAR REGRESIÓN POLINOMIAL (Grado 2)

X = df_limpio[['Tiempo_s']]
y = df_limpio['Temperatura_C']

# Creamos un pipeline que eleva 'Tiempo_s' al cuadrado y entrena el modelo
modelo_poly = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
modelo_poly.fit(X, y)

# 5. PREDICCIÓN INTERACTIVA
tiempo_usuario = float(input("\nIngresa el tiempo en segundos para predecir: "))
prediccion = modelo_poly.predict(pd.DataFrame({'Tiempo_s': [tiempo_usuario]}))[0]

print(f"🔮 Predicción Polinomial: A los {tiempo_usuario}s habrán ~{prediccion:.1f} °C")

# 6. VISUALIZACIÓN DE LA CURVA POLINOMIAL Y LA PREDICCIÓN
max_x = max(df_limpio['Tiempo_s'].max(), tiempo_usuario)
X_extendido = pd.DataFrame({'Tiempo_s': np.linspace(df_limpio['Tiempo_s'].min(), max_x, 100)})
y_extendido = modelo_poly.predict(X_extendido)

plt.figure(figsize=(9, 4.5))
plt.scatter(df_limpio['Tiempo_s'], df_limpio['Temperatura_C'], color='blue', alpha=0.6, label='Datos Limpios')
plt.plot(X_extendido['Tiempo_s'], y_extendido, color='darkorange', linewidth=2.5, label='Modelo Polinomial (Curva)')
plt.scatter([tiempo_usuario], [prediccion], color='green', s=150, zorder=5, marker='*', label=f'Tu Predicción ({tiempo_usuario}s, {prediccion:.1f}°C)')

plt.ylim(18, max(prediccion + 3, 35))
plt.xlabel('Tiempo (s)', fontweight='bold')
plt.ylabel('Temperatura (°C)', fontweight='bold')
plt.title('Modelo de Predicción Curvilínea (Lección 7)', fontweight='bold')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()