from fastapi import FastAPI, UploadFile, File
import boto3
import json, io, uuid
from botocore.exceptions import NoCredentialsError
import os, shutil
import insightface
from insightface.app import FaceAnalysis
import cv2
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
#from faiss_index import FaissIndex

load_dotenv()


app = FastAPI()
origins=[
    "localhost:3000",
    "https://site-panduline-free.onrender.com"
]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou apenas o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configurações da AWS
#AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID ="AKIA3QFM6OASSNO4CHWQ" #os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = "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"#os.getenv
AWS_REGION = "eu-north-1"  # ou sua região
BUCKET_NAME = "app-panduline"

# Cliente S3
s3 = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
@app.get("/")
async def getting():
    
    return {"api":"api no ar"}

_face_app = None

def init_model():
    global _face_app
    if _face_app is None:
        _face_app = FaceAnalysis(name='buffalo_l')
        _face_app.prepare(ctx_id=-1)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    #
    #return {"sucesso":"Main sucess"}
    tmp_path = f"temp_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        key = f"faces/{uuid.uuid4().hex}{os.path.splitext(tmp_path)[1]}"
    try:
      
        s3.upload_file(tmp_path, BUCKET_NAME, key, ExtraArgs={"ContentType": file.content_type})
    #OBTEMOS O EMBEDDING
        init_model()
        img = cv2.imread(tmp_path)
        faces = _face_app.get(img)
        embedding=faces[0].embedding.astype(np.float32)   
        os.remove(tmp_path)


        
        #contents = await file.read()
        #file_stream=io.BytesIO(contents)
        #s3.upload_fileobj(
            #Fileobj=file_stream,
            #Bucket=BUCKET_NAME,
            #Key=file.filename,
            #ExtraArgs={"ContentType": file.content_type}
        #)
        url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        #index.add(embedding)
        print(url)
        print(embedding)
        return {"ur": url, "key":key, "url":embedding}
    except NoCredentialsError:
        return {"error": "Credenciais inválidas"}








