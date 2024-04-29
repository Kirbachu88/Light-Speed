import RPi.GPIO as GPIO
import time
import signal
import sys

game_mode = -2
player_count = 0
p1_time = 0.0
p2_time = 0.0

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

def Reset():
    for led in outputLEDs:
        GPIO.output(led, False)

def Standby():
    GPIO.output(red, True)
    time.sleep(0.5)
    GPIO.output(red, False)
    if game_mode != -2:
        return
    GPIO.output(yellow, True)
    time.sleep(0.5)
    GPIO.output(yellow, False)
    if game_mode != -2:
        return
    GPIO.output(green, True)
    time.sleep(0.5)
    GPIO.output(green, False)
    if game_mode != -2:
        return

def Players():
    global game_mode
    global player_count
    
    print("Game will begin shortly, P2 may join now!")
    
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
    
    print(f'Game Mode: {player_count}-Player')
    game_mode = player_count
    time.sleep(2)

def Single():
    print("Single-Player game")
    exit()

def Versus():
    print("Versus game")
    exit()

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)
       
def p1_button_pressed_callback(channel):
    global p1_time
    global game_mode
    global player_count
    
    if game_mode == -2:
        print("Player 1 Joined!")
        GPIO.output(p1_LED, True)
        game_mode = -1
        player_count = 1
    
    if (game_mode == 1 or game_mode == 2) and (p1_time == 0.0):
        print("Player 1 Action")
        p1_time = time.time()
        print(f'P1 Time elapsed since start: {p1_time - test_time}')
    
def p2_button_pressed_callback(channel):
    global p2_time
    global game_mode
    global player_count
    
    if game_mode == -2:
        print("You must join after Player 1!")
    
    if game_mode == -1:
        print("Player 2 Joined!")
        GPIO.output(p2_LED, True)
        player_count = 2
        
    if (game_mode == 2) and (p2_time == 0.0):
        print("Player 2 Action")
        p2_time = time.time()
        print(f'P2 Time elapsed since start: {p2_time - test_time}')

GPIO.add_event_detect(p1_button, GPIO.FALLING, callback=p1_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(p2_button, GPIO.FALLING, callback=p2_button_pressed_callback, bouncetime=200)

Reset()
test_time = time.time()

print("Waiting for players...")

while True:
    if game_mode == -2:
        Standby()
    elif game_mode == -1:
        Players()
    elif game_mode == 1:
        Single()
    elif game_mode == 2:
        Versus()
    else:
        print("Unexpected Game Mode")
        Reset()
        exit()
