# RPi-basic
# Raspberry Pi: GPIO, LEDs y sensores

Vamos a usar la **Raspberry Pi** para controlar pines GPIO: empezaremos encendiendo un **LED** y terminaremos leyendo **sensores** sencillos.

---

## Esquema de pines (GPIO)
<img width="1299" height="746" alt="Imagen36" src="https://github.com/user-attachments/assets/d086a86f-fd3a-4579-b35f-ea3be32cf9ef" />

---

## Lo mínimo que hay que saber de los GPIO

- La tira de 40 pines mezclan:
  - **Alimentación**:  
    - `3V3` (3.3 voltios) → para alimentar circuitos lógicos.  
    - `5V` → *ojo*, NO conectar nunca a un pin GPIO, solo a módulos que lo permitan.
  - **GND** → tierra / referencia común.
  - **GPIO n** → pines de propósito general, los que usaremos para LEDs y sensores.
  - Pines especiales: I2C (`GPIO 2/3`), SPI (`GPIO 10/9/11`), UART (`GPIO 14/15`), PWM hardware (`GPIO 12/13/18/19`).

- **Tensión de trabajo de los GPIO: 3.3 V**
  - Más de 3.3 V puede freír el pin o la placa.
  - La corriente máxima por pin es baja (del orden de decenas de mA). Para un LED usamos SIEMPRE **resistencia** (por ejemplo 220–330 Ω).

- **Dos numeraciones distintas**:
  - **Número físico de pin** (1–40, el de la fila de pines).
  - **Número GPIO** (BCM: 2, 3, 4, 17, 27, …).  
    En el código usaremos **BCM**, que es lo estándar en ejemplos de Python.

- Esquema típico para un LED:
  - Escogemos, por ejemplo, **GPIO 17** (pin físico 11).
  - Conexión:
    - GPIO 17 → resistencia 220–330 Ω → ánodo (+) del LED.
    - Cátodo (–) del LED → un pin **GND** cualquiera.
  - Cuando el pin está a nivel alto (3.3 V) el LED se enciende; a nivel bajo, se apaga.

---

## Base para programar GPIO en Raspberry Pi OS (Python)

Se mostrará la programación con Python en Raspberry Pi OS.  
Se pueden usar dos librerías:

- [`gpiozero`](https://gpiozero.readthedocs.io) → más sencilla, perfecta para clase.
- `RPi.GPIO` → más “de bajo nivel”, útil para entender mejor lo que pasa.

En las Raspberry Pi modernas **gpiozero viene ya instalado**. Si hiciera falta:

```bash
sudo apt update
sudo apt install python3-gpiozero
```
---

## Estructura básica de un programa GPIO en Python

### 1. Declaración de variables
Nombres para los elementos que vamos a usar:
```python
LED_PIN = 17      # GPIO que usaremos para el LED
BTN_PIN = 27      # GPIO que usaremos para el botón/sensor
```

### 2. Declaración / configuración de los pines
Indicamos al sistema qué hace cada pin (entrada o salida, pull-up/pull-down, etc.).

**Con gpiozero** la configuración se hace al crear los objetos:
```python
from gpiozero import LED, Button

led = LED(LED_PIN)                        # salida
boton = Button(BTN_PIN, pull_up=True)     # entrada con pull-up interno
```

**Con RPi.GPIO** sería algo así:
```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)                    # usamos numeración BCM
GPIO.setup(LED_PIN, GPIO.OUT)             # LED como salida
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # botón como entrada
```

### 3. Manejo de los pines declarados
Normalmente tendremos:
- Un bucle principal, o
- Callbacks que se ejecutan cuando pasa algo.

**Ejemplo con bucle:**
```python
while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
```

**Ejemplo con callbacks/eventos:**
```python
def on_press():
    led.on()

def on_release():
    led.off()

boton.when_pressed = on_press
boton.when_released = on_release
```

**Idea clave:** primero declaras variables, luego configuras los pines y, por último, los usas dentro de la lógica del programa.

---

## 1. Encender un LED con gpiozero (recomendado)

**Archivo:** `led_blink.py`
```python
from gpiozero import LED
from time import sleep

# Usaremos la numeración BCM
LED_PIN = 17      # GPIO17 (pin físico 11)

led = LED(LED_PIN)

print("Parpadeando LED en GPIO17. Ctrl+C para salir.")
try:
    while True:
        led.on()          # LED encendido
        sleep(0.5)
        led.off()         # LED apagado
        sleep(0.5)
except KeyboardInterrupt:
    pass  # salir limpio
```

**Ejecución:**
```bash
python3 led_blink.py
```

Si da problemas de permisos, ejecutar con `sudo python3 led_blink.py` (aunque en Raspberry Pi OS normal no suele hacer falta).

---

## 2. Plantilla general con gpiozero: salida (LED) + entrada (botón/sensor digital)

Esta estructura nos vale luego para muchos sensores digitales (PIR, final de carrera, etc.).
```python
from gpiozero import LED, Button
from signal import pause

LED_PIN = 17      # GPIO para el LED
BTN_PIN = 27      # GPIO para el botón o sensor digital

led = LED(LED_PIN)
btn = Button(BTN_PIN, pull_up=True)  # usa resistencia interna de pull-up

def on_press():
    print("Pulsado / activado → LED ON")
    led.on()

def on_release():
    print("Soltado / desactivado → LED OFF")
    led.off()

btn.when_pressed = on_press
btn.when_released = on_release

print("Listo. Pulsa el botón (GPIO27) para controlar el LED (GPIO17). Ctrl+C para salir.")
pause()  # mantiene el programa vivo esperando eventos
```

**Conexión típica para el botón/sensor digital:**

- Un lado del botón → GND.
- Otro lado → GPIO 27.

Con `pull_up=True` el pin está normalmente a "1" (3.3 V) y cuando pulsas baja a "0".

---

## 3. Versión "bajo nivel" con RPi.GPIO (opcional)

De la siguiente manera sería cómo se hace "a pelo":

### LED parpadeante
```python
import RPi.GPIO as GPIO
import time

LED_PIN = 17

# Modo BCM = usamos los números GPIO (no los físicos)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    print("Parpadeando LED con RPi.GPIO. Ctrl+C para salir.")
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # encender
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)   # apagar
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # deja los pines en estado limpio
```

### Leer un sensor/botón
```python
import RPi.GPIO as GPIO
import time

BTN_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Leyendo botón en GPIO27. Ctrl+C para salir.")
    while True:
        if GPIO.input(BTN_PIN) == GPIO.LOW:   # pulsado (a GND)
            print("PULSADO")
        else:
            print("NO pulsado")
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

---

## De LED a sensores

La idea general::

1. **LED**  
   Configurar un GPIO como salida y cambiarlo entre alto/bajo.

2. **Botón / pulsador**  
   Configurar un GPIO como entrada con resistencia de pull-up o pull-down.

3. **Sensores digitales (PIR, final de carrera, sensor de choque, etc.)**  
   Se tratan igual que el botón: leen 0/1.

4. **Sensores analógicos (temperatura, luz, etc.)**  
   La Raspberry Pi no tiene entradas analógicas, así que usaremos un convertidor ADC externo o sensores que ya den salida digital.

La lógica en el código será la misma: leer valores y actuar (encender LED, registrar datos, etc.).

---

## Buenas prácticas rápidas

- Nunca metas 5 V en un GPIO.
- Usa siempre resistencia con LEDs.
- Comprueba dos veces el pin en el esquema antes de conectar.
- `GPIO.cleanup()` (en RPi.GPIO) al terminar para no dejar el sistema en un estado raro.
