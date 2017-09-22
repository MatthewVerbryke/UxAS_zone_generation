# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import numpy as np


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
                        
        bound --        list of boundary points (list of float 2-tuples)  
        alt_range --    zone altitude range, min to max ([float, float])
        buff --         required buffer size for keep-out zones

    """
    
    zone_count = 0
    max_verts = 64
    
    def __init__(self, uav, uav_alt, uav_buffer, ztype, bound_points, increment):
        
        # Increment count if increment == True
        if increment:
            Zone.zone_count += 1
        
        # Input Parameters
        self.uav = uav
        self.buff = uav_buffer
        self.ztype = ztype
        self.bound = bound_points
        
        # Determine ID
        self.ID = uav + str(zone_count)
        
        # Determine altitude range
        self.alt_range = [uav_alt, uav_alt + 30.0] #<-- the value 30.0 is arbitrary for now
        
        
#EOF
