from elevenlabs.client import ElevenLabs
import gradio as gr

def tts(prompt: str, key: str, voice_id: str) -> bytes | None:
    if not key:
        gr.Warning("ElevenLabs:API Keyを入力してください。")
        return None
    
    with open('elevenlabs_api_key.txt', 'w') as f:
        f.write(key)

    if not prompt:
        gr.Warning("ElevenLabs:プロンプトを入力してください。")
        return None

    client = ElevenLabs(api_key=key)
    response = client.text_to_speech.convert(
      voice_id=voice_id,
      model_id="eleven_v4",
      text=prompt
    )

    audio = b"".join(response)
    gr.Info("ElevenLabs (eleven_v4) で音声を生成しました。")
    return audio
