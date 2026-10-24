import os
from typing import Optional
import gradio as gr
import platform
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile


VOICE_MODELS: dict[str, dict[str, tuple[str, int]]] = {
    "四国めたん": {
        "ノーマル": ("0.vvm", 2),
        "あまあま": ("0.vvm", 0),
        "ツンツン": ("0.vvm", 6),
        "セクシー": ("0.vvm", 4),
        "ささやき": ("5.vvm", 36),
        "ヒソヒソ": ("5.vvm", 37),
    },
    "ずんだもん": {
        "ノーマル": ("0.vvm", 3),
        "あまあま": ("0.vvm", 1),
        "ツンツン": ("0.vvm", 7),
        "セクシー": ("0.vvm", 5),
        "ささやき": ("5.vvm", 22),
        "ヒソヒソ": ("5.vvm", 38),
        "ヘロヘロ": ("15.vvm", 75),
        "なみだめ": ("15.vvm", 76),
    },
    "春日部つむぎ": {"ノーマル": ("0.vvm", 8)},
    "雨晴はう": {"ノーマル": ("0.vvm", 10)},
    "冥鳴ひまり": {"ノーマル": ("1.vvm", 14)},
    "九州そら": {
        "ノーマル": ("2.vvm", 16),
        "あまあま": ("2.vvm", 15),
        "ツンツン": ("2.vvm", 18),
        "セクシー": ("2.vvm", 17),
        "ささやき": ("5.vvm", 19),
    },
    "波音リツ": {"ノーマル": ("3.vvm", 9), "クイーン": ("3.vvm", 65)},
    "中国うさぎ": {
        "ノーマル": ("3.vvm", 61),
        "おどろき": ("3.vvm", 62),
        "こわがり": ("3.vvm", 63),
        "へろへろ": ("3.vvm", 64),
    },
    "玄野武宏": {
        "ノーマル": ("4.vvm", 11),
        "喜び": ("10.vvm", 39),
        "ツンギレ": ("10.vvm", 40),
        "悲しみ": ("10.vvm", 41),
    },
    "剣崎雌雄": {"ノーマル": ("4.vvm", 21)},
    "No.7": {
        "ノーマル": ("6.vvm", 29),
        "アナウンス": ("6.vvm", 30),
        "読み聞かせ": ("6.vvm", 31),
    },
    "後鬼": {
        "人間ver.": ("7.vvm", 27),
        "ぬいぐるみver.": ("7.vvm", 28),
        "人間（怒り）ver.": ("16.vvm", 87),
        "鬼ver.": ("16.vvm", 88),
    },
    "WhiteCUL": {
        "ノーマル": ("8.vvm", 23),
        "たのしい": ("8.vvm", 24),
        "かなしい": ("8.vvm", 25),
        "びえーん": ("8.vvm", 26),
    },
    "白上虎太郎": {
        "ふつう": ("9.vvm", 12),
        "わーい": ("9.vvm", 32),
        "びくびく": ("9.vvm", 33),
        "おこ": ("9.vvm", 34),
        "びえーん": ("9.vvm", 35),
    },
    "ちび式じい": {"ノーマル": ("10.vvm", 42)},
    "櫻歌ミコ": {
        "ノーマル": ("11.vvm", 43),
        "第二形態": ("11.vvm", 44),
        "ロリ": ("11.vvm", 45),
    },
    "ナースロボ＿タイプＴ": {
        "ノーマル": ("11.vvm", 47),
        "楽々": ("11.vvm", 48),
        "恐怖": ("11.vvm", 49),
        "内緒話": ("11.vvm", 50),
    },
    "†聖騎士 紅桜†": {"ノーマル": ("12.vvm", 51)},
    "雀松朱司": {"ノーマル": ("12.vvm", 52)},
    "麒ヶ島宗麟": {"ノーマル": ("12.vvm", 53)},
    "春歌ナナ": {"ノーマル": ("13.vvm", 54)},
    "猫使アル": {
        "ノーマル": ("13.vvm", 55),
        "おちつき": ("13.vvm", 56),
        "うきうき": ("13.vvm", 57),
        "つよつよ": ("21.vvm", 110),
        "へろへろ": ("21.vvm", 111),
    },
    "猫使ビィ": {
        "ノーマル": ("13.vvm", 58),
        "おちつき": ("13.vvm", 59),
        "人見知り": ("13.vvm", 60),
        "つよつよ": ("21.vvm", 112),
    },
    "栗田まろん": {"ノーマル": ("14.vvm", 67)},
    "あいえるたん": {"ノーマル": ("14.vvm", 68)},
    "満別花丸": {
        "ノーマル": ("14.vvm", 69),
        "元気": ("14.vvm", 70),
        "ささやき": ("14.vvm", 71),
        "ぶりっ子": ("14.vvm", 72),
        "ボーイ": ("14.vvm", 73),
    },
    "琴詠ニア": {"ノーマル": ("14.vvm", 74)},
    "青山龍星": {
        "ノーマル": ("15.vvm", 13),
        "熱血": ("15.vvm", 81),
        "不機嫌": ("15.vvm", 82),
        "喜び": ("15.vvm", 83),
        "しっとり": ("15.vvm", 84),
        "かなしみ": ("15.vvm", 85),
        "囁き": ("15.vvm", 86),
    },
    "もち子さん": {
        "ノーマル": ("15.vvm", 20),
        "セクシー／あん子": ("15.vvm", 66),
        "泣き": ("15.vvm", 77),
        "怒り": ("15.vvm", 78),
        "喜び": ("15.vvm", 79),
        "のんびり": ("15.vvm", 80),
    },
    "小夜/SAYO": {"ノーマル": ("15.vvm", 46)},
    "Voidoll": {"ノーマル": ("17.vvm", 89)},
    "ぞん子": {
        "ノーマル": ("18.vvm", 90),
        "低血圧": ("18.vvm", 91),
        "覚醒": ("18.vvm", 92),
        "実況風": ("18.vvm", 93),
    },
    "中部つるぎ": {
        "ノーマル": ("18.vvm", 94),
        "怒り": ("18.vvm", 95),
        "ヒソヒソ": ("18.vvm", 96),
        "おどおど": ("18.vvm", 97),
        "絶望と敗北": ("18.vvm", 98),
    },
    "離途": {"ノーマル": ("19.vvm", 99), "シリアス": ("19.vvm", 101)},
    "黒沢冴白": {"ノーマル": ("19.vvm", 100)},
    "ユーレイちゃん": {
        "ノーマル": ("20.vvm", 102),
        "甘々": ("20.vvm", 103),
        "哀しみ": ("20.vvm", 104),
        "ささやき": ("20.vvm", 105),
        "ツクモちゃん": ("20.vvm", 106),
    },
    "東北ずん子": {"ノーマル": ("21.vvm", 107)},
    "東北きりたん": {"ノーマル": ("21.vvm", 108)},
    "東北イタコ": {"ノーマル": ("21.vvm", 109)},
    "あんこもん": {
        "ノーマル": ("22.vvm", 113),
        "つよつよ": ("22.vvm", 114),
        "よわよわ": ("22.vvm", 115),
        "けだるげ": ("22.vvm", 116),
        "ささやき": ("23.vvm", 117),
    },
    "夜語トバリ": {
        "ノーマル": ("24.vvm", 118),
        "明るい": ("24.vvm", 119),
        "哀しみ": ("24.vvm", 120),
        "呆れ": ("24.vvm", 121),
    },
    "暁記ミタマ": {
        "ノーマル": ("24.vvm", 122),
        "怒り": ("24.vvm", 123),
        "哀しみ": ("24.vvm", 124),
        "ささやき": ("24.vvm", 125),
    },
    "里石ユカ": {"つぼみ": ("24.vvm", 126)},
}


