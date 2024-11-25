#Download Inria dataset from https://project.inria.fr/aerialimagelabeling/

from PIL import Image
import os
from tqdm import tqdm

def crop_resize_and_organize(image_path, output_dir, sizes):
    
    with Image.open(image_path) as img:
        start_x = (img.width - sizes[0]) // 2
        start_y = (img.height - sizes[0]) // 2

        # Start from the maximum size, crop sequentially, and gradually narrow the range.
        current_image = img.crop((start_x, start_y, start_x + sizes[0], start_y + sizes[0]))
        current_image.resize((512, 512)).save(os.path.join(output_dir, f"{sizes[0]}", f"resize_512_from_{sizes[0]}_{os.path.basename(image_path)}"))

        for size in sizes[1:]:
            # Calculate the starting coordinates for the center crop of the new size.
            new_start_x = (current_image.width - size) // 2
            new_start_y = (current_image.height - size) // 2
            current_image = current_image.crop((new_start_x, new_start_y, new_start_x + size, new_start_y + size))
            current_image.resize((512, 512)).save(os.path.join(output_dir, f"{size}", f"resize_512_from_{size}_{os.path.basename(image_path)}"))

            # Specially handle the 512 crop for the 1024 size.
            if size == 1024:
                # Crop 512x512 from the four corners of the matrix.
                for i in range(2):
                    for j in range(2):
                        sub_image = current_image.crop((i * 512, j * 512, i * 512 + 512, j * 512 + 512))
                        sub_image.resize((512, 512)).save(os.path.join(output_dir, f"512", f"crop_512_{i}_{j}_{os.path.basename(image_path)}"))
                
                # Center crop a 512x512 image.
                center_x = (current_image.width - 512) // 2
                center_y = (current_image.height - 512) // 2
                center_image = current_image.crop((center_x, center_y, center_x + 512, center_y + 512))
                center_image.resize((512, 512)).save(os.path.join(output_dir, f"512", f"crop_512_center_{os.path.basename(image_path)}"))

# Iterate through the specified directory to process each large image.
def process_images(directory, output_dir, sizes):
  
    create_folders(output_dir, sizes + [1024])  # Add 1024 to save the cropped 512x512 images.

    filenames = [f for f in os.listdir(directory) if f.endswith(".jpg")]
    for filename in tqdm(filenames, desc="Processing images"):
        crop_resize_and_organize(os.path.join(directory, filename), output_dir, sizes)


def create_folders(output_dir, sizes):
    os.makedirs(output_dir, exist_ok=True)
    for size in sizes:
        os.makedirs(os.path.join(output_dir, str(size)), exist_ok=True)

# Set the path and size.
directory = './Inria_dataset'
output_dir = './crop_Inria'
sizes = [4096, 2048, 1024]
process_images(directory, output_dir, sizes)
