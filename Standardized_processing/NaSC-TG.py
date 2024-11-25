#download NaSC-TG2 http://www.msadc.cn/main/setsubDetail?id=1370312964720037889

import os
from PIL import Image
from tqdm import tqdm
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet


upsampler = RealESRGANer(
    scale=4,  
    model_path='chaofenbianlv_pth/RealESRGAN_x4plus.pth', 
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4), 
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True  
)


def super_resolve_image(image):
   
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    try:
        output, _ = upsampler.enhance(img_cv2, outscale=4)  
    except Exception as e:
        print(f"Error during super-resolution: {e}")
        return image 

   
    output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    
    resized_output_image = output_image.resize((512, 512), Image.BICUBIC)
    return resized_output_image


def process_images(input_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)

    for filename in tqdm(os.listdir(input_folder), desc="Processing images"):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tif', 'tiff')):
            img_path = os.path.join(input_folder, filename)
            try:
                with Image.open(img_path) as img:
                    sr_img = super_resolve_image(img)
                    new_name = os.path.splitext(filename)[0] + '.jpg'
                    sr_img.save(os.path.join(output_folder, new_name))
            except Exception as e:
                print(f"Error processing {img_path}: {e}")



input_folder = './dataset/NaSC-TG2'
output_folder = './dataset/NaSC-TG2_jpg'

process_images(input_folder, output_folder)
