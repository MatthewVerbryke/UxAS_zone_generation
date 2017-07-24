#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/ (FILL IN THIS)
# Additional copyright may be held by others, as reflected in the commit history.


import numpy as np
from scipy import misc
from shapely.geometry import Polygon, MultiPoint
from skimage import measure
import matplotlib.pyplot as plt


#INPUTS



#CONSTANTS
# Get image name
img_name = 'uav_2_pzones.png'

# Get image size
img_size = 259

# Get the desired buffer distance
	#will be based on turn radius + some safety factor(?)
buff_dist = 135.553*img_size/8000 #sys.argv[1]

# Maximum number of vertices per polygon allowed
verts_max = 64


#CREATE POLYGONS FROM HEIGHTMAP IMAGE CONTOURS
def pngToPolygons():

    # Open the heightmap image
    zone_map = misc.imread(img_name)

    # Run through the png and find the contour lines
    cont_points = measure.find_contours(zone_map, 1.0)

    # Find the number of individual shapes in the file
    cont_points_len = len(cont_points)

    polygons = []

    # Create polygons from contours
    for i in range(0,cont_points_len):
        poly_point_un = cont_points[i]
        poly_point_len = len(poly_point_un)

        poly_points = []

        # Correct the orientation of the contours so they match the png
        for j in range(0,poly_point_len):
            poly_points.append([(poly_point_un[j][1]), poly_point_un[j][0]])

        # Create shapely polygon from corrected contours
        polygon = Polygon(poly_points)

        # Store this polygon in the "polygons" list
        polygons.append(polygon)

    return polygons


# CREATE SHAPE FOR IMAGE BOUNDS
def createImageBounds():

    bound_size = float(img_size - 1)
    bound_corners = ([0.,0.], [0.,bound_size], [bound_size,bound_size], [bound_size,0.], [0.,0.])
    bound_np = np.array(bound_corners)
    bound = Polygon(bound_corners)

    return bound


#ELIMINATE INTERNAL POLYGONS
def eliminateInnerRings(polys_in):

    polys_out = []
    poly_num = len(polys_in)

    # Check for inner rings and filter out those that are found
    for i in range(0,poly_num):
        within_flag = False
        for j in range(0,poly_num):
            if (i == j):
                pass
            else:
                chk = polys_in[i].within(polys_in[j])
                if (chk == True):
                    within_flag = True
                else:
                    pass
    
		# If a polygon is not within another one, append it to the output list
        if (within_flag == False):
            polys_out.append(polys_in[i])

    return polys_out


#CREATE BUFFER AROUND POLYGONS
def bufferPolygons(polys_in):

    polys_out = []
    poly_num = len(polys_in)

    # Buffer polygons
    for i in range(0,poly_num):
        poly_now = polys_in[i].buffer(buff_dist)
        polys_out.append(poly_now)

    return polys_out


#CROP POLYGONS INTO IMAGE FRAME
def cropPolygons(polys_in, bounds):

    polys_out = []
    poly_num = len(polys_in)

    # Crop polygons
    for i in range(0,poly_num):
        poly_now = polys_in[i].intersection(bounds)
        polys_out.append(poly_now)

    return polys_out


#MERGE OVERLAPPING POLYGONS
def unionPolygons(polys_in):

	polys_out = []
	polys_temp = polys_in
	exit_flag = False

	# Loop until no more unions are possible
	while (exit_flag == False):
 		
 		# Reset loop variables
		overlaps = []
		polys_new = []
		poly_num = len(polys_temp)
		unioned = [0]*poly_num
		
		# Find overlapping polygons
		for i in range(0,poly_num):
			overlap_i = [False]*poly_num
			for j in range(0,poly_num):
				if (polys_temp[i].intersects(polys_temp[j]) == True) and (i != j):
					overlap_i[j] = True
				else:
					pass

			overlaps.append(overlap_i)

		# Using Numpy, take the upper diagonal of the matrix to remove duplicate overlaps
		overlaps_np = np.array(overlaps)
		overlaps_upper = np.triu(overlaps_np, k=1)

		# Join overlapping pairs of polygons together (once per "i"), and record the results
		for i in range(0,poly_num):
			for j in range(0,poly_num):
				if (unioned[i] == 0) and (overlaps_upper[i][j] == True):
					polys_temp[i] = polys_temp[i].union(polys_temp[j])
					unioned[j] = 1 #polygons that have been absorbed and should no longer be kept
					
		# Create new polygon list
		for i in range(0,poly_num):
			if (unioned[i] == 1):
				pass
			else:
				polys_new.append(polys_temp[i])
				
		# Set exit flag and prepare output, when no more unions are possible
		overlaps_exist = np.any(overlaps_np)
		if (overlaps_exist == False):
			exit_flag = True
			for i in range(0,len(polys_new)):
				if (unioned[i] == 0):
					poly_now = polys_new[i]
					polys_out.append(poly_now)	
					
		# Move this loop's data into the temp variable for the next loop
		polys_temp = polys_new
					
	return polys_out


