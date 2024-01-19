import pygame
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

trigger_pin = 29
echo_pin = 31

# Set up the GPIO pins
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)


def play_mp3(mp3_file_path):

    # Initialize pygame
    pygame.init()

    # Load the MP3 file
    pygame.mixer.music.load(mp3_file_path)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        pass


###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Speak Function %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def measure_distance():
    # Send a 10us pulse to trigger the ultrasonic sensor
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Initialize pulse_start_time and pulse_end_time
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    # Wait for the echo to start
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start_time = time.time()

    # Wait for the echo to end
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end_time = time.time()

    # Calculate the time it took for the ultrasonic wave to return
    pulse_duration = pulse_end_time - pulse_start_time

    # Speed of sound is approximately 343 meters per second (in air)
    # Calculate the distance using the formula: distance = speed * time
    distance = (pulse_duration * 34300) / 2  # Distance in centimeters

    return distance


person_present=False

while True:
    if not person_present:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.5)
        if distance <= 60:
            person_present=True
            play_mp3("welcome.mp3")
            while True:
                distance = measure_distance()
                print(f"Distance: {distance:.2f} cm")
                time.sleep(0.5)
                if distance <=60:
                    pass
                else:
                    person_present=False
                    break
        else:
            pass
    else:
        pass

