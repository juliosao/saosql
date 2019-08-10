#!/usr/bin/python

import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class About:
	def __init__(self,parent=None):  
		"""
		self.glade=glade.XML(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ui/about.glade'),None,None)
		self.glade.signal_autoconnect({
			'on_btnOK_clicked':self.on_btnOK_clicked,			
			})
		"""

		builder = gtk.Builder()
		builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ui/about.glade'))
		builder.connect_signals(self)
		self.dialog=builder.get_object('dlgAbout')
		if parent != None:
			self.dialog.set_transient_for(parent)
		          
	def show(self):	
		self.dialog.run()
		self.dialog.destroy()
		
	def hide(self):
		self.dialog.hide()
	
	def btnOK_clicked(self,b):
		self.result=False
		self.hide()
		

