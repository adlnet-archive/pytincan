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
			a = self.getFilteredStatements(_verb="interacted",_registration="1111-1111-1111-1111",_context=True,_actor={'name':"Steve"},_limit=30,_authoritative=False,_sparse=True,_instructor={'name':"Steve"})
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
	def getFilteredStatements(self,_verb=None,_object=None,_registration=None,_context=None,_actor=None,_since=None,_until=None,_limit=None,_authoritative=None,_sparse=None,_instructor=None):
		url = self._endpoint
		
		if(_verb != None):
			url +="?verb="+str(verb)+"&"
		
		if(_object != None):
			url +="?object="+str(_object)+"&"
		
		if(_registration != None):
			url +="?registration="+str(_registration)+"&"
		
		if(_context != None):
			url +="?context="+str(_context)+"&"
		
		if(_actor != None):
			url +="?actor="+str(_actor)+"&"
		
		if(_since != None):
			url +="?since="+str(_since)+"&"
		
		if(_until != None):
			url +="?until="+str(_until)+"&"
		
		if(_limit != None):
			url +="?limit="+str(_limit)+"&"
		
		if(_authoritative != None):
			url +="?authoritative="+str(_authoritative)+"&"
		
		if(_sparse != None):
			url +="?sparse="+str(_sparse)+"&"
		
		if(_instructor != None):
			url +="?instructor="+str(_instructor)+"&"

		if(url.endswith("&")):
			url[:-1]

		return url