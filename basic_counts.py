#this module does simple counts of various fields from the file metadata

#returns a count of unique user IDs
def count_unique_users(file_dict):
	dict={}
	keys=file_dict.iterkeys()
	for key in keys:
		metadata=file_dict[key]
		datapoint=metadata["user_id"]
		if dict.has_key(datapoint):
			pass
		else:
			dict[datapoint]=0
	unique_count=len(dict)
	return unique_count
	

def count_unique_groups(file_dict):
	dict={}
	keys=file_dict.iterkeys()
	for key in keys:
		metadata=file_dict[key]
		datapoint=metadata["group_id"]
		if dict.has_key(datapoint):
			pass
		else:
			dict[datapoint]=0
	unique_count=len(dict)
	return unique_count


def count_total_files(file_list):
	file_count=len(file_list)
	return file_count


	

