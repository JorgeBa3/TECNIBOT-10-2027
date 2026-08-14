import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# 1. Cargar datos limpios y entrenar modelo polinomial
df = pd.read_csv('datos_limpios.csv')
X, y = df[['Tiempo_s']], df['Temperatura_C']

modelo = make_pipeline(PolynomialFeatures(degree=2), LinearRegression()).fit(X, y)

# 2. Predicción interactiva
t_user = float(input("Ingresa el tiempo en segundos para predecir: "))
pred = modelo.predict(pd.DataFrame({'Tiempo_s': [t_user]}))[0]
print(f"🔮 A los {t_user}s la temperatura será de ~{pred:.1f} °C")

# 3. Graficar datos, curva y predicción
X_ext = pd.DataFrame({'Tiempo_s': np.linspace(df['Tiempo_s'].min(), max(df['Tiempo_s'].max(), t_user), 100)})

plt.figure(figsize=(8, 4))
plt.scatter(df['Tiempo_s'], df['Temperatura_C'], color='blue', alpha=0.6, label='Datos Limpios')
plt.plot(X_ext['Tiempo_s'], modelo.predict(X_ext), color='darkorange', lw=2, label='Modelo Polinomial (Grado 2)')
plt.scatter([t_user], [pred], color='green', s=140, marker='*', zorder=5, label=f'Predicción ({t_user}s: {pred:.1f}°C)')

plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.title('Predicción Curvilínea de Temperatura')
plt.legend()
plt.grid(True, ls='--', alpha=0.5)
plt.tight_layout()
plt.show()