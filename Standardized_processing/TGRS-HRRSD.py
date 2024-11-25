#download dataset from https://github.com/CrazyStoneonRoad/TGRS-HRRSD-Dataset

import os
import warnings
from PIL import Image
from tqdm import tqdm
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

Image.MAX_IMAGE_PIXELS = None

warnings.simplefilter('ignore', Image.DecompressionBombWarning)

upsampler = RealESRGANer(
    scale=2,  
    model_path='chaofenbianlv_pth/RealESRGAN_x2plus.pth', 
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2),
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True 
)


def center_crop(image):
   
    width, height = image.size
    new_size = min(width, height)
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    right = left + new_size
    bottom = top + new_size
    return image.crop((left, top, right, bottom))


def super_resolve_image(image, target_size=(512, 512)):
    
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    try:
        output, _ = upsampler.enhance(img_cv2, outscale=2)
    except Exception as e:
        print(f"Error during super-resolution: {e}")
        return image
    output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    return output_image.resize(target_size, Image.BICUBIC)


def process_image(image, target_size=(512, 512)):
   
    cropped_image = center_crop(image)
    cropped_size = cropped_image.size[0]  
    if cropped_size > target_size[0]:
       
        resized_image = cropped_image.resize(target_size, Image.BICUBIC)
    else:
        
        resized_image = super_resolve_image(cropped_image, target_size)
    return resized_image


def process_images(input_folder, output_folder):
   
    os.makedirs(output_folder, exist_ok=True)

 
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'tif', 'tiff'))]

    for filename in tqdm(image_files, desc="Processing images", ncols=100):
        img_path = os.path.join(input_folder, filename)
        try:
            with Image.open(img_path) as img:
                processed_img = process_image(img)
                new_name = os.path.splitext(filename)[0] + '.jpg'
                processed_img.save(os.path.join(output_folder, new_name))
        except Exception as e:
            print(f"Error processing {img_path}: {e}")



input_folder = './TGRS-HRRSD'  
output_folder = './TGRS-HRRSD_process'  

process_images(input_folder, output_folder)
