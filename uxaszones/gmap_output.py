# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.

import os

import gmplot


def plot_to_google_maps(polys_in, corners, uav_data, img_path):
    
    poly_num = len(polys_in)
    
    # Find heightmap center location
    center_lat = (corners[0] + corners[2])/2
    center_long = (corners[1] + corners[3])/2
    
    # Initialize map
    gmap = gmplot.GoogleMapPlotter(center_lat, center_long, 16)
    
    for i in range(0,poly_num):
        poly_outline = list(polys_in[i].exterior.coords)
        point_len = len(poly_outline)
        points_lat = [None]*point_len
        points_long = [None]*point_len
        #print(poly_outline)
        # Create list of point longitude and latitudes
        for j in range(0,point_len):
            points_lat[j] = poly_outline[j][0]
            points_long[j] = poly_outline[j][1]
        
        # Create polygon object
        gmap.polygon(points_lat, points_long, 'r')
        
        # Create points for each corner of the image (this is a check)
        #corner_lats = (corners[0], corners[2], corners[2], corners[0])
        #corner_longs = (corners[1], corners[1], corners[3], corners[3])
        #gmap.polygon(corner_lats, corner_longs, 'k')
    
    # Change to store directory
    os.chdir(img_path)
    
    # Save data into html
    html_name = "{}_zones.html".format(uav_data)
    gmap.draw(html_name)

#EOF
