from machine import Pin
from time import sleep

# 1. Definimos los componentes (Pines de la tarjeta)
rojo = Pin(2, Pin.OUT)
amarillo = Pin(4, Pin.OUT)
verde = Pin(5, Pin.OUT)

print("¡Semáforo en marcha!")

# 2. Bucle infinito para que se repita siempre
while True:
    # --- LUZ ROJA ---
    rojo.value(1)       # Enciende
    sleep(3)            # Espera 3 segundos
    rojo.value(0)       # Apaga

    # --- LUZ VERDE ---
    verde.value(1)      # Enciende
    sleep(3)            # Espera 3 segundos
    verde.value(0)      # Apaga

    # --- LUZ AMARILLA ---
    amarillo.value(1)   # Enciende
    sleep(1)            # Espera 1 segundo
    amarillo.value(0)   # Apaga