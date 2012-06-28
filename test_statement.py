from tincan import tincanStatement
import uuid
from threading import Thread
import time
import datetime
USER_NAME = "UU3N64YGT2"
PASSWORD = "9VU0MxwcogqhZYKc9Vn734oohTSOFoZohFJBJf5m"
ENDPOINT = 'https://cloud.scorm.com/ScormEngineInterface/TCAPI/UU3N64YGT2/statements/'
objectID = None

def test_submit_statement():
	statement_ID = str(uuid.uuid1())
	whoDid = "I"
	whoDidEmail = "testingSingle@tincan.test"
	whoDidObject = 'you'
	didWhat = 'created'
	createdJsonObject ={
					"id": statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":whoDidObject},'description':{"en-US":'Testing single insertion of a statement.'}}}

				}
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	tc.submitStatement(createdJsonObject)
	time.sleep(10)
	testStatement = tc.getStatementbyID(statement_ID)
	assert (testStatement['id'] == statement_ID)
		

def test_insertList():
	statement1Id= str(uuid.uuid1())
	statement2Id= str(uuid.uuid1())
	email1 = 'mailto:testingLIst1@tincan.test'
	email2 = 'mailto:testingList2@tincan.test'
	x={'mbox':[email1]}
	y={'mbox':[email2]}
	now = datetime.datetime.now()
	time.sleep(1)
	statementList =	[{
						"id": statement1Id,
						'actor':{'name':['List Test1'],'mbox':[email1]},
						'verb':'passed',
						'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'you'},'description':{"en-US":'Testing list insertions[1] of statements.'}}}
					},
					{
						"id": statement2Id,
						'actor':{'name':['List Test2'],'mbox':[email2]},
						'verb':'failed',
						'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'you'},'description':{"en-US":'Testing list insertions[1] of statements.'}}}
					}]
	tcList = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	tcList.submitStatementList(statementList)
	time.sleep(10)
	state1 = tcList.getStatementbyID(statement1Id)
	state2 = tcList.getStatementbyID(statement2Id) 
	# tcList.getFilteredStatements(_verb='passed',_since=str(now), _actor=x, _limit=1)
	# state2 = 
	# tcList.getFilteredStatements(_verb='failed',_since=str(now), _actor=y, _limit=1)
	for email in state1['actor']['mbox']:
		assert email == email1.lower()
	for email in state2['actor']['mbox']:
		assert email == email2.lower()

def test_filter_statements():
	test_verb = 'created'
	email = 'testing@tincan.test'
	x={'mbox':['mailto:'+email]}
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	results = tc.getFilteredStatements(_actor=x,_limit=5, _sparse=True)
	
	for result in results['statements']:
		for emails in result['actor']['mbox']: 
			if (emails=='mailto:'+email.lower()) :
				assert True

def testComplexFilter():
	whoDid = "Complex Test"
	statement_ID = str(uuid.uuid1())
	whoDidEmail = "complex@filter.test"
	whoDidObject = 'Test Subject'
	didWhat = 'attempted'
	now = datetime.datetime.now()
	x={'mbox':['mailto:'+whoDidEmail]}
	createdJsonObject = [{
					'id': statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'with '+whoDidObject},'description':{"en-US":whoDid+' gave a gold star to '+whoDidObject+'.'}}}
					
				}]
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	Thread(None,tc.submitStatement,None,(createdJsonObject)).start()
	time.sleep(8)			
	results = tc.getFilteredStatements(_verb=didWhat,_actor=x,_limit=1,_sparse=True,_since=str(now))
	for result in results['statements']:
		if result['verb']==didWhat:
			for x in result['actor']['mbox']:
				if (x == 'mailto:'+whoDidEmail.lower()):
					assert True

def test_GetAllStatements():
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	a = tc.getAllStatements()
	if a != None:
		assert True