


This code by using StyleGan3 and exploring in z and w space and producing continuous pictures from changing emotions. 
Pre-trained data that want to use for train model can be Can change in (config and resolution). By default, we used "stylegan3-r-ffhq-1024x1024.pkl"

 https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/<MODEL>, where <MODEL> is one of:
 
stylegan3-t-ffhq-1024x1024.pkl, stylegan3-t-ffhqu-1024x1024.pkl, stylegan3-t-ffhqu-256x256.pkl
stylegan3-r-ffhq-1024x1024.pkl, stylegan3-r-ffhqu-1024x1024.pkl, stylegan3-r-ffhqu-256x256.pkl
stylegan3-t-metfaces-1024x1024.pkl, stylegan3-t-metfacesu-1024x1024.pkl
stylegan3-r-metfaces-1024x1024.pkl, stylegan3-r-metfacesu-1024x1024.pkl
stylegan3-t-afhqv2-512x512.pkl
stylegan3-r-afhqv2-512x512.pkl  


First by selecting the desired number to produce a vector with a length of z, and w dimension with a random vector and explore that z,w space then by picking two different pictures and explore 
in liniear apce between.  


after the run clone cell from GitHub in the program put gen_utils.py from https://github.com/PDillis/stylegan3-fun in the folder torch_utils.
We use w_to_image() function to explore in w space.



you can find more result here .