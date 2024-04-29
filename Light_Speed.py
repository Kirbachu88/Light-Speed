import RPi.GPIO as GPIO
import time
import signal
import sys
import random

game_mode = -2
round_time = 0.0
best_time = 99.99
player_count = 0

p1_time = 0.0
p1_wins = 0

p2_time = 0.0
p2_wins = 0

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
    Reset()
    
    global p1_time
    global round_time
    global best_time
    tempo = random.uniform(1, 3)
    
    time.sleep(1)
    print("Get ready...")
    
    GPIO.output(red, True)
    time.sleep(tempo)
    GPIO.output(yellow, True)
    time.sleep(tempo)
    GPIO.output(green, True)
    round_time = time.time()
    print("PRESS!")
    
    time.sleep(2)

    p1_result = p1_time - round_time

    if p1_time == 0.0:
        print("Player 1, you did not press in time!")
    elif p1_result < 0:
        print("Player 1, you pressed too soon!")
    
    print(f'Your time: {p1_result}')
        
    if (p1_result > 0.0) and (p1_result < best_time):
        print("NEW BEST TIME:")
        best_time = p1_result
        print(f'{best_time}')
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(1)
    else:
        print("Best time:")
        print(f'{best_time}')
    
    time.sleep(3)

    p1_time = 0.0

def Versus():
    print("Versus game")
    Reset()
    
    global p1_time
    global p2_time
    global round_time
    global p1_wins
    global p2_wins
    round_time = time.time()
    tempo = random.uniform(1, 3)
    
    time.sleep(1)
    print("Get ready...")
    
    GPIO.output(red, True)
    time.sleep(tempo)
    GPIO.output(yellow, True)
    time.sleep(tempo)
    GPIO.output(green, True)
    round_time = time.time()
    print("PRESS!")
    
    time.sleep(2)
    
    p1_win = True
    p2_win = True
    
    p1_result = p1_time - round_time
    p2_result = p2_time - round_time

    if p1_time == 0.0:
        print("Player 1, you did not press in time!")
        p1_win = False
    elif p1_result < 0:
        print("Player 1, you pressed too soon!")
        p1_win = False
        
    if p2_time == 0.0:
        print("Player 2, you did not press in time!")
        p2_win = False
    elif p2_result < 0:
        print("Player 2, you pressed too soon!")
        p2_win = False
        
    if p1_win and p2_win:
        if p1_result < p2_result:
            p2_win = False
        elif p2_result < p1_result:
            p1_win = False
        else:
            print("A tie???")
    
    Reset()
    
    if p1_win == p2_win:
        print("Nobody wins!")
        print(f'P1 {p1_wins} - {p2_wins} P2')
        GPIO.output(red, True)
        time.sleep(3)
    elif p1_win:
        print("Player 1 wins!")
        if p2_result > 0:
            print(f'Faster by {p2_time - p1_time}')
        p1_wins += 1
        print(f'P1 {p1_wins} - {p2_wins} P2')
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(0.5)
        GPIO.output(p1_LED, False)
        time.sleep(0.5)
        GPIO.output(p1_LED, True)
        time.sleep(1)
    elif p2_win:
        print(f'Player 2 wins!')
        if p1_result > 0:
            print(f'Faster by {p1_time - p2_time}')
        p2_wins += 1
        print(f'P1 {p1_wins} - {p2_wins} P2')
        GPIO.output(p2_LED, True)
        time.sleep(0.5)
        GPIO.output(p2_LED, False)
        time.sleep(0.5)
        GPIO.output(p2_LED, True)
        time.sleep(0.5)
        GPIO.output(p2_LED, False)
        time.sleep(0.5)
        GPIO.output(p2_LED, True)
        time.sleep(0.5)
        GPIO.output(p2_LED, False)
        time.sleep(0.5)
        GPIO.output(p2_LED, True)
        time.sleep(1)
    
    p1_time = 0.0
    p2_time = 0.0

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
        GPIO.output(p1_LED, True)
        p1_time = time.time()
    
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
        GPIO.output(p2_LED, True)
        p2_time = time.time()

GPIO.add_event_detect(p1_button, GPIO.FALLING, callback=p1_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(p2_button, GPIO.FALLING, callback=p2_button_pressed_callback, bouncetime=200)

Reset()

print("Waiting for players...")
print("When the game begins, watch how long it takes for each light to turn on.")
print("Press the button when it reaches green, but not too soon!")
print("Try to get the fastest time on your own or against another!")

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
