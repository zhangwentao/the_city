#!/usr/bin/python
#-*- coding:utf8 -*-
import os
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
id_user_will_be_reply = ''

def main():
	global latest_status_id
	global comment_txt_file_path
	global keys_obj
	global city_position
	keys_obj = util.get_keys(KEY_FILE_PATH)
	net_is_ok = False
	Client.init(keys_obj['client_id'],keys_obj['client_secret'])

	while not net_is_ok:	
		try:
			city_position = Client(keys_obj['username1'],keys_obj['password1'])
		except:
			wait_second = 2
			os.system('clear')		
			print 'net is not ok~,will try after '+str(wait_second)+' second...'
			print 'please check the internet connection!'
			sleep(wait_second)
		else:
			net_is_ok = True	

	InfoWriter.init(keys_obj['info_dir_path'],keys_obj['weibo_file_name'],keys_obj['friends_ids_file_name'],keys_obj['lock_file_name'],keys_obj['user_name_file_name'])
	comment_txt_file_path = keys_obj['info_dir_path']+keys_obj['comment_txt_file_name']
	latest_status_id = str(int(file(keys_obj['info_dir_path']+keys_obj['last_weibo_id_file_name']).readline()))
	print latest_status_id
	run()

def reset_some_file():
	util.write_txt_file(keys_obj['info_dir_path']+keys_obj['weibo_file_name'],'')
	util.write_txt_file(keys_obj['info_dir_path']+keys_obj['user_name_file_name'],'')
	util.write_txt_file(keys_obj['info_dir_path']+keys_obj['friends_ids_file_name'],'')	

def run():
	while not lock:
		print 'run'
		get_status()
		sleep(3)	

def get_status():
	global latest_status_id
	global id_user_will_be_reply
	cur_list = city_position.statuses_mentioned(latest_status_id)['statuses']
	if len(cur_list)>0:
		latest_status_id=status_list.put_in(cur_list)
		print 'latest '+ str(latest_status_id)
	else:
		print 'no new weibo~'
	if not InfoWriter.is_lock():
		if id_user_will_be_reply != '':
			city_position.create_comment(id_user_will_be_reply,util.get_comment_txt(comment_txt_file_path))
			print 'reply to '+id_user_will_be_reply
			id_user_will_be_reply = ''
		write_to_local()
	print 'status list length:'+str(len(status_list.show()))

def write_to_local():
	global id_user_will_be_reply
	reset_some_file()
	util.delete_file_by_type(keys_obj['info_dir_path'],'jpeg')
	if len(status_list.show()) > 0:
		cur_status = status_list.pop_oldest()
		util.write_txt_file(keys_obj['info_dir_path']+keys_obj['last_weibo_id_file_name'],str(cur_status['id']))
		id_user_will_be_reply = str(cur_status['id'])
		cur_status['user']['fids'] = city_position.get_somebody_friends_ids(cur_status['user']['id'])['ids']
		writer = InfoWriter()
		writer.write_info(cur_status)
main()
