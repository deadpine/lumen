import machine
import time

# Initialize the GPIO pins for the RGB LED
r_pin = machine.Pin(6, machine.Pin.OUT)
g_pin = machine.Pin(7, machine.Pin.OUT)
b_pin = machine.Pin(8, machine.Pin.OUT)

# Turn off the LED by setting all pins to high
r_pin.value(1)   # Red off
g_pin.value(1)   # Green off
b_pin.value(1)   # Blue off

print("RGB LED is off.")

# Initialize the microphone on GP28
mic_pin = machine.ADC(28)  # GP28 is an analog pin

# Initialize the button on GP9
button_pin = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

# Function to read the microphone value
def read_mic():
    mic_value = mic_pin.read_u16()  # Read the analog value (0-65535)
    print("Microphone value:", mic_value)
    return mic_value

# Function to check button state
def check_button():
    if button_pin.value() == 0:
        print("Button pressed!")
        return True
    else:
        return False

# Continuously check the button and read the microphone when the button is pressed
while True:
    if check_button():
        mic_value = read_mic()  # Only read the microphone when the button is pressed
        # You can add logic here to process the mic value, control LEDs, etc.
    else:
        print("Button not pressed. No microphone recording.")
    
    time.sleep(0.5)  # Short delay to avoid overwhelming the processor