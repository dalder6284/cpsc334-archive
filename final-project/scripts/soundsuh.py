import pygame
import time

# Initialize the pygame mixer
pygame.mixer.init()

# Load and play the MP3 file
pygame.mixer.music.load("./sounds/man_screaming.mp3")
pygame.mixer.music.set_volume(0.5)


pygame.mixer.music.play()

# Keep the script running while the music is playing
while pygame.mixer.music.get_busy():
    time.sleep(1)