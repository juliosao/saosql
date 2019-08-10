#!/usr/bin/python

import sys
import os
import gi
import MySQLdb
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class Connection:
	def __init__(self,parent=None):  
		builder = gtk.Builder()
		builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ui/connection.glade'))
		builder.connect_signals(self)
		

		self.dialog=builder.get_object('dlgConnection')			
		self.host=builder.get_object('txtHost')
		self.port=builder.get_object('txtPort')
		self.database=builder.get_object('txtDatabase')
		self.user=builder.get_object('txtUser')
		self.password=builder.get_object('txtPassword')
		self.lblStatus=builder.get_object('lblStatus')
		self.result=None
          
	def show(self):	
		self.dialog.run()
		self.dialog.destroy()
		return self.result
		
	def on_btnConectar_clicked(self,b):
		try:
			host=self.host.get_text()
			port=self.port.get_text()
			database=self.database.get_text()
			user=self.user.get_text()
			password=self.password.get_text()

			self.lblStatus.show()
			self.result = MySQLdb.connect(host=host,user=user,passwd=password,db=database,port=int(port))		
			if self.result == None:
				dlg = gtk.MessageDialog(self.dialog, 0, gtk.MessageType.ERROR, gtk.ButtonsType.OK, "Cannot connect to %s:%s@%s" % (user,database,host))
				dlg.set_title("Error")
				dlg.run()
				dlg.destroy()
			self.dialog.hide()
		except Exception as ex:
			dlg = gtk.MessageDialog(self.dialog, 0, gtk.MessageType.ERROR, gtk.ButtonsType.OK, str(ex))
			dlg.set_title("Error")
			dlg.run()
			dlg.destroy()
			self.lblStatus.hide()
		
	
	def on_btnCancelar_clicked(self,b):
		self.result=None
		self.dialog.hide()		
		
		
if __name__ == "__main__":
	p = Connection(None)
	r = p.show()
	sys.exit(0 if r != None else 1)
