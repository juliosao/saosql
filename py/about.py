#!/usr/bin/python

import sys
import os
import gtk
from gtk import glade

class about:
	def __init__(self):  
		self.glade=glade.XML(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ui/about.glade'),None,None)
		self.glade.signal_autoconnect({
			'on_btnOK_clicked':self.on_btnOK_clicked,			
			})
		self.dialog=self.glade.get_widget("dlgAbout")
		          
	def show(self):	
		self.dialog.show()
		
	def hide(self):
		self.dialog.hide()
	
	def on_btnOK_clicked(self,b):
		self.result=False
		self.hide()
		
if __name__ == "__main__":
	p = connection()
	gtk.main()
