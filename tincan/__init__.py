from requests.auth import HTTPBasicAuth
import requests
import json
import urllib
class tincanStatement(object):
	def __init__(self,userName,secret,endpoint,objectID,logger=None):
		self._userName = userName
		self._secret = secret
		self._endpoint = endpoint
		self._objectID =objectID
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
	def getLastStatement(self):
		try:
			url = self._endpoint+"?statementId="+self._objectID
			resp = requests.get(url,
							auth=HTTPBasicAuth(self._userName,self._secret),
							headers={"Content-Type":"application/json"})
			return resp
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getStatementbyID(self, ID):
		try:
			url = self._endpoint+"?statementId="+ID
			resp = requests.get(url,
							auth=HTTPBasicAuth(self._userName,self._secret),
							headers={"Content-Type":"application/json"})
			return resp
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getAllStatements(self):
		try:
			resp = requests.get(self._endpoint,
							auth=HTTPBasicAuth(self._userName,self._secret),
							headers={"Content-Type":"application/json"})
			return resp
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
