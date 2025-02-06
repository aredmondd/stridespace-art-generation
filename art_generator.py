import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage import zoom, map_coordinates, gaussian_filter
import matplotlib.colors as mcolors
import os

# Function to generate a random 3-color palette
def generate_random_palette():
    # Generate 3 random colors using random RGB values
    colors = [(random.random(), random.random(), random.random()) for _ in range(3)]
    return mcolors.LinearSegmentedColormap.from_list("randomPalette", colors)

def generate_super_abstract(run_data):
    # Unpack run data
    distance, duration, pace, elevation, heart_rate, gps_route = run_data

    # Editable parameters for the artwork
    palette = generate_random_palette()  # Random color palette
    canvas_height, canvas_width = 300, 300  # Canvas dimensions (height x width)

    # Adjust the scale of noise based on pace (faster paces = sharper noise)
    noise_scale = 20 + (pace - 10) * 2  # Add some variance to noise scale based on pace
    noise_scale = int(noise_scale)  # Ensure noise_scale is an integer
    pixel_sort_probability = 0.01 + (pace - 5) * 0.01  # More pixel sorting for faster paces
    displacement_scale = 5 + (duration / 30)  # More displacement with longer durations
    gaussian_sigma = 0.005 + (distance / 10) * 0.001  # Higher distances may use more smoothing

    # Step 1: Create a smooth noise field
    low_res = np.random.rand(noise_scale, noise_scale)  # Random noise (30x30)
    smooth_noise = zoom(low_res, (canvas_height / noise_scale, canvas_width / noise_scale), order=3)  # Smooth interpolation

    # Map the smooth noise to cool colors using the random palette
    base_image = palette(smooth_noise)[:, :, :3]  # shape: (300,300,3)

    # Step 2: Apply selective pixel sorting in horizontal segments
    sorted_image = base_image.copy()
    for i in range(canvas_height):
        # With some probability, choose a segment in this row to sort
        if random.random() < pixel_sort_probability:
            start = random.randint(0, canvas_width - 20)
            end = random.randint(start + 10, canvas_width)
            segment = sorted_image[i, start:end, :]

            # Sort strongly for rows with higher lightness
            luminance = 0.2126 * segment[:, 0] + 0.7152 * segment[:, 1] + 0.0722 * segment[:, 2]
            if luminance.mean() > 0.6:  # Higher lightness = stronger sorting
                sort_order = np.argsort(luminance)
                sorted_segment = segment[sort_order]
                sorted_image[i, start:end, :] = sorted_segment
            else:  # Light rows or darker rows could have less sorting
                # Apply less sorting to darker pixels
                sort_order = np.argsort(luminance)
                sorted_segment = segment[sort_order]
                sorted_image[i, start:end, :] = sorted_segment

    # Step 3: Apply a very slight random warp (to blur rigid boundaries)
    grid_y, grid_x = np.meshgrid(np.arange(canvas_height), np.arange(canvas_width), indexing='ij')
    disp_x = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    disp_y = np.random.uniform(-displacement_scale, displacement_scale, (canvas_height, canvas_width))
    new_x = np.clip(grid_x + disp_x, 0, canvas_width - 1)
    new_y = np.clip(grid_y + disp_y, 0, canvas_height - 1)

    warped = np.zeros_like(sorted_image)
    for ch in range(3):
        warped[:, :, ch] = map_coordinates(sorted_image[:, :, ch], [new_y, new_x], order=1, mode='reflect')

    # Step 4: Optionally, apply a mild Gaussian filter (sigma=0.5) to smooth out harsh pixel edges.
    final_image = gaussian_filter(warped, sigma=gaussian_sigma)
    final_image = np.clip(final_image, 0, 1)

    # Save to desktop (replace <your-username> with your macOS username)
    desktop_path = os.path.expanduser("~/Desktop/abstract_run_art.png")

    # Export the art as a PNG file without any white border
    plt.figure(figsize=(8, 8))
    plt.imshow(final_image)
    plt.axis('off')
    plt.savefig(desktop_path, dpi=300, bbox_inches='tight', pad_inches=0)  # Save to desktop
    plt.close()  # Close the plot to avoid displaying in an interactive session

    return final_image

# Example run data (dummy values, as most parameters are not used here)
run_data = (
    1.0,                          # Distance in km
    3,                           # Duration in minutes
    3.0,                          # Pace in min/km
    [0, 10, 5, 15, 10],           # Elevation (ignored)
    140,                          # Average heart rate (ignored)
    [(random.random(), random.random()) for _ in range(100)]  # GPS route (ignored)
)

# Generate and display the abstract artwork
final_img = generate_super_abstract(run_data)
