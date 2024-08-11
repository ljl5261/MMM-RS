# MMM-RS
## Abstract

  Recently, diffusion-based generative paradigms have achieved impressive general image generation capabilities with text prompts due to their accurate distribution modeling and stable training processes. However, generating diverse remote sensing (RS) images, which are significantly different from general images in terms of scale and perspective, remains a formidable challenge. This is primarily due to the lack of a comprehensive RS image generation dataset encompassing various modalities, ground sample distances (GSD), and scenes.In this paper, we propose a Multi-modal, Multi-GSD, Multi-scene Remote Sensing (MMM-RS) dataset and benchmark for text-to-image generation in diverse remote sensing scenarios. Specifically, we first collected nine publicly available RS datasets and standardized all samples. To bridge RS images with textual semantic information, we utilized a large-scale pretrained vision-language model to automatically generate text prompts, followed by hand-crafted rectifications, resulting in information-rich text-image pairs (including multi-modal images).We designed methods to obtain images with different GSD and various environmental conditions (e.g., low-light, foggy) in a single sample. Through extensive manual screening and refining annotations, we ultimately obtained the MMM-RS dataset, comprising approximately 2.1 million text-image pairs.Extensive experimental results verify that our proposed MMM-RS dataset allows off-the-shelf diffusion models to generate diverse RS images across various modalities, scenes, weather conditions, and GSD.

### Data set annotation format
![image](image/1.jpg)

### MMM-RS dataset statistics from different aspects
![image](https://github.com/user-attachments/assets/ee6def45-d532-40de-a9c2-3a76b4be0bf9)

### The framework of information-rich text prompt generation
![image](https://github.com/user-attachments/assets/8f0567c9-96a1-4085-9f61-c5580fa05867)

### The framework of Multi-scene Remote Sensing Image Synthesis
![image](https://github.com/user-attachments/assets/ebbba53a-a396-4430-b456-4303b8c49428)

### A example for generating different GSD images for the same sample
![image](https://github.com/user-attachments/assets/0ffb78ee-2399-415c-ab03-78196177420f)

### RS image generation and cross-model generation
![image](https://github.com/user-attachments/assets/24764fda-dd77-4f60-8dcb-eed741304e26)
![image](https://github.com/user-attachments/assets/ad8b643d-c293-4a02-bd21-585a1c972d77)
![image](https://github.com/user-attachments/assets/eba5d3cb-58cd-4491-bc24-f8860ea93195)

## Dataset Link

  Our data set baidu network backup link: https://pan.baidu.com/s/1u-NbGANT7dSoccXDHthhSw?pwd=1234 
  Or you can use quark web disk:https://pan.quark.cn/s/f4ea192e425c
