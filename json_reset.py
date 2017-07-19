import requests
import sys
import json
import os
import subprocess
import time
import csv
import re

def json_reset():
	for i in range(1,9):
		port = str(i)
		route={
			u'defaultProfile': {
				u'shaper': {
					u'enabled': False
				},
				u'packetDrop': {
					u'enabled': False
				},
				u'ethernetDelay': {
					u'enabled': False
				}  
			}	
		
		}
		url = 'http://10.67.128.148/api/hw/Port/'+port
		r = requests.put(url,auth=('admin','admin'), data=json.dumps(route))
		#print "port"+port+" is reset!"
if __name__ == "__main__":
	json_reset()
	