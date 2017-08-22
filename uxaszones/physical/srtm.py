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


class RetrieveSRTMData():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
        
        # Command line arguments
        self.img_path = sys.argv[1]
        self.img_name_sub = sys.argv[2]
        self.abs_path = sys.argv[3]
        self.bound_box = input('Input AO geodetic bounds: (south, west, north, east): ') #((39.067176, -84.558347, 39.139042, -84.465692)
        
        # Run main program
        self.main()   
        
    #DETERMINE TILES THAT NEED TO BE FETCHED
    def tile_number(self):
        
        # Find lat/long ceiling and floor
        lat_low = int(math.floor(self.bound_box[0]))
        lon_low = int(math.floor(self.bound_box[1]))
        lat_high = int(math.floor(self.bound_box[2]))
        lon_high = int(math.floor(self.bound_box[3]))
        
        # Calculate ranges
        lat_range = lat_high - lat_low + 1
        lon_range = lon_high - lon_low + 1
        
        tile_list = []
        
        # Fill list with needed tiles
        for i in range(0, lat_range):            
            for j in range(0, lon_range):
                tile_list.append(((lat_low + i), (lon_low + j)))
                
        #print tile_list
        return tile_list
        
    #DETERMINE IF TILE IS NORTH OR SOUTH OF EQUATOR
    def determine_n_or_s(self, tile):
        
            # Determine if north or south
            if (tile[0] >= 0):
                return 'N'
            else:
                return 'S'
    
    #DETERMINE IF TILE IS EAST OR WEST OF PRIME MERIDIAN
    def determine_e_or_w(self, tile):
        
            # Determine if west or east
            if (tile[1] >= 0):
                return 'E'
            else:
                return 'W'
    
        
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
                
            return 'North_America'
                
        # South America
        elif ((-53 <= tile[0] < 15 and -93 <= tile[1] <= -33) or
            (tile[0] < -53 and -76 <= tile[1] <= -64)):
                
            return 'South_America'
            
        # Eurasia
        elif ((tile[0] >= 35 and -14 <= tile[1] <= 179) or
            (-10 <= tile[0] < 35 and 60 <= tile[1] <= 179) or
            (-13 <= tile[0] <= -10 and 95 <= tile[1] <= 105) or
            (-10 <= tile[0] <= 10 and -180 <= tile[1] < -135) or
            (51 <= tile [0] <= 60 and -180 <= tile[1] < -170)):
                
            return 'Eurasia'
            
        # Africa
        elif ((tile[0] >= 0 and -32 <= tile[1] < 60) or
            (0 > tile[0] >= -35 and 5 <= tile[1] <= 63) or
            (45 >= tile[0] > 40 and -35 <= tile[1] <= -20)):
                
            return 'Africa'
            
        # Australia
        elif ((-45 <= tile[0] < -10 and 110 < tile[1] < 160) or 
            (-25 <= tile[0] < -10 and 160 <= tile[1] < 179) or
            (-28 <= tile[0] < -10 and -180 <= tile[1] < -105)):
                
            return 'Australia'
            
        # Other
        else:
            return 'Islands'
        
    #FIND DESIRED STRM3 90m TILE SET LOCATION FOR ONLINE SOURCE
    def determine_url(self, tile):
              
        url_stub = 'https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/'
            
        # Determine tile location
        n_or_s = self.determine_n_or_s(tile)
        e_or_w = self.determine_e_or_w(tile)
        
        # Determine continent
        continent = self.determine_continent(tile)
        
        # take absolute values
        lat = abs((tile[0]))
        lon = abs((tile[1]))
        
        # Construct URL and file-name
        file_name = n_or_s + str(lat) + e_or_w + '0' + str(lon) + '.hgt.zip'
        url = url_stub + continent + '/' + file_name 
        
        return url, file_name

    #RETRIEVE HGT.ZIP FILE FROM ONLINE SOURCE
    def retrieve_map(self, url):
        
        # Switch to store directory
        os.chdir(self.img_path)
        
        # Open URL destination
        u = urllib2.urlopen(url)
        
        # Read .zip file and write to store path
        with open(os.path.basename(url), 'wb') as local_file:
            local_file.write(u.read())
            
    #UNZIP HGT FILE 
    def unzip_map(self, file_name):
        
        # Extract .hgt file from .zip file and place it in the store path
        zip_ref = zipfile.ZipFile(file_name, 'r')
        zip_ref.extractall(self.img_path)
        
        # Close .zip file
        zip_ref.close()

    #MAIN LOOP
    def main(self):
        try:
            
            # Get info on required tiles
            tiles = self.tile_number()
            
            for i in range(0,len(tiles)):
                
                # Determine filename and url of each tile
                url, file_name = self.determine_url(tiles[i]) 
                
                # Download and extract the .hgt file from the online source
                self.retrieve_map(url)
                self.unzip_map(file_name)
            
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)
            
            
if __name__ == "__main__":
    RetrieveSRTMData()
        
#EOF
