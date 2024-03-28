from cnsp_model.main import run
from models.predictions import Prediction, PredictionStatus
from datetime import datetime, timezone
from models.prediction_results import PredictionResults
from services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    collection_name = "users"

    def run_predictions(self, uid: str, content):
        us = UserService()
        user = us.get_user(uid)

        current_prediction_id = 1

        if user.predictions is None:
            user.predictions = []
        else:
            current_prediction_id = len(user.predictions) + 1

        current_date_time = datetime.now(timezone.utc)
        current_prediction = Prediction(
            id=current_prediction_id, 
            created_time=current_date_time.strftime("%m/%d/%Y, %H:%M:%S"), 
            status=PredictionStatus.in_progress, 
            predictions=None
        )

        user.predictions.append(current_prediction)

        us.update_user(user)

        df =  run(content)
        predictions = df.apply(self.row_to_prediction, axis=1).tolist()

        user = us.get_user(uid)

        for prediction in user.predictions:
            if prediction.id == current_prediction_id:
                prediction.status = PredictionStatus.success
                if prediction.predictions is None:
                    prediction.predictions = []

                prediction.predictions = predictions

        us.update_user(user)

    def row_to_prediction(self, row) -> PredictionResults:
        tempDate = (datetime.strptime(str(row['date']), "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d")
        return PredictionResults(
            user_id=str(row['user_id']),
            product_id=str(row['product_id']),
            quantity=int(row['quantity']),
            date=tempDate
        )