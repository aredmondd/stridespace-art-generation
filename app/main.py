from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from generator import generate_super_abstract
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

app = FastAPI()

# ✅ Middleware for handling CORS globally (for all responses)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Force CORS headers on every response
class CORSMiddlewareHack(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

app.add_middleware(CORSMiddlewareHack)

@app.get("/")
def read_root():
    return {"message": "Stridespace Python backend is running"}

@app.get("/generate-art")
def generate_art(distance: float, duration: float, emotion: str):
    """Generates abstract art based on run data."""
    image_buffer = generate_super_abstract((distance, duration, emotion))

    # ✅ Send image with explicit CORS headers
    return StreamingResponse(
        content=image_buffer,
        media_type="image/png",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )
