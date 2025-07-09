from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from botocore.exceptions import NoCredentialsError
import os, shutil, cv2, insightface, json, io, uuid, boto3
from dotenv import load_dotenv
from insightface.app import FaceAnalysis
from insightface.model_zoo import model_zoo
import warnings
from faiss_index import FaissIndex
#from sqlalchemy.orm import Session
#from database import SessionLocal, engine
#from models import Base, Person
#from utils.face_encoder import get_embedding
#from utils.s3_upload import upload_file

#from faiss_index import FaissIndex  # se tiver essa classe num outro arquivo

  # ou qualquer valor que seja o dimensional do seu embedding
#CONFIGURAR O DATA BASE------------------------------------------------#####################################################
from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
##########################################################
load_dotenv()
app = FastAPI()
#Base.metadata.create_all(bind=engine)
index = FaissIndex()
origins=[
    "localhost:3000",
    "https://site-panduline-free.onrender.com"
]
###########################################################################################
DATABASE_URL="postgresql://cggomes:nE3cRJBtkPnKDOoDbl7imSjArThmzv42@dpg-d1he362dbo4c73da8iog-a.oregon-postgres.render.com/pessoa_desaparecidas"


#engine=create_engine(DATABASE_URL)
#SessionLocal=sessionmaker(bind=engine)
#Base= declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Pessoa(Base):
    __tablename__="peoples"
    id = Column(Integer, primary_key=True, index=True)
    image_url= Column(String, nullable=False)
    #descript=Column(String, nullable=True)
    #created_at=Column(TIMESTAMP)

#Criar as tables caso não existam
Base.metadata.create_all(bind=engine)
#################################################------------##########################################################




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


_face_app = None


@app.on_event("startup")
def build_index():
    db = SessionLocal()
    index.rebuild_from_db(db)
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def init_model():
    global _face_app
    if _face_app is None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _face_app = FaceAnalysis(name='buffalo_l')
            _face_app.prepare(ctx_id=-1, providers=['CPUExecutionProvider'])# Força CPU# <-- adiciona isso


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session=Depends(get_db)):#db: Session=Depends(get_db), title:str=Form(...)
    #
    #return {"sucesso":"Main sucess"}
    tmp_path = f"temp_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        key = f"faces/{uuid.uuid4().hex}{os.path.splitext(tmp_path)[1]}"
    try:
      
        s3.upload_file(tmp_path, BUCKET_NAME, key, ExtraArgs={"ContentType": file.content_type})
    #OBTEMOS O EMBEDDING
        #init_model()
        #img = cv2.imread(tmp_path)
        #faces = _face_app.get(img)
        #embedding=faces[0].embedding.astype(np.float32)   
        #os.remove(tmp_path)


        #person = Person(image_url= key, embedding=embedding.tolist())
        #db.add(person)
        #db.commit()
        #db.refresh(person)
      
        #contents = await file.read()
        #file_stream=io.BytesIO(contents)
        #s3.upload_fileobj(
            #Fileobj=file_stream,
            #Bucket=BUCKET_NAME,
            #Key=file.filename,
            #ExtraArgs={"ContentType": file.content_type}
        #)
        #######################...ADD TO DATA BASE.............########################---------------------------################

        pessoa=Pessoa(image_url= key) #embedding=embedding.tolist())
        print(pessoa)
        db.add(pessoa)
        db.commit()
        #db.refresh(pessoa)
      
        ######################.................."""""""""""""""""""""""############################################
        url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        #index.add(embedding)
        
        print("Final JSON a ser retornado:")
        print(url)
        return {"image_url": url}
    except NoCredentialsError:
        return {"error": "Credenciais inválidas"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)







