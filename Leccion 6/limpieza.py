import pandas as pd
# 1. Cargar el CSV
df = pd.read_csv('datos_sensores.csv')
print(f"Filas originales: {len(df)}")

# 2. LIMPIEZA L6: Eliminar únicamente filas con datos faltantes (nulos)
df_limpio = df.dropna()
print(f"Filas después de borrar nulos: {len(df_limpio)}")

# Guardar el archivo limpio para la regresión
df_limpio.to_csv('datos_limpios.csv', index=False)