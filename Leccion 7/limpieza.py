from machine import ADC, Pin
from utime import sleep, time

# 1. Configurar el sensor de temperatura (potenciómetro), igual que en lecciones anteriores
pot_temp = ADC(Pin(34))
pot_temp.atten(ADC.ATTN_11DB)

def leer_temp():
    return (pot_temp.read() / 4095.0) * 100.0  # ADC 0-4095 -> 0-100 °C simulados

def graficar_ascii(datos, titulo, ancho=40):
    print("\n" + titulo)
    for t, temp in datos:
        temp_valida = max(0, min(temp, 100))
        barra = "#" * int((temp_valida / 100) * ancho)
        print("t={:5.1f}s | {} {:.1f}°C".format(t, barra, temp))

# 2. RECOLECCIÓN: lee la temperatura cada segundo, directamente en la ESP32
MUESTRAS = 40
ARCHIVO_CRUDO = "datos_sensores_l7.csv"
ARCHIVO_LIMPIO = "datos_limpios.csv"

print("Mueve el potenciómetro. De vez en cuando llévalo al tope o al mínimo")
print("para generar lecturas 'raras' (outliers) que luego vamos a limpiar.\n")

datos_crudos = []
inicio = time()
with open(ARCHIVO_CRUDO, "w") as archivo:
    archivo.write("Tiempo_s,Temperatura_C\n")
    for i in range(MUESTRAS):
        t = time() - inicio
        temp = leer_temp()
        datos_crudos.append((t, temp))
        archivo.write("{},{:.2f}\n".format(t, temp))
        print("[{}/{}] t={}s  Temp={:.1f}°C".format(i + 1, MUESTRAS, t, temp))
        sleep(1)

# 3. LIMPIEZA L7: filtrar valores atípicos (temperaturas ilógicas para una casa: fuera de 0°C a 50°C)
datos_limpios = [(t, temp) for t, temp in datos_crudos if 0 <= temp <= 50]

print("\nMuestras crudas: {}".format(len(datos_crudos)))
print("Muestras después de limpiar: {}".format(len(datos_limpios)))
print("Outliers eliminados: {}".format(len(datos_crudos) - len(datos_limpios)))

# 4. COMPARACIÓN VISUAL (ASCII, directo en la consola de la ESP32): antes vs después de limpiar
graficar_ascii(datos_crudos, "ANTES de limpiar (con outliers)")
graficar_ascii(datos_limpios, "DESPUÉS de limpiar (0°C a 50°C)")

# 5. Guardar el archivo limpio en la memoria de la ESP32 para RegresionPolinomial.py
with open(ARCHIVO_LIMPIO, "w") as archivo:
    archivo.write("Tiempo_s,Temperatura_C\n")
    for t, temp in datos_limpios:
        archivo.write("{},{:.2f}\n".format(t, temp))

print("\nArchivo '{}' guardado en la ESP32.".format(ARCHIVO_LIMPIO))
