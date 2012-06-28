from requests.auth import HTTPBasicAuth
import requests
import json
import urllib
import uuid
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
			self.getFilteredStatements(_verb="created", _context=True)
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	
	def submitStatementList(self, jsonObjectList):
		for statement in jsonObjectList:
			
			try:
				print statement
				resp = requests.post(self._endpoint,
				            data=json.dumps(statement),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
				print resp
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
		url = self._endpoint +"?"
		statementJSON ={}
		if(_verb != None):
			url +="verb="+_verb+"&"
			statementJSON['verb'] = _verb
		if(_object != None):
			url +="object="+str(_object)+"&"
			statementJSON['object'] = _object
		if(_registration != None):
			url +="registration="+str(_registration)+"&"
			statementJSON['registration'] = _registration
		if(_context != None):
			url +="context="+str(_context)+"&"
			statementJSON['context'] = _context
		if(_actor != None):
			url +="actor="+str(_actor)+"&"
			statementJSON['actor'] = _actor
		if(_since != None):
			url +="since="+str(_since)+"&"
			statementJSON['since'] = _since
		if(_until != None):
			url +="until="+str(_until)+"&"
			statementJSON['until'] = _until
		if(_limit != None):
			url +="limit="+str(_limit)+"&"
			statementJSON['limit'] = _limit
		if(_authoritative != None):
			url +="authoritative="+str(_authoritative)+"&"
			statementJSON['authoritative'] = _authoritative
		if(_sparse != None):
			url +="sparse="+str(_sparse)+"&"
			statementJSON['sparse'] = _sparse
		if(_instructor != None):
			url +="instructor="+str(_instructor)
			statementJSON['instructor'] = _instructor
		if(url.endswith('&')):
			url = str(url[:-1])
			
		if (True):
			
			print type(statementJSON)
			print statementJSON
			resp = requests.post(self._endpoint,
						        data=statementJSON,
						        auth=HTTPBasicAuth(self._userName,self._secret))
			
			print resp.text
			return resp
		else:
			resp = requests.get(url,
								auth=HTTPBasicAuth(self._userName,self._secret),
								headers={"Content-Type":"application/json"})
			
			return resp
			