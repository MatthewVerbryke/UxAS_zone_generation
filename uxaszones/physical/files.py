# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.


import math


#DETERMINE TILES THAT NEED TO BE FETCHED
def get_tile_number(bound_box):
        
    # Find lat/long ceiling and floor
    lat_low = int(math.floor(bound_box[0]))
    lon_low = int(math.floor(bound_box[1]))
    lat_high = int(math.floor(bound_box[2]))
    lon_high = int(math.floor(bound_box[3]))
    
    # Calculate ranges
    lat_range = lat_high - lat_low + 1
    lon_range = lon_high - lon_low + 1
    
    tile_list = []
    
    # Fill list with needed tiles
    for i in range(0, lat_range):            
        for j in range(0, lon_range):
            tile_list.append(((lat_low + i), (lon_low + j)))
    
    return tile_list
    
#DETERMINE HGT FILE NAME
def get_file_name(tile):

    # Determine tile location
    lat_dir = n_or_s(tile)
    lon_dir = e_or_w(tile)

    # Take absolute values
    lat = abs((tile[0]))
    lon = abs((tile[1]))
        
    # Construct file name
    if (lon < 100):
        file_name = lat_dir + str(lat) + lon_dir + '0' + str(lon)
    else:
        file_name = lat_dir + str(lat) + lon_dir + str(lon)
    
    return file_name
    
#DETERMINE IF TILE IS NORTH OR SOUTH OF EQUATOR
def n_or_s(tile):
        
    # Determine if north or south
    if (tile[0] >= 0):
        return 'N'
    else:
        return 'S'

#DETERMINE IF TILE IS EAST OR WEST OF PRIME MERIDIAN
def e_or_w(tile):
        
    # Determine if west or east
    if (tile[1] >= 0):
        return 'E'
    else:
        return 'W'
        
        
#EOF
