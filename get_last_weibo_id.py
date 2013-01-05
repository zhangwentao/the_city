#!/usr/bin/python
#-*- coding:utf8 -*-
import util
status_list = util.Status_list()
keys_obj = util.get_keys('keys.json')
util.Client.init(keys_obj['client_id'],keys_obj['client_secret'])
city_position = util.Client(keys_obj['username1'],keys_obj['password1'])
last_weibo_id = 0

while True:
	temp_list = city_position.statuses_mentioned(last_weibo_id)['statuses']
	if len(temp_list) == 0:
		break
	last_weibo_id = status_list.put_in(temp_list)

last_weibo_id_file_path = keys_obj['info_dir_path']+keys_obj['last_weibo_id_file_name']
util.write_txt_file(last_weibo_id_file_path,str(last_weibo_id))
print 'last_weibo_id is:' + str(last_weibo_id)+',is saved to ' + last_weibo_id_file_path
