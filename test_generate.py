# generate.py
from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler,AutoencoderKL
import torch
from transformers import CLIPTextModel, CLIPTokenizer

# 指定使用的CUDA设备（第五张卡，编号为4）
device = torch.device("cuda:6")
local_path = "./stable-diffusion-v1-5"
model_path = "./output/third_train-000009.safetensors"  # 根据自己设置的训练策略找到保存权重的checkpoint文件夹
#vae_path = "./stable-diffusion-v1-5/vae_new"

#vae = AutoencoderKL.from_pretrained(vae_path, torch_dtype=torch.float16)  #vae
pipe = StableDiffusionPipeline.from_pretrained(local_path ,torch_dtype=torch.float16)
pipe.to(device)  # 将模型移动到指定的设备上
pipe.load_lora_weights(model_path)


pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config,use_karras_sigmas=True)#更改调度器为DPM++ 2M Karas
generator = torch.Generator(device="cuda").manual_seed(99)   #种子
prompt = "Satellite imagery,  Ultra-high precision resolution, night ,built-up,a satellite image of a city with lots of buildings, GF2,   GID"  # 生成内容
image = pipe(prompt,generator=generator, num_inference_steps=30, guidance_scale=7.5).images[0]
image.save("./outimages/3/16.png")  # 保存图像名
