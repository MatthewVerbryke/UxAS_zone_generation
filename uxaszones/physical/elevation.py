#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import sys

import numpy as np
import PIL
from PIL import Image

from files import get_tile_number, get_file_name


class GetElevationData():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.img_path = sys.argv[1]
        self.img_name_sub = sys.argv[2]
        self.abs_path = sys.argv[3]
        self.bound_box = input('Input AO geodetic bounds: (south, west, north, east):#(39.067176, -84.558347, 39.139042, -84.465692) ')
        
        # File Properties
        self.hgt_size = 1201
        
        # Run main program
        self.main()
     
    #DETERMINE AO BOUNDS IN HGT 'COORDINATES'
    def hgt_ao_bounds(self):
        
        bounds = [None] * 4
        
        # Loop through all four bound locations
        for i in range(0,4):
            
            # Find the next-lowest, relevent coordinate
            geo_floor = math.floor(self.bound_box[i])
            
            # Find the 'overrun' from the next lowest coordinate
            geo_frac = self.bound_box[i] - geo_floor
            
            # Convert this to HTG cooordinates
            htg_coord = int(round(geo_frac * (self.hgt_size-1)))
            
            # Store bound in bounds list
            bounds[i] = (int(geo_floor), htg_coord)
            
        return bounds

    # RETRIEVE HGT FILE DATA
    def hgt_to_nparray(self, tile):
        
        # Get file name
        file_name = get_file_name(tile) + '.hgt'
        
        # Read data from the HGT file into a numpy array, accounting for the file's big-endianess
        hgt_data = np.fromfile(file_name, dtype = '>i2').reshape((self.hgt_size, self.hgt_size))
        
        return hgt_data

    # CONVERT NUMPY ARRAY TO GREYSCALE PNG IMAGE
    def nparray_to_png(self, nparray):
        
        img_list = list(nparray)
        
        img= Image.new('I', (self.hgt_size, self.hgt_size))
        
        img.putdata(img_list)
        
        img_name = self.img_name_sub + '.png' 
        img.save(img_name)
        
    #'CROP' THE HGT FILE TO THE CORRECT SIZE
    def crop_to_ao(self, bounds, np_array):
        
        s = bounds[0][1]
        w = bounds[1][1]
        n = bounds[2][1]
        e = bounds[3][1]
        
        new_size = (n - s, e - w)
        
        crop_array = [None]*new_size[0]*new_size[1]        
                
        for i in range(0, new_size[0]):
            for j in range(0, new_size[1]):
                crop_array[i*new_size[1] + j] = np_array[s + i, e + j]
                
                
        np.save(self.img_name_sub, crop_array)
        
    def main(self):
        try:
            
            # Get info on required tiles
            tiles = get_tile_number(self.bound_box)
            
            # Convert bounds to 3 arc-second scale
            bounds = self.hgt_ao_bounds()
            
            # Switch to store directory
            os.chdir(self.img_path)
            
            for i in range(0,len(tiles)):
                
                # Pass HGT data into a numpy array
                hgt_array = self.hgt_to_nparray(tiles[i])
                
                # Crop HGT file to AO; output result
                self.crop_to_ao(bounds, hgt_array)
                
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)
            
        
if __name__ == "__main__":
    GetElevationData()

#EOF
