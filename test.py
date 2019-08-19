import os
import sys
import json

with open('config.json.test') as jf:
	data = json.load(jf)
	#base = json.loads(data["Base"])
	for key,value in data["Basic"].items():
		print key,value,type(value)
