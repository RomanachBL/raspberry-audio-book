# import RPi.GPIO as GPIO
import threading
import time
import os
import subprocess
from play_message_accueil import play_audio_message  # Import de la fonction
from audio_recording import record_audio  # Import de la fonction d'enregistrement

# Configuration de la pin GPIO
PIN_HOOK_SWITCH = 18  # Remplacez par la pin utilisée
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIN_HOOK_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_recording():
    """Joue le message d'accueil et démarre l'enregistrement."""
    print("1. Lancement du message d'accueil !\n")
    play_audio_message()  # Lecture du message

    print("2. Lancement du processus d'enregistrement !\n")
    record_audio()  # Enregistrement

def hook_switch_callback(channel):
    """Callback lorsque le combiné est décroché."""
    print("## Combiné décroché\n")
    # Lance le script d'enregistrement dans un nouveau thread
    # recording_thread = threading.Thread(target=start_recording)
    # recording_thread.start()
    start_recording()

def listen_for_hook_switch():
    """Écoute le GPIO pour l'état du combiné."""
    # GPIO.add_event_detect(PIN_HOOK_SWITCH, GPIO.BOTH, callback=hook_switch_callback)

    # Simulation du hook switch avec le prompt utilisateur
    while True:
        user_input = input("Appuyez sur 'p' pour décrocher : ")
        if user_input.lower() == 'p':
            print("Simulation du décroché")
            hook_switch_callback(PIN_HOOK_SWITCH)
        time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

    print("Écoute de l'état du combiné...")
    while True:
        time.sleep(1)  # Garder le thread actif

def main():
    """##### Lancement du programme #####"""
    print("""\n##### Lancement du programme #####\n""")
    try:
        listen_for_hook_switch()
    except KeyboardInterrupt:
        print("Arrêt du script.")
    # finally:
    #     GPIO.cleanup()

if __name__ == "__main__":
    main()