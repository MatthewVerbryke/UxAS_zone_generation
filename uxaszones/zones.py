# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import numpy as np


class Zone:
    """Common object class for all zones
    
    #----Parameters----#
    ID --           unique identification number of the zone (int)
    ztype --        characteristic type and permissablity:
    
                        Phys  Reg   Thr   Comm
                        [int , int , int , int ]
                        
                        where
                        0 - Entry (no characteristic)
                        1 - Entry (characteristic)
                        2 - No Entry
                        
    bound --        list of boundary points (list of float 2-tuples)  
    alt --          zone altitude (float)

    """
    
    def __init__(self, ID, ztype, uav_ID, bound_points):
        
        # Input parameters
        self.ID = ID
        self.ztype = ztype
        self.bound = bound_points
        
        # UAV inputs
        uav_data = np.load('uav.npy')
        [row] = np.where(uav_data == uav_ID)[0]

        self.alt = uav_data[row, 1]
        uav_speed = uav_data[row, 2]
        uav_bank_angle = uav_data[row, 3]

        # Other
        self.max_verts = 64
    
