from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generator import generate_super_abstract

app = FastAPI()

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://stridespace.xyz"],  # Local + Production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Stridespace Python backend is running"}

@app.get("/generate")
def generate_art(distance: float, duration: float, emotion: str):
    """Generates abstract art based on run data."""
    
    image_buffer = generate_super_abstract((distance, duration, emotion))
    
    return Response(content=image_buffer.getvalue(), media_type="image/png")
