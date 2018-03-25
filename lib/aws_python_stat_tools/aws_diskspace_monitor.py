#!/usr/bin/env python

##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = ["GNU General Public License, version 2 (GPL-2.0)", 
                   "BioCom_Public_Use_Copyright_and_License.py"]
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "rightmirem@utr.net"
__status__      = "Test"
##############################################################################

'''
This is intended to run on an Amazon EC2 instance and requires an IAM
role allowing to write CloudWatch metrics. Alternatively, you can create
a boto credentials file and rely on it instead. 

Thanks to the bot group at GitHub https://github.com/boto/boto
Original idea based on https://github.com/colinbjohnson/aws-missing-tools
Modified by Mike Rightmire at BiocomSoftware.com
'''

from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata

import re
import StringIO
import subprocess
import sys


def collect_diskspace():
    """
    collect_diskspace()
    
    :DESCRIPTION:
        Uses subprocess.Popen to run a secure 'df -h' command, and then StrinIO
        to parse out the data into a dictionary of lists.
        
        return is in the format...
        {'Drivename': ['Size', 'Used', 'Avail', 'Use%', 'Mounted', 'on']}
        
        I.E...
        {
        'Filesystem': ['Size', 'Used', 'Avail', 'Use%', 'Mounted', 'on'],
        'tmpfs': ['297M', '0', '297M', '0%', '/dev/shm'], 
        '/dev/xvda1': ['7.8G', '3.6G', '4.2G', '46%', '/'], 
        'devtmpfs': ['282M', '12K', '282M', '1%', '/dev']
        }
    """
    diskinfo = {}
    dfdata = StringIO.StringIO(get_df()) 

    for line in dfdata.readlines():
        data = line.split()
        drive = data.pop(0)
        diskinfo[drive] = []
        loop = True
        while loop:
            try: 
                diskinfo[drive].append(data.pop(0))
            except IndexError, e:
                loop = False

    return diskinfo

def get_df():
    """
    get_df()
    
    :DESCRIPTION:
        Runs a 'df -h' command and returns the entire response as a sting. 
        Further line processing needed. 
        
        This method has commented code to add additional processing such as 
        grep without using the shell=True command which is a security risk.
    """
    # For grep of desired
    #query = "sh"
    
    # df in human readable
    ps_process = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)

    # A grep command 
#     grep_process = subprocess.Popen(["grep", query], 
#                                     stdin=ps_process.stdout, 
#                                     stdout=subprocess.PIPE)
    
    # USE ONLY ONE output = ?_process.communicate()[0] command to run the LAST
    # process created. 
    # output = grep_process.communicate()[0]
    output = ps_process.communicate()[0]

    # Close the process
    ps_process.stdout.close()  # Allow ps_process to receive a SIGPIPE if grep_process exits.

    return output # String. Entire response as a string
    

    
    
def send_multi_metrics(instance_id, region, metrics, namespace='EC2/Disk',
                        unit='Percent'):
    '''
    Send multiple metrics to CloudWatch
    metrics is expected to be a map of key -> value pairs of metrics
    '''
    cw = cloudwatch.connect_to_region(region)
    cw.put_metric_data(namespace, metrics.keys(), metrics.values(),
                       unit=unit,
                       dimensions={"InstanceId": instance_id})

if __name__ == '__main__':
    metadata = get_instance_metadata()
    instance_id = metadata['instance-id']
    region = metadata['placement']['availability-zone'][0:-1]
    diskspace = collect_diskspace()
    for metric in diskspace.keys():
        metric = str(metric)
        # Skip tmp space for now
        if 'tmp'        in metric.lower(): continue
        # Skip headers
        if 'filesystem' in metric.lower(): continue
        diskuse = "".join(['Diskuse.', metric])
        intpercent = ''.join(c for c in diskspace[metric][3] if c in "0123456789")
        if intpercent == "": 
            e = ''.join(["The percentage use data (", 
                         str(diskspace[metric][3]), 
                         ") from drive ", 
                         str(metric), 
                         " is invalid."])
            raise Exception(e)
        
        intpercent = int(intpercent)
        metrics = {diskuse:intpercent} # Percent used
        
    # Send to AWS instance
    send_multi_metrics(instance_id, region, metrics)
    