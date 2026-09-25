import socket
import time
import sqlite3
import random

SERVER = "irc6.undernet.org"
PORT = 6667
BINDHOST = "2001:470:b2af::6"
NICK = "Anya"
CHANNELS = ["#montreal", "#kodi"]

# --- DB SETUP ---
db = sqlite3.connect("anya.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user TEXT,
    message TEXT,
    ts INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS flood (
    user TEXT,
    last_ts INTEGER,
    count INTEGER
)
""")

db.commit()

def log_message(user, msg):
    cur.execute("INSERT INTO memory (user, message, ts) VALUES (?, ?, ?)",
                (user, msg, int(time.time())))
    db.commit()

def anti_flood(user):
    now = int(time.time())
    cur.execute("SELECT last_ts, count FROM flood WHERE user=?", (user,))
    row = cur.fetchone()

    if row is None:
        cur.execute("INSERT INTO flood VALUES (?, ?, ?)", (user, now, 1))
        db.commit()
        return False

    last_ts, count = row

    if now - last_ts > 5:
        cur.execute("UPDATE flood SET last_ts=?, count=? WHERE user=?",
                    (now, 1, user))
        db.commit()
        return False

    if count > 5:
        return True

    cur.execute("UPDATE flood SET last_ts=?, count=? WHERE user=?",
                (now, count + 1, user))
    db.commit()
    return False

def send(sock, msg):
    sock.send((msg + "\r\n").encode("utf-8"))

def connect():
    family = socket.AF_INET6 if ":" in BINDHOST else socket.AF_INET

    sock = socket.socket(family, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.settimeout(300)
    sock.bind((BINDHOST, 0))

    print(f"Connecting to {SERVER}:{PORT} from {BINDHOST}...")
    sock.connect((SERVER, PORT))

    send(sock, f"NICK {NICK}")
    send(sock, f"USER {NICK} 0 * :AnyaBot")

    return sock


def main():
    sock = connect()

    slap_replies = [
        "Hey! calme-toi 😂",
        "Ouch! t’es rough toi 😅",
        "Tabarnak! 😂",
        "Aïe! esti que tu frappes fort 😆"
    ]

    while True:
        try:
            raw = sock.recv(4096)

            if not raw:
                raise ConnectionError("IRC server closed the connection")

            data = raw.decode("utf-8", errors="ignore")

            for line in data.split("\n"):
                line = line.strip()
                if not line:
                    continue

                print(line)

                if line.startswith("PING"):
                    send(sock, "PONG " + line.split()[1])

                if " 001 " in line:
                    for chan in CHANNELS:
                        send(sock, f"JOIN {chan}")

                if "PRIVMSG" in line:
                    parts = line.split(":", 2)
                    if len(parts) < 3:
                        continue

                    # Le channel d'origine est le 3e mot: "nick!user@host PRIVMSG #channel"
                    target = parts[1].split()[2]
                    # Ignore les messages prives (target = notre nick, pas un #channel)
                    if not target.startswith("#"):
                        continue

                    msg = parts[2].strip().lower()
                    nick = line.split("!")[0].replace(":", "")

                    log_message(nick, msg)

                    if anti_flood(nick):
                        continue

                    if "anya" in msg and len(msg) < 120:
                        send(sock, f"PRIVMSG {target} :{nick}: oui je suis là 💜")

                    if msg.startswith("allo anya") or msg.startswith("salut anya"):
                        send(sock, f"PRIVMSG {target} :Allo {nick} 😊")

                    if "slaps anya" in msg or "slap anya" in msg:
                        send(sock, f"PRIVMSG {target} :{random.choice(slap_replies)}")

                    if nick == "alxd" and "anya" in msg:
                        send(sock, f"PRIVMSG {target} :Oui {nick}, je t’écoute 💜")

                    if msg == "!anya":
                        send(sock, f"PRIVMSG {target} :Привет! Я Аня 💖")

                    if msg == "!ping":
                        send(sock, f"PRIVMSG {target} :pong!")

        except Exception as e:
            print("Error:", e)
            time.sleep(2)
            sock = connect()

if __name__ == "__main__":
    main()
