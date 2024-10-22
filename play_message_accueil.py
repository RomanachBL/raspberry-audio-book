import pygame  # Utilisé pour jouer l'audio
import time

# Fonction pour jouer le premier message audio
def play_audio_message(file_path = "./resources/message.wav"):
    """Jouer un message audio."""
    time.sleep(0.5)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Attendre la fin du message
        time.sleep(0.5)
