import RPi.GPIO as GPIO
import time

# Usamos numeración BCM (número GPIO, no número de pin físico)
GPIO.setmode(GPIO.BCM)

# DECLARACIÓN DE PINES (cada segmento)
# Orden: a, b, c, d, e, f, g
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

# TABLA DE DÍGITOS (ESTILO ARDUINO)
# 1 = segmento encendido, 0 = apagado
# Orden de columnas: a, b, c, d, e, f, g
DIGITS = [
    [1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 1, 1, 0, 0, 1, 1],  # 4
    [1, 0, 1, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1],  # 6
    [1, 1, 1, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 0, 0, 1, 1],  # 9
]

try:
    print("Mostrando del 0 al 9, cambiando cada 1 segundo. Ctrl+C para salir.")

    while True:
        # PRIMER for: recorre los dígitos 0..9
        for num in range(10):
            patron = DIGITS[num]  # fila de la "matriz" para este número

            # SEGUNDO for: recorre los segmentos a..g
            for i in range(len(SEGMENTS)):
                valor = patron[i]   # 0 o 1
                pin = SEGMENTS[i]

                if valor == 1:
                    GPIO.output(pin, ON)   # encender segmento
                else:
                    GPIO.output(pin, OFF)  # apagar segmento

            time.sleep(1)  # esperamos 1 segundo antes de pasar al siguiente dígito

except KeyboardInterrupt:
    # Ctrl+C para terminar
    pass

finally:
    # Apagamos todo y limpiamos
    for pin in SEGMENTS:
        GPIO.output(pin, OFF)
    GPIO.cleanup()

