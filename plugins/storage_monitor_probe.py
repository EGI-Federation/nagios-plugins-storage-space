#!/usr/bin/env python3
##############################################################################
# DESCRIPTION
##############################################################################

"""
EGI Online Storage Free Space probe, built using NAP and python3 only
"""

import sys
import json 
import nap.core
import pycurl
from io import BytesIO

PROBE_VERSION = "v0.0.1"

# ########################################################################### #
app = nap.core.Plugin(description="NAGIOS Storage Free Space probe", version=PROBE_VERSION)
app.add_argument("-F", "--file", help="input json file with storage info")
app.add_argument("-T", "--token", help="token needed to access Operations portal API")
app.add_argument("-V", "--VO", help="The VO to test", default="biomed")
app.add_argument("-m", "--min_free_space", help="The min free space in GB ", default="100")
app.add_argument("-O", "--ops_portal_url", help="OPS Portal url", 
            default="https://operations-portal.egi.eu/api/storage_list/json")

def get_storages(args, io):
    buffer = BytesIO()
    c = pycurl.Curl()
    url = args.ops_portal_url + "?vo=%s" % args.VO
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    apikey_header = 'X-API-Key: %s' % args.token
    c.setopt(c.HTTPHEADER, ['accept: application/json',
                                          apikey_header])
    c.perform()
    c.close()
    return buffer.getvalue()

def parse_args(args, io):
    if args.file:
        f = open(args.file)
        return json.load(f)
    elif not args.token:
        io.summary = "Missing token argument" 
        io.status = nap.CRITICAL
        return None
    else:
        return json.loads(get_storages(args,io))
    
@app.metric(seq=1, metric_name="CheckFreeSpace", passive=False)
def metricCheckFreeSpace(args, io):
    """
    Check storage free space
    """
    try:
        storages = parse_args(args, io)
        freesize = 0
        found = False
        if not storages:
            return  
        for storage in storages['storages']:
            if args.hostname in storage['key']:
                for share in storage['storage']:
                    if share['shares']:
                        for info in share['shares']:
                            if 'id' in info:
                                found = True
                                freesize += int(info['FreeSize'])
        if not found:
            io.summary = "The information about the storage %s are not avaiable " % args.hostname  
            io.status = nap.CRITICAL
            return 
        threshold_with_percent = int(args.min_free_space)
        threshold_with_percent += (threshold_with_percent * 5/100)
        if freesize < int(args.min_free_space):
            io.summary = "Free space is less than the threshold configured: %s GB" % str(freesize) 
            io.status = nap.CRITICAL
        elif freesize < threshold_with_percent:
            io.summary = "Free space is close to the minimum threshold configured: %s GB " % str(freesize)
            io.staus = nap.WARNING
        else:
            io.summary = "Free space is above the threshold: %s GB " % str(freesize)
            io.status = nap.OK               
    except Exception as e:
        io.summary = "Error executing probe: %s" % str(e) 
        io.status = nap.CRITICAL

if __name__ == "__main__":
    app.run()