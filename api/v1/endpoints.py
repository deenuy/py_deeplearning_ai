from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import RedirectResponse
from api.models.schemas import PredictRequest, PredictResponse, ErrorResponse
from src.models.logistic_regression_nn import LogisticRegression
from src.data.data_processing import preprocess_data
from api.utils.logging import setup_logger
from api.utils.metrics import metrics
import numpy as np
import os
import time
import logging

router = APIRouter()

# Setup logger
config_path = os.getenv('CONFIG_PATH', 'config/dev/config.yml')
setup_logger('ml_classifier', config_path)
logger = logging.getLogger('ml_classifier')

# Load model
try:
    model = LogisticRegression.load(os.getenv('MODEL_PATH', 'trained_model.pkl'))
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

@router.get("/docs")
async def get_docs():
    """
    Redirect to the MkDocs documentation.
    """
    return RedirectResponse(url="http://localhost:8080")

@router.post("/predict", response_model=PredictResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def predict(image: UploadFile = File(...)):
    try:
        start_time = time.time()
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = preprocess_data(nparr)
        prediction = model.predict(img)

        latency = time.time() - start_time
        prediction_class = int(prediction[0, 0])

        metrics.record_prediction(prediction_class, latency)

        logger.info("Model prediction", extra={
            "prediction_class": prediction_class,
            "prediction_latency": latency,
            "image_filename": image.filename,
        })

        return PredictResponse(prediction=prediction_class)
    except ValueError as ve:
        logger.error(f"Invalid input: {str(ve)}", extra={"image_filename": image.filename})
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred during prediction: {str(e)}", extra={"image_filename": image.filename})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/metrics")
async def get_metrics():
    return metrics.get_metrics()

@router.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@router.get("/readyz")
async def readiness_check():
    # Add any necessary checks (e.g., database connection)
    return {"status": "ready"}