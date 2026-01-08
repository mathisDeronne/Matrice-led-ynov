import bluetooth
import time
import max7219
from machine import Pin, SPI
from bluetooth import BLE

# =========================
# MATRICES
# =========================
spi = SPI(1, baudrate=2_000_000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))
cs_gauche = Pin(17, Pin.OUT)
cs_milieu = Pin(16, Pin.OUT)
cs_droite = Pin(21, Pin.OUT)

d1 = max7219.Matrix8x8(spi, cs_gauche, 4)
d2 = max7219.Matrix8x8(spi, cs_milieu, 4)
d3 = max7219.Matrix8x8(spi, cs_droite, 4)

for d in (d1, d2, d3):
    d.brightness(5)
    d.fill(0)
    d.show()

WIDTH = 32
TOTAL_WIDTH = 96

# =========================
# FILE D’ATTENTE ET TEXTE COURANT
# =========================
queue = []             # nouveaux messages en attente
current_text = "READY" # dernier texte affiché

# =========================
# BLE UART
# =========================
SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
CHAR_UUID_RX = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
CHAR_UUID_TX = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

def advertising_payload(name):
    payload = bytearray()
    payload += b"\x02\x01\x06"
    name_bytes = name.encode()
    payload += bytes([len(name_bytes)+1, 0x09]) + name_bytes
    return payload

class BLE_UART:
    def __init__(self):
        self.ble = BLE()
        self.ble.active(True)
        self.ble.irq(self.irq)
        UART_SERVICE = (
            SERVICE_UUID,
            (
                (CHAR_UUID_RX, bluetooth.FLAG_WRITE),
                (CHAR_UUID_TX, bluetooth.FLAG_NOTIFY),
            ),
        )
        ((self.rx_handle, self.tx_handle),) = self.ble.gatts_register_services((UART_SERVICE,))
        self.connections = set()
        self.start_advertising()

    def irq(self, event, data):
        global queue
        if event == 1:  # CONNECT
            conn_handle, _, _ = data
            self.connections.add(conn_handle)

        elif event == 2:  # DISCONNECT
            conn_handle, _, _ = data
            self.connections.remove(conn_handle)
            self.start_advertising()

        elif event == 3:  # WRITE
            value = self.ble.gatts_read(self.rx_handle)
            try:
                new_text = value.decode().strip()
                print("Texte reçu :", new_text)
                queue.append(new_text)  # ajoute à la file
            except:
                pass

    def start_advertising(self):
        adv = advertising_payload("ESP32-MATRIX")
        self.ble.gap_advertise(100_000, adv)

uart = BLE_UART()

# =========================
# BOUCLE PRINCIPALE – SCROLL INFINI
# =========================
while True:
    # --- Réinstanciation des matrices ---
    d1 = max7219.Matrix8x8(spi, cs_gauche, 4)
    d2 = max7219.Matrix8x8(spi, cs_milieu, 4)
    d3 = max7219.Matrix8x8(spi, cs_droite, 4)
    # Si des messages en attente → on les prend
    if queue:
        current_text = queue.pop(0)

    text_width = len(current_text) * 8
    for x in range(TOTAL_WIDTH, -text_width - 1, -1):

        # Affiche le texte sur les 3 barrettes
        d1.fill(0)
        d1.text(current_text, x - 0, 0, 1)
        d1.show()

        d2.fill(0)
        d2.text(current_text, x - WIDTH, 0, 1)
        d2.show()

        d3.fill(0)
        d3.text(current_text, x - 2 * WIDTH, 0, 1)
        d3.show()

        time.sleep(0.05)

    # Quand le texte a fini → si queue vide, il sera de nouveau affiché
