import numpy as np
import insightface
from insightface.app import FaceAnalysis
import cv2, os

_face_app = None

def init_model():
    global _face_app
    if _face_app is None:
        _face_app = FaceAnalysis(name='buffalo_l')
        _face_app.prepare(ctx_id=0)

def get_embedding(image_path: str):
    init_model()
    img = cv2.imread(image_path)
    faces = _face_app.get(img)
    if not faces:
        return None
    return faces[0].embedding.astype(np.float32)
