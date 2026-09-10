from datetime import datetime

def anya_heure():
    h = datetime.now().hour
    if 5 <= h < 12:
        return "Доброе утро… je viens de me réveiller."
    elif 12 <= h < 18:
        return "Bonne après-midi… je suis en pleine forme."
    elif 18 <= h < 23:
        return "Bonsoir… je deviens un peu mystérieuse."
    else:
        return "Il est tard… je suis en mode chouette nocturne."
