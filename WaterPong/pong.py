#ECE 5725
#ih258, kes334
# Final Project, a Water Pong Robot
# This code has sensors linked to 6 cups at the other end of the table.
# When a cup is sensed, the cup shows up as a red circle on the PiTFT, when 
# the cup has been hit or is gone, it shows up as a green circle on the PiTFT.
# When all six cups are gone, a win screen appears.
# The robot will aim when it is it's turn. (It aims at the next availible cup in order 
# from cup 1 - 6, with the order of the cup pyramid going from top to bottom and left to right.
# To tell the robot that it it's turn, you press button 23, "My Turn" will show up on the screen,
# when it's turn is over, you press button 23 again, it aims back towards the center and the screen
# says "Your Turn"
# This robot also has the capbility to perform reracks. The reracks available are small triangle and 
# and diamond. When the user wants to rerack, they press the rerack button. The screen changes to the
#rerack screen and when they are done rereacking they press the done button


import pygame
import RPi.GPIO as GPIO
import os
import sys
from pygame.locals import *
import time


os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Note that we had to switch the GPIO numbers of cups 3 an 6
cup1 = 22
cup2 = 26
cup3 = 5
#cup3 = 4
cup4 = 13
cup5 = 6
cup6 = 4
#cup6 = 5
servo_pin = 20

#Which cups have been hit or are gone
cups_hit = [False, False, False, False, False, False]

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cup6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Servo Setup for aiming
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)
servo.start(3)
time.sleep(.2)

pygame.init()
size = width, height = 320,240
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0, 0
BLUE = 0,0, 255
GREEN = 0,255, 0
font = pygame.font.SysFont('Corbel', 25)
rerack_text = font.render('Rerack', True, WHITE)
donetext = font.render("DONE", True, BLACK)

#Used to notify what cup we are aimin at
hit = ""
aim = font.render(hit, True, WHITE)


turn = "Your Turn"
turn_text = font.render(turn, True, WHITE)

bigfont = pygame.font.SysFont('Corbel', 50)
win_screen = False
wintext = bigfont.render("You win!!!", True, WHITE)


rerack_screen = False



#shooting = False
aim_cup = 0


# Servo controls. If we are aiming to cup 2 and 4 we move slightly to the left,
# if we're aiming to cup 3 and 5 we move slightly to the right, and if we're aiming
#towards cup 1 and 5 we stay in the center
def bot_shooting(cup):
    print(cup)
    if cup == "cup2" or cup == "cup4":
        print("left")
        servo.ChangeDutyCycle(2.5)
        time.sleep(.2)
    elif cup == "cup3" or cup == "cup6":
        print("right")
        servo.ChangeDutyCycle(3.5)
        time.sleep(.2)
    elif cup == "cup1" or cup == "cup5":
        print("center")
        servo.ChangeDutyCycle(3)
        time.sleep(.2)

# This is the callback function related to button 23, when senses button 23 pressed,
# it it the robot's turn and it aims toward the correct cup, after you press it again, it 
# aims back towards the center and it's turn is done
shooting = False
def turn_change(channel):
    global shooting
    global turn
    global aim_cup
    if shooting == False:
        shooting = True
        bot_shooting("cup" + str(aim_cup + 1))
        turn = "My Turn"
        print("hereererere")
    elif shooting == True:
        shooting = False
        bot_shooting("cup1")
        turn = "Your Turn"
        print("herere2")

GPIO.add_event_detect(23, GPIO.FALLING, callback=turn_change, bouncetime=500)



while GPIO.input(17):
    screen.fill(BLACK)
    
    #Rerack rect 
    rerack_rect = rerack_text.get_rect(center=(40, 20))
    screen.blit(rerack_text, rerack_rect)
    
    #Aim text
    aim = font.render(hit, True, WHITE)
    aim_rect = aim.get_rect(center=(250, 20))
    screen.blit(aim, aim_rect)
    
    
    # My turn vs your turn text 
    turn_text = font.render(turn, True, WHITE)
    turn_rect = turn_text.get_rect(center=(275, 200))
    screen.blit(turn_text, turn_rect)
    
    # Rendering of cups
    if not win_screen and not rerack_screen:
        #Robot circle
        pygame.draw.circle(screen, BLUE, (150, 40), 20)
    

        #Cup Drawing
        if not GPIO.input(cup4):
            pygame.draw.circle(screen, RED, (100, 180), 20)
            cups_hit[3] = False
        else:
            pygame.draw.circle(screen, GREEN, (100, 180), 20)
            cups_hit[3] = True

        if not GPIO.input(cup5):
            pygame.draw.circle(screen, RED, (150, 180), 20)
            cups_hit[4] = False
        else:
            pygame.draw.circle(screen, GREEN, (150, 180), 20)
            cups_hit[4] = True

        if not GPIO.input(cup3):
            pygame.draw.circle(screen, RED, (200, 180), 20)
            cups_hit[5] = False
        else:
            pygame.draw.circle(screen, GREEN, (200, 180),20)
            cups_hit[5] = True

        if not GPIO.input(cup2):
            pygame.draw.circle(screen, RED, (125, 150), 20)
            cups_hit[1] = False
        else:
            pygame.draw.circle(screen, GREEN, (125,150), 20)
            cups_hit[1] = True

        if not GPIO.input(cup6):
            pygame.draw.circle(screen, RED, (175, 150), 20)
            cups_hit[2] = False
        else:
            pygame.draw.circle(screen, GREEN, (175, 150), 20)
            cups_hit[2] = True

        if not GPIO.input(cup1):
            pygame.draw.circle(screen, RED, (150, 120), 20)
            cups_hit[0] = False
        else:
            pygame.draw.circle(screen, GREEN, (150,120), 20)
            cups_hit[0] = True
    # If all the cups are green and have been hit, go to win page
    elif win_screen:
        winrect = wintext.get_rect(center = (150, 150))
        screen.blit(wintext, winrect)
    
    # If the rerack button has been pushed,go to the rerack screen
    elif rerack_screen:
        pygame.draw.circle(screen, GREEN, (160,120), 40)
        done_rect = donetext.get_rect(center=(160,120))
        screen.blit(donetext, done_rect)
    
    try:
        aim_cup = cups_hit.index(False)
        hit = "Aiming at cup " + str(aim_cup + 1)
    except ValueError:
        if not False in cups_hit:
            win_screen = True
            hit = "You Win!"
            print("You Win!")

    # Code to see if the rerack button, or done button on screen has been hit
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if not rerack_screen:
                if (rerack_rect.collidepoint(pos)):
                    rerack_screen = True
            else:
                if (done_rect.collidepoint(pos)):
                    rerack_screen = False



    pygame.display.flip()

GPIO.cleanup()
servo.stop()
quit()
