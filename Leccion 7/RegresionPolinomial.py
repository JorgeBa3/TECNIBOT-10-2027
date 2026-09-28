ARCHIVO_LIMPIO = "datos_limpios.csv"

# 1. Cargar, en la propia ESP32, los datos ya limpios que guardó limpieza.py
datos = []
with open(ARCHIVO_LIMPIO) as archivo:
    archivo.readline()  # salta el encabezado
    for linea in archivo:
        t_txt, temp_txt = linea.strip().split(",")
        datos.append((float(t_txt), float(temp_txt)))

print("Muestras cargadas para el entrenamiento: {}".format(len(datos)))

# 2. Sumatorias del sistema de ecuaciones normales para y = a + b*t + c*t^2
#    (regresión polinomial de grado 2, calculada a mano, sin numpy ni sklearn)
n = len(datos)
s_t = s_t2 = s_t3 = s_t4 = s_y = s_ty = s_t2y = 0.0
for t, y in datos:
    t2 = t * t
    s_t += t
    s_t2 += t2
    s_t3 += t2 * t
    s_t4 += t2 * t2
    s_y += y
    s_ty += t * y
    s_t2y += t2 * y

matriz = [
    [n, s_t, s_t2, s_y],
    [s_t, s_t2, s_t3, s_ty],
    [s_t2, s_t3, s_t4, s_t2y],
]

# 3. Resolver el sistema 3x3 por eliminación gaussiana (a, b, c)
def resolver_3x3(m):
    for i in range(3):
        pivote = m[i][i]
        for j in range(i, 4):
            m[i][j] /= pivote
        for k in range(3):
            if k != i:
                factor = m[k][i]
                for j in range(i, 4):
                    m[k][j] -= factor * m[i][j]
    return m[0][3], m[1][3], m[2][3]

a, b, c = resolver_3x3(matriz)

def predecir(t):
    return a + b * t + c * t * t

# 4. Predicción interactiva
tiempo_usuario = float(input("Ingresa el tiempo en segundos para predecir: "))
prediccion = predecir(tiempo_usuario)
print("\nA los {}s la temperatura estimada es: {:.1f} °C".format(tiempo_usuario, prediccion))

# 5. Curva del modelo en ASCII: datos reales vs. curva polinomial y tu predicción
print("\nCurva del modelo (cada '*' representa la temperatura estimada en ese segundo):")
t_max = max(t for t, _ in datos)
t_max = max(t_max, tiempo_usuario)
paso = max(1, int(t_max / 20))
for t in range(0, int(t_max) + 1, paso):
    temp = predecir(t)
    barra = "*" * int(max(0, min(temp, 100)) / 100 * 40)
    marca = "  <-- tu predicción" if abs(t - tiempo_usuario) < paso else ""
    print("t={:4d}s | {} {:.1f}°C{}".format(t, barra, temp, marca))
