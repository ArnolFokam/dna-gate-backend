import cv2
import numpy as np
from fastapi import File, HTTPException

from core.biometrics import modzy_client, models
from core.preprocessing.image import bytes2image, image2bytes

model_name = "face"


async def get_face_embedding(face_image: File(...)):
    preprocessed_face_image = preprocess_face(await face_image.read(),
                                              face_image.content_type)

    try:
        job = modzy_client.jobs.submit_file(models[model_name]['id'],
                                            models[model_name]['version'],
                                            {'my-input': {'image': preprocessed_face_image}})
        results = modzy_client.results.block_until_complete(job, timeout=None)
        return results['results']['my-input']['results.json']['embedding']
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Please upload a valid image with a face on it",
        )


def validate_face_input(face_image):
    if face_image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail=f"File type of {face_image.content_type} is not supported for face image, supported: jpg, "
                   f"jpeg, png",
        )
    return face_image


def preprocess_face(face_image: bytes, content_type: str):
    im = bytes2image(face_image)

    # detect face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces_detected = face_cascade.detectMultiScale(im,
                                                   scaleFactor=1.1,
                                                   minNeighbors=5,)

    if len(faces_detected) != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Could not identify a suitable face in the image,"
                   f" Please make sure you are in a room with enough lighting "
                   f"and there is only one face in the picture",
        )

    # extract region around face
    x, y, w, h = faces_detected[0]
    eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eyes_cascade.detectMultiScale(im[y:y+h, x:x+w])

    # for in case, we detect the two
    # nostrils as eyes (happens sometimes)
    if len(eyes) < 2 or len(eyes) > 4:
        raise HTTPException(
            status_code=400,
            detail=f"Could not identify a face in image, please make sure "
                   f"your facial features (eyes, nose etc) are not covered.",
        )

    # calculate the midpoint of eye 1 bbox
    # (with respect to image and not face bbox)
    mid_x_eye1 = x + eyes[0][0] + eyes[0][2]//2
    mid_y_eye1 = y + eyes[0][1] + eyes[0][3]//2

    # calculate the midpoint of eye 2 bbox
    # (with respect to image and not face bbox)
    mid_x_eye2 = x + eyes[1][0] + eyes[1][2]//2
    mid_y_eye2 = y + eyes[1][1] + eyes[1][3]//2

    # calculate the coordinates of
    # the region between the eyes
    mid_x = (mid_x_eye1 + mid_x_eye2) // 2
    mid_y = (mid_y_eye1 + mid_y_eye2) // 2

    im = im[max(0, mid_y - (h // 2 + im.shape[0] // 4)): mid_y + (h // 2 + im.shape[0] // 4),
            max(0, mid_x - (w // 2 + im.shape[1] // 8)): mid_x + (w // 2 + im.shape[1] // 8)]

    face_image = image2bytes(im, content_type.rsplit('/')[-1])
    return face_image
