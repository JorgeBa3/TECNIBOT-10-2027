mpremote connect port:rfc2217://localhost:4000 fs cp  '.\TECNIBOT-10-2027\Leccion 1\ssd1306.py' :ssd1306.py + fs cp '.\TECNIBOT-10-2027\Leccion 1\main.py':main.py
mpremote connect port:rfc2217://localhost:4000 run '.\TECNIBOT-10-2027\Leccion 1\main.py'

from machine import Pin
from utime import sleep

pin = Pin(2, Pin.OUT)   # número de pin, no "LED"

print("Leccion 1")
while True:
    try:
        pin.value(not pin.value())
        sleep(1)  # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")