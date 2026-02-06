from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction import PredictionPipeline
from cnnClassifier import logger
from pydantic import BaseModel


# Initialize FastAPI
app = FastAPI(
    title="Kidney Disease Classification API",
    description="Deep Learning API for Kidney CT Scan classification with Swagger documentation.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        try:
            self.classifier = PredictionPipeline(self.filename)
            logger.info("PredictionPipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize PredictionPipeline: {str(e)}")
            self.classifier = None

clApp = ClientApp()


class ImageData(BaseModel):
    image: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/train")
async def trainRoute():
    try:
        os.system("python main.py")
        return JSONResponse(content={"message": "Training done successfully!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/predict")
async def predictRoute(data: ImageData):
    try:
        if clApp.classifier is None:
            # Try to re-initialize if it failed before
            clApp.classifier = PredictionPipeline(clApp.filename)
            
        image = data.image
        decodeImage(image, clApp.filename)
        result = clApp.classifier.predict()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/predict_image")
async def predictImage(file: UploadFile = File(...)):
    try:
        if clApp.classifier is None:
            # Try to re-initialize if it failed before
            clApp.classifier = PredictionPipeline(clApp.filename)

        # Save the uploaded file
        with open(clApp.filename, "wb") as f:
            f.write(await file.read())
            
        result = clApp.classifier.predict()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Force Deployment: 02/05/2026 12:14:48
