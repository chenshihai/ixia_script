import requests
import sys
import json
import os
import subprocess
import time
import csv
import re

ixia_ip = '10.67.128.148'
account ='admin'
passwd ='admin'


#r = requests.get('http://10.67.128.148/api/hw/Port/1',auth=('admin','admin'))
#print r.text

#print "delayMin_1 = 5.0\n"+"delayMax_1 = 680.0\n"+"pdvMode_1 = u'INTERNET'\n" 

'''
ethernetDelayType = raw_input("Please choose ethernetDelayType! 1, 2 or 3\n")
while(1):
	if ethernetDelayType == "1":
		print "ethernetDelayType = 1" 	
		delayMin_1 = 5.0
		delayMax_1 = 680.0
		pdvMode_1 = u'INTERNET'
		delayMin_2 = 10.0
		delayMax_2 = 1200.0
		pdvMode_2 = u'INTERNET'
		break
	elif ethernetDelayType == "2":
		print "ethernetDelayType = 2" 
		delayMin_1 = 5.0
		delayMax_1 = 150.0
		pdvMode_1 = u'INTERNET'
		delayMin_2 = 10.0
		delayMax_2 = 700.0
		pdvMode_2 = u'INTERNET'
		break
	elif ethernetDelayType == "3":
		print "ethernetDelayType = 3"
		delayMin_1 = 5.0
		delayMax_1 = 50.0
		pdvMode_1 = u'GAUSSIAN'
		delayMin_2 = 10.0
		delayMax_2 = 360.0
		pdvMode_2 = u'GAUSSIAN'
		break
	else:
		ethernetDelayType = raw_input("Error!Choose ethernetDelayType! 1, 2 or 3\n")
	
packetDropType = raw_input("Please choose packetDropType! 1, 2\n")
while(1):
	if packetDropType == "1":
		print "packetDropType = 1" 
		interval_1 = 700
		burstlen_1 = 10
		dist_1 = u'UNIFORM'
		delayMin_2 = 10.0
		delayMax_2 = 1200.0
		pdvMode_2 = u'INTERNET'
		break
	elif packetDropType == "2":
		print "packetDropType = 2" 
		interval_1 = 70000
		burstlen_1 = 1000
		dist_1 = u'GAUSSIAN'
		stddev_1 = 10.1
		interval_2 = 70000
		burstlen_2 = 175
		dist_2 = u'GAUSSIAN'
		stddev_2 = 10.1
		break
	else:
		packetDropType = raw_input("Error!Choose packetDropType! 1, 2\n")

		
bitRateType = raw_input("Please choose bitRateType! 1, 2\n")
while(1):
	if bitRateType == "1":
		print "bitRateType = 1" 
		bitRate_1 = 50000
		bitRate_2 = 100000
		break
	elif bitRateType == "2":
		print "bitRateType = 2"
		bitRate_1 = 80000		
		bitRate_2 = 100000
		break
	else:
		bitRateType = raw_input("Error!Choose bitRateType! 1, 2\n")
'''

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
		print "port"+port+" is reset!"


# set and send the json to the ixia server 
def function(delayMin,delayMax,pdvMode,interval,burstlen,dist,stddev,bitRate,port):
	route={
		u'defaultProfile': {
			u'shaper': {
				u'burstTolerance': 64000,
				u'bitRate': bitRate,
				u'enabled': True
			},
			u'packetDrop': {
				u'rdmSel': {
					u'dist': dist,
					u'interval': interval,
					u'burstlen': burstlen,
					u'stddev': stddev
					},
					u'enabled': True
			},
			u'ethernetDelay': {
				u'delay': 0.0,
				  u'isUncorrelated': False,
				  u'delayMax': delayMax,
				  u'maxNegDelta': 0.1,
				  u'pdvMode': pdvMode,
				  u'delayMin': delayMin,
				  u'units': u'MS',
				  u'maxPosDelta': 0.1,
				  u'enabled': True,
				  u'spread': 1.0
			}  
		}	
	
	}
	url = 'http://10.67.128.148/api/hw/Port/'+port
	r = requests.put(url,auth=('admin','admin'), data=json.dumps(route))
	print "\nport"+port+" is finished!"
