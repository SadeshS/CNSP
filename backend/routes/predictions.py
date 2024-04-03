from io import StringIO
from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
import pandas as pd
from services.prediction_service import PredictionService
from routes.deps import get_current_user
import requests
from models.predict_data import PredictData
from config.firebase import storage
from urllib.parse import unquote

router = APIRouter()

@router.post('/predict')
async def predict(downloadURL: PredictData, current_user=Depends(get_current_user)):
    try:
        response = requests.get(downloadURL.url)
        response.raise_for_status()

        ps = PredictionService()

        df = read_csv(response)

        delete_file(downloadURL.url)

        columns_to_check = ['quantity', 'user_id', 'order_id', 'product_id', 'date']

        missing_columns = [col for col in columns_to_check if col not in df.columns]

        if not missing_columns:
            ps.run_predictions(current_user["uid"], df)

            return { "message": "Prediction is running in the background" }
        
        else:
            return JSONResponse(status_code=400, content={ "message": "The dataset is missing the following columns: " + ', '.join(missing_columns) })
    
    except Exception as e:
        raise HTTPException(500, str(e))
    
def read_csv(response):
    string_io = StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(string_io)
    return df

def delete_file(url):
    path_start = url.find("/o/") + 3
    path_end = url.find("?alt=media")
    file_path = url[path_start:path_end]
    file_path = unquote(file_path)
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    blob.delete()
