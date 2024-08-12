# MMM-RS
## Abstract

  Recently, diffusion-based generative paradigms have achieved impressive general image generation capabilities with text prompts due to their accurate distribution modeling and stable training processes. However, generating diverse remote sensing (RS) images, which are significantly different from general images in terms of scale and perspective, remains a formidable challenge. This is primarily due to the lack of a comprehensive RS image generation dataset encompassing various modalities, ground sample distances (GSD), and scenes.In this paper, we propose a Multi-modal, Multi-GSD, Multi-scene Remote Sensing (MMM-RS) dataset and benchmark for text-to-image generation in diverse remote sensing scenarios. Specifically, we first collected nine publicly available RS datasets and standardized all samples. To bridge RS images with textual semantic information, we utilized a large-scale pretrained vision-language model to automatically generate text prompts, followed by hand-crafted rectifications, resulting in information-rich text-image pairs (including multi-modal images).We designed methods to obtain images with different GSD and various environmental conditions (e.g., low-light, foggy) in a single sample. Through extensive manual screening and refining annotations, we ultimately obtained the MMM-RS dataset, comprising approximately 2.1 million text-image pairs.Extensive experimental results verify that our proposed MMM-RS dataset allows off-the-shelf diffusion models to generate diverse RS images across various modalities, scenes, weather conditions, and GSD.

## Dataset format
Download the MMM-RS.zip file from the link provided below. The data set directory should look like this:
```
/MMM-RS
├──weather.zip
  ├──MMM-RS_fog_cleaned.json
  ├──MMM-RS_night_cleaned.json
  ├──MMM-RS_snowy_cleaned.json
  ├──night
    ├──xxx.jpg
    ├──...
  ├──snowy
    ├──xxx.jpg
    ├──...
  ├──fog
    ├──xxx.jpg
    ├──...
├──WHU-OPT-SAR.zip
  ├──MMM-RS_WHU-OPT-SAR.json
  ├──WHU-OPT-SAR_dataset
    ├──RGB_jpg
      ├──xxx.jpg
      ├──...
    ├──NIR_jpg
      ├──xxx.jpg
      ├──...
    ├──sar_jpg
      ├──xxx.jpg
      ├──...
├──Inria.zip
  ├──MMM-RS_Inria.json
  ├─Inria_dataset
    ├──xxx.jpg
    ├──...
├──...
```
The weather folder is divided into three weather folders, and the corresponding prompt word json description file. WHU-OPT-SAR and SEN1-2 have their respective modal classification folders and json files, and the remaining folders are a combination of image folders and json descriptions of the prompt words.

### Data set annotation format
![image](images/1.jpg)

### MMM-RS dataset statistics from different aspects
![image](images/2.jpg)

### The framework of information-rich text prompt generation
![image](images/3.jpg)

### The framework of Multi-scene Remote Sensing Image Synthesis
![image](images/4.jpg)

### A example for generating different GSD images for the same sample
![image](images/5.jpg)

### RS image generation and cross-model generation
![image](images/6.jpg)
![image](images/7.jpg)
![image](images/8.jpg)
## Dataset Link

  Our data set baidu network backup link: https://pan.baidu.com/s/1u-NbGANT7dSoccXDHthhSw?pwd=1234  
  Or you can use quark web disk:https://pan.quark.cn/s/f4ea192e425c
