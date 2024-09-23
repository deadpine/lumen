import machine

# Initialize the GPIO pins for the RGB LED
r_pin = machine.Pin(6, machine.Pin.OUT)
g_pin = machine.Pin(7, machine.Pin.OUT)
b_pin = machine.Pin(8, machine.Pin.OUT)

# Turn off the LED by setting all pins to high
r_pin.value(1)   # Red off
g_pin.value(1) # Green off
b_pin.value(1)  # Blue off

print("RGB LED is off.")
