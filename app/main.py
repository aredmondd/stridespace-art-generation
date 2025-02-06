from fastapi import FastAPI
from app.generator import generate_super_abstract

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stridespace Python backend is running"}

@app.post("/generate")
def generate_art(run_data: dict):
    image = generate_super_abstract(
        (
            run_data["distance"],
            run_data["duration"],
            run_data["pace"],
            run_data["elevation"],
            run_data["heart_rate"],
            run_data["gps_route"],
        )
    )
    return {"status": "success", "message": "Artwork generated!"}
