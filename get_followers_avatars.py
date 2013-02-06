#!/usr/bin/python
#-*- coding:utf8 -*-
import util
import json
from urllib import urlretrieve
keys_obj = util.get_keys("keys.json")
util.Client.init(keys_obj['client_id'],keys_obj['client_secret'])
client = util.Client(keys_obj['username1'],keys_obj['password1'])
ids = client.get_somebody_follower_ids(keys_obj['who_follower_avatar'])
pic_url_list = []
for follower_id in ids:
	print 'id:'+str(follower_id)
	info = client.get_somebody_info(follower_id)
	try:
		#pic_url = info['profile_image_url']
		pic_url = info['avatar_large']
		pic_url_list.append(pic_url)
		urlretrieve(pic_url,'./heads/'+str(follower_id)+'.jpg')
	except:
		print 'err:'+str(follower_id)
		print 'msg:'+json.dumps(info)
		print '\n'
		continue
print 'picNum:'+str(len(pic_url_list))
