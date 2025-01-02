#download MRSCC2.0 from http://www.csu.cas.cn/gb/kybm/sjlyzx/gcxx_sjj/sjj_tgxl/202208/t20220831_6507453.html

import os
from PIL import Image
from tqdm import tqdm
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet


upsampler = RealESRGANer(
    scale=2,  
    model_path='chaofenbianlv_pth/RealESRGAN_x2plus.pth',  
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2), 
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True  
)


def super_resolve_image(image):
    # Convert a PIL image to a cv2 image.
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform super-resolution processing using Real-ESRGAN.
    try:
        output, _ = upsampler.enhance(img_cv2, outscale=2)  
    except Exception as e:
        print(f"Error during super-resolution: {e}")
        return image  

    # Convert a cv2 image back to a PIL image.
    output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    # Resize the image to 512x512.
    resized_output_image = output_image.resize((512, 512), Image.BICUBIC)
    return resized_output_image


def process_images(input_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)
    folder_name = os.path.basename(input_folder)

    for filename in tqdm(os.listdir(input_folder), desc="Processing images"):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'tif', 'tiff')):
            img_path = os.path.join(input_folder, filename)
            try:
                with Image.open(img_path) as img:
                    sr_img = super_resolve_image(img)
                    new_name = f'RGB_{folder_name}_{os.path.splitext(filename)[0] }.jpg'
                    sr_img.save(os.path.join(output_folder, new_name))
            except Exception as e:
                print(f"Error processing {img_path}: {e}")


# path
input_folder = './MRSSC2.0/city'
output_folder = './MRSSC2.0_jpg'

process_images(input_folder, output_folder)
