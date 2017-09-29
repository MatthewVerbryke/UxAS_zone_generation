# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import gmplot
import matplotlib.pyplot as plt
import numpy as np


def print_polygons(polys_in, color):
    """Print the given polygon-list in a matplotlib plot with the specified color"""
    
    # NOTE: This will correct the orientation of the PNG coordinate frame 
    # to the real world frame, where (0,0) is the northeast corner.   
    
    poly_num = len(polys_in)
    
    # Plot
    for i in range(0,poly_num):
        
        # Convert polygon bound to numpy array
        poly_outline = list(polys_in[i].bound.exterior.coords)
        poly_outlines = np.array(poly_outline)
        
        # Plot polygon with correct orientation
        plt.plot(poly_outlines[:,0], poly_outlines[:,1], color)
        
def plot_to_google_maps(zone_list, ao_bound, uav_ID, img_path, check):
    """Create a google map HTML file to visualize the zones on a real-world map"""
    
    zone_total = len(zone_list)
    
    # Find heightmap center location
    center_lat = (ao_bound[0] + ao_bound[2])/2
    center_lon = (ao_bound[1] + ao_bound[3])/2
    
    # Initialize map
    gmap = gmplot.GoogleMapPlotter(center_lat, center_lon, 16)
    
    for i in range(0,zone_total):
        
        # Put boundary points into a list
        zone_bound = list(zone_list[i].bound.exterior.coords)
        
        bound_point_length = len(zone_bound)
        points_lat = [None]*bound_point_len
        points_long = [None]*bound_point_len

        # Create individual lists for point longitudes and latitudes
        for j in range(0,bound_point_length):
            points_lat[j] = zone_bound[j][0]
            points_long[j] = zone_bound[j][1]
        
        # Create gmplot polygon object
        gmap.polygon(points_lat, points_long, 'r')
        
        # For testing purposes, plot AO boundaries to ensure the zones match up to the AO
        if check:
            corner_lats = (ao_bound[0], ao_bound[2], ao_bound[2], ao_bound[0])
            corner_longs = (ao_bound[1], ao_bound[1], ao_bound[3], ao_bound[3])
            
            # Create gmplot polygon object
            gmap.polygon(corner_lats, corner_longs, 'k')
    
    # Save data into HTML
    html_name = "{}_zones.html".format(uav_ID)
    gmap.draw(html_name)

#EOF
