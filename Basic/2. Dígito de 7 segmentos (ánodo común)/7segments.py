import RPi.GPIO as GPIO
import time

# Usamos numeración BCM (número GPIO, no número de pin físico)
GPIO.setmode(GPIO.BCM)

# --- DECLARACIÓN DE PINES (cada segmento) ---
SEG_A = 5
SEG_B = 6
SEG_C = 13
SEG_D = 19
SEG_E = 26
SEG_F = 21
SEG_G = 20

SEGMENTS = [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G]

# Display de ÁNODO COMÚN:
#   - Común del display → 3V3
#   - Para ENCENDER segmento: GPIO a LOW
#   - Para APAGAR segmento: GPIO a HIGH
ON = GPIO.LOW
OFF = GPIO.HIGH

# CONFIGURACIÓN DE LOS PINES
for pin in SEGMENTS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, OFF)   # empezamos con todo apagado

def clear():
    """Apaga todos los segmentos."""
    for pin in SEGMENTS:
        GPIO.output(pin, OFF)

# MANEJO DE LOS PINES (dibujar dígitos)

def show_1():
    """Muestra el dígito 1 (segmentos b y c)."""
    clear()
    GPIO.output(SEG_B, ON)
    GPIO.output(SEG_C, ON)

def show_2():
    """Muestra el dígito 2 (segmentos a, b, d, e, g)."""
    clear()
    GPIO.output(SEG_A, ON)
    GPIO.output(SEG_B, ON)
    GPIO.output(SEG_D, ON)
    GPIO.output(SEG_E, ON)
    GPIO.output(SEG_G, ON)

# MAIN

try:
    print("Mostrando 1 y 2 alternando cada 1 segundo. Ctrl+C para salir.")
    while True:
        show_1()
        time.sleep(1)
        show_2()
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+C para terminar
    pass

finally:
    clear()
    GPIO.cleanup()
