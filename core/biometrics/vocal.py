import io
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write


from fastapi import File, HTTPException
from modzy.error import Error

from core.biometrics import modzy_client, models
from core.preprocessing.voice import remove_noise

model_name = "voice"


async def get_voice_embedding(voice_recording: File(...)):
    voice_recording = preprocess_voice(await voice_recording.read())

    try:
        job = modzy_client.jobs.submit_file(models[model_name]['id'],
                                            models[model_name]['version'],
                                            {'my-input': {'input': voice_recording}})
        results = modzy_client.results.block_until_complete(job, timeout=None)
        return results['results']['my-input']['results.json']['embeddings']
    except (Error, KeyError) as e:
        if isinstance(e, KeyError):
            raise HTTPException(
                status_code=400,
                detail=f"Please upload a valid voice recording",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred",
            )


def validate_voice_input(voice_recording: File(...)):
    if voice_recording.content_type not in ["audio/ogg", "audio/wav"]:
        raise HTTPException(
            status_code=400,
            detail=f"File type of {voice_recording.content_type} is not supported for voice recording, supported: "
                   f"ogg, wav",
        )
    return voice_recording


def preprocess_voice(voice_recording: bytes):
    data, rate = sf.read(io.BytesIO(voice_recording), dtype=np.int16)
    de_noised_recording = remove_noise(data, rate)
    file = io.BytesIO()
    write(file, rate, de_noised_recording)
    return file.read()
