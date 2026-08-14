import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# 1. Cargar datos
df = pd.read_csv('datos.csv')

# 2. Limpiar datos
df = df.dropna()

df = df[
    (df['Temperatura_C'] >= 0) &
    (df['Temperatura_C'] <= 50) &
    (df['Luz_lux'] >= 0)
]


# 3. Seleccionar los datos para K-means
X = df[['Temperatura_C', 'Luz_lux']]


# 4. Escalar los datos
escalador = StandardScaler()
X_escalado = escalador.fit_transform(X)


# 5. Crear y entrenar K-means
modelo = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = modelo.fit_predict(X_escalado)


# 6. Graficar los grupos
plt.figure(figsize=(8, 5))

for cluster in range(4):

    grupo = df[df['Cluster'] == cluster]

    plt.scatter(
        grupo['Temperatura_C'],
        grupo['Luz_lux'],
        label=f'Cluster {cluster}'
    )


# Centroides
centros = escalador.inverse_transform(
    modelo.cluster_centers_
)

plt.scatter(
    centros[:, 0],
    centros[:, 1],
    marker='X',
    s=200,
    color='black',
    label='Centroides'
)

plt.xlabel('Temperatura (°C)')
plt.ylabel('Luz (lux)')
plt.title('K-means: Temperatura y Luz')
plt.legend()
plt.grid(True)
plt.show()


# 7. Probar una nueva medición
temperatura = float(input('Temperatura (°C): '))
luz = float(input('Luz (lux): '))

nuevo = escalador.transform([[temperatura, luz]])

cluster = modelo.predict(nuevo)[0]

print(f'\nLa nueva medición pertenece al Cluster {cluster}')