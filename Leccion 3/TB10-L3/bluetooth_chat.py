import bluetooth
import struct
from micropython import const

IRQ_CONNECT = const(1)
IRQ_DISCONNECT = const(2)
IRQ_WRITE = const(3)


class BluetoothChat:

    UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    UART_TX = (
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_NOTIFY,
    )

    UART_RX = (
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_WRITE,
    )

    UART_SERVICE = (
        UART_UUID,
        (UART_TX, UART_RX),
    )

    def __init__(self, nombre="ESP32"):

        self.nombre = nombre

        self.ble = bluetooth.BLE()
        self.ble.active(True)

        ((self.tx, self.rx),) = self.ble.gatts_register_services(
            (self.UART_SERVICE,)
        )

        self.conexiones = set()
        self.mensaje = None

        self.ble.irq(self._irq)

        self._advertise()

    def _payload(self):

        nombre = self.nombre.encode()

        payload = bytearray()

        payload += struct.pack("BBB", 2, 0x01, 0x06)

        payload += struct.pack("BB", len(nombre) + 1, 0x09)
        payload += nombre

        return payload

    def _advertise(self):

        self.ble.gap_advertise(
            100000,
            adv_data=self._payload()
        )

    def _irq(self, event, data):

        if event == IRQ_CONNECT:

            conn, _, _ = data

            self.conexiones.add(conn)

            print("Bluetooth conectado")

        elif event == IRQ_DISCONNECT:

            conn, _, _ = data

            if conn in self.conexiones:
                self.conexiones.remove(conn)

            print("Bluetooth desconectado")

            self._advertise()

        elif event == IRQ_WRITE:

            self.mensaje = self.ble.gatts_read(self.rx).decode().strip()

    def enviar(self, texto):

        if isinstance(texto, str):
            texto = texto.encode()

        for conn in self.conexiones:
            self.ble.gatts_notify(conn, self.tx, texto)

    def hay_mensaje(self):

        return self.mensaje is not None

    def leer(self):

        texto = self.mensaje
        self.mensaje = None
        return texto
