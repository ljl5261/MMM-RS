import os
from PIL import Image
from tqdm import tqdm
import cv2
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import numpy as np

# Initialize the Real-ESRGAN
upsampler = RealESRGANer(    
    scale=2,
    model_path='chaofenbianlv_pth/RealESRGAN_x2plus.pth',  # Update to the actual model path
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2),
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True)

def super_resolve_image(image):
    """
    Real ESRGAN is used to process the image with super resolution
    """
    # Convert PIL image to cv2 image
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    try:
        output, _ = upsampler.enhance(img_cv2, outscale=4)
    except Exception as e:
        print(f"Error during super-resolution: {e}")
        return image
    
    # Convert the cv2 image back to the PIL image and adjust it to 512x512
    output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    resized_output_image = output_image.resize((512, 512), Image.BICUBIC)
    return resized_output_image

def center_crop(image):
    """
    Center crop the image to make it a square
    """
    width, height = image.size
    new_size = min(width, height)  # The side length of a square is the minimum of its width and height
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    right = left + new_size
    bottom = top + new_size
    return image.crop((left, top, right, bottom))

def crop_images(image):
    """
    Crop out the 512x512 area in the center, bottom left, and top right corner of the input image
    """
    width, height = image.size
    crops = []
    # center
    if width > 512 and height > 512:
        center = image.crop(((width - 512) // 2, (height - 512) // 2, (width + 512) // 2, (height + 512) // 2))
        crops.append(('center', center))
    # left_bottom
    left_bottom = image.crop((0, max(height - 512, 0), min(512, width), height))
    crops.append(('left_bottom', left_bottom))
    # right_top
    right_top = image.crop((max(width - 512, 0), 0, width, min(512, height)))
    crops.append(('right_top', right_top))
    return crops

def process_images(input_folder, output_folder):
    """
    Process all images in the input folder, crop images greater than 512x512, and super resolution processes images less than or equal to 512x512
    """
    os.makedirs(output_folder, exist_ok=True)

    # Calendar all images in the input folder
    for img_name in tqdm(os.listdir(input_folder), desc="Processing"):
        img_path = os.path.join(input_folder, img_name)
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                # Images larger than 512x512 crop multiple areas
                if width > 512 and height > 512:
                    suffixes = ['_center', '_left_bottom', '_right_top']
                    crops = crop_images(img)
                    for suffix, cropped_img in crops:
                        new_name = os.path.splitext(img_name)[0] + suffix + '.jpg'
                        cropped_img.save(os.path.join(output_folder, new_name))
                else:
                    # Images less than or equal to 512x512 are first center cropped and then super-resolution processed
                    cropped_img = center_crop(img)
                    sr_img = super_resolve_image(cropped_img)
                    new_name = os.path.splitext(img_name)[0] + '_sr.jpg'
                    sr_img.save(os.path.join(output_folder, new_name))
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

# path
input_folder = './fmow'
output_folder = './fmow_process'

process_images(input_folder, output_folder)
