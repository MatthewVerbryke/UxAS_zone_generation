#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import sys

import numpy as np

from files import get_tile_number, get_file_name
from visualization import array_to_png


class GetElevationData():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.img_path = sys.argv[1]
        self.img_name_sub = sys.argv[2]
        self.abs_path = sys.argv[3]
        self.bound_box = (float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])) #(39.067176, -84.558347, 39.139042, -84.465692) 
        
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
            
            # Convert this to hgt cooordinates
            htg_coord = int(round(geo_frac * (self.hgt_size-1)))
            
            # Store bound in bounds list
            bounds[i] = (int(geo_floor), htg_coord)

        s = bounds[0]
        w = bounds[1]
        n = bounds[2]
        e = bounds[3]
        
        return s, w, n, e

    # RETRIEVE HGT FILE DATA
    def hgt_to_nparray(self, tile):
        
        # Get file name
        file_name = get_file_name(tile) + '.hgt'
        
        if os.path.isfile(file_name):
            # Read data from the hgt file into a numpy array, accounting for the file's big-endianess
            hgt_data = np.fromfile(file_name, dtype = '>i2').reshape((self.hgt_size, self.hgt_size))
        else:
            # Create array of zero values (assumes srtm.py couldn't find anything and tile is likely to be an ocean tile)
            hgt_data = np.zeros((self.hgt_size, self.hgt_size))
    
        return hgt_data

    #MERGE ALL RELEVANT DATA SETS
    def merge_hgt_data(self, s, w, n, e):
        
        # Pre-allocate array
        merged_tiles = np.zeros((self.ew_size, self.ns_size))
        
        # Loop through each tile
        for ns in self.ns_tiles:
            for ew in self.ew_tiles:
                
                # Put tile data into numpy array
                hgt_data = self.hgt_to_nparray((ns,ew))

                # Determine tile data offset
                ns_off = (self.hgt_size - 1)*(ns - s[0] + 1)
                ew_off = (self.hgt_size - 1)*(ew - w[0])
                
                # Place tile data into the new hgt file in the correct location
                for i in range(0,self.hgt_size):
                    for j in range(0,self.hgt_size):
                        merged_tiles[ew_off + j][ns_off - i] = hgt_data[i][j]
        
        return merged_tiles
        
    #CROP THE MERGED DATA SET TO THE SPECIFIED BOUNDS
    def crop_np_array(self, s, w, n, e, np_array):
        
        # Determine the size of the croped data set
        ew = self.ew_size - ((w[1]) + (self.hgt_size - e[1])) + 1
        ns = self.ns_size - ((s[1]) + (self.hgt_size - n[1])) + 1
        
        # Determine upper buffers
        e_buffer = w[1] + ew + 1
        n_buffer = s[1] + ns + 1

        # Slice the array along the bounds
        crop_array = np_array[w[1]:e_buffer, s[1]:n_buffer]       
        
        return crop_array
        
    def main(self):
        try:
            
            # Get info on required tiles
            tiles = get_tile_number(self.bound_box)
            
            # Determine bound information
            s, w, n, e = self.hgt_ao_bounds()  
            
            # Get tile 'axis' info
            self.ns_tiles = range(s[0], n[0] + 1)
            self.ew_tiles = range(w[0], e[0] + 1)
        
            # Determine data-set size for all tiles      
            self.ns_size = self.hgt_size*len(self.ns_tiles) - 1*(len(self.ns_tiles) - 1)
            self.ew_size = self.hgt_size*len(self.ew_tiles) - 1*(len(self.ew_tiles) - 1)
                      
            # Switch to store directory
            os.chdir(self.img_path)
            
            # Merge relevant hgtdata sets
            merged_hgts = self.merge_hgt_data(s, w, n, e)
            
            # Crop hgt data set
            ao_array = self.crop_np_array(s, w, n, e, merged_hgts)
            
            # Visualize data
            array_to_png(merged_hgts, 'hgt')
            array_to_png(ao_array, self.img_name_sub)
              
                
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)
            
        
if __name__ == "__main__":
    GetElevationData()

#EOF
