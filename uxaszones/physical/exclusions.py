#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import csv
import os
import string
import sys

import PIL
from PIL import Image
import numpy as np

from visualization import array_to_png


class GenerateExclusionAreas():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
        
        # Command line arguments
        self.store_path = sys.argv[1]
        self.scenario_name = sys.argv[2]
        self.bound_box = (float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))
        
        # Run main program
        self.main()
    
    # DETERMINE TERRAIN EXCLUSIONS AT THE PROVIDED UAV'S ALTITUDE
    def determine_exclusions(self, alt, heights, ID):
        
        # Create blank array to hold exclusion array
        height_size = np.shape(heights)
        new_array = np.zeros(height_size)
        
        # Set value to max in new array if terrain height is greater than altitude
        new_array[heights >= alt] = 255
        
        # Check that the entire map at altitude is not convered by obstructions
        check_array = np.zeros(height_size)
        check_array.fill(255)
        
        if np.array_equal(new_array, check_array):
            print("Error: UAV {} has an altitude below the lowest elevation on the map.".format(ID))
            exit()
        
        # Output new array to PNG
        array_to_png(new_array, '{}_obstructions'.format(ID), False)
        
        return new_array

    # MAIN LOOP
    def main(self):
        
        try:
            
            # Switch to store directory
            os.chdir(self.store_path)
            
            # Get terrain info
            heights = np.load("{}.npy".format(self.scenario_name))
            
            # Get UAV info
            uavs = np.load("uav.npy")
            uav_num, foo = np.shape(uavs)
            
            # Sort altitudes min --> max
            sorted_uavs = sorted(uavs, key=lambda uav: uav[1])
            
            all_array = np.zeros(np.shape(heights))
            
            for i in range(0,uav_num):
                
                # Iterate through uav list to determine terrian obstructions
                obstruct_array = self.determine_exclusions(sorted_uavs[i][1], heights, int(sorted_uavs[i][0]))
                
                # Determine scale for combining obstruction maps
                scale_h = int(255/uav_num)*(i+1)
        
                # Add obstructions to all_obstructions visualization
                all_array[obstruct_array == 255] = scale_h
                
            # Output all array to PNG
            array_to_png(all_array, 'all_obstructions', False)
                
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)
            
            
if __name__ == "__main__":
    GenerateExclusionAreas()
    
    
#EOF
