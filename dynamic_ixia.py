# -*- coding: UTF-8 -*-
import requests
import sys
import json
import os
import subprocess
import time
import csv
import re
import random
import threading

ixia_ip = '10.67.128.148'
account ='admin'
passwd ='admin'
#file_path = "./Test/ixia.log"
#r = requests.get('http://10.67.128.148/api/hw/Port/1',auth=('admin','admin'))
#print r.text 

# set and send the json to the ixia server 
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
		# print "port"+port+" is reset!"
		
	
def json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port):
	#print delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port
	route={
		u'defaultProfile': {
			u'shaper': {
				u'burstTolerance': 64000,
				u'bitRate': bitrate,
				u'enabled': True
			},
			u'packetDrop': {
				u'rdmSel': {
					u'dist': dist,
					u'interval': interval,
					u'burstlen': burstlen,
					u'stddev': 10.0
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
       #print "\nport"+port+" is finished!\n"
	

def mode1(port,file_path,id):
	print 'thread %s is running...' % threading.current_thread().name
	i = 8
	while(i):
		start_time = time.time()
		a = random.gauss(16.5,4)
		if a < 3:
			a = 3
		elif a > 40:
			a = 40
		#print "a1 = %s" % a
		b = random.uniform(3,5)
		#print "b1 = %s" % b
		b2 = 1.5 
		b1 = b - b2 
		
		
		#y = random.randint(1,200)
		#print "y = %s" % y
		#burstlen_2 = y * 100
		#bitrate_2 = 100000 / y 
		
		delayMin = 10.0
		delayMax = 360.0
		pdvMode = u'GAUSSIAN'
		interval = 20000
		burstlen = 50
		dist = u'UNIFORM'
		bitrate = 100000
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port)
		#print "thread1 sleep = %s" % a
		time.sleep(a)
		list_a = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,a]
		
		delayMin = 200.0
		delayMax = 2000.0
		pdvMode = u'INTERNET'
		y = random.randint(0,15)
		#print "y = %s" % y
		interval = 50
		burstlen = y
		dist = u'UNIFORM'
		bitrate = 100000/(y+1)
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port) 
		#print "thread1 sleep = %s" % b1
		time.sleep(b1)
		list_b1 = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,y,b1]
		
		delayMin = 2000.0
		delayMax = 95000.0
		pdvMode = u'INTERNET'
		y = random.randint(15,49)
		#print "y = %s" % y
		interval = 50
		burstlen = y
		dist = u'UNIFORM'
		bitrate = 100000/(y+1)
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port) 
		#print "thread1 sleep = %s" % b2
		time.sleep(b2)
		list_b2 = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,y,b2]
		
		i = i - 1
		end_time = time.time()
		
		str_log = id+" "+threading.current_thread().name+" "+"mode1 "+str(start_time)+" "+str(end_time)+" "
		for item in list_a:
			str_log += str(item)+" "
		for item in list_b1:
			str_log += str(item)+" "
		for item in list_b2:
			str_log += str(item)+" "
		str_log += "\n"
		mutex.acquire()
		# print "opening--------"
		file = open(file_path,'a+')
		file.write(str_log)
		file.close()
		mutex.release()
	print 'thread %s is ended...' % threading.current_thread().name	
	
