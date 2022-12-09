# Manipulating images features with styleGAN3
The source code of stylegan3 is available at this link https://github.com/NVlabs/stylegan3

This folder contains four files that need to be in precise positions to work, follow the below skeleton:

```
grid_gen 
├──stylegan3
│   ├── torch_utils
│   │    └── gen_utils.py 
│   │  
│   ├── grid_images
│   │
│   ├── gen_featureGrid.py
│   └── glass_feature  
│
└── slider.py
```
The folder grid_images will be automatically maked after the first use of gen_featuresGrid.py. If you want to see the produced images, download the zip folder from https://drive.google.com/file/d/1HuTk7wks7vUUtv0qHkdMmBRRwxb8ZBV_/view?usp=share_link . 
The zip contains the folder _grid_images_ that must be placed in the indicated location.

### gen_utils.py
This code can be founded at https://github.com/PDillis/stylegan3-fun in the **torch_utils** folder.
Essentially only one function is needed from this file ( _w_to_image()_ ), that allow to produce output images from an edited W-space. 

### glass_feature
This file contains a small portion of the data responsible for the presence of the glasses. The search for the feature corresponding to the presence of the glasses, in the network used (ffhqu-256x256), is considered subject to multiple layers or portions of layers, therefore there is no certainty of being able to find that same portion of data within a other base image. 

### gen_featureGrid.py
This code produces the images corresponding to the three features that were analyzed. In styleGAN3 an image as array is an input for the mapping network produce a w tensor of dim 1 x 16 x 512 (because for this production is used the ffhqu-256x256). Every layer with dimension 512 represents a feature for the image that will be produced in the end. The analyzed features are:
- Feature A: Smiling face or not, linked to layers 5 and 6 of W vector
- Feature B: Eyes open or closed, linked to layers 7 and 8 of W vector
- Feature C: Glasses on or not, linked to a little part of layer 2 of W vector and dependent on the eyes layers value

To run the code:
```sh
python gen_featureGrid.py --n_samples=6 --outdir=grid_images --network=https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-ffhqu-256x256.pkl
```
_n_samples_ and _outdir_ have default values, the same as written above. It's possibile to try the code with other networks like:
- stylegan3-r-metfacesu-1024x1024.pkl
- stylegan3-t-afhqv2-512x512.pkl
- stylegan3-t-ffhq-1024x1024.pkl

Other networks will produce better quality images, but bigger networks have more layer in the W space.

### slider.py
The slider.py takes all the **n_samples**x**n_samples**x**n_samples** images (because we have three features) from _grid_images_ and show them in a dinamic slider that can be used to understand the feature manipulation with styleGAN3.
