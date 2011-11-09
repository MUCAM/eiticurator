try:
	ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	while 1:
		result_type, result_data = l.result(ldap_result_id, 0)
		if (result_data == []):
			break
		else:
			## here you don't have to append to a list
			## you could do whatever you want with the individual entry
			## The appending to list is just for illustration. 
			if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)
	print result_set
except ldap.LDAPError, e:
	print e
