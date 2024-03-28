from fastapi import File, UploadFile, HTTPException, APIRouter, BackgroundTasks
from services.prediction_service import PredictionService

router = APIRouter()

@router.post('/predict/{uid}')
async def predict(background_tasks: BackgroundTasks, uid: str, file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(400, 'Invalid file type. Please uploda a CSV file.')
    
    try:
        ps = PredictionService()

        content = await file.read()

        background_tasks.add_task(ps.run_predictions, uid, content)

        return { "message": "Prediction is running in the background" }
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        await file.close()
