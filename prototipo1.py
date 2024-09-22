import machine
import time

# Configuración de los pines
button = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Botón conectado a GP9 (con PULL_DOWN)
sound_sensor = machine.ADC(28)  # Sensor de sonido conectado a GP28 (ADC)

# Configuración de los pines LED con PWM
led_r = machine.PWM(machine.Pin(6))  # LED Rojo en GP6
led_g = machine.PWM(machine.Pin(7))  # LED Verde en GP7
led_b = machine.PWM(machine.Pin(8))  # LED Azul en GP8

# Configuración de frecuencia PWM (opcional)
led_r.freq(1000)  # Frecuencia de 1kHz para LED Rojo
led_g.freq(1000)  # Frecuencia de 1kHz para LED Verde
led_b.freq(1000)  # Frecuencia de 1kHz para LED Azul

# LED integrado de la Raspberry Pi Pico W
pico_led = machine.Pin('LED', machine.Pin.OUT)

# Encender el LED de la Raspberry Pi Pico para indicar que el código está corriendo
pico_led.value(1)

# Variable para controlar el estado del sensor de sonido (activado o desactivado)
sound_detection_enabled = False  # Comienza desactivado

# Variable para almacenar el último estado del botón
last_button_state = 0  # Estado anterior del botón

# Función para cambiar el color del LED RGB usando valores entre 0 y 255
def set_rgb_color(r, g, b):
    print(f"Configurando color LED RGB: Rojo={r}, Verde={g}, Azul={b}")
    
    # Convertir el rango de 0-255 a 0-65535 para PWM
    led_r.duty_u16(int(r * 257))  # 255 * 257 = 65535
    led_g.duty_u16(int(g * 257))
    led_b.duty_u16(int(b * 257))

# Función para detectar sonido y cambiar el color del LED basado en el nivel del sonido
def detect_sound():
    print("Detectando sonido...")
    
    # Leer el valor del sensor de sonido (0-65535)
    sound_value = sound_sensor.read_u16()
    print(f"Valor del sensor de sonido: {sound_value}")  # Debugging
    
    # Normalizamos el valor a un rango 0-255
    sound_level = min(255, int(sound_value / 256))  # Convertir 0-65535 a 0-255
    
    # Más azul (grave) en valores bajos, más amarillo (rojo+verde) en valores altos
    r = min(255, sound_level * 2)  # Rojo aumenta con el nivel de sonido
    g = min(255, sound_level)      # Verde aumenta un poco más lento
    b = 255 - sound_level          # Azul disminuye a medida que el sonido es más agudo
    
    set_rgb_color(r, g, b)

# Función para manejar el botón con debounce y mostrar el estado del botón
def button_pressed():
    global last_button_state
    # Leer el estado actual del botón
    button_state = button.value()
    print(f"Estado del botón: {button_state}")  # Debugging del botón

    if button_state == 1 and last_button_state == 0:  # Botón recién presionado
        time.sleep(0.05)  # Delay para debounce
        if button.value() == 1:  # Verificar de nuevo después del debounce
            print("Botón presionado!")
            last_button_state = 1  # Actualizar el último estado
            return True
    elif button_state == 0:
        last_button_state = 0  # Actualizar el último estado
    return False

# Bucle principal
while True:
    # Verificar si el botón fue presionado
    if button_pressed():
        # Cambiar el estado de la detección de sonido
        sound_detection_enabled = not sound_detection_enabled  # Toggle estado
        print(f"Detección de sonido {'activada' if sound_detection_enabled else 'desactivada'}")
        time.sleep(0.3)  # Evitar que múltiples presiones ocurran rápidamente

    if sound_detection_enabled:
        detect_sound()  # Detectar el sonido y cambiar el color del LED si está activado
    else:
        set_rgb_color(255, 255, 255)  # Apagar el LED RGB si la detección está desactivada

    # Espera pequeña para evitar consumir demasiados recursos
    time.sleep(0.1)
