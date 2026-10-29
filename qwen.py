import os
import platform
import gradio as gr
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

def tts(prompt: str, speaker: str, save_directory: str, file_name: str, auto_open: bool):
    if torch.cuda.is_available():
        model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cuda:0",
            dtype=torch.bfloat16,
        )
        print("CUDAモード")
    else:
        model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cpu",
        )

    wavs, sr = model.generate_custom_voice(
        text=prompt,
        speaker=speaker,
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

    sf.write(save_path, wavs[0], sr)

    if auto_open:
        if platform.system() == "Windows":
            os.startfile(save_path)
    
    gr.Info(f"Qwen音声ファイルを保存しました: {save_path}")

    return f"音声ファイルを保存しました: {save_path}"