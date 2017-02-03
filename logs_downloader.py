"""Simple program to download files using a scraper."""
import os.path as path
import os
import shlex
import ConfigParser
import logging
import sys
import subprocess
import time
import re
import pprint
from configparser import ConfigParser
from lxml import html
from requests import get
import requests
from datetime import datetime

# Get Date in required format
now = datetime.now().strftime('%A.%d-%b-%Y.%H%MHrs')
try:
    file_name = __file__
except NameError:
    file_name = 'logsDownloader.py'

# Script name
script_name = path.basename(file_name)
print("Script name is %s", (script_name,))

log_file_name = file_name + ".log"

print("Log file name set as %s", (log_file_name,))

# get Data from properties file
property_file = file_name + ".properties"
print('Property File name is %s', (property_file,))

# Setup Logging
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

if len(sys.argv) >= 2 and sys.argv[1] in LEVELS.keys():
    level_name = sys.argv[1]
else:
    level_name = 'info'


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
level = LEVEL.get(level_name, logging.NOTSET)
logging.basicConfig(level=level, format=FORMAT,
                    filename=log_file_name, filemode='w')
log = logging.getLogger(script_name)

# Reading Properties file
try:
    config_section = 'Configuration' # Name of section in properties file
    selection_secion = 'Selection' # Name of section in properties file
    parser = ConfigParser.ConfigParser()
    parser.read(property_file)
    src_url = parser.get(config_section, 'url')
     = parser.get(config_section, '')
    maven_lifecycle_arguments = parser.get(
        config_section, 'maven_lifecycle_arguments')
    maven_jvm_arguments = parser.get(
        config_section, 'maven_jvm_arguments')
    project_names = parser.get(selection_secion, 'project_names')
except ConfigParser.Erro & IOError:
    exception_info = "Cannot parse property file. Details are : " + str(err)
    log.error(exception_info)
    sys.exit(exception_info)


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


PAGE = requests.get('https://archive.org/download/ia_webserverlogs_201702')
print("response as text", PAGE.text)

TREE = html.fromstring(PAGE.content)

LOG_URL = TREE.xpath(".//*[@id='content']/ul[1]/li[1]/a/@href").pop()
# LOG_NAME = TREE.xpath(".//*[@id='content']/ul[1]/li[1]/a/text()")
# split from right with / sep and into only two parts, then get the second
# (first from right)
LOG_NAME = LOG_URL.rsplit("/", 1)[-1]

print("log name : ", LOG_NAME)
print("log url : ", LOG_URL)
download(LOG_URL, path.join("downloads", LOG_NAME))
