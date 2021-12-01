from fastapi import File, HTTPException

from core.biometrics import modzy_client, models
from core.preprocessing.voice import bytes2voice, voice2bytes

model_name = "voice"


async def get_voice_embedding(voice_recording: File(...)):
    voice_recording = preprocess_voice(await voice_recording.read(),
                                       voice_recording.content_type)

    try:
        job = modzy_client.jobs.submit_file(models[model_name]['id'],
                                            models[model_name]['version'],
                                            {'my-input': {'input': voice_recording}})
        results = modzy_client.results.block_until_complete(job, timeout=None)
        return results['results']['my-input']['results.json']['embeddings']
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Please upload a valid voice recording",
        )


def validate_voice_input(voice_recording: File(...)):
    if voice_recording.content_type not in ["audio/ogg", "audio/wav"]:
        raise HTTPException(
            status_code=400,
            detail=f"File type of {voice_recording.content_type} is not supported for voice recording, supported: "
                   f"ogg, wav",
        )
    return voice_recording


def preprocess_voice(voice_recording: bytes, content_type: str):
    # TODO: implement voice processing steps first before using voice
    # voice = bytes2voice(voice_recording, content_type)
    # voice_recording = voice2bytes(voice)
    return voice_recording
