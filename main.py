from fastapi import FastAPI, UploadFile, File
import boto3
import json, io
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()
origins=[
    "localhost:3000",
    "https://site-panduline-free.onrender.com"
]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Ou apenas o domínio do frontend
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
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    #
    #return {"sucesso":"Main sucess"}
    try:
        contents = await file.read()
        file_stream=io.BytesIO(contents)
        s3.upload_fileobj(
            Fileobj=file_stream,
            Bucket=BUCKET_NAME,
            Key=file.filename,
            ExtraArgs={"ContentType":file.content_type}
        )
        url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        print(url)
        return {"url": url}
    except NoCredentialsError:
        return {"error": "Credenciais inválidas"}








