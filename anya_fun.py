import random
from datetime import datetime

def get_insulte():
    insultes = [
        "espèce de canard rouillé",
        "bot de bas étage",
        "crétin de l’espace",
        "champion du lag",
        "pigeon numérique"
    ]
    return random.choice(insultes)

def get_canard():
    facts = [
        "Les canards ont des accents régionaux.",
        "Un canard peut voler jusqu’à 100 km/h.",
        "Les canards sont mon animal préféré, quack.",
        "Les canards sont les vrais maîtres du réseau Ghost."
    ]
    return random.choice(facts)

def get_fete():
    today = datetime.now().strftime("%m-%d")
    fetes = {
        "01-01": "Nouvel An 🎉",
        "02-14": "Saint-Valentin ❤️",
        "07-01": "Fête du Canada 🍁",
        "12-25": "Noël 🎄"
    }
    return fetes.get(today, "Aucune fête spéciale aujourd’hui.")
