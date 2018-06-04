import sys
from PyQt5.QtWidgets import QApplication, QWidget
from slots import MainWindowSlots
import search
import design
import requests
from lxml import html
from bs4 import BeautifulSoup
import re
from string import *
from google import google
import sys
import codecs
import webbrowser

class MainWindow(MainWindowSlots):
	def __init__(self, form):
		self.setupUi(form)
		''' self.connect_slots()
   		 def connect_slots(self):
		name = self.lineEdit.text() 
        self.pushButton.clicked.connect(push_search(name))
        return None'''
		name = self.lineEdit.text() 
		self.pushButton.clicked.connect(self.push_search)

	def push_search(self):
		name = self.lineEdit.text() 
		print name
		self.status_changed('Search...')
		db = search.load_db('mtbf.db')
		print 'db_load'
		t = ''
		
		url_new, comp_type, soup2 = search.find_type_on_newegg(name)
		t += '<p>' + 'Link to component on NewEgg:' + '</p>'
		t += '<a href="' + url_new + '">' + url_new + "</a>"
		t += '<p>' + "\n\nComponent name: " + name  + '</p>'
		t += '<p>' + "\nComponent type: " + '</p>'
		default_mtbf, comp_type = search.find_default_mtbf(comp_type, soup2, db)
		t += ", ".join([str(x) for x in comp_type] )

		self.status_changed('Search MTBF in Google...')
		
		extra_tag = ''
		num_page=2
		
		if self.cb_mtbf.isChecked():
			extra_tag += 'MTBF MTTF'
		if self.cb_fit.isChecked():
			extra_tag += 'FIT failures in time'
		if self.cb_extra.isChecked():
			extra_tag += self.lineEdit_2.text() 
		
		s_e = str(self.comboBox.currentText())
		if s_e == 'Google':
			num_page = 1
			
		search_result = search.google_search(name, extra_tag, num_page)
		new_t = search.parse_mtbf(search_result)
		self.status_changed('Results:')
		print new_t
		t += new_t
		self.textBrowser.setText(t)
		self.mtbf_label.setText(default_mtbf)
		
	def status_changed(self, text):
		self.status_label.setText(text)
		
	
		
		
	
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = MainWindow(window)
    window.show()
    

		
	
    sys.exit(app.exec_())
