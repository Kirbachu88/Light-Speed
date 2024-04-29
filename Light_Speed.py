import RPi.GPIO as GPIO
import time
import signal
import sys

game_mode = 0
player_count = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

outputLEDs = [17,27,22,6,19]

red = 17
yellow = 27
green = 22

p1_LED = 19
p1_button = 26

p2_LED = 6
p2_button = 5

for led in outputLEDs:
    GPIO.setup(led, GPIO.OUT)

GPIO.setup(p1_button, GPIO.IN)
GPIO.setup(p2_button, GPIO.IN)

def Test():
    GPIO.output(red, True)
    time.sleep(1)
    GPIO.output(red, False)
    time.sleep(1)
    
def Standby():
    GPIO.output(red, True)
    time.sleep(0.5)
    GPIO.output(red, False)
    if game_mode != 0:
        return
    GPIO.output(yellow, True)
    time.sleep(0.5)
    GPIO.output(yellow, False)
    if game_mode != 0:
        return
    GPIO.output(green, True)
    time.sleep(0.5)
    GPIO.output(green, False)
    if game_mode != 0:
        return

def Players():
    GPIO.output(red, False)
    GPIO.output(yellow, False)
    GPIO.output(green, False)
    
    GPIO.output(green, True)
    time.sleep(2)
    GPIO.output(green, False)
    GPIO.output(yellow, True)
    time.sleep(2)
    GPIO.output(yellow, False)
    GPIO.output(red, True)
    
    print(f'Players: {player_count}')
    time.sleep(2)
    game_mode = player_count

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def button_pressed_callback(channel):
    global game_mode
    global player_count
    
    if game_mode == 0:
        game_mode = 1
        player_count += 1
        
def p1_button_pressed_callback(channel):
    global p1_time
    print("Player 1 Press")
    
    global game_mode
    global player_count
    
    if game_mode == 0:
        game_mode = 1
        player_count += 1
    
def p2_button_pressed_callback(channel):
    global p2_time
    print("Player 2 Press")
    
    global game_mode
    global player_count
    
    if game_mode == 0:
        game_mode = 1
        player_count += 1

GPIO.add_event_detect(p1_button, GPIO.FALLING, callback=p1_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(p2_button, GPIO.FALLING, callback=p2_button_pressed_callback, bouncetime=200)

while True:
    if game_mode == 0:
        Standby()
    else:
        Players()
