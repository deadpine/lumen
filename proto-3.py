import machine
import time

# Initialize the GPIO pins for the RGB LED
r_pin = machine.Pin(6, machine.Pin.OUT)
g_pin = machine.Pin(7, machine.Pin.OUT)
b_pin = machine.Pin(8, machine.Pin.OUT)

# Turn off the LED by setting all pins to high
r_pin.value(1)   # Red off
g_pin.value(1) # Green off
b_pin.value(1)  # Blue off

print("RGB LED is off.")

# Initialize the button on GP9
button_pin = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

# Function to check button state
def check_button():
    if button_pin.value() == 0:
        print("Button pressed!")
        return True
    else:
        print("Button not pressed.")
        return False

# Continuously read the microphone and button values
while True:
    button_pressed = check_button()
    
    # Add your own logic for when the button is pressed or not
    if button_pressed:
        # You can add logic here to turn on/off the LED, etc.
        pass
    # Delay in logs
    time.sleep(1)