def mode2(port,file_path,id):
	print 'thread %s is running...' % threading.current_thread().name
	i = 8
	while(i):
		start_time = time.time()
		a = random.gauss(26.5,6)
		if a < 3:
			a = 3
		elif a > 70:
			a = 70
		#print "a1 = %s" % a
		b = random.uniform(3,5)
		#print "b1 = %s" % b
		b2 = 1.5 
		b1 = b - b2 
		
		
		#y = random.randint(1,200)
		#print "y = %s" % y
		#burstlen_2 = y * 100
		#bitrate_2 = 100000 / y 
		delayMin = 10.0
		delayMax = 660.0
		pdvMode = u'GAUSSIAN'
		interval = 20000
		burstlen = 50
		dist = u'UNIFORM'
		bitrate = 100000
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port)
		#print "thread2 sleep = %s" % a
		time.sleep(a)
		list_a = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,a]
		
		delayMin = 300.0
		delayMax = 2000.0
		pdvMode = u'INTERNET'
		y = random.randint(0,15)
		#print "y = %s" % y
		interval = 50
		burstlen = y
		dist = u'UNIFORM'
		bitrate = 100000/(y+1)
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port)
		#print "thread2 sleep = %s" % b1
		time.sleep(b1)
		list_b1 = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,y,b1]
		
		delayMin = 2000.0
		delayMax = 15000.0
		pdvMode = u'INTERNET'
		y = random.randint(15,49)
		#print "y = %s" % y
		interval = 50
		burstlen = y
		dist = u'UNIFORM'
		bitrate = 100000/(y+1)
		json_function(delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,port)
		#print "thread2 sleep = %s" % b2
		time.sleep(b2)
		list_b2 = [delayMin,delayMax,pdvMode,interval,burstlen,dist,bitrate,y,b2]
		
		i = i - 1
		end_time=time.time()
		
		str_log = id+" "+threading.current_thread().name+" "+"mode2 "+str(start_time)+" "+str(end_time)+" "
		for item in list_a:
			str_log += str(item)+" "
		for item in list_b1:
			str_log += str(item)+" "
		for item in list_b2:
			str_log += str(item)+" "
		str_log += "\n"
		mutex.acquire()
		file = open(file_path,'a+')
		file.write(str_log)
		file.close()
		mutex.release()
		
	print 'thread %s is ended...' % threading.current_thread().name	


if __name__ == "__main__":
	#json_reset()
	
	'''
	input_mode = raw_input("Please choose mode Type! 1 = All Carrier1,2 = All Carrier2 or 3 = Carrier1 and Carrier2\n")
	
	while(1):
		if input_mode != "1" and input_mode != "2" and input_mode != "3":
			input_mode = raw_input("ERROR!Please choose mode Type! 1 = All Carrier1,2 = All Carrier2 or 3 = Carrier1 and Carrier2\n")
		else:
			break
	'''
	#input_rtt_type = raw_input("Please choose RTT Type! 1 or 2\n")	
		
	#while(1):
	#	if input_rtt_type != "1" and input_rtt_type != "2" :
	#		input_rtt_type = raw_input("ERROR!Please choose RTT Type! 1 or 2\n")
	#	else:
	#		break
	#print 'thread %s is running...' % threading.current_thread().name
	#time.sleep(30)
	#for i in range(0,len(sys.argv)):
		#print "sys.argv[%d]",i,sys.argv[i]
	file_path = sys.argv[1] + "/dynamic_ixia.log"	
	print "filepath:",file_path
	if sys.argv[2] == "1":
		t1 = threading.Thread(target=mode1, name = 'carrier1',args = ('3',file_path,sys.argv[3]))
		t2 = threading.Thread(target=mode1, name = 'carrier2',args = ('7',file_path,sys.argv[3]))
		
	elif sys.argv[2] == "2":
		t1 = threading.Thread(target=mode2, name = 'carrier1',args = ('3',file_path,sys.argv[3]))
		t2 = threading.Thread(target=mode2, name = 'carrier2',args = ('7',file_path,sys.argv[3]))
		
	elif sys.argv[2] == "3":
		t1 = threading.Thread(target=mode1, name = 'carrier1',args = ('3',file_path,sys.argv[3]))
		t2 = threading.Thread(target=mode2, name = 'carrier2',args = ('7',file_path,sys.argv[3]))
	
	#t1 = threading.Thread(target=mode1, name = 'carrier1',args = ('4',))
	#t2 = threading.Thread(target=mode2, name = 'carrier2',args = ('8',))

	time.sleep(12)
	json_function(5.0,50.0,u'GAUSSIAN',20000,1,u'UNIFORM',100000,'3')	
	json_function(10.0,360.0,u'GAUSSIAN',20000,1,u'UNIFORM',100000,'7')
	
	mutex = threading.Lock()
	time.sleep(4)
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print 'thread %s is ended...' % threading.current_thread().name
	