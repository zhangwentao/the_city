#!/usr/bin/python
#-*- coding:utf8 -*-

import httplib
import urllib
import json

HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
access_token = ""
urlretrieve = urllib.urlretrieve

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

def api_proxy(api_url,param_obj={},method='GET'):
	conn = httplib.HTTPSConnection("api.weibo.com")  
	param=urllib.urlencode(param_obj)
	url = '/2/'+api_url+'.json?'
	if method == 'GET':
		conn.request(method,url+param)  
	elif method == 'POST':
		conn.request(method,url,param,HEADERS)  
	backen_data =conn.getresponse().read()  
	obj = json.loads(backen_data)
	return obj

def api_proxy_with_access_token(api_url,param_obj={},method='GET'):
	'''get data(object) from weibo http api with access token that was fore obtained.'''
	param_obj_inner ={'access_token':access_token}
	param_obj_inner.update(param_obj) 
	obj = api_proxy(api_url,param_obj_inner,method);
	return obj

def obtain_access_key(client_id,client_secret,usrname,passwd):
	access_token = get_access_token(client_id,client_secret,usrname,passwd)	

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

def status_cmp(a,b):
	a_id = int(a['id'])
	b_id = int(b['id'])
	if a_id > b_id:
		return 1
	elif a_id == b_id:
		return 0
	else:
		return -1

class Status_list():
	def __init__(self):
		self.status_list = []

	def put_in(self,new_list):
		new_list.sort(status_cmp)
		self.status_list.extend(new_list)				
		latest_status_id = new_list[len(new_list)-1]['id']
		return latest_status_id	

	def pop_oldest(self):
		self.status_list.pop()	
	
	def show(self):
		return self.status_list

class InfoWriter():
	info_dir_path = ''
	weibo_file_name = ''
	friends_ids_file_name = ''
	lock_file_name = ''				

	@classmethod
	def init(cls,info_dir_path,weibo_file_name,friends_ids_file_name,lock_file_name):
		cls.info_dir_path = info_dir_path
		cls.weibo_file_name = weibo_file_name
		cls.friends_ids_file_name = friends_ids_file_name
		cls.lock_file_name = lock_file_name	

	def writePic(self,user_id,pic_url):
		file_name = self.__class__.info_dir_path + user_id+'jpeg' 
		urlretrieve(pic_url,file_name)	
		
	def writeWeibo(self,weibo_text):
		self.write_txt_file(self.__class__.weibo_file_name,weibo_text)	
	
	def write_fiends_ids(self,id_list):
		ids_str = ''
		for friend_id in id_list:
			ids_str += (str(friend_id)+' ') 
 	      	write_txt_file(self.__class__.friends_ids_file_name,ids_str) 

	def write_txt_file(self,file_name,text):
		file_path = self.__class__.info_dir_path + file_name	
		file = file(file_path,'w')
		file.write((text).encode('gb2312'))
		file.close()
	
	def write_info(self,status_obj):
		self.writeWeibo(status_obj['text'])
		self.writePic(status_obj['user']['id'])
		self.write_fiends_ids(status_obj['user']['fids'])
		lock_file_path = self.__class__.info_dir_path+self.__class__.lock_file_path
		self.write_txt_file(lock_file_path,'1')	
	
	def is_lock():
		lock_file_path = self.__class__.info_dir_path+self.__class__.lock_file_path
		result = file(lock_file_path).readline()
		lock = int(result)
		if lock:
			return True
		else:
			return False
