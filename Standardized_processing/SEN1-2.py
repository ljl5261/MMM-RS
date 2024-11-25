#download dataset from https://github.com/zhu-xlab/SEN12MS
import os
from PIL import Image
from tqdm import tqdm
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from multiprocessing import Pool

# 初始化Real-ESRGAN
def initialize_upsampler(gpu_id):
    return RealESRGANer(
        scale=4,
        model_path='./MMM_RS_dataset/chaofenbianlv_pth/RealESRGAN_x2plus.pth',  # 更新为实际的模型路径
        model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2),
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=True,
        device=f'cuda:{gpu_id}'
    )

def super_resolve_image_batch(images, upsampler):
    results = []
    for image in images:
        # 将PIL图像转换为cv2图像
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # 使用Real-ESRGAN进行超分辨率处理
        try:
            output, _ = upsampler.enhance(img_cv2, outscale=4)
        except Exception as e:
            print(f"Error during super-resolution: {e}")
            results.append(image)  # 如果出现错误，返回原图像
            continue
        
        # 将cv2图像转换回PIL图像
        output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        # 调整图像大小到512x512
        resized_output_image = output_image.resize((512, 512), Image.BICUBIC)
        results.append(resized_output_image)
    return results

def process_single_image_batch(args):
    filenames, input_folder, output_folder, gpu_id = args
    upsampler = initialize_upsampler(gpu_id)
    
    for filename in filenames:
        img_path = os.path.join(input_folder, filename)
        try:
            with Image.open(img_path) as img:
                sr_img = super_resolve_image_batch([img], upsampler)[0]
                new_name = os.path.splitext(filename)[0] + '.jpg'
                sr_img.save(os.path.join(output_folder, new_name))
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

def process_images(input_folder, output_folder, gpu_ids, batch_size=10):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'tif', 'tiff'))]
    tasks = [(files[i:i + batch_size], input_folder, output_folder, gpu_ids[i // batch_size % len(gpu_ids)]) for i in range(0, len(files), batch_size)]
    
    with Pool(processes=len(gpu_ids)) as pool:
        list(tqdm(pool.imap_unordered(process_single_image_batch, tasks), total=len(tasks), desc="Processing images"))

# 路径
input_folder = './final_MMM-RS/dataset/SEN1-2/SEN1-2_dataset1'  #all of SEN1-2 dataset 
output_folder = './final_MMM-RS/dataset/SEN1-2/SEN1-2_dataset_new/SEN1-2_RGB'
gpu_ids = [0, 1, 2, 3, 4, 5]  # 使用GPU 0到5

process_images(input_folder, output_folder, gpu_ids, batch_size=256)
