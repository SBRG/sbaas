from ConfigParser import SafeConfigParser
import os as __os
from os.path import split as __split, join as __join, abspath as __abspath, \
    isfile as __isfile
from sys import modules

self = modules[__name__]

config = SafeConfigParser()
# set the default settings for the database
config.add_section("DATABASE")
config.set("DATABASE", "host", "localhost:5432")
config.set("DATABASE", "database", "metabolomics")
#config.set("DATABASE", "database", "sbaas")
config.set("DATABASE", "password", "dmccloskey")
config.set("DATABASE", "schema", "public")
config.set("DATABASE", "user", "dmccloskey")
# set the default settings for the data directories
config.add_section("DATA_DIR")
config.set("DATA_DIR", "sbaas", "C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas\\sbaas")
config.set("DATA_DIR", "workspace", "C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas_workspace\\sbaas_workspace\\workspace")
config.set("DATA_DIR", "workspace_data", "C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas_workspace\\sbaas_workspace\\workspace_data")
config.set("DATA_DIR", "visualization_data", "C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas_workspace\\sbaas_workspace\\visualization_data")
config.set("DATA_DIR", "visualization_resources", "C:\\Users\\dmccloskey-sbrg\\Documents\\GitHub\\sbaas_workspace\\sbaas_workspace\\visualization_resources")

# save options as variables for the database
self.host = config.get("DATABASE", "host")
self.database = config.get("DATABASE", "database")
self.password = config.get("DATABASE", "password")
self.schema = config.get("DATABASE", "schema")
self.user = config.get("DATABASE", "user")
# save options as variables for the data directories
self.sbaas = config.get("DATA_DIR", "sbaas")
self.workspace = config.get("DATA_DIR", "workspace")
self.workspace_data = config.get("DATA_DIR", "workspace_data")
self.visualization_data= config.get("DATA_DIR", "visualization_data")
self.visualization_resources = config.get("DATA_DIR", "visualization_resources")