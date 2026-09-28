from machine import Pin, PWM, ADC
from utime import sleep
import math

# Importar librerías y configurar pines
pot_temp = ADC(Pin(34))       # potenciómetro = temperatura de la casa
ldr_luz = ADC(Pin(35))        # LDR = luz natural
verde = Pin(2, Pin.OUT)       # LED DÍA
amarillo = Pin(4, Pin.OUT)    # LED TARDE
rojo = Pin(5, Pin.OUT)        # LED NOCHE
buzzer = PWM(Pin(25))         # alarma de salida
pot_temp.atten(ADC.ATTN_11DB) # 0 a 3.3 V en el ADC
ldr_luz.atten(ADC.ATTN_11DB)
verde.off()
amarillo.off()
rojo.off()
buzzer.duty(0)
modos = ["DIA", "TARDE", "NOCHE"]  # solo para guiar la recolección
luces = [verde, amarillo, rojo]    # orden del camino de salida
paso_salida = 0
UMBRAL_TEMP = 80              # temp y luz altas = emergencia
UMBRAL_LUZ = 80

# Definir funciones
def leer():
    temp = (pot_temp.read() / 4095.0) * 100.0  # ADC 0-4095 -> 0-100
    luz = (ldr_luz.read() / 4095.0) * 100.0
    return (temp, luz)            # un punto (x, y) para el clustering

def dist(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)  # distancia euclidiana

def kmeans(datos, k=3):
    n = len(datos)
    centros = [datos[i * n // k] for i in range(k)]  # un centro por modo
    for _ in range(8):
        grupos = [[] for _ in range(k)]
        for p in datos:
            d = [dist(p, c) for c in centros]
            grupos[d.index(min(d))].append(p)  # cada punto al centro más cercano
        for i in range(k):
            if grupos[i]:
                mx = sum(p[0] for p in grupos[i]) / len(grupos[i])
                my = sum(p[1] for p in grupos[i]) / len(grupos[i])
                centros[i] = (mx, my)          # el centro se mueve al promedio
    return centros

def apagar_luces():
    verde.off()
    amarillo.off()
    rojo.off()

def aplicar(modo):
    buzzer.duty(0)
    apagar_luces()
    if modo == "DIA":
        verde.on()                # de día: luz principal
    elif modo == "TARDE":
        amarillo.on()             # tarde: luz suave
    else:
        rojo.on()                 # de noche: luz de pasillo

def camino_salida():
    global paso_salida
    buzzer.freq(2000)
    buzzer.duty(512)              # suena la alarma
    apagar_luces()
    luces[paso_salida].on()       # una LED a la vez: marca la salida
    paso_salida = (paso_salida + 1) % 3

# 1) Recolectar CSV sin etiquetas (K-means las va a descubrir)
archivo = open("datos.csv", "w")
archivo.write("Temperatura_C,Luz\n")
for modo in modos:
    print("Simula la casa:", modo)
    print("  DIA = luz alta, pot medio-alto (no al tope)")
    print("  TARDE = luz y pot a la mitad")
    print("  NOCHE = tapa la LDR y baja el pot")
    sleep(4)                      # tiempo para colocar los sensores
    for i in range(8):
        p = leer()
        archivo.write("{:.2f},{:.2f}\n".format(p[0], p[1]))
        print(i + 1, "temp=", round(p[0], 1), "luz=", round(p[1], 1))
        sleep(0.4)
archivo.close()

# 2) K-means a mano (K = 3) en la ESP32
datos = []
archivo = open("datos.csv")
archivo.readline()                # salta el encabezado
for linea in archivo:
    a, b = linea.strip().split(",")
    datos.append((float(a), float(b)))
archivo.close()
centros = kmeans(datos)
orden = sorted(range(3), key=lambda i: centros[i][1])  # de menos luz a más luz
nombres = [""] * 3
nombres[orden[0]] = "NOCHE"       # el de menos luz = de noche
nombres[orden[1]] = "TARDE"
nombres[orden[2]] = "DIA"         # el de más luz = de día
print("Centroides (el modelo no sabía los nombres):")
for i in range(3):
    print(" ", nombres[i], "temp=", round(centros[i][0], 1), "luz=", round(centros[i][1], 1))
print("Emergencia: pot al maximo y mucha luz")

# 3) En vivo: dia/tarde/noche, o alarma si temp y luz estan altas
while True:
    p = leer()
    if p[0] > UMBRAL_TEMP and p[1] > UMBRAL_LUZ:
        camino_salida()           # buzzer + 3 LEDs en secuencia
        print("EMERGENCIA camino de salida", "temp=", round(p[0], 1), "luz=", round(p[1], 1))
    else:
        d = [dist(p, c) for c in centros]
        modo = nombres[d.index(min(d))]  # gana el centro más cercano
        aplicar(modo)
        print(modo, "temp=", round(p[0], 1), "luz=", round(p[1], 1))
    sleep(0.25)
