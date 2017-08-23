#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import os
import sys
import urllib2
import zipfile

from files import get_tile_number, get_file_name


class RetrieveSRTMData():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
        
        # Command line arguments
        self.img_path = sys.argv[1]
        self.img_name_sub = sys.argv[2]
        self.abs_path = sys.argv[3]
        self.bound_box = input('Input AO geodetic bounds: (south, west, north, east): ')#(39.067176, -84.558347, 39.139042, -84.465692)
        
        # Switch to store directory
        os.chdir(self.img_path)
        
        # Run main program
        self.main()   
        
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
        
        # Determine continent
        continent = self.determine_continent(tile)
        
        # Build url
        file_name = get_file_name(tile) + '.hgt.zip'
        url = url_stub + continent + '/' + file_name 
        
        return url, file_name

    #RETRIEVE HGT.ZIP FILE FROM ONLINE SOURCE
    def retrieve_map(self, url):
        
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
            tiles = get_tile_number(self.bound_box)
            
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
