#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import sys
import urllib2
import zipfile

import numpy as np

from visualization import array_to_png


class RetrieveAODataSRTM3():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
        
        # Command line arguments
        self.store_path = sys.argv[1]
        self.scenario_name = sys.argv[2]
        self.bound_box = (float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

        # URL stub
        self.url_stub = "https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/"

        # HGT Properties
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
        
    #DETERMINE SRTM 'CONTINENT'
    def determine_continent(self, tile):
        
        #Note: I'm still checking if these definitions always work
        
        # Out of data set
        if (tile[0] < -56 or tile[0] > 60 or tile[1] >= 180 or tile[1] < -180):
            
            print("Error: selected data is outside the SRTM dataset range.")
            exit()
        
        # North America
        elif ((tile[0] >= 15 and -149 <= tile[1] <= -40) or
            (tile[0] >= 30 and -170 <= tile[1] <= -150) or
            tile == (10, -110)):
                
            return "North_America"
                
        # South America
        elif ((-53 <= tile[0] < 15 and -93 <= tile[1] <= -33) or
            (tile[0] < -53 and -76 <= tile[1] <= -64)):
                
            return "South_America"
            
        # Eurasia
        elif ((tile[0] >= 35 and -14 <= tile[1] <= 179) or
            (-10 <= tile[0] < 35 and 60 <= tile[1] <= 179) or
            (-13 <= tile[0] <= -10 and 95 <= tile[1] <= 105) or
            (-10 <= tile[0] <= 10 and -180 <= tile[1] < -135) or
            (51 <= tile [0] <= 60 and -180 <= tile[1] < -170)):
                
            return "Eurasia"
            
        # Africa
        elif ((tile[0] >= 0 and -32 <= tile[1] < 60) or
            (0 > tile[0] >= -35 and 5 <= tile[1] <= 63) or
            (45 >= tile[0] > 40 and -35 <= tile[1] <= -20)):
                
            return "Africa"
            
        # Australia
        elif ((-45 <= tile[0] < -10 and 110 < tile[1] < 160) or 
            (-25 <= tile[0] < -10 and 160 <= tile[1] < 179) or
            (-28 <= tile[0] < -10 and -180 <= tile[1] < -105)):
                
            return "Australia"
            
        # Other
        else:
            return "Islands"
        
    #DETERMINE HGT FILE NAME
    def get_file_name_url(self, tile):

        # Determine if north or south
        if (tile[0] >= 0):
            lat_dir = "N"
        else:
            lat_dir = "S"

        # Determine if west or east
        if (tile[1] >= 0):
            lon_dir = "E"
        else:
            lon_dir = "W"

        # Take absolute values
        lat = abs((tile[0]))
        lon = abs((tile[1]))
            
        # Construct file name
        if (lon < 100):
            file_name = lat_dir + str(lat) + lon_dir + "0" + str(lon) + ".hgt"
        else:
            file_name = lat_dir + str(lat) + lon_dir + str(lon) + ".hgt"

        # Determine continent
        continent = self.determine_continent(tile)    
        
        # Construct url
        url = self.url_stub + continent + "/" + file_name + ".zip"
        
        return url, file_name
    
    #RETRIEVE HGT.ZIP FILE FROM ONLINE SOURCE
    def retrieve_htg_data(self, url, file_name):
        try:
            
            # Open URL destination
            u = urllib2.urlopen(url)
            
            # Read .zip file and write to store path
            with open(os.path.basename(url), "wb") as local_file:
                local_file.write(u.read())
            
            zip_name = file_name + ".zip"
            
            # Extract .hgt file from .zip file and place it in the store path
            zip_ref = zipfile.ZipFile(zip_name, "r")
            zip_ref.extractall(self.store_path)
        
            # Close and delete .zip file
            zip_ref.close()
        
            # Read data from the hgt file into a numpy array, accounting for the file's big-endianess
            hgt_data = np.fromfile(file_name, dtype = ">i2").reshape((self.hgt_size, self.hgt_size))

            return hgt_data
                
        except:

            # Assume file does not exist because it is an ocean tile (need to test)
            print("Couldn't find {}; assuming ocean tile\n".format(url))

            # Create array of zero values 
            hgt_data = np.zeros((self.hgt_size, self.hgt_size))
        
            return hgt_data
            
    def merge_hgt_data(self, s, w, n, e):
        
        # Pre-allocate array
        merged_tiles = np.zeros((self.ew_size, self.ns_size))
        
        # Loop through each tile
        for ns in self.ns_tiles:
            for ew in self.ew_tiles:
                
                # Get tile name and url
                url, file_name = self.get_file_name_url((ns,ew))
                
                # Put tile data into numpy array
                hgt_data = self.retrieve_htg_data(url, file_name)
                
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
        
    #MAIN LOOP
    def main(self):
        try:
            
            # Determine bound information
            s, w, n, e = self.hgt_ao_bounds()
            
            # Get tile 'axis' info
            self.ns_tiles = range(s[0], n[0] + 1)
            self.ew_tiles = range(w[0], e[0] + 1)
        
            # Determine data-set size for all tiles together      
            self.ns_size = self.hgt_size*len(self.ns_tiles) - 1*(len(self.ns_tiles) - 1)
            self.ew_size = self.hgt_size*len(self.ew_tiles) - 1*(len(self.ew_tiles) - 1)
            
            # Switch to store directory
            os.chdir(self.store_path)
            
            # Merge relevant hgtdata sets
            merged_hgts = self.merge_hgt_data(s, w, n, e)

            # Crop hgt data set
            ao_array = self.crop_np_array(s, w, n, e, merged_hgts)
            
            # Visualize data
            array_to_png(merged_hgts, 'hgt', True)
            array_to_png(ao_array, self.scenario_name, True)
            
            # Output data to npy file
            np.save(self.scenario_name, ao_array)           
                
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)
            
        
if __name__ == "__main__":
    RetrieveAODataSRTM3()

#EOF
