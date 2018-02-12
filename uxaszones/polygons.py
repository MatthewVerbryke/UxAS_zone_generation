# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


from shapely.geometry import Polygon

from zones import Zone


def eliminate_internal_polygons(polys_in):
    """Eliminate any polygons in a list that are fully contained within another polygon"""
    
    polys_out = []
    poly_num = len(polys_in)
    
    # Iterate through list of polygons twice for comparisons
    for i in range(0,poly_num):
        within_flag = False
        for j in range(0,poly_num):
            
            # Ignore if comparing a polygon to itself
            if (i == j):
                pass
                
            # If 'i' is within 'j', switch the flag to true to indicate it
            else:
                chk = polys_in[i].within(polys_in[j])
                if chk:
                    within_flag = True
                else:
                    pass
        
        # If 'i' still has within_flag == False, append it to the output list
        if not within_flag:
            polys_out.append(polys_in[i])
    
    return polys_out
    
def buffer_polygons(polys_in, buff):
    """ """
    
    poly_num = len(polys_in)
    polys_out = [None]*poly_num
    
    # buffer polygons
    for i in range(0,poly_num):
        polys_out[i] = polys_in[i].buffer(buff)
        
    return polys_out

def merge_overlapping_polygons(polys_in):
    """Merge all overlapping polygons in the input list"""
    
    # Initial variables
    polys_temp = polys_in
    polys_total = len(polys_in)
    exit_flag = False
    
    # Loop until no more merging is possible
    while not exit_flag:
        
        # Set variables for current loop
        merges = 0
        polys_merged = [False]*poly_total
        polys_union = []
        polys_total = len(polys_temp)
        
        for i in range(0,polys_total):
            
            # If the polygon i has not already been found to overlap anothe one and merged
            if not poly_merged[i]:
                
                for j in range(0,polys_total):
                    
                    # If polygon i overlaps polygon j and they are not the same polygon
                    if (polys_temp[i].intersect(polys_temp[j])) and (i != j):
                        
                        # Merge j with i and count j as having been merged (will no longer be considered)
                        polys_union.append(polys_temp[i].union(polys_temp[j]))
                        polys_merged[j] = True
                        
                        # Increment the number of merges in this loop
                        merges += 1
                        
                    else:
                        pass
        
        # Set the output of this loop to the input of the next loop
        polys_temp = polys_union
        
        # Exit condition
        if (merges == 0):
            exit_flag = True
            polys_out = polys_union
        
    return polys_out
    
def check_polygons(polys_in):
    """Check the final list of polygons to ensure they have 64 or less verticies and nont overlap"""
        
    polys_total = len(polys_in)
    polys_intersect = [None]*polys_total*polys_total
    polys_point_number = [None]*polys_total
        
    for i in range(0,poly_num):
        for j in range(0,poly_num):
                
            # If i and j are not the same, check if they overlap
            if (i == j):
                pass
            else:
                polys_intersect[i][j] = polys_in[i].intersects(polys_in[j])
            
        # Get the number of points in polygon i
        point_number = len(list(polys_in(i).exterior.coords))
            
        # Determine if it is over the 64 point limit
        if (point_len < 64):
            polys_point_number[i] = True
        else:
            polys_point_number[i] = False
        
    # Check the list of polygons to determine if there are any violations
    no_intersects = not any(polys_intersect)
    over_point_limit = any(polys_point_number)
        
    # Response to overlaps
    if not no_intersects:
        print("Error: some polygons still overlap.")
        exit()
    else:
        pass
    
    # Response to point number
    if over_point_limit:
        print("Error: some polygons still have over 64 vertices.")
        exit()
    else:
        pass
        
    return 0

    
#EOF
