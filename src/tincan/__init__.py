from requests.auth import HTTPBasicAuth
import requests
import json
import urllib
import uuid
import dataValidation
class tincanStatement(object):
	def __init__(self,userName,secret,endpoint,logger=None):
		self._userName = userName
		self._secret = secret
		self._endpoint = endpoint
		self.logger = logger
		
	def submitStatement(self, jsonObject):	  
		try:
			if(not dataValidation.validateVerb(jsonObject['verb'])):
				raise ValueError(jsonObject['verb'])
			resp = requests.post(self._endpoint,
				            data=json.dumps(jsonObject),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
			print resp.json
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
		except ValueError as e:
			if self.logger is not None:
				self.logger.error("INVALID VERB: "+str(e)+" is not a valid verb.")
			print "INVALID VERB: "+str(e)+" is not a valid verb."


	def submitStatementList(self, jsonObjectList):
		for statement in jsonObjectList:	
			try:
				if(not dataValidation.validateVerb(statement['verb'])):
					raise ValueError(statement['verb'])
				resp = requests.post(self._endpoint,
				            data=json.dumps(statement),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
			except IOError as e:
				if self.logger is not None:
					self.logger.error(e)
			except ValueError as e:
				if self.logger is not None:
					self.logger.error("INVALID VERB: "+e+" is not a valid verb.")
				print "INVALID VERB: "+str(e)+" is not a valid verb."
		
	def getStatementbyID(self, ID):
		try:
			url = self._endpoint+"?statementId="+ID

			resp = requests.get(url,
								auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getAllStatements(self):
		try:
			resp = requests.get(self._endpoint,
							auth=HTTPBasicAuth(self._userName,self._secret),
							headers={"Content-Type":"application/json"})
			return resp.json
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getFilteredStatements(self,_verb=None,_object=None,_registration=None,_context=None,_actor=None,_since=None,_until=None,_limit=None,_authoritative=None,_sparse=None,_instructor=None):
		statementJSON ={}
		if(_verb != None):
			statementJSON['verb'] = _verb
		if(_object != None):
			statementJSON['object'] = json.dumps(_object)
		if(_registration != None):
			statementJSON['registration'] = _registration
		if(_context != None):

			statementJSON['context'] = _context
		if(_actor != None):

			statementJSON['actor'] = json.dumps(_actor)

		if(_since != None):

			statementJSON['since'] = _since
		if(_until != None):

			statementJSON['until'] = _until
		if(_limit != None):

			statementJSON['limit'] = _limit
		if(_authoritative != None):

			statementJSON['authoritative'] = _authoritative
		if(_sparse != None):

			statementJSON['sparse'] = _sparse
		if(_instructor != None):

			statementJSON['instructor'] = json.dumps(_instructor)
		
		url = self._endpoint +"?"+ urllib.urlencode(statementJSON)
		if (len(url)> 2048):	
			resp = requests.post(self._endpoint,
							    data=statementJSON,
							    auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		else:
			resp = requests.get(url,
						    auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		

