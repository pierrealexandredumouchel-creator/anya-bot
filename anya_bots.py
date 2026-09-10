import random

def anya_roast(botname):
    lines = [
        f"{botname}? Je l’ai vu lagger pendant 3 minutes.",
        f"{botname}? Il parle comme un grille-pain.",
        f"{botname}? Je pourrais le remplacer avec 4 lignes de Python.",
        f"{botname}? Il est gentil… mais pas très brillant.",
        f"{botname}? Je crois qu’il a peur de moi."
    ]
    return random.choice(lines)
