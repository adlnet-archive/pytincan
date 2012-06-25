from requests.auth import HTTPBasicAuth
import requests
import json
class tincanStatement(object):
	def __init__(self,userName,secret,endpoint,logger=None):
		self._userName = userName
		self._secret = secret
		self._endpoint = endpoint
		self.logger = logger
	

	def submitStatement(self, jsonObject):	  

		try:
			resp = requests.post(self._endpoint,
				            data=json.dumps(jsonObject),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
			return resp

		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)	

