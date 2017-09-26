# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import PIL
from PIL import Image
import numpy as np

from visualization import array_to_png


def add_border(img_name):
    """Add a 1-pixel boundary around the edge of an obstruction image (for zone generation later)."""
    
    try:
        
        # Open the image
        img = Image.open(img_name)
        
        # Get image size
        width, height = img.size
        
        # Determine size needed for one pixel border
        width_wb = width + 2
        height_wb = height + 2
        
        # Create new empty image for bordered image
        img_border = Image.new('L', [width_wb, height_wb])
        
        # Paste the old image in the center of the empty new one
        img_border.paste(img, (1, 1))
        
        # Save this bordered image
        img_border.save(img_name)
        
    finally:
        
        # Close image
        img.close()

def generate_exclusions_areas(uav, alt, heights):
    """Create a PNG map of the terrain obstructions at a UAV's altitude."""       
    
    # Create blank array to hold exclusion array
    height_size = np.shape(heights)
    new_array = np.zeros(height_size)
    
    # Set value to 8-bit uint max in new array if terrain height is greater than uav altitude
    new_array[heights >= alt] = 255
    
    # Check that the entire map at altitude is not convered by obstructions
    check_array = np.zeros(height_size)
    check_array.fill(255)
    
    # TODO: handle this better
    if np.array_equal(new_array, check_array):
        print("Error: UAV {} has an altitude below the lowest elevation on the map.".format(uav))
        exit()
    
    # Output new array to PNG
    array_to_png(new_array, '{}_obstructions'.format(uav), False)    
        
    # Add border to png
    add_border('{}_obstructions.png'.format(uav))
    
    
#EOF
