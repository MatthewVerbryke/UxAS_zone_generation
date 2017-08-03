#!/bin/bash -e
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.

# Get scenario name
echo "what is the name of your scenario?:"
read SCENARIO_NAME
echo " "

# Get static paths
RELATIVE_PATH="`dirname \"$0\"`"
ABSOLUTE_PATH="`( cd \"$RELATIVE_PATH\" && pwd )`"
SCENARIO_PATH="/home/$USER/UxAS_pulls/OpenUxAS/examples/$SCENARIO_NAME/MessagesToSend"

# Get PNG name
echo "What is the name of your heightmap image? (the image name without .png):"
read YOURIMAGENAME

# Create output storage folder
cd ~/Documents/uxas_zones/

if [ -d "$YOURIMAGENAME" ]
then
        echo "Error: Directory '$YOURIMAGENAME' already exists."
        exit
else
        mkdir $YOURIMAGENAME
fi

# Create copy of heightmap image
STORE_PATH="/home/$USER/Documents/uxas_zones/$YOURIMAGENAME"
cp ~/Pictures/heightmaps/$YOURIMAGENAME/$YOURIMAGENAME.png $STORE_PATH
cp ~/Pictures/heightmaps/$YOURIMAGENAME/data.csv $STORE_PATH

# Generate exclusion areas for each UAV
cd $ABSOLUTE_PATH/uxaszones
python exclusion_gen.py "$SCENARIO_PATH" "$STORE_PATH" "$YOURIMAGENAME"

# Add border to images
python border_create.py "$SCENARIO_PATH" "$STORE_PATH"

# Generate polygons from raster images
python png_to_polygons.py "$SCENARIO_PATH" "$STORE_PATH" "$YOURIMAGENAME" "$ABSOLUTE_PATH"


