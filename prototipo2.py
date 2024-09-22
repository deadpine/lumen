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

# Programa
# Encender el LED de la Raspberry Pi Pico para indicar que el código está corriendo
pico_led.value(1)

# Variable para controlar el estado del sensor de sonido (activado o desactivado)
sound_detection_enabled = False  # Comienza desactivado

# Variable para almacenar el último estado del botón
last_button_state = 1  # Estado anterior del botón

# Función para cambiar el brillo del LED Rojo usando un valor entre 0 y 65535
def set_red_brightness(brightness):
    print(f"Configurando brillo del LED Rojo: {brightness}")
    
    # Ajustar el brillo del LED rojo
    led_r.duty_u16(int(brightness))

# Función para apagar todas las luces RGB
def turn_off_rgb():
    print("Apagando LED RGB")
    led_r.duty_u16(0)  # Apaga el LED rojo
    led_g.duty_u16(0)  # Apaga el LED verde (por si acaso)
    led_b.duty_u16(0)  # Apaga el LED azul (por si acaso)

# Función para detectar sonido y cambiar el brillo del LED basado en el nivel del sonido
def detect_sound():
    print("Detectando sonido...")
    
    # Leer el valor del sensor de sonido (0-65535)
    sound_value = sound_sensor.read_u16()
    print(f"Valor del sensor de sonido: {sound_value}")  # Debugging
    
    # Ajustar el nivel de sonido para que controle el brillo (0-65535)
    sound_level = min(65535, sound_value)  # Mantener el valor dentro del rango PWM
    
    # Establecer el brillo del LED rojo en función del nivel de sonido
    set_red_brightness(sound_level)
    
    # Asegurarse de que los otros LEDs estén apagados
    led_g.duty_u16(0)  # Asegurarse de que el LED verde esté apagado
    led_b.duty_u16(0)  # Asegurarse de que el LED azul esté apagado

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
        detect_sound()  # Detectar el sonido y cambiar el brillo del LED si está activado
    else:
        turn_off_rgb()  # Apagar todas las luces RGB si la detección está desactivada

    # Espera pequeña para evitar consumir demasiados recursos
    time.sleep(0.1)