#CREATE CONVEX POLYGON FROM CONCAVE POLYGONS
def concaveToConvex(polys_in):
	
	polys_out = []
	poly_num = len(polys_in)
	
	# Create convex hull from Shapely multipoint object
	for i in range(0,poly_num):
		poly_points = list(polys_in[i].exterior.coords)
		poly_multipoints = MultiPoint(poly_points)
		poly_now = poly_multipoints.convex_hull
		polys_out.append(poly_now)
	return polys_out
	

#SIMPLIFY POLYGONS
def simplifyPolygons(polys_in):
	
	polys_out = []
	poly_num = len(polys_in)
	simp_factor = 0.05

	# Simplify the polygons with the "simp_factor"
	for i in range(0,poly_num):
		poly_in_points = list(polys_in[i].exterior.coords)# print(len(poly_in_points))
		if (len(poly_in_points) >= 64): 
			poly_now = polys_in[i].simplify(simp_factor)
			polys_out.append(poly_now)
			
			# Verify the simplified number of points are valid
			poly_now_points = list(poly_now.exterior.coords)
			verts_num = (len(poly_now_points))
			if (verts_num < 64) and ((verts_num > 2)):
				pass
			else:
				print("\nAt least one polygon has an invalid number of points.")
				print("Pick a different simplification factor and try again.\n")
				exit()
		else:
			polys_out.append(polys_in[i])
		
	return polys_out
	
	
#CHECK FINAL POLYGONS
def checkPolygons(polys_in):
	
	poly_num = len(polys_in)
	poly_check = []
	
	for i in range(0,poly_num):
		for j in range(0,poly_num):
			if (i == j):
				pass
			else:
				poly_check.append(polys_in[i].intersects(polys_in[j]))
			
	no_true_values = not any(poly_check)
	
	if (no_true_values == True):
		return 1
	else:
		return 0
		
	
#PRINT POLYGONS
def printPolygons(polys_in):
	
	poly_outlines = []
	poly_num = len(polys_in)
	
	#prepare each polygon for printing
	for i in range(0,poly_num):
		poly_outline = list(polys_in[i].exterior.coords)
		poly_outlines = np.array(poly_outline)
		plt.plot(poly_outlines[:,1], poly_outlines[:,0])


#MAIN LOOP
def main():
	
	# Create image bounds
	img_bounds = createImageBounds()
    
	# Get the polygons from the heightmap
	polys_raw = pngToPolygons()
	
	# Filter out fully contained polygons
	polys_extern_only = eliminateInnerRings(polys_raw)
	
	# Create buffer around polygons
	polys_buff = bufferPolygons(polys_extern_only)
	
	# Crop buffered polygons back into the image frame
	polys_crop = cropPolygons(polys_buff, img_bounds)
	
	# Merge overlapping polygons
	polys_union = unionPolygons(polys_crop)
	
	# Create convex polygon for each polygon
	polys_convex = concaveToConvex(polys_union)
	
	# Simplify the polygons to less than 64 verticies each
	polys_simple = simplifyPolygons(polys_convex)
	# Check Results
	chk = checkPolygons(polys_simple)
	
	if (chk == 1):
		printPolygons(polys_simple)
		printPolygons(polys_extern_only)
		printPolygons([img_bounds])
		plt.show()	
	elif (chk == 0):
		print("Something is invalid; you'll probably need to try a different combination of functions or different values.\n")
	else:
		print("Something went really wrong.\n")

#RUN PROGRAM		
main()
	
	
#EOF
