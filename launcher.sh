#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-tk fonts-ipafont

echo "仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv "venv"
fi

# shellcheck disable=SC1090
source "venv/bin/activate"

echo "pip を更新中..."
python -m pip install --upgrade pip

echo "google-genai と gradio をインストール中..."
python -m pip install google-genai gradio

echo "アプリを起動中..."
cd app
python gemini_linux.py
