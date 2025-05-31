import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import random
import pygame
import os
import json
import subprocess
from datetime import datetime

switch_pin = 21
GpioPins = [18, 23, 24, 25]

# Steps to move from time (index - 1) to get to time (index)
time_gaps = [43, 42, 42, 43, 42, 42, 43, 42, 42, 43, 42, 42]
current_time = 0

# Configuration for probabilities and delays
normal_chance = 0.8
interactive_delay = 8

# Initialize the motor
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

# Initialize pygame mixer for sound
pygame.mixer.init()
sounds_folder = "/home/student334/receipt-printer/scripts/sounds"  # Replace with your folder containing sound files
fortunes_file = "/home/student334/receipt-printer/scripts/random_fortunes.json"


# Load the fortunes JSON file
def load_fortunes():
    """Loads fortunes from the JSON file."""
    try:
        with open(fortunes_file, "r") as f:
            data = json.load(f)
        return data.get("normal_fortunes", []), data.get("interactive_fortunes", [])
    except FileNotFoundError:
        print("random_fortunes.json not found!")
        return [], []
    except json.JSONDecodeError:
        print("Error decoding random_fortunes.json!")
        return [], []


normal_fortunes, interactive_fortunes = load_fortunes()


def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now().strftime("%A, %B %d, %Y %I:%M %p")


def calculate_steps(new_time):
    global current_time
    if new_time == current_time:
        return 0

    total_steps = 0
    position = current_time

    while position != new_time:
        total_steps += time_gaps[position % 12]
        position = (position + 1) % 12

    current_time = new_time
    return total_steps


def move_motor(channel):
    new_time = random.randint(0, 11)
    steps = calculate_steps(new_time)
    if steps > 0:
        mymotortest.motor_run(GpioPins, 0.001, steps, False, False, "half", 0)
        print(f"Moved to {new_time} o'clock with {steps} steps.")
        play_random_sound()

        # Choose and print a fortune
        fortune_type, fortune = get_random_fortune()
        if fortune_type == "normal":
            print_to_printer(fortune, include_date=True)  # Add date for normal fortunes
        elif fortune_type == "interactive":
            print_interactive_fortune(fortune)  # Handle date within this function


def play_random_sound():
    """Plays a random sound file from the specified folder."""
    try:
        sound_files = [f for f in os.listdir(sounds_folder) if f.endswith(".mp3")]

        if not sound_files:
            print("No sound files found in the folder!")
            return

        random_sound = random.choice(sound_files)
        print(f"Playing sound: {random_sound}")

        pygame.mixer.music.load(os.path.join(sounds_folder, random_sound))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Error playing sound: {e}")


def get_random_fortune():
    global normal_chance
    """Randomly decides whether to print a normal or interactive fortune."""
    if random.random() < normal_chance:  # 80% chance
        return "normal", random.choice(normal_fortunes)
    else:  # 20% chance
        return "interactive", random.choice(interactive_fortunes)


def print_interactive_fortune(fortune):
    global interactive_delay
    """Handles printing an interactive fortune with a delay."""
    part_one = fortune.get("part_one", "")
    part_two = fortune.get("part_two", "")
    
    # Print the first part with the date
    print_to_printer(part_one, include_date=True)  
    time.sleep(interactive_delay)  # Wait for the delay
    # Print the second part without the date
    print_to_printer(part_two, include_date=False)


def print_to_printer(output_line, include_date=False):
    """Sends a formatted receipt to the printer with head and padding."""
    try:
        if include_date:
            output_line = f"Today is {get_current_datetime()}\n\n{output_line}"

        # Calculate the number of content lines (32 characters per line)
        content_lines = (len(output_line) + 31) // 32

        # Add three header lines
        header = "\n" * 3

        total_lines = content_lines + 3

        if total_lines < 18:
            padding_lines = 18 - total_lines
        else:
            padding_lines = 0

        padding = "\n" * padding_lines

        final_output = header + output_line + padding

        # Send to printer via `lp`
        process = subprocess.Popen(["lp"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=final_output)

        print(f"Printed receipt with {total_lines + padding_lines} total lines.")
    except Exception as e:
        print(f"Error printing to printer: {e}")


# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add event detection for the switch
GPIO.add_event_detect(switch_pin, GPIO.BOTH, callback=move_motor, bouncetime=10)

print_to_printer("Testing... Script is all set to go!")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
