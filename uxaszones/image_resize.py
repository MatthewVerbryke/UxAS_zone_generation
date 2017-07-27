# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.

import math
import os
import PIL
import sys
from PIL import Image


def imageResizeAndRescale(img_path, img_name):
    try:
        
        # Get cwd
        setdir = os.getcwd()
        
        # Set image size
        img_size = 257
        
        # Find and open .png
        os.chdir(img_path)
        img = Image.open('{}.png'.format(img_name))
        
        # Resize Image
        img = img.resize((int(img_size), int(img_size)), PIL.Image.ANTIALIAS) 
        
        # Rescale all pixels to the range 0 to 255 (in line with unit8 values)
        img_list = list(img.getdata())
        max_img = max(img_list)
        min_img = min(img_list)
        scale_factor = 255.0/(max_img - min_img)
        img_list2 = [0]*img_size*img_size

        for i in range(0,img_size):
            for j in range(0,img_size):
                img_list2[i*img_size + j] = int((img_list[i*img_size + j] - min_img)*scale_factor)
                if (img_list2[i*img_size + j] > 255) or (img_list2[i*img_size + j] < 0) or (img_list2[i*img_size + j]-int(img_list2[i*img_size + j]) != 0):
                    print("img_list2[%d][%d] = %r" % (i,j,img_list2[i*img_size + j]))

        img.putdata(img_list2)

        # Convert to uint8 greyscale image
        img = img.convert('L')

        # Save image
        new_img_name = '{}.png'.format(img_name)
        img.save(new_img_name) 
        
        return new_img_name
        
    finally:
        
        # Close image
        img.close()

        # Change back Directory
        os.chdir(setdir)

#EOF
