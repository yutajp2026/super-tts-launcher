import os
from google import genai
import gradio as gr
import base64
import platform

def tts(prompt: str, speaker: str, save_directory: str, file_name: str, key: str, auto_open: bool):
    if not key:
        return "API Keyを入力してください。"
    
    with open('gemini_api_key.txt', 'w') as f:
        f.write(key)

    if not prompt:
        return "プロンプトを入力してください。"
    
    client = genai.Client(api_key=key)

    interaction = client.interactions.create(
        model="gemini-3.8-flash-tts",
        input=[{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": prompt,
            }],
        }],
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": speaker},
            ]
        },
    )


    if not save_directory:
        if platform.system() == "Windows":
            import getpass
            save_directory = f"C:/Users/{getpass.getuser()}/Downloads/"
        else:
            os.makedirs("output", exist_ok=True)
            save_directory = "output"

    if not file_name:
        file_name = "output.wav"
    else:
        file_name += ".wav"

    save_path = os.path.join(save_directory, file_name)

    with open(save_path, "wb") as f:
        f.write(base64.b64decode(interaction.output_audio.data))

    if auto_open:
        if platform.system() == "Windows":
            os.startfile(save_path)

    gr.Info(f"音声ファイルを保存しました: {save_path}")

    return f"音声ファイルを保存しました: {save_path}"
