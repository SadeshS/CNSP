from io import StringIO
from fastapi import Depends, File, UploadFile, HTTPException, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
import pandas as pd
from services.prediction_service import PredictionService
from routes.deps import get_current_user

router = APIRouter()

@router.post('/predict')
async def predict(background_tasks: BackgroundTasks, current_user=Depends(get_current_user), file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(400, 'Invalid file type. Please uploda a CSV file.')
    
    try:
        ps = PredictionService()

        content = await file.read()

        df = read_csv(content)

        columns_to_check = ['quantity', 'user_id', 'order_id', 'product_id', 'date']

        missing_columns = [col for col in columns_to_check if col not in df.columns]

        if not missing_columns:
            background_tasks.add_task(ps.run_predictions, current_user["uid"], df)

            return { "message": "Prediction is running in the background" }
        
        else:
            return JSONResponse(status_code=400, content={ "message": "The dataset is missing the following columns: " + ', '.join(missing_columns) })
    
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        await file.close()

def read_csv(content):
    string_io = StringIO(content.decode("utf-8"))
    df = pd.read_csv(string_io)
    return df
