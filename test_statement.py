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
	whoDid = "Me"
	whoDidEmail = "testing@tincan.test"
	whoDidObject = 'you'
	didWhat = 'created'
	createdJsonObject =[{
					"id": statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'with '+whoDidObject},'description':{"en-US":whoDid+' gave a gold star to '+whoDidObject+'.'}}}

				}]
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	Thread(None,tc.submitStatement,None,(createdJsonObject)).start()
	time.sleep(10)
	testStatement = tc.getStatementbyID(statement_ID)
	if testStatement['id'] == statement_ID:
		assert True

def test_filter_statements():
	test_verb = 'created'
	email = 'testing@tincan.test'
	x={'mbox':['mailto:'+email]}
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	results = tc.getFilteredStatements(_actor=x,_limit=5, _sparse=True)
	
	for result in results['statements']:
		for emails in result['actor']['mbox']: 
			if (emails=='mailto:'+email) :
				assert True

def testComplexFilter():
	whoDid = "Complex Test"
	statement_ID = str(uuid.uuid1())
	whoDidEmail = "complex@filter.test"
	whoDidObject = 'Test Subject'
	didWhat = 'attempted'
	now = datetime.datetime.now()
	x={'mbox':['mailto:'+whoDidEmail]}
	createdJsonObject =[{
					'id': statement_ID,
					'actor':{'name':[whoDid],'mbox':['mailto:'+whoDidEmail]},
					'verb':didWhat,
					'object':{'id':str(uuid.uuid1()),'definition':{'name':{"en-US":'with '+whoDidObject},'description':{"en-US":whoDid+' gave a gold star to '+whoDidObject+'.'}}},
					
				}]
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	Thread(None,tc.submitStatement,None,(createdJsonObject)).start()
	time.sleep(8)			
	results = tc.getFilteredStatements(_verb=didWhat,_actor=x,_limit=1,_sparse=True,_since=str(now))
	for result in results['statements']:
		if result['verb']==didWhat:
			print result
			for x in result['actor']['mbox']:
				if (x == 'mailto:'+whoDidEmail):
					assert True
					
def test_GetAllStatements():
	tc = tincanStatement(USER_NAME,PASSWORD,ENDPOINT)
	a = tc.getAllStatements()
	if a != None:
		assert True