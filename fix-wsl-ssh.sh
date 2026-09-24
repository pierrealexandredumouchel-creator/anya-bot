#!/bin/bash

WIN_SSH="/mnt/c/Users/$USER/.ssh"
WSL_SSH="$HOME/.ssh"

echo "=== FIX SSH POUR WSL ==="

# Créer ~/.ssh si absent
mkdir -p "$WSL_SSH"

# Copier la clé id_empire si elle existe
if [ -f "$WIN_SSH/id_empire" ]; then
    cp "$WIN_SSH/id_empire" "$WSL_SSH/"
    chmod 600 "$WSL_SSH/id_empire"
    echo "Clé id_empire copiée ✔"
else
    echo "ATTENTION: id_empire manquante dans Windows"
fi

# Copier le fichier config
if [ -f "$WIN_SSH/config" ]; then
    cp "$WIN_SSH/config" "$WSL_SSH/"
    chmod 600 "$WSL_SSH/config"
    echo "SSH config copié ✔"
else
    echo "ATTENTION: config manquant dans Windows"
fi

echo "=== TEST SSH WSL ==="
ssh -o BatchMode=yes -o ConnectTimeout=5 piotr "echo OK" 2>/dev/null && echo "piotr : OK" || echo "piotr : ECHEC"

echo "Terminé ✔"
