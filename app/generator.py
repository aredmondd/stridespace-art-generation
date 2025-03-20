import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage import zoom, map_coordinates, gaussian_filter
import matplotlib.colors as mcolors
from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def generate_random_palette(emotion):
    emotion_factors = {
        "very bad": (0.4, 0.3),
        "bad": (0.55, 0.4),
        "neutral": (0.7, 0.5),
        "good": (0.8, 0.65),
        "very good": (0.9, 0.75)
    }
    saturation, brightness = emotion_factors.get(emotion, (0.7, 0.5))
    colors = [(random.random() * saturation, random.random() * saturation, random.random() * brightness) for _ in range(3)]
    return mcolors.LinearSegmentedColormap.from_list("emotionPalette", colors)

def generate_super_abstract(distance, duration, emotion):
    pace = duration / distance if distance > 0 else 0

    palette = generate_random_palette(emotion)
    canvas_height, canvas_width = 320, 320  # Increased canvas size for cropping

    noise_scale = max(10, int(20 + (pace - 10) * 2))
    displacement_scale = 5 + (duration / 30)
    gaussian_sigma = 0.005 + (distance / 10) * 0.001

    low_res = np.random.rand(noise_scale, noise_scale)
    smooth_noise = zoom(low_res, (canvas_height / noise_scale, canvas_width / noise_scale), order=3)
    base_image = palette(smooth_noise)[:, :, :3]

    grid_y, grid_x = np.meshgrid(np.arange(canvas_height), np.arange(canvas_width), indexing='ij')
    disp_x = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    disp_y = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    new_x = np.clip(grid_x + disp_x, 0, canvas_width - 1)
    new_y = np.clip(grid_y + disp_y, 0, canvas_height - 1)

    warped = np.zeros_like(base_image)
    for ch in range(3):
        warped[:, :, ch] = map_coordinates(base_image[:, :, ch], [new_y, new_x], order=1, mode='reflect')

    final_image = gaussian_filter(warped, sigma=gaussian_sigma)
    final_image = np.clip(final_image, 0, 1)
    final_image = final_image[10:-10, 10:-10]  # Crop back to 300x300

    img_buffer = BytesIO()
    plt.figure(figsize=(8, 8))
    plt.imshow(final_image)
    plt.axis('off')
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    img_buffer.seek(0)

    return img_buffer

@app.get("/generate-art/")
async def generate_art(distance: float, duration: float, emotion: str):
    img_buffer = generate_super_abstract(distance, duration, emotion)
    return StreamingResponse(img_buffer, media_type="image/png")
