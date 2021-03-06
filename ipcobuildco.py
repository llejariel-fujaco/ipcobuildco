import sys
import time
import os
import logging
from logging.config import dictConfig
import getopt
from configobj import ConfigObj
from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd
import csv
import unicodedata
import re
import ipaddress

from ftplib import FTP
import codecs
import binascii
import gzip
import multiprocessing
import threading
import queue

import requests
import json

import dictionary

###############################################################################
# pip install --upgrade pip
# pip install --upgrade pandas
# pip install --upgrade requests
# pip install --upgrade configobj
###############################################################################

###############################################################################
# Globals
###############################################################################
thisname='defaultprg'

###############################################################################
def is_gz_file(filepath):
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'

###############################################################################
def main():
    logger.info('-------------------------------------------------------------------')
    logger.info('Start '+thisname)

    logger.info('Params list=[{}]'.format(params))
    logger.info('Config list=[{}]'.format(config))
    logger.info('thisname=[{}]'.format(thisname))
    dictionary.isNoise('AH AH AH')

    co_name='SMART ADVERTISING COMPANY FRANCE FR MZ'
    logger.info('get_all_token: {0} => {1}'.format(co_name,dictionary.get_all_tokens(co_name)))

    logger.info('get_company_canonical {0} => {1}'.format(co_name,dictionary.get_company_canonical(co_name)))

    logger.info('Done '+thisname)
    logger.info('-------------------------------------------------------------------')

## -------------------------------------------------------------------
## ---- Tech functions

## -------------------------------------------------------------------
## init_log():
def init_log():
    ## Logging init
    logging_config = { 
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': { 
            'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}
        },
        'handlers': { 
            'ch': {'level': 'INFO','formatter': 'standard','class': 'logging.StreamHandler'},
            'fh': {'level': 'INFO','formatter': 'standard','class': 'logging.handlers.RotatingFileHandler',
                   'filename': thisname+'.log','mode': 'a','encoding': 'utf-8',
                   'maxBytes': 10485760,'backupCount': 5,}
       },
        'loggers': {
            '': {'handlers': ['ch','fh'],'level': 'INFO','propagate': True},
        }
    }
    logging.config.dictConfig(logging_config)
    logging_init=logging.getLogger(__name__)
    return(logging_init)

## -------------------------------------------------------------------
## read_cli():
def read_cli():
    help_str=thisname+'.py -p <param_name>'
    params={'param_name':''}
    logger.info('Reading params')
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:",["param_name="])
    except getopt.GetoptError as opterr:        
        logger.error(opterr)
        logger.error(help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logger.error(help_str)
            sys.exit()
        elif opt in ("-p", "--param_name"):
            params['param_name'] = arg
            
    logger.info('In read_cli list=[{}]'.format(params['param_name']))
    return(params)

## -------------------------------------------------------------------
## read_config():
def read_config():
    cwd=os.getcwd()
    return(ConfigObj(cwd+'/python_run_prod.env'))

## -------------------------------------------------------------------
## Main procedure
if __name__ == '__main__':
    config=read_config()
    if 'prg_name' in config:
        thisname=config['prg_name']

    logger=init_log()
    params=read_cli()

    main()
