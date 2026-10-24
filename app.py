import os
import time
import webbrowser
import gradio as gr
import platform
import gemini_tts

if os.path.exists('gemini_api_key.txt'):
    with open('gemini_api_key.txt', "r", encoding="utf-8") as f:
        gemini_api_key = f.read()

with gr.Blocks() as demo:
    with gr.Tab("Gemini"):
        gr.Markdown("# Gemini 3.1 Flash TTS Preview")
        gr.Markdown("API Keyは[ここ](https://aistudio.google.com/api-keys)から取得してください。")
        prompt = gr.Textbox(label="prompt", placeholder="入力テキスト。")
        api_key = gr.Textbox(label="API Key", placeholder="Gemini API Key", value=gemini_api_key if os.path.exists('gemini_api_key.txt') else "", type="password")
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
        save_directory = gr.Textbox(label="save_directory", placeholder="音声を保存するディレクトリ。")
        file_name = gr.Textbox(label="file_name", placeholder="保存するファイル名。")
        auto_open = gr.Checkbox(label="auto_open", value=True)
        output = gr.Audio(label="Output")

        generate_button = gr.Button("Generate")
        generate_button.click(fn=gemini_tts.tts, inputs=[prompt, speaker, save_directory, file_name, api_key, auto_open], outputs=output)
    with gr.Tab("メニュー"):
        gr.Markdown("# サーバー")
        def quit(save_keys: bool):
            if not save_keys:
                if os.path.exists('gemini_api_key.txt'):
                    os.remove('gemini_api_key.txt')
            gr.Info("アプリケーション終了。タブは手動で閉じてください。")
            time.sleep(1)
            os._exit(0)
        save_keys = gr.Checkbox(label="APIキーを保持", value=True, interactive=True)
        quit_btn = gr.Button("終了")
        quit_btn.click(fn=quit, inputs=[save_keys], outputs=[])

if platform.system() == "Windows":
    webbrowser.open('http://127.0.0.1:7860')
else:
    print("下記のURLをブラウザで開いてください。")

demo.launch()