# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


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
    
    # Bring-up plot of all polygons
    plt.show()
    
#EOF
