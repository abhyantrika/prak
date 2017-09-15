import requests
from requests.auth import HTTPBasicAuth
import json
import re
import sys
import logging
import csv

API_END = 'http://127.0.0.1:8000/'
API_KEY = 'password123'
username = 'admin'



def admin_get_details():
	response = requests.get(API_END+'details/')#,auth=HTTPBasicAuth(username,API_KEY))
	if response.status_code in [201,200]:
		return response.json()
	else:
		return{'error':'error'}

def main():
	details = admin_get_details()
	headers = details[0].keys()
	try:
		with open('admin.csv','w') as file_admin:
			dw = csv.DictWriter(file_admin,delimiter = '\t',fieldnames = headers)
			dw.writeheader()
			for d in details:
				if d['gender'] == True:
					d['gender'] = "Male"
				else:
					d['gender'] = "Female"
				dw.writerow(d)
		sys.stdout.writelines("CSV file with details of users created!!\n")
		sys.stdout.flush()
	except:
		sys.stdout.writelines("Error in CSV creation.Maybe number of entries is NULL\n")
		sys.stdout.flush()

if __name__ == '__main__':
	main()				