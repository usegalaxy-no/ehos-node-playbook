#!/usr/bin/python3
#
#
#
#
# Kim Brugger (20 Sep 2018), contact: kim@brugger.dk

import sys


import argparse
from munch import Munch
try:
    import json
except ImportError:
    import simplejson as json


import ehos
import ehos.utils
import ehos.log_utils as logger
import ehos.htcondor
import ehos.instances

def main():

    parser = argparse.ArgumentParser(description='ehos_status: print ehos status in telegraf format')
    parser.add_argument('config_files', nargs="*", metavar='config-files',  help="yaml formatted config files", default=[ehos.utils.find_config_file('ehos.yaml')])
    parser.add_argument('--list', action='store_true') # expected by ansible
    args = parser.parse_args()



    logger.init(name='ehosd' )
    logger.set_log_level( 0 )



    config = ehos.utils.get_configurations(args.config_files)
    condor = ehos.htcondor.Condor()
    clouds = ehos.connect_to_clouds( config )
    instances = ehos.instances.Instances()
    instances.add_clouds( clouds )

    # get the current nodes
    instances.update( condor.nodes() )
    nodes = instances.node_state_counts()
    hosts = {"all":{"hosts":[]}, "_meta": {"hostvars":{}}}
    for node in instances.get_nodes():
        ip_addr = node.ip.pop(0)
        hosts['all']['hosts'].append( ip_addr )
        hosts["_meta"]['hostvars'][ip_addr] = {}


    print( json.dumps( hosts ))

if __name__ == '__main__':
    main()
else:
    print("Not to be run as a library")
    sys.exit( 1 )

