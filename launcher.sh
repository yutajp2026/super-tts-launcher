#!/bin/bash

echo "仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv "venv"
fi

# shellcheck disable=SC1090
source "venv/bin/activate"

echo "pip を更新中..."
python -m pip install --upgrade pip

echo "パッケージをインストール中..."
python -m pip install -r requirements.txt

echo "アプリを起動中..."
python app.py
