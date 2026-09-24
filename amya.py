#!/usr/bin/env python3
import socket
import time

from anya_server import SERVER, PORT, CHANNELS, ZNC_PASS
from anya_db import init_db, log_seen, get_seen, add_quote, random_quote
from anya_fun import get_insulte, get_canard, get_fete
from anya_weather import get_weather
from anya_personality import anya_intro, anya_sarcasme, anya_cute
from anya_mood import anya_humeur
from anya_time import anya_heure
from anya_bots import anya_roast


def send(sock, msg):
    """Envoie un message IRC et l'affiche dans le terminal."""
    sock.send((msg + "\r\n").encode("utf-8"))
    print(">>", msg)


def connect():
    """Connexion au serveur IRC."""
    sock = socket.socket()
    sock.connect((SERVER, PORT))

    if ZNC_PASS:
        send(sock, f"PASS {ZNC_PASS}")

    send(sock, "NICK Anya")
    send(sock, "USER Anya 0 * :AnyaBot")
    return sock


def main():
    init_db()
    sock = connect()

    while True:
        try:
            data = sock.recv(4096).decode("utf-8", errors="ignore")
        except Exception:
            print("Connexion perdue… reconnexion dans 5 sec.")
            time.sleep(5)
            sock = connect()
            continue

        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue

            print("<<", line)

            # PING/PONG
            if line.startswith("PING"):
                send(sock, "PONG " + line.split()[1])
                continue

            # JOIN après connexion
            if " 001 " in line:
                for chan in CHANNELS:
                    send(sock, f"JOIN {chan}")
                continue

            # PRIVMSG
            if "PRIVMSG" in line:
                parts = line.split(":", 2)
                if len(parts) < 3:
                    continue

                msg = parts[2].strip()
                user = line.split("!")[0][1:]

                # Log du seen
                log_seen(user)

                # Commandes
                if msg == "!anya":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_intro()}")

                elif msg == "!ping":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :pong!")

                # Seen
                elif msg.startswith("!seen "):
                    target = msg.split(" ", 1)[1]
                    seen = get_seen(target)
                    if seen:
                        send(sock, f"PRIVMSG {CHANNELS[0]} :{target} vu le {seen}")
                    else:
                        send(sock, f"PRIVMSG {CHANNELS[0]} :jamais vu {target}")

                # Quotes
                elif msg.startswith("!quote "):
                    quote = msg.split(" ", 1)[1]
                    add_quote(user, quote)
                    send(sock, f"PRIVMSG {CHANNELS[0]} :quote ajouté pour {user}")

                elif msg == "!quote":
                    q = random_quote()
                    if q:
                        send(sock, f"PRIVMSG {CHANNELS[0]} :{q[0]} a dit: {q[1]}")
                    else:
                        send(sock, f"PRIVMSG {CHANNELS[0]} :aucune citation")

                # Météo
                elif msg.startswith("!weather "):
                    city = msg.split(" ", 1)[1]
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{get_weather(city)}")

                # Fun
                elif msg == "!insulte":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{get_insulte()}")

                elif msg == "!canard":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{get_canard()}")

                elif msg == "!fete":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{get_fete()}")

                # Personnalité russe cute / sarcasme
                #elif msg == "!cute":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_cute()}")

                elif msg == "!sarcasme":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_sarcasme()}")

                # Humeur aléatoire
                elif msg == "!humeur":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_humeur()}")

                # Heure intelligente
                elif msg == "!heure":
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_heure()}")

                # Roast bots
                elif msg.startswith("!roast "):
                    target = msg.split(" ", 1)[1]
                    send(sock, f"PRIVMSG {CHANNELS[0]} :{anya_roast(target)}")


if __name__ == "__main__":
    main()
