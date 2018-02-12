# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


from math import pi, sin, cos, radians, sqrt

from shapely.geometry import Polygon


def pixel_to_geodetic(polys_in, lat_low, lon_low):
    """Convert a boundary point list from 'pixel' coordinates to geodetic coordinates.
    TODO: Something is off on the scale part, figure it out"""
    
    # In SRTM3 data, one pixel is 3 archseconds
    # NOTE: if physical source changes, this conversion factor no longer works
    pix_to_geo = 1.0/1201.0
    
    poly_num = len(polys_in)
    polys_out = [None]*poly_num
    
    for i in range(0,poly_num):
        
        poly_outline = list(polys_in[i].exterior.coords)
        point_total = len(poly_outline)
        geo_point_list = [None]*point_total
        
        # Convert each point
        for j in range(0,point_total):
            
            lat = poly_outline[j][1]*pix_to_geo + lat_low
            lon = poly_outline[j][0]*pix_to_geo + lon_low
            geo_point_list[j] = (lat, lon)
            
        # Place new list into Shapely polygon
        polys_out[i] = Polygon(geo_point_list)
        
    return polys_out
    
def local_to_geodetic(local_len, lat_low, lat_high):
    """For the AO location, convert meters to geodetic coordinates."""
    
    #NOTE: the number of meters in a geodetic coordinate depends on the 
    #      location in the world. Specifically, the length of 1 degree of
    #      latitude and longitude are dependent on the latitude.
    
    lats = (lat_low, lat_high)
    
    # Constants (for WGS84 ellipsoid)
    a = 6378137.0 #equatorial radius(m)
    e2 = 0.00669437999014 #eccentricity squared
    
    lat_len = [None, None]
    lon_len = [None, None]
    
    for i in range(0,2):
        
        # Convert from degrees to radians
        latr = radians(lats[i])

        # Length of 1 degree of latitude (meters) as a function of latitude
        lat_len[i] = 111132.954 - 559.822*cos(2*latr) + 1.175*cos(4*latr)
        
        # Length of 1 degree of longitude (meters) as a function of latitude
        lon_len[i] = (pi*a*cos(latr))/(180*sqrt(1.0-e2*(sin(latr))**2))
        
    # Compute number of degrees per meter for each scale
    deg_per_meter = (1./lat_len[1], 1./lat_len[0], 1./lon_len[1], 1./lon_len[0])
    
    # Pick the largest value 
    output = max(deg_per_meter)*local_len
    # NOTE: this is done because this function is only used to determine
    #       the buffer in geodetic coordinates, and since only one buffer
    #       length can be used, the safest option is to pick the largest 
    #       buffer
    # TODO: see if there is a better way to do this
    return output


#EOF
