import gpiod
import threading
import time
import os
import subprocess
from play_message_accueil import play_audio_message  # Import de la fonction
from audio_recording import record_audio  # Import de la fonction d'enregistrement

def main():
    print("""\n##### Lancement du programme #####\n""")

    try:
        print("1. Lancement du message d'accueil !\n")
        play_audio_message()  # Lecture du message

        print("2. Lancement du processus d'enregistrement !\n")
        record_audio(None)  # Enregistrement
        
    except KeyboardInterrupt:
        print("Arrêt du script.")

if __name__ == "__main__":
    main()