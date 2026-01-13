import bluetooth
import time
import max7219
from machine import Pin, SPI
from bluetooth import BLE
import machine

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
queue = []
current_text = "READY"

# =========================
# VARIABLES BLE (NOUVEAU)
# =========================
rx_buffer = ""
rx_last_time = 0
RX_TIMEOUT_MS = 300   # délai max entre chunks BLE

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
        global rx_buffer, rx_last_time, queue

        if event == 1:  # CONNECT
            conn_handle, _, _ = data
            self.connections.add(conn_handle)

        elif event == 2:  # DISCONNECT
            conn_handle, _, _ = data
            self.connections.discard(conn_handle)
            self.start_advertising()

        elif event == 3:  # WRITE
            value = self.ble.gatts_read(self.rx_handle)
            try:
                chunk = value.decode()
                rx_buffer += chunk
                rx_last_time = time.ticks_ms()

                # Fin explicite si \n reçu
                if "\n" in rx_buffer:
                    full_text = rx_buffer.replace("\n", "").strip()
                    print("Texte complet reçu :", full_text)
                    queue.append(full_text)
                    rx_buffer = ""

            except:
                pass

    def start_advertising(self):
        adv = advertising_payload("ESP32-MATRIX")
        self.ble.gap_advertise(100_000, adv)

uart = BLE_UART()
ranger = "Pensez a ranger le materiel et a nettoyer les tables avant de partir"
# =========================
# BOUCLE PRINCIPALE – SCROLL
# =========================
while True:

    # --- TIMEOUT BLE (NOUVEAU) ---
    if rx_buffer and time.ticks_diff(time.ticks_ms(), rx_last_time) > RX_TIMEOUT_MS:
        full_text = rx_buffer.strip()
        print("Texte reçu (timeout) :", full_text)
        
        # Textes pré-définis
        if full_text == "!RANGER":
            full_text = ranger
        
        if full_text == "!RESET":
            machine.reset()

        if full_text == "!HELP":
            full_text = "Help at https://github.com/mathisDeronne/Matrice-led-ynov"
        
        
        
        
        queue.append(full_text)
        rx_buffer = ""

    # --- Réinstanciation des matrices ---
    d1 = max7219.Matrix8x8(spi, cs_gauche, 4)
    d2 = max7219.Matrix8x8(spi, cs_milieu, 4)
    d3 = max7219.Matrix8x8(spi, cs_droite, 4)

    for d in (d1, d2, d3):
        d.brightness(5)

    # Nouveau message ?
    if queue:
        current_text = queue.pop(0)

    text_width = len(current_text) * 8

    for x in range(TOTAL_WIDTH, -text_width - 1, -1):

        d1.fill(0)
        d1.text(current_text, x, 0, 1)
        d1.show()

        d2.fill(0)
        d2.text(current_text, x - WIDTH, 0, 1)
        d2.show()

        d3.fill(0)
        d3.text(current_text, x - 2 * WIDTH, 0, 1)
        d3.show()

        time.sleep(0.05)


