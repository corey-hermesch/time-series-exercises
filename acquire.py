# IMPORTS

import pandas as pd

import requests
import math
import os
import json

# FUNCTIONS

def get_swapi_df(entity='people'):
    """
    This function will accept the entity of a Star Wars API URI
    - default entity = 'people'
    - other options: 'planets', 'films', 'starships', etc.
    - requests json files for all pages for the entity requested utilizing swapi,
      and writes data to a local csv
    - OR if csv already exists, reads in data from local csv
    - returns a dataframe of all entities requested
    """
    # set filename for csv file to read or to write later after pulling data from Star Wars API
    filename = 'sw_' + entity + '.csv'
    
    # if filename exists, read from the csv file
    if os.path.isfile(filename):
        entity_df = pd.read_csv(filename)
        print ("csv file found and read")
        return entity_df
    
    # else get data from swapi
    else:
        
        # set base_url per Star Wars API documentation
        base_url = 'https://swapi.dev/api/'

        # set entity uri per documentation
        entity_uri = base_url + entity + '/'

        # get the initial request
        response = requests.get(entity_uri)
        data = response.json()

        # initialize list of entities
        entity_list = []
        entity_list = entity_list + data['results']

        # set num_pages to be number of pages we need to ask for
        num_pages = math.ceil(data['count'] / len(data['results']))

        # make a loop to get all the pages worth of data
        for i in range (1, num_pages):
            #set next_uri
            next_uri = data['next']

            # get the response and put the json into data
            response = requests.get(next_uri)
            data = response.json()

            # add the results portion to people_list
            entity_list = entity_list + data['results']
            
        # make df and write to csv
        entity_df = pd.DataFrame(entity_list)
        entity_df.to_csv(filename, index=False)
        
        print (f'csv file not found, data read from {entity_uri}, csv created')
        return entity_df


# defining a function to read german power data
def get_german_power_df(filename='opsd_germany_daily.csv'):
    """
    This function will
    - accept a filename of a local csv (default 'opsd_germany_daily.csv')
    - read in data to a dataframe from a local csv OR from 
      https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv
    - return the dataframe
    """
    
    # if filename exists, read from the csv file
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
        print ("csv file found and read")
    
    # else get data from web
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df.to_csv(filename)
        print(f'csv file not found; data read from {url}')
    
    return df