if __name__ == "__main__":
	#json_reset()
	'''
	for i in range(0,len(sys.argv)):
		print "sys.argv",i,sys.argv[i]
	'''
	file_path = sys.argv[1] + "/static_ixia.log"	
	print "filepath:",file_path
	
	#--------------ethernetDelayType----------------
	if sys.argv[2] == "1":
		#print "ethernetDelayType = 1" 	
		delayMin_1 = 5.0
		delayMax_1 = 680.0
		pdvMode_1 = u'INTERNET'
		delayMin_2 = 10.0
		delayMax_2 = 1200.0
		pdvMode_2 = u'INTERNET'
	elif sys.argv[2] == "2":
		#print "ethernetDelayType = 2" 
		delayMin_1 = 5.0
		delayMax_1 = 150.0
		pdvMode_1 = u'INTERNET'
		delayMin_2 = 10.0
		delayMax_2 = 700.0
		pdvMode_2 = u'INTERNET'
	elif sys.argv[2] == "3":
		#print "ethernetDelayType = 3"
		delayMin_1 = 5.0
		delayMax_1 = 50.0
		pdvMode_1 = u'GAUSSIAN'
		delayMin_2 = 10.0
		delayMax_2 = 360.0
		pdvMode_2 = u'GAUSSIAN'
		
	#-------------packetDropType------------------	
	if sys.argv[3] == "1":
		#print "packetDropType = 1" 
		interval_1 = 700
		burstlen_1 = 10
		dist_1 = u'UNIFORM'
		stddev_1 = 10.1
		interval_2 = 20000
		burstlen_2 = 50
		dist_2 = u'UNIFORM'
		stddev_2 = 10.1
	elif sys.argv[3] == "2":
		#print "packetDropType = 2" 
		interval_1 = 70000
		burstlen_1 = 1000
		dist_1 = u'GAUSSIAN'
		stddev_1 = 10.1
		interval_2 = 70000
		burstlen_2 = 175
		dist_2 = u'GAUSSIAN'
		stddev_2 = 10.1	
		
	#----------------bitRateType----------------------	
	if sys.argv[4] == "1":
		#print "bitRateType = 1" 
		bitRate_1 = 50000
		bitRate_2 = 100000
	elif sys.argv[4] == "2":
		#print "bitRateType = 2"
		bitRate_1 = 80000		
		bitRate_2 = 100000
	
	
	interval_3 = 20000
	burstlen_3 = 1
	interval_4 = 20000
	burstlen_4 = 1
	
	function(delayMin_1,delayMax_1,pdvMode_1,interval_3,burstlen_3,dist_1,stddev_1,bitRate_1,'3')#port 3
	function(delayMin_2,delayMax_2,pdvMode_2,interval_4,burstlen_4,dist_2,stddev_2,bitRate_2,'7')#port 7
	
	time.sleep(16)		
	
	function(delayMin_1,delayMax_1,pdvMode_1,interval_1,burstlen_1,dist_1,stddev_1,bitRate_1,'3')#port 3
	function(delayMin_2,delayMax_2,pdvMode_2,interval_2,burstlen_2,dist_2,stddev_2,bitRate_2,'7')#port 7

	list_1 = [delayMin_1,delayMax_1,pdvMode_1,interval_1,burstlen_1,dist_1,stddev_1,bitRate_1]
	list_2 = [delayMin_2,delayMax_2,pdvMode_2,interval_2,burstlen_2,dist_2,stddev_2,bitRate_2]
	str_time = time.time()
	str_log = sys.argv[5]+" carrier1 "+str(str_time)+" "	
	for item in list_1:
		str_log += str(item)+" "
	str_log += "\n"
	str_log += sys.argv[5]+" carrier2 "+str(str_time)+" "
	for item in list_2:
		str_log += str(item)+" "
	str_log += "\n"	
	file = open(file_path,'a+')
	file.write(str_log)
	file.close()
	
		
	



