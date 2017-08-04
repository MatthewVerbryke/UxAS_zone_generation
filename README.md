# UxAS Zone Generator

## Summary

This repository contains a program that can be used to automatically generate zones, based on given heightmaps, geographic information, and vehicle data, for [AFRL-RQ](http://www.wpafb.af.mil/afrl/rq/)'s Unmanned Systems Autonomy Services (UXAS) architecture. The program will use the given inputs to determine the obstructions for each UAV (based on altitude), perform raster-to-vector conversion to generate polygons of these areas, and use polygon manipulation to create and output buffered polygonal zones in the appropriate format for UxAS to use.  Also provided as an output are images and figures that are intended to allow the user to confirm that the output is correct.

## Requirements

You need to install [OpenUxAS](https://github.com/afrl-rq/OpenUxAS) program on your system for this program to work. Follow the instructions presented on that page.

This program has the following python library dependencies:
  * [Pillow](http://pillow.readthedocs.io/en/3.0.x/index.html)
  * [lxml](http://lxml.de/)
  * [gmplot](https://github.com/eli-s-goldberg/gmplot)
  * [scipy](https://scipy.org/index.html) stack
  * [shapely](https://pypi.python.org/pypi/Shapely)
  * [skimage](http://scikit-image.org/)
  * [utm](https://pypi.python.org/pypi/utm)
  
The system was designed and tested in Ubuntu 16.04 LTS

## Installation

Clone this repository into the `UXAS_pulls` directory on your system.

In your `home/$USER/Pictures` directory, create a new folder called `heightmaps`. In the `home/$USER/Documents`, create another folder called `uxas_zones`.

## Instructions

### Setup

To use this program for a new scenario, you will first need to create a new scenario directory in `OpenUxAS/examples` with an appropriate name. In order for this program to function, you need to create and fill out Air Vehicle Configuration and Air Vehicle State xml files for each uav in your scenario. Use the default UxAS examples as a guide to determine naming, formatting, and necessary directory locations for these files.

Next, you will need to get your heightmap image for the desired area, and the following data about this area: 
  * maximum and minimum terrain heights found in the area (in meters)
  * latitude and longitude of the northeast (top-right) corner of the heightmap
  * latitude and longitude of the southwest (bottom-left) corner of the heightmap
  * real-world side length of the heightmap (in meters)
  
![alt text](/doc/image_data.png "Required Image Data")

Finally, you will need to assemble these data inputs in the correct location for the program to locate. Within the `home/$user/Pictures/heightmaps/` directory, create a new folder with the same name you intend to give/gave to your heightmap image (i.e. if your image is `IMAGENAME.png`, the directory will be called `IMAGENAME`). Under this new directory, place your heightmap image and create a new file called `data.csv`. The contents of this file need to be in the following order:

![alt text](/doc/data_csv.png ".csv File Format")

You should now be ready to run the program

### Usage

To run the program, change directory into the `uxas_zone_generation` directory in `UxAS_pulls`, and run the main script:

```
./uxaszones.sh
```

The program will ask for two inputs: the name of the scenario and the name of the heightmap image. *_Ensure that these match up to the name of your scenario and heightmap image name, respectively_*; otherwise the program will throw an exception.

If you need to run the program for your scenario again for whatever reason, you will need to delete the storage file produced by the program in the `home/$USER/Documents/uxas_zones` directory. The program tries to guard against overriding an already existing scenario output, and will therefore exit if it detects that an storage file with the provided name already exists. 

### Outputs

The program creates outputs in two file locations. The final zones are output directly into the UxAS scenario file location in the correct format. To provide more human-understandable output, the program also outputs data to the storage file mentioned earlier, in the `home/$USER/Documents/uxas_zones` directory. The outputs here include:

  * A rescaled copy of the original heightmap image
  * A copy of the original .csv data file
  * Map of terrain that is at the UAV's altitude (and therefore somewhere the UAV cannot go) for each UAV (`UAV_ID`_obstructions.png)
  * All of these obstruction maps shown together (all_obstructions.png)
  * PyPlot figures of the generated polygonal zones compared to the original terrain obsructions (`UAV_ID`_zones.pdf)
  * PyPlot showing all zones outputted to UxAS together (all_zones.pdf)
  * An .html for each UAV that shows the final zones in google maps(`UAV_ID`_zones.html)
  
![alt text](/doc/outputs.png "Program Outputs")
  
## Notes

  * The polygon maniputlation methods contained in `png_to_polygons.py` have been written so that it should be somewhat easy to rearrange the order in which they are executed, if so desired.
  * It has not been tested yet, but the method used to translate between local coordinates (meters from a predefined fixed location) and geodetic coordinates (latitude, longitude) may break down the closer your area of operations is to the Earth's poles.
  * Buffer distance is based on the UAV's maximum bank angle and nominal speed
  * Assumptions contained in separate documents (coming soon)

## Future Work

  * More testing
  * Automate (to some degree) the collection of heightmap data
  * Extension beyond physical keep-in-zones to other types (keep-in? regualatory airspace?)
  * Better handling of 'over-detailed' zones (polygons with 64 or more vertices, as UxAS can't handle them)
  * Splitting off methods contained in `png_to_polygons.py` into their own files for better reusability.
  * Allow for choosing concave zones if your path planner can handle it.

## License

This program is licensed under the BSD 3-clause license, as presented in the LICENSE file

Program is Copyright (c) University of Cincinnati
