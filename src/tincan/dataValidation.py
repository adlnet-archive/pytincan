import re

def validateVerb(verb):
	##Builds a list of valid verbs
	valid_verbs=['experienced','attended','attempted','completed','passed','failed','answered','interacted','imported','created','shared','voided']	
	##Checks to see if the verb is in the valid_verbs list
	return verb.strip().lower() in valid_verbs

def validateAgent(agent):
	##Checks to see if the agent object contains the unique identifier email(mbox)
	email_regex = re.compile(r"^mailto:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
	if 'mbox' in agent:
		for email in agent['mbox']:
			if(not bool(email_regex.match(email))):
				return False
		return True