def validateVerb(verb):
	##Builds a list of valid verbs
	valid_verbs=['experienced','attended','attempted','completed','passed','failed','answered','interacted','imported','created','shared','voided']	
	##Checks to see if the verb is in the valid_verbs list
	return verb.strip().lower() in valid_verbs
