import gpiod
import time

# Numéro du GPIO connecté (remplace 17 par le bon numéro si besoin)
BUTTON_PIN = 17
chip = gpiod.Chip('gpiochip0')
line = chip.get_line(BUTTON_PIN)

# Configuration de la broche en entrée
line.request(consumer="test", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

try:
    while True:
        # Lecture directe de la broche
        state = line.get_value()
        print(f"État brut de la broche : {state}")
        
        # Interprétation simple
        if state == 1:
            print("Décroché")
        else:
            print("Raccroché")
            
        time.sleep(3)
except KeyboardInterrupt:
    pass
finally:
    line.release()