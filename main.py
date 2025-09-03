from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient, errors
from routes.paises import router as rota_paises

urlInterna = "mongodb://202872:202872@10.0.237.41:27017/?authSource=202872"
urlExterna = "mongodb://202872:202872@177.67.253.61:27017/?authSource=202872"

@asynccontextmanager
async def lifespan(app: FastAPI):   
    print("iniciando o server!!")
    yield   print("desligando o server!!")
app = FastAPI(lifespan=lifespan)

async def  conectar_com_banco():   
     try:
          db = MongoClient(urlInterna, serverSelectionTimeoutMS=2000) 
          db.admin.command("ping") 
          print("Conectado na rede interna")
          print(db); 
          return db
     except errors.ServerSelectionTimeoutError:
          db = MongoClient(urlExterna, serverSelectionTimeoutMS=2000)
          db.admin.command("ping") 
          print("Conectado na rede externa")
          print(db)
          return db

@asynccontextmanager 
async def lifespan(app: FastAPI):
     cliente_mongo = await conectar_com_banco()  
     app.db = cliente_mongo["202872"]    
     print("iniciando o server!!")  
     yield   
     print("desligando o server!!") 
app = FastAPI(lifespan=lifespan)

app = FastAPI(lifespan=lifespan)
app.include_router(rota_paises)

