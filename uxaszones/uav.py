# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


from math import tan, radians


class UAV(object):
    """Common object class for UAVs
    
    Attributes:
        ID --           unique name for the UAV (string)
        speed --        nominal airspeed of the UAV (float)
        alt --          altitude of the UAV (float)
        bank_angle --   maximum banking angle of the UAV (float)
        turn_radius --  minimum turning radius of the UAV (float)
        obstruct --     filename containing the physical-obstruction map for the UAV (string)
        restrict --     filename containing the regulatory-restriction map (NOT IMPLEMENTED YET)
        threat --       filename containing the threat-level map (NOT IMPLEMENTED YET)
        comms --        filename containing the threat-level map (NOT IMPLEMENTED YET)
        zone_list --    list of IDs for all zones relevant to the UAV (list of strings)
    
    """
    
    def __init__(self, ID, airspeed, altitude, max_bank_angle):
        """Create instance of a UAV object"""
        
        # Input attirbutes
        self.ID = ID
        self.speed = airspeed
        self.alt = altitude
        self.bank_angle = max_bank_angle
        
        # Determine minimum turning radius
        self.turn_radius = (self.speed**2)/(9.81*tan(radians(self.bank_angle)))
        
        # Construct mapnames
        self.obstruct = ID + '_obstructions.png'
        
        # Initialize zone list
        self.zone_list = []
        
    def display_info(self):
        """ Output UAV information to the terminal."""
        
        print("UAV {self.ID}\n"
              "\n"
              "  airspeed:               {self.speed} m/s\n"
              "  altitude:               {self.alt} m\n"
              "  maximum bank angle:     {self.bank_angle} deg\n"
              "  minimum turning radius: {self.turn_radius} m\n"
              "\n".format(self=self))

#EOF