def tts(
    prompt: str,
    speaker: str,
    save_directory: str,
    file_name: str,
    auto_open: bool,
    style: str,
):
    if speaker not in VOICE_MODELS:
        return f"未対応の話者です: {speaker}"

    available_styles = VOICE_MODELS[speaker]
    if style  == "":
        style = "ノーマル" if "ノーマル" in available_styles else next(iter(available_styles))
    if style not in available_styles:
        styles = ", ".join(available_styles)
        return f"{speaker} の利用可能スタイルはこれらのみです: {styles})"
    if not prompt:
        return "プロンプトを入力してください。"

    model_filename, style_id = available_styles[style]

    voicevox_onnxruntime_path = os.path.join(
        "voicevox_core",
        "onnxruntime",
        "lib",
        Onnxruntime.LIB_RECOMMENDED_VERSIONED_FILENAME,
    )
    open_jtalk_dict_dir = os.path.join(
        "voicevox_core", "dict", "open_jtalk_dic_utf_8-1.11"
    )
    synthesizer = Synthesizer(
        Onnxruntime.load_once(filename=voicevox_onnxruntime_path),
        OpenJtalk(open_jtalk_dict_dir),
    )

    model_dir = os.path.join("voicevox_core", "models", "vvms")
    with VoiceModelFile.open(os.path.join(model_dir, model_filename)) as model:
        synthesizer.load_voice_model(model)

    wav = synthesizer.tts(prompt, style_id)

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

    save_path = os.path.join(save_directory, f"{file_name}")
    with open(save_path, "wb") as output_file:
        output_file.write(wav)

    if auto_open:
        if platform.system() == "Windows":
            os.startfile(save_path)

    gr.Info(f"VoiceVox音声ファイルを保存しました: {save_path}")

    return f"音声ファイルを保存しました: {save_path}"