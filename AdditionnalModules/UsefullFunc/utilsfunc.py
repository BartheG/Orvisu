import os

#Find file recursively starting in 'path' directory
def find(name, path):
	for root, _, files in os.walk(path):
		if name in files:
			return os.path.join(root, name)
	return False

#Find files corresponding to a pattern
import fnmatch
def findMatch(name,path):
	paths=[]
	for root, _, files in os.walk(path):
		[paths.append(os.path.join(root, i)) for i in files if fnmatch.fnmatch(i, name)]
	return paths

#Sort list by name ascending
import re
def sortByName(data):
	if type(data)!=list:
		raise TypeError
	if len(data)<=0:
		raise IndexError
	data_w_idx={ key:float(re.findall(r'\d+',i)[-1]) for key,i in enumerate(data) }
	sorted_x = sorted(data_w_idx.items(), key=lambda kv: kv[1])
	return [data[i] for i in dict(sorted_x).keys()]