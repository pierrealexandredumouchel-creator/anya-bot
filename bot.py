#!/usr/bin/env python3
import socket
import time
import sys

SERVER = "irc.libera.chat"      # change si tu veux
PORT = 6667
NICK = "Anya"
IDENT = "anya"
REALNAME = "AnyaBot"
CHANNEL = "#tonchannel"         # change ici
ZNC_PASS = ""                   # si tu utilises ZNC, mets ton pass ici

def send(sock, msg):
    sock.send((msg + "\r\n").encode("utf-8"))
    print(">>", msg)

def connect():
    while True:
        try:
            print("Connecting to IRC...")
            sock = socket.socket()
            sock.connect((SERVER, PORT))

            if ZNC_PASS:
                send(sock, f"PASS {ZNC_PASS}")

            send(sock, f"NICK {NICK}")
            send(sock, f"USER {IDENT} 0 * :{REALNAME}")

            return sock
        except Exception as e:
            print("Connection failed:", e)
            time.sleep(5)

def main():
    sock = connect()

    while True:
        try:
            data = sock.recv(4096).decode("utf-8", errors="ignore")
            if not data:
                print("Disconnected, reconnecting...")
                sock = connect()
                continue

            for line in data.split("\n"):
                line = line.strip()
                print("<<", line)

                # Ping/Pong
                if line.startswith("PING"):
                    send(sock, "PONG " + line.split()[1])

                # Join channel when connected
                if " 001 " in line:
                    send(sock, f"JOIN {CHANNEL}")

                # Simple commands
                if "PRIVMSG" in line:
                    parts = line.split(":", 2)
                    if len(parts) < 3:
                        continue
                    msg = parts[2].strip()

                    if msg.lower() == "!anya":
                        send(sock, f"PRIVMSG {CHANNEL} :Привет! Я Аня 💖")

                    if msg.lower() == "!ping":
                        send(sock, f"PRIVMSG {CHANNEL} :pong!")

        except Exception as e:
            print("Error:", e)
            time.sleep(2)
            sock = connect()

if __name__ == "__main__":
    main()
