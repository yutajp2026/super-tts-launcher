import os
import time
import webbrowser
import gradio as gr
import platform
import gemini_tts
import voicevox
import elevenlabs_tts

if os.path.exists('gemini_api_key.txt'):
    with open('gemini_api_key.txt', "r", encoding="utf-8") as f:
        gemini_api_key = f.read()
if os.path.exists('elevenlabs_api_key.txt'):
    with open('elevenlabs_api_key.txt', "r", encoding="utf-8") as f:
        elevenlabs_api_key = f.read()

with gr.Blocks() as demo:
    with gr.Tab("Gemini"):
        gr.Markdown("# Gemini 3.8 Flash TTS")
        gr.Markdown("API Keyは[ここ](https://aistudio.google.com/api-keys)から取得してください。")
        prompt = gr.Textbox(label="prompt", placeholder="入力テキスト。")
        api_key = gr.Textbox(label="API Key", placeholder="Gemini API Key", value=gemini_api_key if os.path.exists('gemini_api_key.txt') else "")
        speakers = [
            "Zephyr",
            "Puck",
            "Charon",
            "Kore",
            "Fenrir",
            "Leda",
            "Orus",
            "Aoede",
            "Callirrhoe",
            "Autonoe",
            "Enceladus",
            "Iapetus",
            "Umbriel",
            "Algieba",
            "Despina",
            "Erinome",
            "Algenib",
            "Rasalgethi",
            "Laomedeia",
            "Achernar",
            "Alnilam",
            "Schedar",
            "Gacrux",
            "Pulcherrima",
            "Achird",
            "Zubenelgenubi",
            "Vindemiatrix",
            "Sadachbia",
            "Sadaltager",
            "Sulafat",
        ]
        speaker = gr.Dropdown(label="speaker", choices=speakers, value="Kore")
        audio_output = gr.Audio(label="生成音声", buttons=["download"])

        generate_button = gr.Button("Generate")
        generate_button.click(fn=gemini_tts.tts, inputs=[prompt, speaker, api_key], outputs=audio_output)
    with gr.Tab("ElevenLabs"):
        gr.Markdown("# Eleven V4")
        gr.Markdown("API Keyは[ここ](https://elevenlabs.io/app/developers/api-keys)から取得してください。")
        gr.Markdown("音声IDは[ここ](https://elevenlabs.io/app/voice-library)から確認できます。")
        prompt = gr.Textbox(label="prompt", placeholder="入力テキスト。")
        voice_id = gr.Textbox(label="voice_id", placeholder="音声ID。ElevenLabsのサイトで確認できます。", value="JBFqnCBsd6RMkjVDRZzb")
        api_key = gr.Textbox(label="API Key", placeholder="ElevenLabs API Key", value=elevenlabs_api_key if os.path.exists('elevenlabs_api_key.txt') else "")
        audio_output = gr.Audio(label="生成音声", buttons=["download"])
        generate_button = gr.Button("Generate")
        generate_button.click(fn=elevenlabs_tts.tts, inputs=[prompt, api_key, voice_id], outputs=audio_output)
    with gr.Tab("Voicevox"):
        gr.Markdown("# Voicevox Core")
        if os.getenv("device") == "cuda":
            gr.Markdown("CUDAモード")
        prompt = gr.Textbox(label="prompt", placeholder="入力テキスト。")
        speaker = gr.Dropdown(label="speaker", choices=list(voicevox.VOICE_MODELS.keys()), value="ずんだもん")
        style = gr.Textbox(label="style", placeholder="スタイル。hなどと入力すると選択したキャラクターの一覧が表示されます。")
        audio_output = gr.Audio(label="生成音声", buttons=["download"])
        generate_button = gr.Button("Generate")
        generate_button.click(fn=voicevox.tts, inputs=[prompt, speaker, style], outputs=audio_output)
    with gr.Tab("メニュー"):
        gr.Markdown("# サーバー")
        def quit(save_keys: bool):
            if not save_keys:
                if os.path.exists('gemini_api_key.txt'):
                    os.remove('gemini_api_key.txt')
                if os.path.exists('elevenlabs_api_key.txt'):
                    os.remove('elevenlabs_api_key.txt')
            gr.Info("アプリケーション終了。タブは手動で閉じてください。")
            time.sleep(1)
            os._exit(0)
        save_keys = gr.Checkbox(label="APIキーを保持", value=True, interactive=True)
        quit_btn = gr.Button("終了")
        quit_btn.click(fn=quit, inputs=[save_keys], outputs=[])
        gr.Markdown("# 製品について")
        gr.Markdown("https://github.com/yutajp2026/super-tts-launcher")
        version = os.getenv("VERSION")
        if version:
            gr.Markdown("最新のバージョンは、上記GitHubページで確認できます。")
            gr.Markdown("現在使用しているアプリのバージョン: " + version)

if platform.system() == "Windows":
    webbrowser.open('http://127.0.0.1:7860')
else:
    print("下記のURLをブラウザで開いてください。")

demo.launch()