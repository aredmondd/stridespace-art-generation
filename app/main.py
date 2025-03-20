from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generator import generate_super_abstract
from fastapi.responses import Response

app = FastAPI()

# ✅ CORS middleware applied globally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily
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

    # ✅ Add CORS headers explicitly to the image response
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }

    return Response(
        content=image_buffer.getvalue(),
        media_type="image/png",
        headers=headers
    )
