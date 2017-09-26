# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import math
import os
import urllib2
import zipfile

import numpy as np

from visualization import array_to_png


def convert_to_hgt_scale(bounds):
    """Convert the boundary location from geodetic (degrees) to HGT "coordinates" (degree count, 3-arc-second intervals)."""
    
    hgt_bounds = [None]*4
    
    # Loop through all four bound locations
    for i in range(0,4):
        
        # Find the next-lowest, relevant coordinate
        geo_floor = math.floor(bounds[i])
        
        # Find the 'overrun' from the next-lowest coordinate
        geo_frac = bounds[i] - geo_floor
            
        # Convert this to HGT cooordinates
        hgt_coord = int(round(geo_frac * (1201-1)))
            
        # Store bound in bounds list
        hgt_bounds[i] = (int(geo_floor), hgt_coord)

    s = hgt_bounds[0]
    w = hgt_bounds[1]
    n = hgt_bounds[2]
    e = hgt_bounds[3]
        
    return s, w, n, e

def determine_continent(tile):
    """Determine on which continent group (TODO) the AO is located."""
    
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
        
def construct_filename_url(tile):
    """Construct the filename and url of the specified HGT tile."""

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
    continent = determine_continent(tile)    
        
    # Construct url
    url_stub = "https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/"
    url = url_stub + continent + "/" + file_name + ".zip"
    
    return url, file_name
    
def retrieve_htg_data(url, file_name):
    """Retrieve HGT data from the USGS website with the specified url and filename"""
    try:
        
        # Open URL destination
        u = urllib2.urlopen(url)
            
        # Read .zip file and write to store path
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(u.read())
            
        zip_name = file_name + ".zip"
            
        # Extract HGT file from ZIP file and place it in the store path
        zip_ref = zipfile.ZipFile(zip_name, "r")
        zip_ref.extractall(os.getcwd())
        
        # Close ZIP file
        zip_ref.close()
        
        # Read data from the HGT file into a numpy array, accounting for the file's big-endianess
        hgt_data = np.fromfile(file_name, dtype = ">i2").reshape((1201, 1201))

        return hgt_data
                
    except:

        # Assume file does not exist because it is an ocean tile
        print("Couldn't find {}; assuming ocean tile\n".format(url))

        # Create array of zero values 
        hgt_data = np.zeros((1201, 1201))
        
        return hgt_data

def retrieve_AO_data_STRM3(bounds):
    """Retrieve the heightmap data for the AO from the USGS STRM 3-arc-second global dataset"""

    # TODO: change this to an optional argument
    visualize = True

    # Determine bound information
    s, w, n, e = convert_to_hgt_scale(bounds)
    
    # Get tile 'axis' info
    ns_tiles = range(s[0], n[0] + 1)
    ew_tiles = range(w[0], e[0] + 1)
    
    # Determine data-set size for all tiles together      
    ns_size = 1201*len(ns_tiles) - 1*(len(ns_tiles) - 1)
    ew_size = 1201*len(ew_tiles) - 1*(len(ew_tiles) - 1)

    merged_tiles = np.zeros((ew_size, ns_size))
        
    # Loop through each tile
    for ns in ns_tiles:
        for ew in ew_tiles:
                
            # Get tile name and url
            url, file_name = construct_filename_url((ns,ew))
                
            # Put tile data into numpy array
            hgt_data = retrieve_htg_data(url, file_name)
                
            # Determine tile data offset
            ns_off = (1201 - 1)*(ns - s[0] + 1)
            ew_off = (1201 - 1)*(ew - w[0])
                
            # Place tile data into the new merged HGT file
            for i in range(0, 1201):
                for j in range(0, 1201):
                    merged_tiles[ew_off + j][ns_off - i] = hgt_data[i][j]
    
    # Determine the size of the croped data set
    ew = ew_size - ((w[1]) + (1201 - e[1])) + 1
    ns = ns_size - ((s[1]) + (1201 - n[1])) + 1
        
    # Determine upper buffers
    e_buffer = w[1] + ew + 1
    n_buffer = s[1] + ns + 1

    # 'Crop' the merged HGT data set to the AO bounds
    crop_array = merged_tiles[w[1]:e_buffer, s[1]:n_buffer]       
    
    # Visualize data
    if visualize:
        array_to_png(merged_tiles, 'hgt_mosaic', True)
        array_to_png(crop_array, 'ao_hgt', True)
            
    return crop_array


#EOF
