#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/ (FILL IN THIS)
# Additional copyright may be held by others, as reflected in the commit history.


import PIL
from PIL import Image



img = Image.open('uav_2_pzones.png')
img_size = img.size


img_border_size = []
for i in range(0,2):
    img_border_size.append(img_size[i] + 2)


img_border = Image.new('L', img_border_size)


img_border.paste(img, ((img_border_size[0] - img_size[0])/2, (img_border_size[1] - img_size[1])/2))


img_border.save('uav_2_pzones.png')
