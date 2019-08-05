#!/usr/bin/python

import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class connection:
	def __init__(self,parent):  
		builder = gtk.Builder()
		builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ui/connection.glade'))
		builder.connect_signals(self)
		self.dialog=builder.get_object('dlgConnection')
		print self.dialog

		self.parent=parent
		self.host=builder.get_object
		self.port=builder.get_object
		self.database=builder.get_object
		self.user=builder.get_object
		self.password=builder.get_object
		self.result=builder.get_object
          
	def show(self):	
		self.dialog.show()
		
	def hide(self):
		self.dialog.hide()
		self.dialog.destroy()

	def on_btnConectar_clicked(self,b):
		self.host=self.glade.get_widget('txtHost').get_text()
		self.port=self.glade.get_widget('txtPuerto').get_text()
		self.database=self.glade.get_widget('txtBaseDatos').get_text()
		self.user=self.glade.get_widget('txtUsuario').get_text()
		self.password=self.glade.get_widget('txtPass').get_text()
		self.result=True
		self.hide()
		print "Iniciando callback..."
		self.parent.conectar(self.host,self.port,self.database,self.user,self.password);
		
	
	def on_btnCancelar_clicked(self,b):
		self.result=False
		self.hide()		
		print "no-conectando..."
		
if __name__ == "__main__":
	p = connection(None)
	p.show()

	gtk.main()
