import pygame  # Utilisé pour jouer l'audio
import time
import os

# Fonction pour jouer le premier message audio
def play_audio_message():
    """Jouer un message audio."""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'resources', 'message_bip.mp3')

    time.sleep(0.5)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Attendre la fin du message
        time.sleep(0.5)
