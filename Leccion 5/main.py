import time
from machine import ADC, Pin

# 1. Configuración de Entradas Analógicas

pot_temp = ADC(Pin(34))      # Potenciómetro (Temperatura)
ldr_luz = ADC(Pin(35))       # Fotoresistencia (Luz)

# Ajuste de voltaje (0 - 3.3V en ESP32)
pot_temp.atten(ADC.ATTN_11DB)
ldr_luz.atten(ADC.ATTN_11DB)

def leer_sensores():

    """Lee y mapea los sensores analógicos."""
    raw_temp = pot_temp.read()
    temp_celsius = (raw_temp / 4095.0) * 100.0
    raw_luz = ldr_luz.read()
    porcentaje_luz = (raw_luz / 4095.0) * 100.0
    return temp_celsius, porcentaje_luz

# 2. Configuración de Registro y Límite

NOMBRE_ARCHIVO = "datos_sensores.csv"
MAX_REGISTROS = 40  # Límite máximo de datos a guardar

# Crear/Reiniciar el archivo CSV con sus encabezados
with open(NOMBRE_ARCHIVO, "w") as f:
    f.write("Muestra,Tiempo_s,Temperatura_C,Luz_Porcentaje\n")

print(f"Archivo '{NOMBRE_ARCHIVO}' preparado.")
print(f"Iniciando registro de {MAX_REGISTROS} muestras en memoria Flash...")

# 3. Bucle de recolección de datos
contador_muestras = 0
tiempo_inicio = time.time()



while contador_muestras < MAX_REGISTROS:
    temp, luz = leer_sensores()
    segundos_transcurridos = time.time() - tiempo_inicio
    contador_muestras += 1
    # Formatear la línea de datos
    linea_csv = f"{contador_muestras},{segundos_transcurridos},{temp:.2f},{luz:.2f}\n"
    # Guardar en modo 'append' ('a')
    with open(NOMBRE_ARCHIVO, "a") as f:
        f.write(linea_csv)

    print(f"[{contador_muestras}/{MAX_REGISTROS}] Temp: {temp:.1f}°C | Luz: {luz:.1f}%")
    time.sleep(1)  # Toma un dato cada 1 segundo

print(f"Se han guardado con éxito los {MAX_REGISTROS} datos en '{NOMBRE_ARCHIVO}'.")