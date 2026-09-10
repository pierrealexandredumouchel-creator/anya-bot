import random

def anya_humeur():
    moods = [
        "hyperactive",
        "fatiguée",
        "vodka-mode",
        "grincheuse",
        "chouette",
        "glaciale",
        "trop mignonne pour être vraie",
        "mode ninja",
        "mode espion russe",
        "mode caféine"
    ]
    mood = random.choice(moods)
    return f"Aujourd’hui, Anya est en mode: {mood}."
