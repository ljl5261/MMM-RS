#download dataset from https://github.com/AmberHen/WHU-OPT-SAR-dataset

from PIL import Image
import os
from tqdm import tqdm


def process_folder(input_folder, output_folder, tile_size=(512, 512)):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all TIFF image files in the input folder
    images = [img for img in os.listdir(input_folder) if img.lower().endswith('.tif')]

    # Initialize tqdm progress bar
    pbar = tqdm(total=len(images), desc=f'Processing {input_folder}')

    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        with Image.open(img_path) as img:
            # Adjust channels
            if img.mode == 'L':  # Single channel
                img = img.convert('RGB')
            elif img.mode in ['RGBA', 'CMYK']:  # More than three channels
                img = img.convert('RGB')

            img_width, img_height = img.size

            # Calculate the number of complete tiles in each dimension
            num_tiles_width = img_width // tile_size[0]
            num_tiles_height = img_height // tile_size[1]

            # Loop over the image to extract tiles
            for i in range(num_tiles_width):
                for j in range(num_tiles_height):
                    left = i * tile_size[0]
                    upper = j * tile_size[1]
                    right = left + tile_size[0]
                    lower = upper + tile_size[1]

                    # Crop the image to the defined box
                    cropped_img = img.crop((left, upper, right, lower))

                    output_filename = f"{img_name[:-4]}_{i*512}_{j*512}_{os.path.basename(input_folder)}.jpg"
                    cropped_img.save(os.path.join(output_folder, output_filename), 'JPEG')

        # Update progress bar after each image is processed
        pbar.update(1)

    # Close the progress bar
    pbar.close()


def main():
    folders = ["NIR", "RGB", "SAR"]
    output_folders = ["NIR_jpg", "RGB_jpg", "SAR_jpg"]

    for input_folder, output_folder in zip(folders, output_folders):
        process_folder(input_folder, output_folder)


# Run the main function
if __name__ == "__main__":
    main()
