import wave
import os
import datetime
import time
import threading  # Pour gérer l'entrée utilisateur
import sys

class NoAlsaErrors:
    def __enter__(self):
        self._stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr.close()
        sys.stderr = self._stderr

with NoAlsaErrors():
    import pyaudio  # Importe PyAudio sans afficher les erreurs ALSA

duration_max=60 # Durée max en seconde d'un enregistrement
current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(current_dir, 'livre_or_enregistrements')

if not os.path.exists(base_path):
    os.makedirs(base_path)

# Fonction pour récupérer le prochain nom du fichier
def get_next_filename():
    """Trouver le prochain nom de fichier à utiliser pour l'enregistrement."""

    # Lister les fichiers existants
    fichiers = os.listdir(base_path)
    numeros = [int(f.split('_')[0]) for f in fichiers if f.endswith('.wav')]

    # Générer un horodatage au format hh-mm-ss
    timestamp = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    
    if numeros:
        return os.path.join(base_path, f"{max(numeros) + 1:05d}_message_{timestamp}.wav")
    else:
        return os.path.join(base_path, f"00001_message_{timestamp}.wav")

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
def listen_for_gpio():
    global recording
    global line
    while recording:
        # Lecture directe de la broche
        state = line.get_value()

        # Interprétation simple
        if state == 0:
            print("Arrêt de l'enregistrement demandé par l'utilisateur.")
            recording = False
            break

        time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

# Enregistrement audio
def record_audio(lineFromMain, duration=duration_max):
    """Enregistrer l'audio après avoir joué le message."""

    global recording
    global line

    recording = True

    if lineFromMain is not None :
        line = lineFromMain

    chunk = 4096  # Taille des morceaux d'audio
    sample_format = pyaudio.paInt16  # Format audio
    channels = 1  # Mono
    rate = 44100  # Fréquence d'échantillonnage
    p = pyaudio.PyAudio()

    # Initialisation de l'enregistrement
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True,
                    input_device_index=0)

    print("========> Enregistrement en cours...")

    frames = []
    start_time = time.time()

    # Lancer les threads pour écouter l'utilisateur et le GPIO
    if lineFromMain is not None :
        threading.Thread(target=listen_for_gpio, daemon=True).start()
    else :
        threading.Thread(target=listen_for_stop, daemon=True).start()

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
