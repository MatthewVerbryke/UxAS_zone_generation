#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import sys
import os

import PIL
from PIL import Image

from get_uav_data import parseAllFiles


class createBorder():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
            
        # Command line arguments
        self.scenario_path = sys.argv[1]
        self.img_path = sys.argv[2]
        
        # Get relevant UAV data from UxAS scenario files
        self.uxas_data = parseAllFiles(self.scenario_path)
        
        # Set number of UAVs
        self.uav_tot = self.uxas_data[0]
        
        # Change directory to image storage location
        os.chdir(self.img_path)
        
        # Run program
        self.main()
    
    #ADD BORDER TO GIVEN IMAGE
    def add_border(self, img_name, i):
        
        # Open the image
        img = Image.open(img_name)

        # Get image size
        img_size, height = img.size

        # New image has a single pixel border all the way around
        img_border_size = img_size + 2

        # Create new empty image for bordered image
        img_border = Image.new('L', [img_border_size,img_border_size])

        # Paste the old image in the center of the empty new one
        img_border.paste(img, ((img_border_size - img_size)/2, (img_border_size - img_size)/2))

        # Save this bordered image
        img_border.save(img_name)
        
        # Close image
        img.close()
        
    #MAIN PROGRAM
    def main(self):
        try:
        
            # Loop through all "p-zone" images
            for i in range(0,self.uav_tot):
                
                # Get current UAV ID
                current_uav = self.uxas_data[i+1][0]
                
                # Open the heightmap image
                img_name = '{}_obstructions.png'.format(current_uav)
                
                # Add border to image
                self.add_border(img_name, i)

        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)


if __name__ == "__main__":
    createBorder()
    
#EOF
