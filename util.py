#!/usr/bin/python
#-*- coding:utf8 -*-

import httplib
import urllib
import json
import glob
import os
import time


sleep = time.sleep
HEADERS = {"Content-type": "application/x-www-form-urlencoded"}
urlretrieve = urllib.urlretrieve

def get_keys(key_file_path):
	data = ''
	key_file = file(key_file_path)
	while True:
		line = key_file.readline()
		if len(line) == 0:
			break
		data += line
	return json.loads(data)

def get_access_token(client_id,client_secret,usrname,passwd):
	param_obj = {'grant_type':'password'};
	param_obj['client_id']=client_id
	param_obj['client_secret']=client_secret
	param_obj['username'] = usrname
	param_obj['password'] = passwd
	param=urllib.urlencode(param_obj)
	conn = httplib.HTTPSConnection("api.weibo.com")  
	conn.request('POST','/oauth2/access_token',param,HEADERS)  
	backen_data =conn.getresponse().read()  
	obj = json.loads(backen_data)
	return obj['access_token']

def delete_file_by_type(dir_path,file_type):
	for f in glob.glob(dir_path+'*.'+file_type):
		os.unlink(f)

def write_txt_file(file_path,text):
	text_file = file(file_path,'w')
	text_file.write((text).encode('gb2312'))
	text_file.close()

def formate_output(raw):
	raw = raw.decode('utf-8')
	result=u''
	counter = 0
	max_count = 14
	for char in raw:
		if counter == 14:
			result+=u' '	
			counter = 0
		result+=char			
		counter+=1
	return result.encode('utf-8')

def api_proxy(api_url,param_obj={},method='GET'):
	while True:	
		try:
			conn = httplib.HTTPSConnection("api.weibo.com")  
			param=urllib.urlencode(param_obj)
			url = '/2/'+api_url+'.json?'
			if method == 'GET':
				conn.request(method,url+param)  
			elif method == 'POST':
				conn.request(method,url,param,HEADERS)  
			backen_data =conn.getresponse().read()  
			obj = json.loads(backen_data)
		except:
			wait_second = 2
			os.system('clear')		
			print 'net is not ok~,will try after '+str(wait_second)+' second...'
			print 'please check the internet connection!'
			sleep(wait_second)
		else:
			break
	return obj

def get_comment_txt(comment_file_path):
	result = file(comment_file_path).readline()		
	return result

def status_cmp(a,b):
	a_id = int(a['id'])
	b_id = int(b['id'])
	if a_id > b_id:
		return 1
	elif a_id == b_id:
		return 0
	else:
		return -1

class Client:
	client_id=''
	client_secret=''
	@classmethod
	def init(cls,client_id,client_secret):
		cls.client_id = client_id
		cls.client_secret = client_secret

	def __init__(self,user_name,pass_word):
		self.access_token = get_access_token(self.__class__.client_id,self.__class__.client_secret,user_name,pass_word)

	def proxy_for(self,api_url,param_obj={},method='GET'):
		param_obj_inner = {'access_token':self.access_token}
		param_obj_inner.update(param_obj)
		return api_proxy(api_url,param_obj_inner,method)

	def statuses_mentioned(self,since_id=0):
		api_url = "statuses/mentions"
		count = 200
		filter_by_type = 1	
		param_obj = {'since_id':since_id,'count':count,'filter_by_type':filter_by_type}
		return self.proxy_for(api_url,param_obj)

	def get_somebody_friends_ids(self,somebody_id):
		api_url = "friendships/friends/bilateral/ids"	
		count = 1999
		param_obj = {'uid':somebody_id,'count':count}	
		return self.proxy_for(api_url,param_obj)
	
	def create_comment(self,weibo_id,comment):
		api_url = "comments/create"	
		param_obj = {'id':weibo_id,'comment':comment}
	 	return self.proxy_for(api_url,param_obj,'POST')	

	def get_somebody_info(self,somebody_id):
		api_url = "users/show"
		param_obj = {'uid':somebody_id}
		return self.proxy_for(api_url,param_obj)

	def get_somebody_follower_ids(self,somebody_id):
		follower_ids = []
		page_cursor = -1
		count_perpage = 5000
		api_url = "friendships/followers/ids"
		while page_cursor != 0:
			if page_cursor < 0:
				page_cursor = 0
			param_obj = {'uid':somebody_id,'cursor':page_cursor,'count':count_perpage}
			backen_data = self.proxy_for(api_url,param_obj)
			page_cursor = backen_data['next_cursor']
			follower_ids.extend(backen_data['ids'])
		return follower_ids

class Status_list():
	def __init__(self):
		self.status_list = []

	def put_in(self,new_list):
		new_list.sort(status_cmp)
		self.status_list.extend(new_list)				
		latest_status_id = new_list[len(new_list)-1]['id']
		return latest_status_id

	def pop_oldest(self):
		return self.status_list.pop(0)	
	
	def show(self):
		return self.status_list

class InfoWriter():
	info_dir_path = ''
	weibo_file_name = ''
	friends_ids_file_name = ''
	user_name_file_name = ''
	lock_file_name = ''				

	@classmethod
	def init(cls,info_dir_path,weibo_file_name,friends_ids_file_name,lock_file_name,user_name_file_name):
		cls.info_dir_path = info_dir_path
		cls.weibo_file_name = weibo_file_name
		cls.friends_ids_file_name = friends_ids_file_name
		cls.user_name_file_name = user_name_file_name
		cls.lock_file_name = lock_file_name	
	
	@classmethod	
	def is_lock(cls):
		lock_file_path = cls.info_dir_path+cls.lock_file_name
		result = file(lock_file_path).readline()
		lock = int(result)
		if lock:
			return True
		else:
			return False

	def writePic(self,user_id,pic_url):
		file_name = self.__class__.info_dir_path + str(user_id)+'.jpeg' 
		urlretrieve(pic_url,file_name)	
		
	def writeWeiboPic(self,pic_name,pic_url):
		file_name = self.__class__.info_dir_path + pic_name +'.jpeg' 
		urlretrieve(pic_url,file_name)	

	def writeWeibo(self,weibo_text):
		self.write_txt_file(self.__class__.weibo_file_name,formate_output(weibo_text.encode('utf-8')).decode('utf-8'))	
	
	def write_name(self,user_name):
		self.write_txt_file(self.__class__.user_name_file_name,user_name)

	def write_fiends_ids(self,id_list):
		ids_str = ''
		counter = 0
		id_list_len = len(id_list)
		for friend_id in id_list:
			counter += 1	
			ids_str += str(friend_id) 
			if counter < id_list_len:
				ids_str += ' '	 
 	      	self.write_txt_file(self.__class__.friends_ids_file_name,ids_str) 

	def write_txt_file(self,file_name,text):
		file_path = self.__class__.info_dir_path + file_name	
		text_file = file(file_path,'w')
		text_file.write(text.encode('gb2312'))
		text_file.close()
	
	def write_info(self,status_obj):
		self.writeWeibo(status_obj['text'])
		self.writePic(status_obj['user']['id'],status_obj['user']['profile_image_url'])
		self.writeWeiboPic("weibo_pic",status_obj['original_pic'])
		self.write_fiends_ids(status_obj['user']['fids'])
		self.write_name(status_obj['user']['name'])
		self.write_txt_file(self.__class__.lock_file_name,'1')	
