#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 13:27:47 2018

@author: ejreidelbach

:DESCRIPTION:

:REQUIRES:
   
:TODO:
"""
 
#==============================================================================
# Package Import
#==============================================================================
import json
import os  
import pandas as pd

#==============================================================================
# Function Definitions / Reference Variable Declaration
#==============================================================================

#==============================================================================
# Working Code
#==============================================================================

# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/wow')

# ingest the US region realm data
with open('data/realms_us.json', 'r') as f:
    json_us = json.load(f)
    
# ingest the EU region realm data
with open('data/realms_eu.json', 'r') as f:
    json_eu = json.load(f)
    
# ingest the Connected Realm data
with open('data/realms_connected.json', 'r') as f:
    json_connected = json.load(f)    

# extract a complete realm list for both regions
list_realms_eu = ['eu-' + realm for realm in list(json_eu['realms'].keys())]
list_realms_us = ['us-' + realm for realm in list(json_us['realms'].keys())]

# simplify the connected realms such that there is only one listing per realm
list_connected_eu = []
list_connected_us = []

for key, value in json_connected.items():
    # handle EU realms
    if key.startswith('eu-'):
        temp_list = [key] + value
        temp_list.sort()
        if temp_list not in list_connected_eu:
            list_connected_eu.append(temp_list)
    # handle US realms    
    else:
        temp_list = [key] + value
        temp_list.sort()
        if temp_list not in list_connected_us:
            list_connected_us.append(temp_list)



# extract the demographics data
dict_demographics = {}
dict_demographics['us'] = json_us['demographics']
dict_demographics['eu'] = json_eu['demographics']
dict_demographis['us-pvp']