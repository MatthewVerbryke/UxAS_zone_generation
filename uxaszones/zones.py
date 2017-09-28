# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


#import numpy as np
from shapely.geometry import Polygon, MultiPoint


class Zone(object):
    """Common object class for all zones
    
    Attributes:
        ID --           unique ID of the zone (string)
        uav --          ID of the relevant UAV(string)
        ztype --        characteristic type and permissablity:
    
                        Phys  Reg   Thr   Comm
                        [int , int , int , int]
                        
                        where
                        0 - Entry (no characteristic)
                        1 - Entry (characteristic)
                        2 - No Entry
                        
        bound --        zone boundary points (Shapely 'Polygon' object)  
        alt_range --    zone altitude range, min to max ([float, float])

    """
    
    zone_count = 0
    max_verts = 64
    
    def __init__(self, uav, uav_alt, uav_buffer, ztype, bound_points, increment):
        """Create instance of a zone object."""
        
        # Increment count if increment == True
        if increment:
            Zone.zone_count += 1
        
        # Input Parameters
        self.uav = uav
        self.buff = uav_buffer
        self.ztype = ztype
        self.bound = bound_points
        
        # Determine ID
        self.ID = uav + '_' + str(Zone.zone_count)
        
        # Determine altitude range
        self.alt_range = [uav_alt, uav_alt + 30.0] #<--NOTE: the value 30.0 is arbitrary for now
        
    def buffer(self, uav_buffer):
        """Add a buffer to the zone, equal to the relevant UAV's minimum turn radius using the Shapely buffer method."""

        # Add buffer to the zone
        buffed_bound = self.bound.buffer(uav_buffer)
        
        # Update the bound to the buffered boundary
        self.bound = buffed_bound
                
    def crop(self, ao_bounds):
        """'Crop' the zone to the boundaries of the AO using the Shapely intersection method."""

        # Crop away boundary points outside the AO
        cropped_bound = self.bound.intersection(ao_bounds)
        
        # Update the bound to the cropped boundary
        self.bound = cropped_bound
        
    def make_convex(self):
        """Create a convex zone around the current zone using the Shapely convex_hull method"""
        
        # Put boundary points into a Shapely MultiPoint Object
        bound_points_list = list(self.bound.exterior.coords)
        bound_multipoint = MultiPoint(bound_points_list)
        
        # Create convex-hull around all the bound points
        convex_bound = bound_multipoint.convex_hull
        
        # Update the bound to the convex boundary
        self.bound = convex_bound
        
    def reduce_vertices(self):
        """Reduce the number of boundary points in the zone using the Shapely simplify method."""
        
        # Simplification factor
        simple_factor = 0.0
        
        # Put boundary points into a list
        bound_point_list = list(self.bound.exterior.coords)
        
        # while there are more than 64 points in the boundary point list
        while (len(boundary_point_list) >= Zone.max_verts):
            
            # Increment simplification factor
            simple_factor += 0.01
            
            # Simplify the boundary points using the new simplification factor
            simple_bound = self.bound.simplify(simple_factor)
            
            # Put simplified boundary points into a list
            bound_point_list = list(simp_bound.exterior.coords)
        
        # Update the bound to the simple boundary
        self.bound = simple_bound
            
    def display_info(self):
        """Output zone information to the terminal."""
        
        zoutput = [None]*4
        
        # Determine characteristics output
        for i in range(0,4):
            if (self.ztype[i] == 0):
                zoutput[i] = "None"
            elif (self.ztype[i] == 1):
                zoutput[i] = "Permissive"
            else:
                zoutput[i] = "Restrictive"
                
        # Find if UAVs are permitted to enter the zone
        if 2 in self.ztype:
            permit = "No"
        else:
            permit = "Yes"
        
        # Print information
        print("ZONE {self.ID}\n"
              "\n"
              "  altitude range:  {self.alt_range[0]}m to {self.alt_range[1]}m\n"
              "  characteristics:".format(self=self))
        print("      physical:      {z[0]}\n"
              "      regulatory:    {z[1]}\n"
              "      threat:        {z[2]}\n"
              "      communication: {z[3]}".format(z=zoutput))
        print("  UAVs permitted to enter: {permit}"
              "\n".format(permit=permit))
        
        
#EOF
