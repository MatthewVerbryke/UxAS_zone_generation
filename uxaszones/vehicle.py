# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import glob
import os
import sys

import lxml.etree as ET
import numpy as np

from uav import UAV


class configXMLCollector(object):
    """A collector object for UxAS 'AirVehicleConfiguration' XML files"""
        
    # Initialize data lists
    def __init__(self):
        self.ID = []
        self.alt = []
        self.airspeed = []
        self.bank_angle = []
            
        self.cur_data = None

    # Start
    def start(self, tag, attrib):
        pass

    # End (append current data to relevant data list)
    def end(self, tag):
        if (tag == "ID"):
            self.ID.append(str(self.cur_data))
        elif (tag == "Airspeed"):
            self.airspeed.append(float(self.cur_data))
        elif (tag == "MaxBankAngle"):
            self.bank_angle.append(float(self.cur_data))
                
        self.cur_data = None
        
    # Get current data
    def data(self, data):
        self.cur_data = data
            
    # No comments
    def comment(self, text):
        pass
        
    # Close object	
    def close(self):
        return

class stateXMLCollector(object):
    """A collector object for UxAS 'AirVehicleState' XML files."""
        
    # Initialize data lists
    def __init__(self):
        self.ID = []
        self.alt = []
        self.airspeed = []
        self.bank_angle = []
            
        self.cur_data = None

    # Start
    def start(self, tag, attrib):
        pass
        
    # End (append current data to relevant data list)
    def end(self, tag):
        if (tag == "Altitude"):
            self.alt.append(float(self.cur_data))
            
        self.cur_data = None
    
    # Get current data
    def data(self, data):
        self.cur_data = data
            
    # No comments
    def comment(self, text):
        pass
            
    # Close object
    def close(self):
        return

def find_xmls():
    """Find and return all 'AirVehicleConfiguration' and 'AirVehicleState' files in the specified scenario."""
            
    # Get all 'AirVehicleConfiguration' and 'AirVehicleState' files
    vehc_configs = glob.glob("AirVehicleConfiguration_V*")
    vehc_states = glob.glob("AirVehicleState_V*")
        
    # Check to make sure that their are equal numbers of config and state files
    if (len(vehc_configs) != len(vehc_states)):
        print("Error: number of configuration and state files do not match.")
        exit()            
    
    return vehc_configs, vehc_states
            
def parse_xml(in_file, collect_type):
    """Parse the specified XML file."""
        
    # Get file contents
    contents = open(in_file, 'r').read()
        
    # Logic for choosing file type collector
    if (collect_type == 0):
        collector = configXMLCollector()
    elif (collect_type == 1):
        collector = stateXMLCollector()
            
    # Run parser to target collector	
    parser = ET.XMLParser(target= collector)
        
    # Set result
    result = ET.XML(contents, parser)
        
    return collector         
            
def retrieve_uav_data(config_file, state_file):
    """Retrieve data for a UAV from the corresponding configutation and state data files."""
        
    # Parse through config file
    config_collector = parse_xml(config_file, 0)
                
    # Parse through state file
    state_collector = parse_xml(state_file, 1)
                
    # Set data to holding variables
    [ID_data] = config_collector.ID
    [airspeed_data] = config_collector.airspeed
    [bank_angle_data] = config_collector.bank_angle
    [alt_data] = state_collector.alt

    return str(ID_data), float(airspeed_data), float(bank_angle_data), float(alt_data)
            
def generate_scenario_uavs():
    """Create a list containing a UAV object instance for each UAV in the scenario"""
    
    # Find config and state files
    vehc_configs, vehc_states = find_xmls()
        
    # Determine number of UAVs
    vehc_num = len(vehc_configs)
        
    uavs = [None]*vehc_num
        
    for i in range(0,vehc_num):
            
        # Retrieve data for each uav
        ID, airspeed, bank_angle, alt = retrieve_uav_data(vehc_configs[i], vehc_states[i])
            
        # Create UAV instance for each UAV and store in uavs list
        uavs[i] = UAV(ID, airspeed, alt, bank_angle)
            
    return uavs
 
#EOF
