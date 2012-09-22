#!/usr/bin/python
#-*- coding:utf8 -*-
import httplib
import urllib
import json

HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
access_token = ""

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
#	access_token = obj['access_token']

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
