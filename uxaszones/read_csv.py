# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.


import csv
import os


#OPEN, READ, AND GET DATA FROM CSV DATA FILE
def read_csv_input(img_path, data_return):    
    
    # Change directory to the image path
    os.chdir(img_path)
    
    data_list = []

    # Open file and read data
    with open('data.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data_value = float(row[0])
            data_list.append(data_value)
    
    # Retrieve height data
    if (data_return == 'heights'):

        # Get maximum and minimum heights found in the heightmap image
        max_height = data_list[0]
        min_height = data_list[1]
        
        # Check height validity
        if (max_height < min_height):
            print ('Error: Maximum height is less than minimum height')
            exit()
            
        # Calculate height range in image
        height_range = max_height - min_height      
        
        return height_range
      
    # Retrieve location data    
    elif (data_return == 'location'):

        # Get Latitude and Longitude of the Northeast and Southwest corner of the image
        ne_corner_lat = data_list[2]
        ne_corner_long = data_list[3]
        sw_corner_lat = data_list[4]
        sw_corner_long = data_list[5]

        return [ne_corner_lat, ne_corner_long, sw_corner_lat, sw_corner_long]
    
    # Retreive image scale data
    elif (data_return == 'side_length'):
            
        # Get side length of image area on earth's surface
        img_len = data_list[6]
            
        return img_len

#EOF
