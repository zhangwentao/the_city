#!/usr/bin/python
#-*- coding:utf8 -*-

import util
import time
import json
KEY_FILE_PATH = './keys.json'

Client = util.Client
Status_list = util.Status_list
InfoWriter = util.InfoWriter
sleep = time.sleep
lock=False
city_position=None
status_list = Status_list()
latest_status_id=0
comment_txt_file_path = ''
keys_obj={}
def main():
	global comment_txt_file_path
	global keys_obj
	print 'init'
	global city_position
	keys_obj = get_keys()
	Client.init(keys_obj['client_id'],keys_obj['client_secret'])
	city_position = Client(keys_obj['username1'],keys_obj['password1'])
	InfoWriter.init(keys_obj['info_dir_path'],keys_obj['weibo_file_name'],keys_obj['friends_ids_file_name'],keys_obj['lock_file_name'],keys_obj['user_name_file_name'])
	comment_txt_file_path = keys_obj['info_dir_path']+keys_obj['comment_txt_file_name']
	run()

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
	if not InfoWriter.is_lock():
		write_to_local()	
	print 'st:'+str(len(status_list.show()))

def write_to_local():
	if len(status_list.show()) > 0:
		cur_status = status_list.pop_oldest()
		print cur_status
		print status_list.show()
		print 'go:\n'
		print cur_status
		print city_position.get_somebody_friends_ids(cur_status['user']['id'])
		cur_status['user']['fids'] = city_position.get_somebody_friends_ids(cur_status['user']['id'])['ids']
		util.delete_file_by_type(keys_obj['info_dir_path'],'jpeg')
		writer = InfoWriter()
		city_position.create_comment(cur_status['id'],util.get_comment_txt(comment_txt_file_path))
		writer.write_info(cur_status)
main()
