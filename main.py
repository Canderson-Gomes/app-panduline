from fastapi import FastAPI, UploadFile, File
import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou apenas o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configurações da AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

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
    
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    #
    #return {"sucesso":"Main sucess"}
    try:
        contents = await file.read()
        s3.upload_fileobj(
            Fileobj=bytes(contents),
            Bucket=BUCKET_NAME,
            Key=file.filename
        )
        url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        return {"url": url}
    except NoCredentialsError:
        return {"error": "Credenciais inválidas"}








'''
AKIA3QFM6OASSNO4CHWQ
  yrmBgsrnXZGerrg3nBoma4oPkRArVkRU5Ueem+wD


'''
    
