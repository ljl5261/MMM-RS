#download TG1HRSSC from http://www.msadc.cn/main/setsubDetail?id=1369487569196158978

import os
from PIL import Image
from tqdm import tqdm
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

# 初始化Real-ESRGAN
upsampler = RealESRGANer(
    scale=2,  
    model_path='chaofenbianlv_pth/RealESRGAN_x4plus.pth', 
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2), 
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=True  
)


def super_resolve_image(image):
    # 将PIL图像转换为cv2图像
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 使用Real-ESRGAN进行超分辨率处理
    try:
        output, _ = upsampler.enhance(img_cv2, outscale=2)  
    except Exception as e:
        print(f"Error during super-resolution: {e}")
        return image  # 如果出现错误，返回原图像

    # 将cv2图像转换回PIL图像
    output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    # 调整图像大小到512x512
    resized_output_image = output_image.resize((512, 512), Image.BICUBIC)
    return resized_output_image


def process_images(input_folder, output_folder):
    # 确保输出文件夹存在
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


# 路径
input_folder = './dataset/TG1HRSSC'
output_folder = './dataset/TG1HRSSC_jpg'

process_images(input_folder, output_folder)
