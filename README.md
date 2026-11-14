# Super TTS Launcher

入力したテキストから音声を生成するデスクトップ向けアプリです。ブラウザー上の画面から、話者や保存先を指定して手軽に音声を作成できます。

# アプリの特徴

- 生成スタイル
  - 多種類の音声合成に対応: 現時点では[Gemini API](https://ai.google.dev/gemini-api/docs/speech-generation?hl=ja)、[ElevenAPI](https://elevenlabs.io/docs/eleven-api/quickstart)、[VOICEVOX Core](https://github.com/VOICEVOX/voicevox_core)に対応しています。タブで切り替えて利用できます。
  - 話者・スタイルを選択: 話者や、一部ではスタイルを選べます。

- 生成音声をWebUI内で再生・ダウンロード: 生成後すぐに画面内のプレーヤーで確認し、ダウンロードボタンからブラウザーの機能で保存できます。

- クイック起動
  - ローカルのブラウザーで操作: アプリを起動すると、ブラウザーから使える画面が開きます(Windowsのみ)。
  - CUDAに対応: 対応するNVIDIA GPU環境では、一部機能をCUDAモードで起動します。

# インストール
## Windows
[Releases](https://github.com/yutajp2026/super-tts-launcher/releases)にインストーラを公開
## Linux
1. 下記のコマンドでPythonとgitをインストール
```bash
# Debian系(Ubuntuなど)
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```
```bash
# Red Hat系(Oracle Linuxなど)
sudo dnf install python3 python3-pip python3-venv git
```
```bash
# Arch系
sudo pacman install python3 python3-pip python3-venv git
```
```bash
# SUSE系
sudo zypper install python3 python3-pip python3-venv git
```
2. `git clone https://github.com/yutajp2026/super-tts-launcher.git`でこのリポジトリをクローン
3. `cd super-tts-launcher`でスクリプトディレクトリに移動
4. `bash launcher.sh`で実行 ⚠️linuxの場合は自動でブラウザを開きません。
5. `git pull`でアップデート

# ライセンス

本プロジェクトは、必要に応じて自由に改変・利用できます。ただし、悪用は厳禁です。なお、改変時や音声の使用時は各AIのライセンスを守ってください。VOICEVOXに関しては音声のクレジット表記
が必要です。
