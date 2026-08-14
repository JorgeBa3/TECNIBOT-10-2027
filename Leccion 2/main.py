import time
from machine import ADC, Pin

# 1. Componentes
rojo = Pin(5, Pin.OUT)
amarillo = Pin(4, Pin.OUT)
verde = Pin(2, Pin.OUT)

# LDR en Pin 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # Rango 0 a 3.3V 

# Umbral de activación
UMBRAL_LUZ = 400

def apagar_leds():
    """Apaga todos los LEDs"""
    rojo.value(0)
    amarillo.value(0)
    verde.value(0)

def semaforo_activo():
    """Verifica si hay suficiente luz"""
    return ldr.read() >= UMBRAL_LUZ

def secuencia_luz(pin_luz, segundos):
    """Enciende un LED durante X segundos. 
    Retorna False si se tapa la LDR"""
    apagar_leds()
    pin_luz.value(1)
    
    # Verifica cada 0.1 segundos durante toda la secuencia
    iteraciones = int(segundos * 10)
    for i in range(iteraciones):
        if not semaforo_activo():  # Si se tapa durante la fase
            apagar_leds()
            return False
        time.sleep(0.1)
    
    return True

# Inicialización
print("¡Semáforo Fotosensible Listo!")
time.sleep(2)
# 3. Bucle Principal
while True:
    if semaforo_activo():
        # Hay luz -> Opera el semáforo
        print("Modo DÍA - Semáforo activo")
        # Fase Rojo (10s)
        if not secuencia_luz(rojo, 10):
            continue
        # Fase Verde (15s)
        if not secuencia_luz(verde, 15):
            continue
        # Fase Amarillo (5s)
        if not secuencia_luz(amarillo, 5):
            continue
    else:
        # Oscuridad -> Pausa
        apagar_leds()
        print(f"Modo NOCHE - Pausa (LDR: {ldr.read()})")
        time.sleep(0.5)