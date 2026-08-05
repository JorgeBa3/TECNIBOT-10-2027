from machine import Pin, SoftI2C
from mpu6050 import MPU6050
from bluetooth_chat import BluetoothChat

import math
import time

# Bluetooth
bt = BluetoothChat("ALARMA-SISMICA")

# LED del ESP32
led = Pin(2, Pin.OUT)

# Sensor
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c)

# Umbral de detección
UMBRAL = 0.25

# Número de lecturas consecutivas necesarias
LECTURAS = 10
contador = 0
print("Sistema iniciado")

while True:
    ax, ay, az, gx, gy, gz = mpu.leer()
    magnitud = math.sqrt(ax**2 + ay**2 + az**2)
    vibracion = abs(magnitud - 1)
    print(round(vibracion, 3))
    
    if vibracion > UMBRAL:
        contador += 1
    else:
        contador = 0
        led.off()
    if contador >= LECTURAS:
        led.on()
        mensaje = "ALERTA SISMICA \n"
        print(mensaje)
        bt.enviar(mensaje)
        contador = 0
        # Esperar 3 segundos para no enviar muchas alertas
        time.sleep(3)
    time.sleep_ms(100)
