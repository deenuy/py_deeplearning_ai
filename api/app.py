from fastapi import FastAPI
from api.v1 import endpoints as v1
import uvicorn

app = FastAPI(
    title="Image Classifier API",
    description="API for classifying images using a logistic regression model.",
    version="1.0.0",
)

app.include_router(v1.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=int(os.getenv('PORT', 8000)), reload=True)