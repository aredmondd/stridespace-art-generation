from fastapi import FastAPI
from generator import generate_super_abstract

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
            run_data["emotion"],
        )
    )
    return {"status": "success", "message": "Artwork generated!"}

def save_local_image():
    """Generates and saves the image locally."""
    distance = 5
    duration = 30
    emotion = "very good"

    # Generate the image buffer
    img_buffer = generate_super_abstract(distance, duration, emotion)

    # Save the buffer as a PNG file
    with open("local_test.png", "wb") as f:
        f.write(img_buffer.getvalue())

    print("✅ Image saved as 'local_test.png'")

# Call the function directly
if __name__ == "__main__":
    save_local_image()