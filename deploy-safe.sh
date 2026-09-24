#!/bin/bash

# --- CONFIG ---
WSL_DIR="$HOME/anya"
PIOTR="piotr"
PIOTR_DIR="/root/anya"
BACKUP_DIR="/root/anya-backups"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

echo "=== Déploiement SAFE d'Anya ==="

# --- Vérifier que le dossier existe ---
if [ ! -d "$WSL_DIR" ]; then
    echo "ERREUR: Le dossier $WSL_DIR n'existe pas."
    exit 1
fi

# --- Vérifier que bot.py existe ---
if [ ! -f "$WSL_DIR/bot.py" ]; then
    echo "ERREUR: bot.py est manquant dans WSL."
    exit 1
fi

# --- Créer un backup sur PIOTR ---
echo "Création du backup sur PIOTR..."
ssh $PIOTR "mkdir -p $BACKUP_DIR"
ssh $PIOTR "tar czf $BACKUP_DIR/anya-backup-$TIMESTAMP.tar.gz $PIOTR_DIR"

# --- Déployer le code (sans venv, sans DB, sans logs) ---
echo "Déploiement du code..."
rsync -av --exclude 'venv' --exclude '__pycache__' --exclude '*.db' --exclude '*.log' --exclude 'nohup.out' "$WSL_DIR/" "$PIOTR:$PIOTR_DIR/"

# --- Redémarrer Anya ---
echo "Redémarrage du bot..."
ssh $PIOTR "systemctl restart anya"

echo "=== Déploiement terminé avec succès ✔ ==="
