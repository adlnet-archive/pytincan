def validateVerb(verb):
	valid_verbs=['experienced','attended','attempted','completed','passed','failed','answered','interacted','imported','created','shared','voided']	
	return verb.strip().lower() in valid_verbs
