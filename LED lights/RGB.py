from machine import  Pin, PWM
from time import sleep

R = PWM(Pin(5))
G = PWM(Pin(6))
B = PWM(Pin(7))
R.freq(1000)
G.freq(1000)
B.freq(1000)

print("Welcome to void loop Robotech & Automation")
def RGB(a,b,c):
    R.duty_u16(a*257)
    G.duty_u16(b*257)
    B.duty_u16(c*257)

while True:
    RGB(255,0,0)
    sleep(0.5)
    RGB(255,128,0)
    sleep(0.5)
    RGB(255,255,0)
    sleep(0.5)
    RGB(128,255,0)
    sleep(0.5)
    RGB(0,255,0)
    sleep(0.5)
    RGB(0,255,128,)
    sleep(0.5)
    RGB(0,255,255)
    sleep(0.5)
    RGB(0,128,255)
    sleep(0.5)
    RGB(0,0,255)
    sleep(0.5)
    RGB(127,0,255)
    sleep(0.5)
    RGB(255,0,255)
    sleep(0.5)
    RGB(255,0,127)
    sleep(0.5)
    RGB(128,128,128)
    sleep(0.5)
    
    
    
    

    
    
