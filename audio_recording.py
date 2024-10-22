import pyaudio
import wave
import os
import datetime
import time
import threading  # Pour gérer l'entrée utilisateur
# import RPi.GPIO as GPIO

# PIN_HOOK_SWITCH = 18  # Le numéro GPIO du hook switch
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIN_HOOK_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

duration_max=60 # Durée max en seconde d'un enregistrement
base_path = "./livre_or_enregistrements/" # Chemin du dossier où seront sauvegardés les enregistrements

if not os.path.exists(base_path):
    os.makedirs(base_path)

# Fonction pour récupérer le prochain nom du fichier
def get_next_filename():
    """Trouver le prochain nom de fichier à utiliser pour l'enregistrement."""

    # Lister les fichiers existants
    fichiers = os.listdir(base_path)
    numeros = [int(f.split('_')[0]) for f in fichiers if f.endswith('.wav')]

    # Générer un horodatage au format hh-mm-ss
    timestamp = datetime.datetime.now().strftime("%H-%M-%S")
    
    if numeros:
        return os.path.join(base_path, f"{max(numeros) + 1:05d}_message-audio_{timestamp}.wav")
    else:
        return os.path.join(base_path, f"00001_message-audio_{timestamp}.wav")

# Fonction d'écoute de l'entrée utilisateur
def listen_for_stop():
    global recording
    while recording:
        user_input = input("Appuyez sur 's' pour arrêter : ")
        if user_input.lower() == 's':
            print("Arrêt de l'enregistrement demandé par l'utilisateur.")
            recording = False
            break

# Fonction d'écoute du hook switch GPIO
# def listen_for_gpio():
#     global recording
#     while recording:
#         if GPIO.input(PIN_HOOK_SWITCH) == GPIO.LOW:  # Si le combiné est reposé
#             print("Combiné reposé, arrêt de l'enregistrement.")
#             recording = False
#             break
#         time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

# Enregistrement audio
def record_audio(duration=duration_max):
    """Enregistrer l'audio après avoir joué le message."""
    global recording
    chunk = 1024  # Taille des morceaux d'audio
    sample_format = pyaudio.paInt16  # Format audio
    channels = 1  # Mono
    rate = 44100  # Fréquence d'échantillonnage
    p = pyaudio.PyAudio()

    # Initialisation de l'enregistrement
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)

    print("========> Enregistrement en cours...")

    frames = []
    start_time = time.time()
    recording = True

    # Lancer les threads pour écouter l'utilisateur et le GPIO
    threading.Thread(target=listen_for_stop, daemon=True).start()
    # threading.Thread(target=listen_for_gpio, daemon=True).start()

    while recording:
        data = stream.read(chunk)
        frames.append(data)

        # Vérifier si le temps d'enregistrement est écoulé
        if (time.time() - start_time) > duration:
            print("Durée maximale atteinte, arrêt de l'enregistrement.")
            recording = False
            break

    # Fin de l'enregistrement
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Création du nom de fichier avec incrémentation
    filename = get_next_filename()
    
    # Sauvegarde de l'enregistrement dans un fichier WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Enregistrement terminé. Fichier sauvegardé sous {filename}.\n")
