from pydub import AudioSegment


def bytes2voice(bytes_string, content_type: str):
    """"convert bytes string to audio"""
    voice = AudioSegment(bytes_string,
                         sample_width=2,
                         frame_rate=30000,
                         channels=2,
                         format=content_type.rsplit('/')[-1])
    return voice


def voice2bytes(sound):
    """convert audio to bytes string"""
    return sound.raw_data
