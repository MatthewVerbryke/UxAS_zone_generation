# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.

import os
import string
import sys
from sys import argv


def uxas_zone_output(poly_in_list, scenario_path, absolute_path, alt_data, zone_count):
    try:
        
        # Get cwd
        setdir = os.getcwd()
        
        # Get number of polygons for the UAV
        poly_len = len(poly_in_list)
        
        # Change to template directory
        os.chdir(absolute_path + '/uxaszones/templates')
        
        # Read in 'keep_out_zone.txt'
        template = open('keep_out_zone.txt', 'r')
        tempholdtext = template.read()
        template.close()
        file_temp = str(tempholdtext)
        
        # Read in 'poly_point.txt'
        template2 = open('poly_point.txt', 'r')
        tempholdtext2 = template2.read()
        template2.close()
        file_points = str(tempholdtext2)
        point_store = ""
        
        # Fill in point information for each polygon
        for i in range(0,poly_len):
            point_data = str(file_points);
            point_data = point_data.replace( "$LATITUDE$", str(poly_in_list[i][0]))
            point_data = point_data.replace( "$LONGITUDE$", str(poly_in_list[i][1]))
            point_store = point_store + str(point_data)
            
        # Fill in zone infromation
        file_info = str(file_temp)
        file_info = file_info.replace( "$ZONETYPE$", 'Physical')
        file_info = file_info.replace( "$ZONENUMBER$", str(zone_count))
        file_info = file_info.replace( "$ALTMIN$", str(alt_data[0]))
        file_info = file_info.replace( "$ALTMAX$", str(alt_data[1]))
        file_info = file_info.replace( "$POLYPOINTS$", str(point_store))
        file_content = str(file_info)
        
        # Change to scenario directory
        os.chdir(scenario_path)
        
        file_name = 'KeepOutZone_{}.xml'.format(zone_count)
        
        # Write all data into the file
        with open(file_name, 'w+') as f:
            f.write(file_content)
            f.close()
            
        return (zone_count + 1)
            
    finally:
        
        # Switch back to cwd
        os.chdir(setdir)
            
#EOF
