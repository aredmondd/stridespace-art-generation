from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from generator import generate_super_abstract
from starlette.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

# ✅ Global CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Stridespace Python backend is running"}

@app.get("/generate-art")
def generate_art(distance: float, duration: float, emotion: str):
    """Generates abstract art based on run data."""
    image_buffer = generate_super_abstract((distance, duration, emotion))
    
    # ✅ Use StreamingResponse for the image
    return StreamingResponse(
        BytesIO(image_buffer.getvalue()),
        media_type="image/png"
    )
