import os
import platform
from elevenlabs.client import ElevenLabs

def tts(prompt: str, key: str, save_directory: str, file_name: str, auto_open: bool, voice_id: str):
    if not key:
        return "API Keyを入力してください。"
    
    with open('elevenlabs_api_key.txt', 'w') as f:
        f.write(key)

    if not prompt:
        return "プロンプトを入力してください。"

    client = ElevenLabs(api_key=key)
    response = client.text_to_speech.convert(
      voice_id=voice_id,
      model_id="eleven_v4",
      text=prompt
    )

    if not save_directory:
        if platform.system() == "Windows":
            import getpass
            save_directory = f"C:/Users/{getpass.getuser()}/Downloads/"
        else:
            os.makedirs("output", exist_ok=True)
            save_directory = "output"
    
    if not file_name:
        file_name = "output.mp3"
    else:
        file_name += ".mp3"
    
    save_path = os.path.join(save_directory, file_name)
    
    with open(save_path, "wb") as f:
        f.write(b"".join(response))
    if auto_open:
        os.startfile(save_path)
    return "音声の生成が完了しました。"