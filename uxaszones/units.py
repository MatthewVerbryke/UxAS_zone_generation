# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


from math import pi, sin, cos, radians, sqrt


def pixel_to_geodetic(lat_low, lon_low, zone_bound, pix_to_geo):
    """Convert a boundary point list from 'pixel' coordinates to geodetic coordinates."""
    
    # Convert bound polygon to point list
    bound_point_list = list(zone_bound.exterior.coords)
    
    point_total = len(bound_point_list)
    geo_point_list = [None]*point_total
    
    # Convert each point
    for i in range(0,point_total):
        lat = bound_point[i][1]*pix_to_geo + lat_low
        lon = bound_point[j][0]*pix_to_geo + lon_low
        geo_point_list[i] = (lat, lon)
        
    # Place new list into Shapely polygon
    converted_bound = Polygon(geo_point_list)
    
    return converted_bound
    
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
    output = max(deg_per_meter) 
    # NOTE: this is done because this function is only used to determine
    #       the buffer in geodetic coordinates, and since only one buffer
    #       length can be used, the safest option is to pick the largest 
    #       buffer
    # TODO: see if there is a better way to do this
    
    return output


#EOF
