# Importa las librerias
from machine import Pin
from utime import sleep

# Número de pin
pin = Pin(2, Pin.OUT)   

print("Inicio Lección 1")
while True:
    try:
        pin.value(not pin.value())
        sleep(1)  # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")