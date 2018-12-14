
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from commands import getoutput, getstatusoutput
import simplejson
import textwrap
import urllib2
import grp
import sys
import os
import re
import json
from easydict import EasyDict as edict
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__version__ = "0.1.23"

API_KEY = os.environ.get('AIzaSyB5U6iCtTTkLHH576hV7Zbx-2hTAOq3tts')



args = edict({'api_key':'AIzaSyB5U6iCtTTkLHH576hV7Zbx-2hTAOq3tts', 'demo':False, 'json_prettify':True, 'map_type':'SATELLITE', 'verbose':True, 'wifi_interface':'wlo1', 'with_overview':True})


def prettify_json(json_data):
    if args.json_prettify:
        return '\n'.join([l.rstrip() for l in simplejson.dumps(json_data, sort_keys=True, indent=4*' ').splitlines()])
    else:
        return simplejson.dumps(json_data)



def get_signal_strengths(wifi_scan_method):
    
    wifi_data = []

    # GNU/Linux
    if wifi_scan_method is 'iw':
        iw_command = 'iw dev %s scan' % (args.wifi_interface)
        iw_scan_status, iw_scan_result = getstatusoutput(iw_command)

        if iw_scan_status != 0:
            if len(iw_scan_result.split('\n')) > 10:
                k=1
                # print ("[...]")
            exit(1)
        else:
            parsing_result = re.compile("BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\d]+)", re.MULTILINE).findall(iw_scan_result)

            wifi_data = [(bss[0].replace(':', '-'), int(bss[1])) for bss in parsing_result]

    
    return wifi_data


def check_prerequisites():
    if sys.platform.startswith(('linux', 'netbsd', 'freebsd', 'openbsd')) or sys.platform == 'darwin':
        wifi_scan_method = None
        perm_cmd = None
        if sys.platform.startswith('linux'):
            if os.geteuid() != 0:
                which_sudo_status, which_sudo_result = getstatusoutput('which sudo')
                if which_sudo_status is 0:
                    current_user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
                    if 'sudo' in current_user_groups or \
                       'admin' in current_user_groups:
                        perm_cmd = 'sudo --preserve-env'
                if perm_cmd is None:
                    for su_gui_cmd in ['gksu', 'kdesu', 'ktsuss', 'beesu', 'su -c', '']:
                        which_cmd_status, which_cmd_result = getstatusoutput('which '+su_gui_cmd.split()[0])
                        if which_cmd_status is 0:
                            break
                    if su_gui_cmd:
                        perm_cmd = su_gui_cmd
                    else:
                        print ("Error: this script need to be run as root !")
                        exit(1)
            if perm_cmd:
                if args.verbose:
                    k=1
                if perm_cmd is 'sudo --preserve-env':
                    os.execvp(perm_cmd.split()[0], perm_cmd.split() + [
                                  ' '.join(['./' + sys.argv[0].lstrip('./')])
                              ] + sys.argv[1:])
                else:
                    os.execvp(perm_cmd.split()[0], perm_cmd.split() + [
                                  ' '.join(['./' + sys.argv[0].lstrip('./')] + sys.argv[1:])
                              ])

            which_iw_status, which_iw_result = getstatusoutput('which iw')
            if which_iw_status != 0:
                if 'ubuntu' in getoutput('uname -a').lower():

                    k=1
                elif 'gentoo' in getoutput('cat /etc/*release').lower():
                    k=1
                exit(1)
            else:
                wifi_scan_method = 'iw'
        elif sys.platform == 'darwin':
            aiport_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
            if not os.path.exists(aiport_path):
                k=1
                exit(1)
            else:
                wifi_scan_method = 'airport'
        elif sys.platform.startswith(('netbsd', 'freebsd', 'openbsd')):
            if os.geteuid() != 0:
                current_user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
                if 'wheel' in current_user_groups:
                    perm_cmd = 'su -c'
                else:
                    exit(1)

            wifi_scan_method = 'ifconfig'

    else:
        exit(1)

    return wifi_scan_method


class MyParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('erreur: %s\n\n' % message)
        sys.exit(2)


def mainf():
    print("mainf")

    



    if args.demo:
        if args.verbose:
            k=1
            print(1)
        wifi_data = [
            ('00-fe-f4-25-ee-30', -40),
            ('02-fe-f4-25-ee-30', -44),
            ('12-fe-f4-25-ee-30', -44),
            ('00-26-5a-7e-0d-02', -60),
            ('90-01-3b-30-04-29', -60),
            ('2c-b0-5d-bd-db-4a', -50)
        ]
    else:
        print(2)
        wifi_scan_method = check_prerequisites()

        if args.verbose:
            k=1
            print(12)
        wifi_data = get_signal_strengths(wifi_scan_method)
        print(wifi_data)
        
    if args.verbose:
        k=1
        print(3)
    location_request = {
        'considerIp': False,
        'wifiAccessPoints':[
            {
                "macAddress": mac,
                "signalStrength": signal
            } for mac, signal in wifi_data]
    }



    if args.api_key:
        print(4)
        API_KEY = args.api_key
    if not API_KEY or API_KEY is 'YOUR_KEY':
        k=1
        print(6)
        exit(1)
    else:
        location_request['considerIp']=True
        json_data = simplejson.JSONEncoder().encode(location_request)
        location_request['considerIp']=True
        http_request = urllib2.Request('https://www.googleapis.com/geolocation/v1/geolocate?key=' + API_KEY)
        http_request.add_header('Content-Type', 'application/json')

        if args.verbose:
            k=1
        api_result = simplejson.loads(urllib2.urlopen(http_request, json_data).read())

        if args.verbose:
            k=1
        print(api_result)
        return (api_result['location']['lat'],api_result['location']['lng'],api_result['accuracy'])

        
