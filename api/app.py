from fastapi import FastAPI
from api.v1 import endpoints as v1
from api.utils.logging import setup_logger
import uvicorn
import os
import time
import logging

# Setup logger
config_path = os.getenv('CONFIG_PATH', 'config/dev/config.yml')
setup_logger('ml_classifier', config_path)
logger = logging.getLogger('ml_classifier')

app = FastAPI(
    title="Image Classifier API",
    description="API for classifying images using a logistic regression model.",
    version="1.0.0",
)

app.include_router(v1.router, prefix="/api/v1")

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    logger.info("Request received", extra={
        "method": request.method,
        "url": str(request.url),
        "client_ip": request.client.host,
    })
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request completed", extra={
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "duration": process_time,
    })
    return response

if __name__ == "__main__":
    logger.info("Starting application")
    uvicorn.run("api.app:app", host="0.0.0.0", port=int(os.getenv('PORT', 8000)), reload=True)