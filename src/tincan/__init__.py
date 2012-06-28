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
		##Attempts to submit a single statement
		try:
			##Validates that the verb is valid
			if(not dataValidation.validateVerb(jsonObject['verb'])):
				raise ValueError("INVALID VERB: "+jsonObject['verb'])
			##Validates the statement has a unique identifier
			if(not dataValidation.validateAgent(jsonObject['actor'])):
				raise ValueError("NO ACTOR EMAIL")
			resp = requests.post(self._endpoint,
				            data=json.dumps(jsonObject),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
			
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
		except ValueError as e:
			if self.logger is not None:
				self.logger.error(e)
			else:
				print e


	def submitStatementList(self, jsonObjectList):
		##Submits a list of Statements
		for statement in jsonObjectList:	
			try:
				##Validates that the verb is valid
				if(not dataValidation.validateVerb(statement['verb'])):
					raise ValueError("INVALID VERB: "+statement['verb'])
				##Validates the statement has a unique identifier
				if(not dataValidation.validateAgent(statement['actor'])):
					raise ValueError("NO ACTOR EMAIL")

				resp = requests.post(self._endpoint,
				            data=json.dumps(statement),
				            auth=HTTPBasicAuth(self._userName,self._secret),
				            headers={"Content-Type":"application/json"})
			except IOError as e:
				if self.logger is not None:
					self.logger.error(e)
				else:
					print e
			except ValueError as e:
				if self.logger is not None:
					self.logger.error(e)
				else:	
					print e
		
	def getStatementbyID(self, ID):
		##Attempts to retrieve a statement by its ID
		try:
			url = self._endpoint+"?statementId="+ID
			resp = requests.get(url,
								auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getAllStatements(self):
		##Attempts to retrieve every TinCan Statement from the End point
		try:
			resp = requests.get(self._endpoint,
							auth=HTTPBasicAuth(self._userName,self._secret),
							headers={"Content-Type":"application/json"})
			return resp.json
		except IOError as e:
			if self.logger is not None:
				self.logger.error(e)
	def getFilteredStatements(self,_verb=None,_object=None,_registration=None,_context=None,_actor=None,_since=None,_until=None,_limit=None,_authoritative=None,_sparse=None,_instructor=None):
		queryObject ={}
		##Builds the statement query object
		if(_verb != None):
			queryObject['verb'] = _verb
		if(_object != None):
			queryObject['object'] = json.dumps(_object)
		if(_registration != None):
			queryObject['registration'] = _registration
		if(_context != None):
			queryObject['context'] = _context
		if(_actor != None):
			queryObject['actor'] = json.dumps(_actor)
		if(_since != None):
			queryObject['since'] = _since
		if(_until != None):
			queryObject['until'] = _until
		if(_limit != None):
			queryObject['limit'] = _limit
		if(_authoritative != None):
			queryObject['authoritative'] = _authoritative
		if(_sparse != None):
			queryObject['sparse'] = _sparse
		if(_instructor != None):
			queryObject['instructor'] = json.dumps(_instructor)
		##Encodes the query object into a query string
		url = self._endpoint +"?"+ urllib.urlencode(queryObject)
		##If the URL Length exceeds max URL length then query using post
		if (len(url)> 2048):	
			resp = requests.post(self._endpoint,
							    data=queryObject,
							    auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		else:
			resp = requests.get(url,
						    auth=HTTPBasicAuth(self._userName,self._secret))
			return resp.json
		

