# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.

import math
import os
import sys

import numpy as np
import PIL
from PIL import Image


#CONVERT A NUMPY ARRAY INTO A PNG FOR VISUALIZATION PURPOSES
def array_to_png(np_array, img_name, rescale):
    
    try:
        # Determine dimensions of the numpy array
        width, height = np_array.shape

        # Create new image of type 8-bit unsigned integer (uint8)
        img = Image.new('L', (height, width))
        
        # 'Flatten' the input array
        np_flat = np_array.flatten()
        
        # Rescale if input 'rescale' is True
        if rescale:
            # Filter out data errors
            for i in range(0,len(np_flat)):
                if (np_flat[i] == -32768):
                    np_flat[i] = 0
            
            # Determine scaling factor to 'uint8'
            max_img = max(np_flat)
            min_img = min(np_flat)
            scale_factor = 255.0/(max_img - min_img)
        
            # Multiply all values by scale_factor
            img_list = scale_factor*(np_flat - min_img)
            
        else:
            img_list = np_flat
                    
        # Save data to png file
        img.putdata(img_list)
        img.save('{}.png'.format(img_name))

    finally:
        
        # Close image
        img.close()


#EOF
