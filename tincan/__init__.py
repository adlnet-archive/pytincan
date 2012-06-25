from requests.auth import HTTPBasicAuth
import requests
import uuid
import json
class TinCan(object):
	def __init__(self,userName,secret,endpoint,logger=None):
		self.userName = userName
		self.secret = secret
		self.endpoint = endpoint
		self.logger = logger
	def sendToLRS(self,whoDid,whoDidEmail,didWhat,whoDidObject,hashtag,reason):
		#Call functions to get account variables
		statement_id = str(uuid.uuid1())
		objectID = str(uuid.uuid1())		
		#Creates the TinCan statement
		tc_star =[{
					"id":statement_id,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':objectID,'definition':{'name':{"en-US":'with '+ whoDidObject},'description':{"en-US":whoDid+' gave a gold star to '+whoDidObject+'.'}}},
					'context':{'extensions':{'Hashtag':'#'+hashtag, 'Reason':reason }}
				}]
		try:
			resp = requests.post(self.endpoint,
				            data=json.dumps(tc_star),
				            auth=HTTPBasicAuth(self.userName,self.secret),
				            headers={"Content-Type":"application/json"})
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
