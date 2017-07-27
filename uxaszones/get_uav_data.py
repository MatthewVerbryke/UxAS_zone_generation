# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/ (FILL IN THIS)
# Additional copyright may be held by others, as reflected in the commit history.

# NOTE: This is not an executable file. It is only called by other scripts.


import glob
import lxml.etree as ET
import os
import sys


# FIND AND RETURN ALL'AirVehicleConfiguration' AND 'AirVehicleState' FILES IN THE UXAS EXAMPLES FOLDER
def findXMLs(scenario_path):

    # Change directory to examples folder
    os.chdir(scenario_path)
        
    # Get all 'AirVehicleConfiguration' and 'AirVehicleState' files
    vehc_configs = glob.glob('AirVehicleConfiguration_V*')
    vehc_state = glob.glob('AirVehicleState_V*')
        
    return [vehc_configs, vehc_state]


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
		

# XML PARSER		
def XMLParse(in_file, collect_type):
	
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

		
# PARSE THROUGH ALL XML FILES OF THE TWO TYPES AND RETURN THE RELEVANT DATA FROM THEM
def parseAllFiles(scenario_path):
	
	# Get cwd
	setdir = os.getcwd()
	
	# Find config and state files
	vehc_files = findXMLs(scenario_path)
	
	# Check to make sure that their are equal numbers of config and state files
	if (len(vehc_files[0]) != len(vehc_files[1])):
		print("Error: number of configuration and state files do not match.")
		exit()
	else:
		vehc_num = len(vehc_files[0])
		
	# Get and store data from xml files
	uav_data = [vehc_num]
	
	for i in range(0,vehc_num):
		
		# Parse through config files
		config_file = vehc_files[0][i]
		config_collector = XMLParse(config_file, 0)
		
		# Parse through state files
		state_file = vehc_files[1][i]
		state_collector = XMLParse(state_file, 1)
		
		# Set data to holding variables
		ID_data = config_collector.ID
		airspeed_data = config_collector.airspeed
		bank_angle_data = config_collector.bank_angle
		alt_data = state_collector.alt
		
		# Append data to list of lists, creating a sub list for each UAV
		uav_data.append([ID_data[0], alt_data[0], airspeed_data[0], bank_angle_data[0]])
		
		# Reset collectors for next loop
		state_collector = None
		config_collector = None
		
	# Switch back to the cwd
	os.chdir(setdir)	
		
	return uav_data


#EOF
