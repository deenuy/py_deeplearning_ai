from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from api.models.schemas import PredictRequest, PredictResponse, ErrorResponse
from src.models.logistic_regression_nn import LogisticRegression
from src.data.data_processing import preprocess_data
import numpy as np
import os
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
async def predict(request: PredictRequest):
    """
    Endpoint for making predictions.

    Expects a JSON payload with an 'image' key containing the image data.
    Returns a JSON response with the prediction.
    """
    try:
        image = preprocess_data(np.array(request.image))
        prediction = model.predict(image)

        return PredictResponse(prediction=int(prediction[0, 0]))
    except ValueError as ve:
        logger.error(f"Invalid input: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")