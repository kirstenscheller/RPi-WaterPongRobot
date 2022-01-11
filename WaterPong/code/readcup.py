#ECE 5725 Final Project
#ih258, kes334

import pygame
import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while GPIO.input(17):
    if not GPIO.input(22):
        print("Cup")
        time.sleep(1)

GPIO.cleanup()


