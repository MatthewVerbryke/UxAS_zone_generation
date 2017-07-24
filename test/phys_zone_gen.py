#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/ (FILL IN THIS)
# Additional copyright may be held by others, as reflected in the commit history.

#ASSUMES UAV ALTITUDES ARE DESCRETIZED!

import PIL
import string
import sys
from PIL import Image

#Find heightmap image
print(' ')
img_name_input = raw_input('What is the name of the heightmap image?:\n')
img_name = img_name_input + '.png'
print(' ')

# Input maximum and minimum heights found in the heightmap image
max_height = float(input('Maximum height in the heightmap area:\n'))
print(' ') 
min_height = float(input('Minimum height in the heightmap area:\n'))
print(' ')
height_range = max_height - min_height

# Check input validity
if (max_height < min_height):

    print ('Error: Maximum height is less than minimum height')
    exit()

# Determine conversion factor between height(in meters) and specific bit value in image (0-255)
scale_size = 255./height_range

# Input number of UAVs in scenario
	#in the future, read number of 'AirVehicleConfiguration_V#.xml' files located in the OpenUxAS scenario
uav_tot = input('Number of UAVs:\n')
print (' ')

# Input altitudes for each UAV, with checking
	##in the future, read from 'AirVehicleState_V#.xml' files located in the OpenUxAS scenario
uav_data = [['ground', 0.0]]


for i in range(1,uav_tot +1):

    valid_in = False
    while (valid_in == False):
	alt_in = float(input('UAV #{} altitude:\n'.format(i)))
	print(' ')
	if (alt_in > 0):
	    uav_data.append(['{}'.format(i), alt_in])
	    valid_in = True
	else:
            print('Invalid: try again\n')
	    print(' ')

# Add in maximum height from heightmap
uav_data.append(['max height', height_range])

# Sort altitudes min --> max
sorted_uav_data = sorted(uav_data, key=lambda uav: uav[1])

# Add scaled altitudes
for i in range(0,uav_tot+2):

    sorted_uav_data[i].append(int(scale_size*sorted_uav_data[i][1]))

# Open image
img = Image.open(img_name)

# Find image size
img_size, height = img.size

# Get data from heightmap image and create new list for modified data
imglist = list(img.getdata())
imglist_all = [0]*img_size*img_size

# Determine and print-out exclusion zones for each UAV
for i in range(0, uav_tot+2):

    if (sorted_uav_data[i][0] == 'ground') or (sorted_uav_data[i][0] == 'max height'):
	pass
    else:
        imglist_out = [0]*img_size*img_size
        for j in range(img_size):
            for k in range(img_size):
                if (sorted_uav_data[i][2] >= 255):
	            pass
                elif (imglist[j*img_size + k] >= sorted_uav_data[i][2]):
                    imglist_all[j*img_size + k] = sorted_uav_data[i][2]
		    imglist_out[j*img_size + k] = 255

        img.putdata(imglist_out)
        uav_num = sorted_uav_data[i][0]
        img.save('uav_{}_pzones.png'.format(uav_num))

# Create image and save it for all UAVs
img.putdata(imglist_all)
img.save('{}_all_zones.png'.format(img_name))

#Close image
img.close()

#EOF
