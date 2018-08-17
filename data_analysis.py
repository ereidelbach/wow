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
# Create lists containing the races within each faction
list_horde = ['Blood Elf', 'Orc', 'Tauren', 'Undead', 'Troll', 'Goblin',
              'PandarenH', 'Nightborne', 'Highmountain Tauren']
list_alliance = ['Human', 'Night Elf', 'Draenei', 'Worgen', 'Dwarf',
                 'Gnome', 'PandarenA', 'Lightforged Draenei', 'Void Elf']

# Create a list for classes that can fulfill the healing and tanking roles in groups
list_role_heal = ['Druid', 'Monk', 'Paladin', 'Priest', 'Shaman']
list_role_tank = ['Death Knight', 'Demon Hunter', 'Druid', 'Monk', 'Paladin', 'Warrior']

'''
    This function will read in all US realm data, call the transform_realm
    function to flatten it, and then collate the data into one large dictionary 
    
    Input:  name (string) - name of specific realm to read in
        Default value is ALL which dictates that all realms be read in
    Output: list_realms (list) - Flattened realm data, with new 
        variables, for all US realms
'''
def ingest_realm_data_us(name='ALL'):
    DIR = 'data/realms-us'

    # Handle ingest of single realm    
    if name != 'ALL':
        realm_file = [realm for realm in [file for file  in os.listdir(DIR) if os.path.isfile(
                os.path.join(DIR, file))] if name.lower() in realm].pop()
        with open(DIR + '/' + realm_file, 'r') as f:
            return(transform_realm(json.load(f)))

    # Handle ingest of all realms
    else:      
        list_realms = []
        for realm in [file for file  in os.listdir(DIR) if os.path.isfile(
                os.path.join(DIR, file))]:
            with open(DIR + '/' + realm, 'r') as f:
                dict_realm_raw = json.load(f)
            print('Starting realm: ' + dict_realm_raw['meta']['slug'])
            list_realms.append(transform_realm(dict_realm_raw))
        return list_realms

'''
    This function will take realm data as input, flatten it, and add data 
    for a character's faction and role types (i.e. healer and/or tank).
    
    Input:  realm_data (dictionary) - Original, nested realm data
    Output: dict_realm (dictionary) - Flattened realm data with new variables
'''
def transform_realm(realm_data):  
    # Create a new dictionary for storing flattened data
    dict_realm = {}
    
    # Handle `Gender`
    for gender_key, gender_value in realm_data['characters'].items():
        # Handle `Class`
        for class_key, class_value in gender_value.items():
            # Handle `Race`
            for race_key, race_value in class_value.items():
                # Handle `Level`
                # In some cases, the character level is the index in a list
                #   rather than a key in a dictionary -- we fix that
                if type(race_value) is list:
                    race_value = {race[0]:race[1] for race in list(enumerate(race_value))}
                for level_key, level_value in race_value.items():
                    # Handle `CharacterName` 
                    for char in level_value:
                        # Create dict entry for each character
                        dict_char = {
                                'gender':gender_key
                                ,'class':class_key
                                ,'race':race_key
                                ,'level':level_key
                                }
                        
                        # Insert the faction into each character's data
                        if dict_char['race'] in list_horde:
                            dict_char['faction'] = 'Horde'
                        elif dict_char['race'] in list_alliance:
                            dict_char['faction'] = 'Alliance'
                        else:
                            dict_char['faction'] = 'Unknown'
                        
                        # Insert the Healer role into each character's data
                        if dict_char['class'] in list_role_heal:
                            dict_char['healer'] = 1
                        else:
                            dict_char['healer'] = 0

                        # Insert the Tank role into each character's data
                        if dict_char['class'] in list_role_tank:
                            dict_char['tank'] = 1
                        else:
                            dict_char['tank'] = 0                        

                        # Insert the realm into the dictionary
                        dict_char['realm'] = realm_data['meta']['slug']
                        
                        # Insert the character into the realm dictionary
                        #   if there are no missing values
                        if (dict_char['gender'] == '' or
                            dict_char['class'] == '' or
                            dict_char['race'] == '' or
                            dict_char['level'] == ''):
                            pass
                        else:
                            dict_realm[char] = dict_char
    return dict_realm

#==============================================================================
# Working Code
#==============================================================================

#------------------------------------------------------------------------------
# Region Data Ingest
#------------------------------------------------------------------------------
# Set the project working directory
os.chdir(r'/home/ejreidelbach/projects/wow')

df = pd.DataFrame.from_dict(ingest_realm_data_us('Ysera'), orient='index')

# ingest the US region realm data
#with open('data/realms_us.json', 'r') as f:
#    json_us = json.load(f)
    
## ingest the EU region realm data
#with open('data/realms_eu.json', 'r') as f:
#    json_eu = json.load(f)
#    
## ingest the Connected Realm data
#with open('data/realms_connected.json', 'r') as f:
#    json_connected = json.load(f)    
#
#------------------------------------------------------------------------------
# Realm Names
#------------------------------------------------------------------------------
## extract a complete realm list for both regions
#list_realms_eu = ['eu-' + realm for realm in list(json_eu['realms'].keys())]
#list_realms_us = ['us-' + realm for realm in list(json_us['realms'].keys())]
#
## simplify the connected realms such that there is only one listing per realm
#list_connected_eu = []
#list_connected_us = []
#
#for key, value in json_connected.items():
#    # handle EU realms
#    if key.startswith('eu-'):
#        temp_list = [key] + value
#        temp_list.sort()
#        if temp_list not in list_connected_eu:
#            list_connected_eu.append(temp_list)
#    # handle US realms    
#    else:
#        temp_list = [key] + value
#        temp_list.sort()
#        if temp_list not in list_connected_us:
#            list_connected_us.append(temp_list)


#------------------------------------------------------------------------------
# Realm Data Ingest
#------------------------------------------------------------------------------
#realms = ingest_realm_data_us()

# create a dataframe out of the data
df_realm = pd.DataFrame.from_dict(dict_realm, orient='index')