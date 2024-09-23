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

# Function to map the microphone values between 50000 and 65535 to LED brightness (inverted)
# Now, with more pronounced scaling for brightness control
def map_volume_to_brightness(volume):
    # Ignore values below 50000
    if volume < 50000:
        volume = 50000
    # More aggressive scaling: compress volume range more drastically
    scaled_volume = (volume - 50000) ** 1.5  # Exponential to emphasize differences
    max_scaled_volume = (65535 - 50000) ** 1.5  # Maximum possible value for normalization
    brightness = 65535 - int(scaled_volume * (65535 / max_scaled_volume))  # Inverted brightness
    return brightness

# Continuously check the button and read the microphone when the button is pressed
while True:
    if check_button():
        mic_value = read_mic()  # Only read the microphone when the button is pressed
        brightness = map_volume_to_brightness(mic_value)

        # Set the RGB LED brightness (using red for example; adjust others as needed)
        r_pin.duty_u16(brightness)  # Inverted brightness of the red LED
        g_pin.duty_u16(65535)  # Adjust the green similarly
        b_pin.duty_u16(brightness)  # Adjust the blue similarly

        print(f"Button pressed! Microphone value: {mic_value}, LED brightness: {brightness}")
    
    else:
        # Turn off the LED when the button is not pressed (inverted logic)
        r_pin.duty_u16(65535)   # Turn off red (inverted off)
        g_pin.duty_u16(65535)   # Turn off green
        b_pin.duty_u16(65535)   # Turn off blue

        print("Button not pressed. No microphone listening.")

    time.sleep(0.1)  # Delay of 0.5 seconds between checks
