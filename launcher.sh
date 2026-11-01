#!/bin/bash

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 が見つかりません。Python 3 をインストールしてください。" >&2
    exit 1
fi

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
python -m pip install https://github.com/VOICEVOX/voicevox_core/releases/download/0.17.1/voicevox_core-0.17.1-cp310-abi3-manylinux_2_34_x86_64.whl

if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
    device=cuda
else
    device=cpu
fi

if [ ! -d "voicevox_core" ]; then
    binary=download-linux-x64
    curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary} -o voicevox-download
    chmod +x voicevox-download
    ./voicevox-download --devices ${device}
fi

echo "アプリを起動中..."
python app.py
