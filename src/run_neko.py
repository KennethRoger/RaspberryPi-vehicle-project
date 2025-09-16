# Importing necessary libraries

import RPi.GPIO as GPIO
import adafruit_us100
import serial
import pygame
from picamera import PiCamera
import random
import time
import sys

# Setting up GPIO nummbering to physcial pin numbers
GPIO.setmode(GPIO.BOARD)

# Defining UART pins for ultrasonic sensor 
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3)
print(uart)
us100 = adafruit_us100.US100(uart)

# Motor driver a pins
in1_a = 13
in2_a = 15
in3_a = 16
in4_a = 18

# Motor driver b pins
in1_b = 29
in2_b = 31
in3_b = 32
in4_b = 33

# Setting motor pins
GPIO.setup(in1_a, GPIO.OUT)
GPIO.setup(in2_a, GPIO.OUT)
GPIO.setup(in3_a, GPIO.OUT)
GPIO.setup(in4_a, GPIO.OUT)
GPIO.setup(in1_b, GPIO.OUT)
GPIO.setup(in2_b, GPIO.OUT)
GPIO.setup(in3_b, GPIO.OUT)
GPIO.setup(in4_b, GPIO.OUT)

# Initializing pygame
pygame.init()

# Setting up pygame display
pygame.display.set_mode((500, 500))
pygame.display.set_caption('AI RC')

# Setting direction flags
forward = False
backward = False
left = False
right = False
nw_direction = False
ne_direction = False
sw_direction = False
se_direction = False
rotate_left = False
rotate_right = False

# Defining functions for movement
def moveForward():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)
    
def moveBackward():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)
            
    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)

def moveLeft():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)

def moveRight():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)

def moveNW():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)

def moveNE():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)
    
def moveSW():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)
    
def moveSE():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)

def rotateLeft():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)
            
    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)

def rotateRight():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)
            
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)

def stop():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)
    
    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)

# Setting up picamera
camera = PiCamera()
#camera.rotation = 180
camera.resolution = (1920, 1080)

# Providing directory location to save pictures
save_directory = "/home/neko/Desktop/py_projects/rc_projects/py_images"

# Defining function for image capture
def captureImage():
    timestamp = time.strftime("%d-%m-%Y_%H:%M:%S")
    image_path = f"{save_directory}/image_{timestamp}.jpg"
    print('Capturing Image...')
    camera.capture(image_path)
    print(f"Image captured and saved to {image_path}")

random_rotate_direction = [rotateLeft, rotateRight] 

try:
    # Setting up infinite loop script
    while True:
        # Setting up pygame for acquiring keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if case for exiting program safely
                GPIO.cleanup()
                pygame.quit()
                sys.exit()

            # Acquiring keydown events from keyboard for diffent direction 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP8:
                    forward = True
                if event.key == pygame.K_KP2:
                    backward = True
                if event.key == pygame.K_KP4:
                    left = True
                if event.key == pygame.K_KP6:
                    right = True
                    
                if event.key == pygame.K_KP7:
                    nw_direction = True
                if event.key == pygame.K_KP9:
                    ne_direction = True
                if event.key == pygame.K_KP1:
                    sw_direction = True
                if event.key == pygame.K_KP3:
                    se_direction = True
                if event.key == pygame.K_KP5:
                    stop()

                if event.key == pygame.K_a:
                    rotate_left = True
                if event.key == pygame.K_d:
                    rotate_right = True

                # Keydown event for image capture
                if event.key == pygame.K_o:
                    captureImage()
                
                # Keydown event for obstacle detection
                if event.key == pygame.K_p:
                    auto_mode = True
                    
                    # Loop block for directional navigation with US 100
                    while auto_mode:
                        distance = us100.distance
                        time.sleep(0.1)
                        print(distance)
                        if distance <= 35:
                            rndir = random.choice(random_rotate_direction)
                            stop()
                            captureImage()
                            time.sleep(1)
                            while True:
                                distance = us100.distance
                                time.sleep(0.1)
                                rndir()
                                time.sleep(0.1)
                                if distance > 35:
                                    rndir()
                                    time.sleep(0.5)
                                    stop()
                                    time.sleep(1)
                                    break
                        else:
                            moveForward()
                            time.sleep(0.1)
                        # Keydown event to stop obstacle detection and revert to manual
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    auto_mode = False

            # Acquiring Keyup event to detect stop inputs
            if event.type == pygame.KEYUP:
                forward = backward = left = right = nw_direction = ne_direction = sw_direction = se_direction = rotate_left = rotate_right = False
                stop()
        
        # if cases for each direction        
        if forward:
            moveForward()
            
        if backward:
            moveBackward()

        if left:
            moveLeft()

        if right:
            moveRight()

        if nw_direction:
            moveNW()

        if ne_direction:
            moveNE()

        if sw_direction:
            moveSW()

        if se_direction:
            moveSE()

        if rotate_left:
            rotateLeft()

        if rotate_right:
            rotateRight()

# Exception block to stop program with Keyboard interrupt(ctrl+c) and cleaning up Rpi
except KeyboardInterrupt:
    camera.close()
    GPIO.cleanup()
