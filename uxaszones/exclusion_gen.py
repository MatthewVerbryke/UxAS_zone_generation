#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

#ASSUMES UAV ALTITUDES ARE DESCRETIZED!

import csv
import os
import string
import sys

import PIL
from PIL import Image

from get_uav_data import parse_all_files
from image_resize import image_resize_and_rescale
from read_csv import read_csv_input


class exclusionAreaGenerator():

    def __init__(self):

        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.scenario_path = sys.argv[1]
        self.img_path = sys.argv[2]
        self.img_name_sub = sys.argv[3]
        self.img_name = self.img_name_sub + '.png'
        
        # Run program
        self.main()

    #CREATE SORTED UAV DATA LIST (UAV NAME, RAW ALTITUDE, SCALED ALTITUDE)
    def create_sorted_data_list(self, height_range, uxas_input):

        # Determine conversion factor between height(in meters) and specific bit value in image (0-255)
        scale_size = 255./height_range

        # Initialize 'uav_data' list with ground level
        uav_data = [['ground', 0.0]]

        # Altitudes for each UAV
        for i in range(1,self.uav_tot+1):
            ID_in = uxas_input[i][0]
            alt_in = uxas_input[i][1]
            uav_data.append([ID_in, alt_in])

        # Add in maximum height from heightmap
        uav_data.append(['max height', height_range])

        # Sort altitudes min --> max
        sorted_uav_data = sorted(uav_data, key=lambda uav: uav[1])

        # Add scaled altitudes
        for i in range(0,self.uav_tot+2):
            sorted_uav_data[i].append(int(scale_size*sorted_uav_data[i][1]))

        return sorted_uav_data

    #FOR EACH UAV, FIND THE AREAS OF THE HEIGHTMAP IMAGE THAT ARE AT ITS ALTITUDE AND MARK THEM AS A EXCLUSION AREA IN A NEW PNG MAP
    def determine_exclusions(self, sorted_uav_data):
        try:

            # Open image
            img = Image.open(self.img_name)

            # Find image size
            img_size, height = img.size

            # Get data from heightmap image and create new list for modified data
            imglist = list(img.getdata())
            imglist_all = [0]*img_size*img_size

            # Determine and print-out exclusion zones for each UAV
            for i in range(0,self.uav_tot+2):

                if (sorted_uav_data[i][0] == 'ground') or (sorted_uav_data[i][0] == 'max height'):
                    pass
                else:
                    imglist_out = [0]*img_size*img_size
                    for j in range(img_size):
                        for k in range(img_size):
                            if (sorted_uav_data[i][2] >= 255):
                                pass
                            elif (imglist[j*img_size + k] >= sorted_uav_data[i][2]):
                                imglist_all[j*img_size + k] = sorted_uav_data[i][2]
                                imglist_out[j*img_size + k] = 255

                    img.putdata(imglist_out)
                    uav_name = sorted_uav_data[i][0]
                    img.save('{}_obstructions.png'.format(uav_name))

            # Create image and save it for all UAVs
            img.putdata(imglist_all)
            img.save('all_obstructions.png')

        finally:
            
            #Close image
            img.close()
        
    # MAIN BLOCK
    def main(self):
        
        try:
            # Get data from csv file
            height_range = read_csv_input(self.img_path, 'heights')

            # Get data from uxas scenario file
            uxas_input = parse_all_files(self.scenario_path)

            # Get number of UAVs in scenario
            self.uav_tot = uxas_input[0]

            # Create sorted UAV data list
            sorted_uav_data = self.create_sorted_data_list(height_range, uxas_input)

            # Rescale image
            scaled_img_name = image_resize_and_rescale(self.img_path, self.img_name_sub)

            # Determine exclusion areas on the map
            self.determine_exclusions(sorted_uav_data)

        finally:
            # Switch back to the cwd
            os.chdir(self.setdir)


if __name__ == "__main__":
    exclusionAreaGenerator()
        
#EOF
