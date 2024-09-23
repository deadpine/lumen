import machine
import time

# Initialize the GPIO pins for the RGB LED with PWM for brightness control
r_pin = machine.PWM(machine.Pin(6))  # Set up for PWM to control brightness
g_pin = machine.PWM(machine.Pin(7))  # Set up for PWM
b_pin = machine.PWM(machine.Pin(8))  # Set up for PWM

# Set the PWM frequency for smoother brightness control
r_pin.freq(1000)
g_pin.freq(1000)
b_pin.freq(1000)

# Initialize the microphone on GP28
mic_pin = machine.ADC(28)  # GP28 is an analog pin

# Initialize the button on GP9
button_pin = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

# Function to read the microphone value
def read_mic():
    mic_value = mic_pin.read_u16()  # Read the analog value (0-65535)
    return mic_value

# Function to check button state
def check_button():
    return button_pin.value() == 0

# Function to map microphone values to inverted PWM brightness (0 -> 65535 becomes 65535 -> 0)
def map_volume_to_brightness(volume):
    # Invert the mic value for the LED (0 -> 65535 becomes 65535 -> 0)
    brightness = 65535 - min(max(volume, 0), 65535)  # Ensure it's within bounds and invert
    return brightness

# Continuously check the button and read the microphone when the button is pressed
while True:
    if check_button():
        mic_value = read_mic()  # Only read the microphone when the button is pressed
        brightness = map_volume_to_brightness(mic_value)

        # Set the RGB LED brightness (using red for example; adjust others as needed)
        r_pin.duty_u16(brightness)  # Inverted brightness of the red LED
        g_pin.duty_u16(brightness)  # Adjust the green similarly
        b_pin.duty_u16(brightness)  # Adjust the blue similarly

        print(f"Button pressed! Microphone value: {mic_value}, LED brightness: {brightness}")
    
    else:
        # Turn off the LED when the button is not pressed (inverted logic)
        r_pin.duty_u16(65535)   # Turn off red (inverted off)
        g_pin.duty_u16(65535)   # Turn off green
        b_pin.duty_u16(65535)   # Turn off blue

        print("Button not pressed. No microphone listening.")

    time.sleep(0.1)  # Short delay to avoid overwhelming the processor
