#!/bin/bash

echo "🛠️ Installation des dépendances Python dans un environnement virtuel..."

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install PyQt6 faker PyPDF2
pip install pycryptodome

echo "✅ Dépendances installées."
echo "🚀 Lancement de l'application..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
python3 src/main.py

