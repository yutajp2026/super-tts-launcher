from google import genai
import base64
import gradio as gr

def tts(prompt: str, speaker: str, key: str) -> bytes | None:
    if not key:
        gr.Warning("Gemini:API Keyを入力してください。")
        return None
    
    with open('gemini_api_key.txt', 'w') as f:
        f.write(key)

    if not prompt:
        gr.Warning("Gemini:プロンプトを入力してください。")
        return None
    
    client = genai.Client(
        api_key=key,
        http_options={"api_version": "v1beta"},
    )

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


    audio = base64.b64decode(interaction.output_audio.data)
    gr.Info("Gemini (gemini-3.8-flash-tts) で音声を生成しました。")
    return audio
