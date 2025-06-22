from fastapi import FastAPI, File, UploadFile
from firebase_admin import credentials, initialize_app, storage
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa Firebase
cred = credentials.Certificate("firebase_config.json")
initialize_app(cred, {
    'storageBucket': 'https://api-imgs-panduline.firebaseapp.com/'
})
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Lê o conteúdo
    contents = await file.read()
    file_name = f"{uuid.uuid4()}_{file.filename}"

    # Salva no Firebase
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(contents, content_type=file.content_type)
    blob.make_public()  # Torna o arquivo acessível publicamente

    return {"file_url": blob.public_url}
