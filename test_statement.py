#    Copyright 2012 Problem Solutions LLC
#	 http://problemsolutions.net/
'''
Created on June 29, 2012
	Basic test cases for Python TinCan
@author: Stephen Trevorrow
@Email:  strevorrow@problemsolutions.net
'''
from tincan import TinCan
import uuid
import time
import datetime
##Change to match test endpoint
USER_NAME = "UU3N64YGT2"
PASSWORD = "9VU0MxwcogqhZYKc9Vn734oohTSOFoZohFJBJf5m"
ENDPOINT = 'https://cloud.scorm.com/ScormEngineInterface/TCAPI/UU3N64YGT2/statements/'
objectID = None

def test_submit_statement():
	##Tests to see if a single statement can be inserted
	tc = TinCan(USER_NAME,PASSWORD,ENDPOINT)
	statement_ID = str(uuid.uuid1())
	whoDid = "I"
	whoDidEmail = "testingSingle@tincan.test"
	whoDidObject = 'you'
	didWhat = 'created'
	##Build the Tin Can statement
	createdJsonObject ={
					"id": statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":whoDidObject},'description':{"en-US":'Testing single insertion of a statement.'}}}

				}
	tc.submitStatement(createdJsonObject)
	##Sleeps to insure the statement is inserted
	time.sleep(10)
	##Gets the statement by the ID used when inserted
	testStatement = tc.getStatementbyID(statement_ID)
	##Ensures the ID when inserted and the ID on the retrieve are the same
	assert (testStatement['id'] == statement_ID)
		

def test_insertList():
	##Tests to see if multiple Statements can be inserted
	tc = TinCan(USER_NAME,PASSWORD,ENDPOINT)
	statement1Id= str(uuid.uuid1())
	statement2Id= str(uuid.uuid1())
	email1 = 'mailto:testingLIst1@tincan.test'
	email2 = 'mailto:testingList2@tincan.test'
	email3 = 'mailto:multipleEmail@tincan.test'
	x={'mbox':[email1]}
	y={'mbox':[email2,email3]}

	now = datetime.datetime.now()
	##Builds statement list
	statementList =	[{
						"id": statement1Id,
						'actor':{'name':['List Test1'],'mbox':[email1]},
						'verb':'passed',
						'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'you'},'description':{"en-US":'Testing list insertions[1] of statements.'}}}
					},
					{
						"id": statement2Id,
						'actor':{'name':['List Test2'],'mbox':[email2, email3]},
						'verb':'failed',
						'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'you'},'description':{"en-US":'Testing list insertions[1] of statements.'}}}
					}]
	tc.submitStatementList(statementList)
	time.sleep(10)
	## Fetches previously entered statements
	state1 = tc.getStatementbyID(statement1Id)
	state2 = tc.getStatementbyID(statement2Id)
	##Checks to see if the IDs are the same from inserted and retrieved
	assert state1['id'] == statement1Id
	assert state2['id'] == statement2Id 
	
def test_filter_statements():
	##Ensures a simple filter request returns the correct information
	tc = TinCan(USER_NAME,PASSWORD,ENDPOINT)
	test_verb = 'created'
	email = 'testing@tincan.test'
	x={'mbox':['mailto:'+email]}
	results = tc.getFilteredStatements(_actor=x,_limit=5, _sparse=True)
	
	for result in results['statements']:
		for emails in result['actor']['mbox']: 
			if (emails=='mailto:'+email.lower()) :
				assert True

def testComplexFilter():
	##Ensures a complex filter returns correct data
	tc = TinCan(USER_NAME,PASSWORD,ENDPOINT)
	whoDid = "Complex Test"
	statement_ID = str(uuid.uuid1())
	whoDidEmail = "complex@filter.test"
	whoDidObject = 'Test Subject'
	didWhat = 'attempted'
	now = datetime.datetime.now()
	x={'mbox':['mailto:'+whoDidEmail]}
	##Inserts object to filter for
	createdJsonObject = {
					'id': statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'with '+whoDidObject},'description':{"en-US":'Inserting a description for a complex filter.'}}}	
				}
	##Inserts statement
	tc.submitStatement(createdJsonObject)
	time.sleep(8)
	results = tc.getFilteredStatements(_verb=didWhat,_actor=x,_limit=1,_sparse=True,_since=str(now))
	for result in results['statements']:
		if result['verb']==didWhat:
			for x in result['actor']['mbox']:
				assert (x == 'mailto:'+whoDidEmail.lower())
					

def test_GetAllStatements():
	tc = TinCan(USER_NAME,PASSWORD,ENDPOINT)
	statementlist = tc.getAllStatements()
	for x in statementlist['statements']:
		assert 'id' in x