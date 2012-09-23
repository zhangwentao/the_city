#!/usr/bin/python
#-*- coding:utf8 -*-

import util
import time
import json
KEY_FILE_PATH = './keys.json'
dATA_DIR_PATH = './info/' 

Client = util.Client
Status_list = util.Status_list
sleep = time.sleep
lock=False
city_position=None
status_list = Status_list()
latest_status_id=0
def main():
	print 'init'
	global city_position
	keys_obj = get_keys()
	Client.init(keys_obj['client_id'],keys_obj['client_secret'])
	city_position = Client(keys_obj['username1'],keys_obj['password1'])
	
def get_keys():
	data = file(KEY_FILE_PATH).readline()
	print data
	return json.loads(data)

def run():
	while not lock:
		print 'run'
		get_status()
		sleep(3)	

def get_status():
	global latest_status_id
	cur_list = city_position.statuses_mentioned(latest_status_id)['statuses']
	if len(cur_list)>0:
		latest_status_id=status_list.put_in(cur_list)
	print 'st:'+str(len(status_list.show()))


main()
