import requests
from lxml import html
from bs4 import BeautifulSoup
import re
from string import *

def print_msg(msg, spaces=False):
	if spaces:
	    print ''
	    print msg
	    print ''
	else:
	    print msg
	
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
	return db
			
		
db = load_db('mtbf.db')	
print db
print_msg("db loaded", True)	
print_msg("Input component name:", True)
name = raw_input()
url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + name + "&ignorear=0&N=-1&isNodeId=1"
print url
r = requests.get(url)
print_msg("search for component...", True)
soup = BeautifulSoup(r.content, "html.parser")
#print soup
url_new = str(soup.find('div','items-view is-grid' ))
#i = url_new.find('<a class="items-title" href="') 
i = url_new.find('item-title') 
j = url_new.find('"', i+19) 
url_new=url_new[i+18:j]

print_msg('Url to this component on NewEgg:')
print_msg(url_new, True)

r2 = requests.get(url_new)
soup2 = BeautifulSoup(r2.content, "html.parser")
soup2 = str(soup2.find('ol', id="baBreadcrumbTop"))
comp_type = find_rec(soup2, 'title', 0)

print_msg('Name: ' + name)
print_msg('Tags:' )
for i in range(1,len(comp_type)):
	j = soup2.find('"',comp_type[i]+8)
	comp_type[i] = soup2[comp_type[i]+7:j].lower()
	print comp_type[i] 
	
result = {k: db[k] for k in db.viewkeys() & set(comp_type)}

print_msg(result.values(), True)	







