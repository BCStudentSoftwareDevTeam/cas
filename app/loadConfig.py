'''
This script loads the yaml file, which holds all
configuration information.
'''

import yaml, os

#For Logging
import logging

def load_config(filename = 'app/config.yaml'):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg
