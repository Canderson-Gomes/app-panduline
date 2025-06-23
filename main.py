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
cred = credentials.Certificate("api-imgs-panduline-firebase-adminsdk-fbsvc-75557b552c.json")
initialize_app(cred, {
    'storageBucket': 'api-imgs-panduline.appspot.com'
})
@app.get("/apiload")
async def get_api():
    return {"myapi":"From my api PanduLine"}
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

    return {"file_url": blob.public_url, "dat":"Deu certo!"}
