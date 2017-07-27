#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/ (FILL IN THIS)
# Additional copyright may be held by others, as reflected in the commit history.


from get_uav_data import parseAllFiles
from math import tan, radians
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from PIL import Image
from read_csv import readCSVInput
from scipy import misc
from shapely.geometry import Polygon, MultiPoint
from skimage import measure
import sys



class pngToPolygons():
    
    def __init__(self):
        
        # Get cwd
        self.setdir = os.getcwd()
        
        # Command line arguments
        self.scenario_path = sys.argv[1]
        self.img_path = sys.argv[2]
        img_name = sys.argv[3] + '.png'
        
        # Get relevant UAV data from UxAS scenario files
        uxas_data = parseAllFiles(self.scenario_path)
        
        # Set number of UAVs
        self.uav_tot = uxas_data[0]
        
        # Get image actual side length        
        img_len = readCSVInput(self.img_path, 'side_length')
        
        # Get image size
        os.chdir(self.img_path)
        
        img = Image.open(img_name)
        self.img_size, height = img.size
        img.close     
           
        gravity = 9.81 #m/s^2
        self.buff_dist = [0]*self.uav_tot
        self.ID = [0]*self.uav_tot
        
        # Determine UAV turn radii from scenario data
        for i in range(0,self.uav_tot):
            speed = uxas_data[i+1][2]
            bank_angle = radians(uxas_data[i+1][3])
            turn_rad = (speed ** 2)/(gravity * tan(bank_angle))
                        
            # Determine buffer distances
            self.buff_dist[i] = turn_rad * float(self.img_size)/float(img_len)
            
            # Get UAV IDs
            self.ID[i] = uxas_data[i+1][0]
        
        # Maximum number of vertices per polygon allowed
        self.verts_max = 64
    
        # Run main program
        self.main()
 
 
 
    #CREATE POLYGONS FROM HEIGHTMAP IMAGE CONTOURS
    def polygonsFromPNGs(self, i):

        # Get current UAV ID
        current_uav = self.ID[i-1]

        # Open the heightmap image
        zone_map = misc.imread('{}_pzones.png'.format(current_uav))

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
    def createImageBounds(self):

        bound_size = float(self.img_size - 1)
        bound_corners = ([0.,0.], [0.,bound_size+2], [bound_size+2,bound_size+2], [bound_size+2,0.], [0.,0.])
        bound_np = np.array(bound_corners)
        bound = Polygon(bound_corners)

        return bound


    #ELIMINATE INTERNAL POLYGONS
    def eliminateInnerRings(self, polys_in):

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
    def bufferPolygons(self, polys_in, uav_number):

        polys_out = []
        poly_num = len(polys_in)

        # Buffer polygons
        for i in range(0,poly_num):
            poly_now = polys_in[i].buffer(self.buff_dist[uav_number])
            polys_out.append(poly_now)

        return polys_out


    #CROP POLYGONS INTO IMAGE FRAME
    def cropPolygons(self, polys_in, bounds):

        polys_out = []
        poly_num = len(polys_in)

        # Crop polygons
        for i in range(0,poly_num):
            poly_now = polys_in[i].intersection(bounds)
            polys_out.append(poly_now)

        return polys_out


    #MERGE OVERLAPPING POLYGONS
    def unionPolygons(self, polys_in):

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
                        #unioned[i] = 2 #polygons that have absorbed another polygon
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
    def concaveToConvex(self, polys_in):
        
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
    def simplifyPolygons(self, polys_in):
        
        polys_out = []
        poly_num = len(polys_in)
        simp_factor = 0.01

        # Simplify the polygons with the "simp_factor"
        for i in range(0,poly_num):
            poly_in_points = list(polys_in[i].exterior.coords)# print(len(poly_in_points))
            if (len(poly_in_points) >= self.verts_max): 
                poly_now = polys_in[i].simplify(simp_factor)
                polys_out.append(poly_now)
                
                # Verify the simplified number of points are valid
                poly_now_points = list(poly_now.exterior.coords)
                verts_num = (len(poly_now_points))
                if (verts_num < self.verts_max) and ((verts_num > 2)):
                    pass
                else:
                    print("\nAt least one polygon has an invalid number of points.")
                    print("Pick a different simplification factor and try again.\n")
                    exit()
            else:
                polys_out.append(polys_in[i])
            
        return polys_out
        
        
    #CHECK FINAL POLYGONS
    def checkPolygons(self, polys_in):
        
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
            return 0
        else:
            return 1
            
        
    #PRINT POLYGONS
    def printPolygons(self, polys_in):
        
        poly_outlines = []
        poly_num = len(polys_in)
        
        #prepare each polygon for printing
        for i in range(0,poly_num):
            poly_outline = list(polys_in[i].exterior.coords)
            poly_outlines = np.array(poly_outline)
            plt.plot(poly_outlines[:,1], poly_outlines[:,0])


    #MAIN LOOP
    def main(self):
        try:
            
            # Create image bounds
            img_bounds = self.createImageBounds()
            
            for i in range(0,self.uav_tot):
                
                # Get the polygons from the heightmap
                polys_raw = self.polygonsFromPNGs(i)
                   
                # Filter out fully contained polygons
                polys_extern_only = self.eliminateInnerRings(polys_raw)
                    
                # Create buffer around polygons
                polys_buff = self.bufferPolygons(polys_extern_only, i)
                    
                # Crop buffered polygons back into the image frame
                polys_in_loop = self.cropPolygons(polys_buff, img_bounds)
                
                chk = 1
                
                # This is meant to ensure that there are no overlapping and/or concave polygons left
                while (chk == 1):
                        
                    # Merge overlapping polygons
                    polys_union = self.unionPolygons(polys_in_loop)
                        
                    # Create convex polygon for each polygon
                    polys_convex = self.concaveToConvex(polys_union)
                        
                    # Simplify the polygons to less than 64 verticies each
                    polys_simple = self.simplifyPolygons(polys_convex)
                        
                    # Check results
                    chk = self.checkPolygons(polys_simple)
                    
                    # Prepare for next loop
                    polys_in_loop = polys_simple
                
                #self.printPolygons(polys_simple)
                self.printPolygons(polys_extern_only)
                self.printPolygons(polys_simple)
                self.printPolygons([img_bounds])
                plt.show()
                
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)


if __name__ == "__main__":
    pngToPolygons()
	
#EOF
