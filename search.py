import requests
from lxml import html
from bs4 import BeautifulSoup
import re
from string import *
from google import google
import sys
import codecs


'''response = GoogleSearch().search("something")
for result in response.results:
    print("Title: " + result.title)
    print("Content: " + result.getText())'''

if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')
	

	
def print_msg(msg, spaces=False):
	if spaces:
	    print ''
	    print msg
	    print '' 
	else:
	    print msg
		
def print_line():
	print '\n_____________________________________________________________________\n'

def find_rec(p_from,p_subs,p_ind):
	l_next=find(p_from,p_subs,p_ind)
	if l_next==-1: 
		return []
	else: 
		return [l_next]+find_rec(p_from,p_subs,l_next+1)
	
def load_db(f):
	db = {}
	db_f = open(f, 'r')
	for line in db_f:
		words = line.split()
		db[words[0].lower()] = words[1]
	db_f.close()
	print_msg('Database loaded', True)
	return db
	
def google_search(name, extra_tags=None):
	def_tags = "MTBF MTTF"
	num_page = 1
	search_query = name + " " + def_tags
	search_results = google.search(search_query, num_page)
	first_res = search_results[0]
	return search_results
	
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def parse_mtbf(search_results):
	none_results = True
	print_msg('', True)
	for i in range(0,len(search_results)):
		if "MTBF" in search_results[i].description and hasNumbers(search_results[i].description):
				print_msg(search_results[i].description.encode('ascii', 'ignore'), True)
				print_msg(search_results[i].link.encode('ascii', 'ignore'))
				print_msg(u'', True)
				none_results = False
	if none_results:
		print_msg('None results fot MTBF characteristic')
	
def start_logo():
	print_msg('',True)	
	print_msg('MTBF search (alpha 0.1)\n______________________________________________________________')
	logo = " |  \/  |__   __|  _ \|  ____|                         | | \n | \  / |  | |  | |_) | |__     ___  ___  __ _ _ __ ___| |__ \n | |\/| |  | |  |  _ <|  __|   / __|/ _ \/ _` | '__/ __| '_ \ \n | |  | |  | |  | |_) | |      \__ \  __/ (_| | | | (__| | | |\n |_|  |_|  |_|  |____/|_|      |___/\___|\__,_|_|  \___|_| |_|\n"
	print(logo)

def valid_input():
	print_msg('Input component name:',True)
	name = raw_input()
	return name

def find_type_on_newegg(name):
	url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + name + "&ignorear=0&N=-1&isNodeId=1"
	r = requests.get(url)
	print_msg("search for component...", True)
	soup = BeautifulSoup(r.content, "html.parser")
	url_new = str(soup.find('div','items-view is-grid' ))
	i = url_new.find('item-title') 
	j = url_new.find('"', i+19) 
	url_new=url_new[i+18:j]

	print_msg('Url to this component on NewEgg:')
	print_msg(url_new, True)

	r2 = requests.get(url_new)
	soup2 = BeautifulSoup(r2.content, "html.parser")
	soup2 = str(soup2.find('ol', id="baBreadcrumbTop"))
	comp_type = find_rec(soup2, 'title', 0)
	return comp_type, soup2
	
	
start_logo()
db = load_db('mtbf.db')	
name = valid_input()
comp_type, soup2 = find_type_on_newegg(name)
print_msg('Name: ' + name)
print_msg('Tags:' )
pattern = re.compile(r'\w+')
for i in range(1,len(comp_type)):
	j = soup2.find('"',comp_type[i]+8)
	comp_type[i] = soup2[comp_type[i]+7:j].lower()
	comp_type[i] = pattern.findall(comp_type[i])[0]
	print(comp_type[i])
	
result = {k: db[k] for k in db.viewkeys() & set(comp_type)}
print_line()
if result:
	print_msg('MTBF of this components type equals ' + str(result.values()[0]) + ' hours', True)	
	print_line()
	
print_msg('Search MTBF data in Google ... ')
search_result = google_search(name)
parse_mtbf(search_result)
print_line() 







