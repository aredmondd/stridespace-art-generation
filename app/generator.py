import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage import zoom, map_coordinates, gaussian_filter
import matplotlib.colors as mcolors
from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# Function to generate a random 3-color palette
def generate_random_palette():
    colors = [(random.random(), random.random(), random.random()) for _ in range(3)]
    return mcolors.LinearSegmentedColormap.from_list("randomPalette", colors)

# Function to generate abstract artwork based on run data
def generate_super_abstract(distance, duration, pace):
    # Editable parameters for the artwork
    palette = generate_random_palette()
    canvas_height, canvas_width = 300, 300

    # Adjust the scale of noise based on pace
    noise_scale = max(10, int(20 + (pace - 10) * 2))  # Ensure a reasonable scale
    pixel_sort_probability = max(0.01, 0.01 + (pace - 5) * 0.01)
    displacement_scale = 5 + (duration / 30)
    gaussian_sigma = 0.005 + (distance / 10) * 0.001  

    # Step 1: Create a smooth noise field
    low_res = np.random.rand(noise_scale, noise_scale)
    smooth_noise = zoom(low_res, (canvas_height / noise_scale, canvas_width / noise_scale), order=3)
    base_image = palette(smooth_noise)[:, :, :3]

    # Step 2: Apply selective pixel sorting
    sorted_image = base_image.copy()
    for i in range(canvas_height):
        if random.random() < pixel_sort_probability:
            start = random.randint(0, canvas_width - 20)
            end = random.randint(start + 10, canvas_width)
            segment = sorted_image[i, start:end, :]
            luminance = 0.2126 * segment[:, 0] + 0.7152 * segment[:, 1] + 0.0722 * segment[:, 2]
            sort_order = np.argsort(luminance)
            sorted_image[i, start:end, :] = segment[sort_order]

    # Step 3: Apply slight warping
    grid_y, grid_x = np.meshgrid(np.arange(canvas_height), np.arange(canvas_width), indexing='ij')
    disp_x = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    disp_y = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    new_x = np.clip(grid_x + disp_x, 0, canvas_width - 1)
    new_y = np.clip(grid_y + disp_y, 0, canvas_height - 1)

    warped = np.zeros_like(sorted_image)
    for ch in range(3):
        warped[:, :, ch] = map_coordinates(sorted_image[:, :, ch], [new_y, new_x], order=1, mode='reflect')

    # Step 4: Apply Gaussian smoothing
    final_image = gaussian_filter(warped, sigma=gaussian_sigma)
    final_image = np.clip(final_image, 0, 1)

    # Save image to an in-memory file
    img_buffer = BytesIO()
    plt.figure(figsize=(8, 8))
    plt.imshow(final_image)
    plt.axis('off')
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    img_buffer.seek(0)  # Reset buffer position for reading

    return img_buffer

@app.get("/generate-art/")
async def generate_art(distance: float, duration: float, pace: float):
    # Call your generate_super_abstract function with the appropriate parameters
    img_buffer = generate_super_abstract(distance, duration, pace)  # Pass real values for the run data

    # Return the image as a streaming response
    return StreamingResponse(img_buffer, media_type="image/png")
