#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/uxas_zone_generation
# Additional copyright may be held by others, as reflected in the commit history.


import glob
import os
import sys

import lxml.etree as ET
import numpy as np


# XML COLLECTOR FOR THE 'AirVehicleConfiguration' FILES
class configXMLCollector(object):
        
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
            
# XML COLLECTOR FOR THE 'AirVehicleState' FILES
class stateXMLCollector(object):
        
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
            
class RetrieveUAVData():
    
    def __init__(self):

        # Get cwd
        self.setdir = os.getcwd()

        # Command line arguments
        self.scenario_path = sys.argv[1]
        self.store_path = sys.argv[2]
        
        # Run program
        self.main()
        
    # FIND AND RETURN ALL'AirVehicleConfiguration' AND 'AirVehicleState' FILES IN THE UXAS EXAMPLES FOLDER
    def find_xmls(self):

        # Switch to examples directory
        os.chdir(self.scenario_path)
            
        # Get all 'AirVehicleConfiguration' and 'AirVehicleState' files
        vehc_configs = glob.glob("AirVehicleConfiguration_V*")
        vehc_states = glob.glob("AirVehicleState_V*")
        
        # Check to make sure that their are equal numbers of config and state files
        if (len(vehc_configs) != len(vehc_states)):
            print("Error: number of configuration and state files do not match.")
            exit()            
        
        return vehc_configs, vehc_states
        
    # XML PARSER		
    def parse_xml(self, in_file, collect_type):
        
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
        
    # RETRIEVE UAV DATA
    def return_uav_data(self, vehc_config, vehc_state):
        
        # Parse through config files
        config_file = vehc_config
        config_collector = self.parse_xml(config_file, 0)
                
        # Parse through state files
        state_file = vehc_state
        state_collector = self.parse_xml(state_file, 1)
                
        # Set data to holding variables
        ID_data = config_collector.ID
        airspeed_data = config_collector.airspeed
        bank_angle_data = config_collector.bank_angle
        alt_data = state_collector.alt
        
        # Append data to list of lists, creating a sub list for each UAV
        uav_data = np.array([int(ID_data[0]), float(alt_data[0]), float(airspeed_data[0]), float(bank_angle_data[0])])

        return uav_data
        
    # MAIN LOOP
    def main(self):
        
        try:        
        
            # Find config and state files
            vehc_configs, vehc_states = self.find_xmls()
            
            # Determine number of UAVs
            vehc_num = len(vehc_configs)
            
            # Preallocate output array
            out_array = np.zeros((vehc_num, 4))
            
            # Retrieve and store data for each uav
            for i in range(0,vehc_num):
                out_array[i] = self.return_uav_data(vehc_configs[i], vehc_states[i])
            
            # Switch to store directory
            os.chdir(self.store_path)
            
            # Output data to npy file
            np.save("uav", out_array)
            
        finally:
            
            # Switch back to the cwd
            os.chdir(self.setdir)


if __name__ == "__main__":
    RetrieveUAVData()

#EOF
