import os
import re
from typing import List, Optional, Tuple, Union
import click
import dnnlib
import numpy as np
import PIL.Image
import torch
import legacy
import torch_utils
from torch_utils import gen_utils
import copy
import pickle

""" This file works directly with styleGAN3, for use it you need first of all to download the styleGAN3 source code """

def parse_vec2(s: Union[str, Tuple[float, float]]) -> Tuple[float, float]:
    '''Parse a floating point 2-vector of syntax 'a,b'.

    Example:
        '0,1' returns (0,1)
    '''
    if isinstance(s, tuple): return s
    parts = s.split(',')
    if len(parts) == 2:
        return (float(parts[0]), float(parts[1]))
    raise ValueError(f'cannot parse 2-vector {s}')




@click.command()
@click.option('--n_samples','n_samples', type=int, help='Number of samples for the linspace',default=6)
@click.option('--network', 'network_pkl', help='Network pickle filename', required=True)
@click.option('--trunc', 'truncation_psi', type=float, help='Truncation psi', default=1, show_default=True)
@click.option('--class', 'class_idx', type=int, help='Class label (unconditional if not specified)')
@click.option('--noise-mode', help='Noise mode', type=click.Choice(['const', 'random', 'none']), default='const', show_default=True)
@click.option('--translate', help='Translate XY-coordinate (e.g. \'0.3,1\')', type=parse_vec2, default='0,0', show_default=True, metavar='VEC2')
@click.option('--rotate', help='Rotation angle in degrees', type=float, default=0, show_default=True, metavar='ANGLE')
@click.option('--outdir', help='Where to save the output images', type=str, default='grid_images', metavar='DIR')

def gen_grid(network_pkl: str,
    truncation_psi: float,
    noise_mode: str,
    outdir: str,
    n_samples:int,
    translate: Tuple[float,float],
    rotate: float,
    class_idx: Optional[int]):


    device = torch.device('cpu')
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore

    os.makedirs(outdir, exist_ok=True)
    
    #Change the random state to obtaine a different starting image, for the experiment was used randomstate=3
    zB = torch.from_numpy(np.random.RandomState(3).randn(1, G.z_dim))
    
    #Getting the W latent space from the styleGAN network 
    all_w = G.mapping(zB.to(device), None)
    w_avg = G.mapping.w_avg
    all_wB = w_avg + (all_w - w_avg) * truncation_psi

    
    #Make a deepcopy of the W space for backup to use it in with less importnat features
    backup_image=copy.deepcopy(all_wB.numpy())
    
    #The main component of the manipulation
    walk=all_wB.numpy()
    
    
    #Color setting RGB
    walk[0][15]=np.full(512, 0.9)
    walk[0][14]=np.ones(512)
    walk[0][13]=np.ones(512)
    walk[0][12]=np.ones(512)
    
    
    #General Settings
    walk[0][9]=np.full(512, 1)  
    walk[0][10]=np.full(512, 1) 
    walk[0][11]=np.full(512, 0) 
    walk[0][3]=backup_image[0][3]
    walk[0][4] =backup_image[0][4]
    
    
    
    #Settings for the xy space (traslation and rotation)
    walk[0][0]=np.full(512, 0)
    walk[0][1]=np.full(512, 0.8)
    
    #The glass feature is hard to find with the 256-network, so it was findend once and saved into a file named 'glass_feature' 
    with open('glass_feature', 'rb') as handle:
        gf = pickle.load(handle)
    
   
    tempA = np.linspace(np.zeros(512), np.ones(512),n_samples) # 5 6
    
    tempB = np.linspace(np.zeros(512), np.ones(512)/2,n_samples) #7 8
    
    tempC = np.linspace(np.full(512, 0), np.concatenate((np.full(208, 0),gf,np.full(288, 0))),n_samples) #0 with - 1 without glasses
    
    
    for i in range(n_samples): #Smile
        for j in range(n_samples): #Eyes
            for k in range(n_samples): #Glasses
                walk[0][7]=tempB[j]
                walk[0][8]=tempB[j]
                walk[0][2]=tempC[k]
                walk[0][5]=tempA[i]
                walk[0][6]=tempA[i]
                img =gen_utils.w_to_img(G, torch.from_numpy(copy.deepcopy(walk)), noise_mode)
                PIL.Image.fromarray(img[0], 'RGB').save(f'{outdir}/grid_{i}{j}{k}.png')
    
    






if __name__ == "__main__":
    gen_grid() 
