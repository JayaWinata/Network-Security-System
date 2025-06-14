import sys, os
import certifi

ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from src.utils.utils import load_object
from src.utils.ml_utils.estimator import NetworkModel
from src.constant import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from src.exception.exception import NetworkSecurityException
from src.pipeline.training_pipeline import TrainingPipeline
from src.logging.logger import logger

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool
import pandas as pd

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./templates')

@app.get('/', tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successfull")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post('/predict')
async def predict(request: Request, file: UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model = load_object('final_model/model.pkl')
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        os.makedirs('prediction_output', exist_ok=True)
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {'request': request, 'table': table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
