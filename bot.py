import requests
from requests.auth import HTTPBasicAuth
import json
import re
import sys
import logging

API_END = 'http://127.0.0.1:8000/'

#No auth
#API_KEY = 'password123'
#username = 'admin'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('stages.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_response(q_no,url):
	response = requests.get(API_END+url+str(q_no)+'/')#,auth=HTTPBasicAuth(username,API_KEY))
	if response.status_code in [201,200]:
		r = response.json()[0]
		r['questions'] = eval(r['questions'])
		return r['questions']
	else:
		return {'error':'error'}

def post_response(url,data):
	response = requests.post(API_END+url,data ={key:str(value) for key,value in data.items()})#auth=HTTPBasicAuth(username,API_KEY)
	if response.status_code in [201,200]:
		return response.json()
	else:
		return {'error':'error'}

def read_json(filename):
	f = open(filename)
	d = json.load(f)
	d.pop('function')
	return d['questions']

def initialize():
	print("Choose Track")
	choice = input("Press 1 for Track 1 (assignment_1_input_1.json) \n Press 2 for Track 2 (assignment_1_input_2.json)\n")
	if choice == '1':
		q = read_json('assignment_1_input_1.json')
	elif choice == '2':
		q = read_json('assignment_1_input_2.json')

	print("Preparing the bot...")

	c = 0
	for i in q:
		k = {'questions':i,'q_no':c}
		post_response('question/',k)
		c+=1
	print("Bot Created..!")	
	print('*'*78)

def botty(instruction_no):

	instr_dict = get_response(instruction_no,'query/')
	keys = instr_dict.keys()
	if 'text' in keys:
		print(instr_dict['text'])
		if 'options' in keys:
			print(instr_dict['options'])
		t = input()
		globals()[instr_dict['var']] = t
		variables = (instr_dict['var'],t)
		instruction_no+=1
	return variables	


def botty_2(instruction_no,variables):
	instr_dict = get_response(instruction_no,'query/')
	keys = instr_dict.keys()

	if 'instruction' in keys:
		if 'instruction_var' in keys:
			ins_var = (i for i in instr_dict['instruction_var'])
			ins = instr_dict['instruction']%(ins_var)	
		else:
			ins = instr_dict['instruction_no']
		print(ins)

	if 'text' in keys:
		print(instr_dict['text'])

		if 'options' in keys:
			print(instr_dict['options'])

		if 'var' in keys:
			globals()[instr_dict['var']] = input()
			variables.append((instr_dict['var'],eval(instr_dict['var'])))
		
		if 'conditions' in keys:
			cond = instr_dict['conditions']



	return variables		


def main_2():
	variables = []
	variables = botty_2(1,variables)


def main():
	instruction_no = 0
	instr_dict = get_response(instruction_no,'query/')
	keys = instr_dict.keys()
	variables = []

	if 'instruction' in keys:
		print(instr_dict['instruction'])
		if len(keys)==1:
			instruction_no+=1
	
	for _ in range(3):
		variables.append(botty(instruction_no))
		instruction_no+=1

	#age
	c = 0
	while True:
		instr_dict = get_response(instruction_no,'query/')
		keys = instr_dict.keys()
		if 'text' in keys:
			if c==0:
				print(instr_dict['text'])
			if 'var' in keys:
				t = input()
				globals()[instr_dict['var']] = t
		instruction_no+=1
		c+=1

		instr_dict_2 = get_response(instruction_no,'query/')
		cond = instr_dict_2['conditions'][0][0]
		if not eval(cond):
			break
		else:
			instruction_no-=1
			print(instr_dict_2['text'])
			continue	
	variables.append((instr_dict['var'],t))	
	instruction_no+=1		
	
	instr_dict = get_response(instruction_no,'query/')		
	print(instr_dict['instruction'])
	instruction_no+=1


	data = {}
	for v in variables:
		if v[0] in ['first_name','last_name','gender','age']:
			data[v[0]] = v[1]
	post_response('details/',data)
	


	#name and stuff
	try:
		instr_dict = get_response(instruction_no,'query/')		
		keys = instr_dict.keys()
		globals()[instr_dict['var']] = eval(instr_dict['formula'])
		instruction_no+=1
		variables.append((instr_dict['var'],eval(instr_dict['formula'])))
		


		instr_dict = get_response(instruction_no,'query/')		
		keys = instr_dict.keys()
		if 'instruction_var' in keys:
			print(instr_dict['instruction']%(variables[-1][1]))
		instruction_no+=1	

		#matrix setup
		instr_dict = get_response(instruction_no,'query/')		
		keys = instr_dict.keys()
		globals()[instr_dict['var']] = eval(instr_dict['formula'])
		instruction_no+=1
		v = instr_dict['var']

		for _ in range(3):
			instr_dict = get_response(instruction_no,'query/')		
			keys = instr_dict.keys()
			print(instr_dict['text'])
			t = input()
			eval(v).append(t)
			instruction_no+=1
		variables.append((v,eval(v)))		
		
		#formula and transpose
		for _ in range(2):
			instr_dict = get_response(instruction_no,'query/')
			globals()[instr_dict['var']] = eval(instr_dict['formula'])
			variables.append((instr_dict['var'],eval(instr_dict['formula'])))
			instruction_no+=1

		instr_dict = get_response(instruction_no,'query/')		
		print(instr_dict['instruction'])
		instruction_no+=1	

		#Display transpose
		instr_dict = get_response(instruction_no,'query/')	
		for i in range(int(instr_dict['list_length'])):
			a = eval(instr_dict['instruction_var'][0])
			b = eval(instr_dict['instruction_var'][1])
			print(instr_dict['instruction']%(a,b))
	except:
		pass		
	print("GoodBye!")		

def delete():
	response = requests.get(API_END+'delete/')#,auth=HTTPBasicAuth(username,API_KEY))


if __name__ == '__main__':
	initialize()
	main_2()
	delete()