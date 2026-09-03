# 🩷 Anya — IRC Bot Modulaire (Undernet / Libera / ZNC)

> Petite bot russe numérique, sarcastique, cute, chouette, mood‑based, avec DB, météo, quotes, roast, fêtes, canards, seen, multi‑channels et modules avancés.

---

## 🎵 Playlist Vandresse (Geocities Style)

[YouTube Playlist — Vandresse](https://www.youtube.com/playlist?list=PLIk2NJhFJy5U)

> À écouter pendant que tu codes Anya.  
> Ambiance rétro, cyber‑occult, Ghost Network vibes.

---
# 🤖 Anya — IRC AI Bot

Anya est un bot IRC intelligent écrit en Python.  
Elle se connecte à Undernet, écoute les messages, répond avec une IA (OpenAI, Claude, Gemini, etc.), et offre plusieurs modules : météo, fun, personnalité, humeur, temps, etc.

Ce projet est conçu pour tourner sur un VPS Linux (Ubuntu 24.04+), avec un environnement virtuel Python et un service systemd pour un fonctionnement 24/7.

---

## ✨ Fonctionnalités

- Connexion IRC (Undernet ou autre réseau)
- Réponses IA via API (OpenAI par défaut)
- Commandes météo
- Commandes fun
- Gestion de la personnalité
- Gestion de l’humeur
- Logs complets dans `/var/log/anya.log`
- Déploiement automatisé via `deploy.sh`
- Service systemd pour exécution continue

---

## 📦 Installation (VPS)

### 1. Cloner ou transférer le projet

Sur votre VPS :

```bash
mkdir /root/anya
cd /root/anya
Transférez vos fichiers via SCP ou Git.

2. Créer le venv
bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install httpx
🔧 Configuration systemd
Créer le fichier :

bash
nano /etc/systemd/system/anya.service
Contenu :

ini
[Unit]
Description=Anya IRC Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/anya
Environment="PYTHONPATH=/root/anya/venv/lib/python3.12/site-packages"
ExecStart=/root/anya/venv/bin/python3 /root/anya/anya.py
Restart=always
RestartSec=5
User=root

StandardOutput=append:/var/log/anya.log
StandardError=append:/var/log/anya.log

[Install]
WantedBy=multi-user.target
Activer le service :

bash
systemctl daemon-reload
systemctl enable anya.service
systemctl start anya.service
Vérifier :

bash
systemctl status anya.service
tail -f /var/log/anya.log
🚀 Déploiement automatique (WSL → VPS)
Dans votre machine locale (WSL) :

Créer deploy.sh :

bash
#!/bin/bash

SERVER="67.215.13.169"

echo "[1] Packaging Anya..."
rm -f anya.tar.gz
tar czf anya.tar.gz *

echo "[2] Sending to VPS..."
scp anya.tar.gz root@$SERVER:/root/

echo "[3] Deploying on VPS..."
ssh -t root@$SERVER "
cd /root &&
rm -rf anya &&
mkdir anya &&
tar xzf anya.tar.gz -C anya &&
cd anya &&
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
pip install httpx &&
systemctl restart anya.service
"

echo "[4] Deployment complete."
Exécuter :

bash
chmod +x deploy.sh
./deploy.sh
🧠 API IA (OpenAI)
Dans anya.py, configurez votre clé :

python
r = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {OPENAI_KEY}"},
    json=payload,
)
📁 Structure du projet
Code
anya/
├── anya.py
├── anya_server.py
├── anya_db.py
├── anya_fun.py
├── anya_weather.py
├── anya_personality.py
├── anya_mood.py
├── anya_time.py
├── anya_bots.py
├── requirements.txt
└── venv/
📝 Logs
Les logs sont écrits dans :

Code
/var/log/anya.log
Pour suivre en direct :

bash
tail -f /var/log/anya.log
❤️ Crédits
Développement : alxd  
Support technique : Copilot  
Inspiration : Undernet, IRC, AI bots

📜 Licence
MIT License — utilisez, modifiez, partagez librement.


## 🚀 Fonctionnalités

- Multi‑serveurs IRC (Undernet, Libera)
- Multi‑channels (#montreal, #kodi)
- Support ZNC (PASS auto)
- Météo (OpenWeatherMap)
- Seen (SQLite)
- Quotes + random
- Insultes random
- Fêtes du jour
- Canards random
- Personnalité russe cute
- Sarcasme
- Humeur aléatoire
- Heure intelligente
- Roast des autres bots
- Architecture modulaire PRO

---

## 🧩 Structure

