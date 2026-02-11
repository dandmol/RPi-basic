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

### 1. Importar librerías necesarias
```python
import RPi.GPIO as GPIO
from time import sleep
```

### 2. Configuración inicial del GPIO
```python
# Desactivar advertencias (warnings)
GPIO.setwarnings(False)

# Configurar el modo de numeración de pines
# GPIO.BOARD = usa el número físico del pin (1-40)
# GPIO.BCM = usa el número GPIO de Broadcom
GPIO.setmode(GPIO.BOARD)
```

### 3. Configurar cada pin (entrada o salida)
```python
# Configurar el pin 3 como SALIDA y establecer estado inicial en BAJO
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)

# Configurar el pin 5 como ENTRADA con resistencia pull-up
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
```

### 4. Usar los pines en el programa

**Para controlar una salida (LED):**
```python
GPIO.output(3, GPIO.HIGH)  # Encender (nivel alto, 3.3V)
GPIO.output(3, GPIO.LOW)   # Apagar (nivel bajo, 0V)
```

**Para leer una entrada (botón/sensor):**
```python
estado = GPIO.input(5)  # Lee el estado del pin 5
if estado == GPIO.LOW:
    print("Botón pulsado")
else:
    print("Botón soltado")
```

### 5. Limpieza al finalizar
```python
GPIO.cleanup()  # Libera los recursos y deja los pines en estado seguro
```

**Idea clave:** Primero importas las librerías, luego configuras el modo y los pines, después los usas en tu lógica, y al final limpias los recursos.
