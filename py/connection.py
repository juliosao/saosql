#!/usr/bin/python

import sys
import gtk
import os
from gtk import glade

class connection:
	def __init__(self,parent):  
		self.glade=glade.XML(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ui/connect.glade'),None,None)
		self.glade.signal_autoconnect({
			'on_btnConectar_clicked':self.on_btnConectar_clicked,
			'on_btnCancelar_clicked':self.on_btnCancelar_clicked,
			})
		self.parent=parent
		self.dialog=self.glade.get_widget("frmConect");
		self.host=None
		self.port=None
		self.database=None
		self.use=None
		self.password=None
		self.result=False
          
	def show(self):	
		self.dialog.show();
		
	def hide(self):
		self.dialog.hide();

	def on_btnConectar_clicked(self,b):
		self.host=self.glade.get_widget('txtHost').get_text()
		self.port=self.glade.get_widget('txtPuerto').get_text()
		self.database=self.glade.get_widget('txtBaseDatos').get_text()
		self.user=self.glade.get_widget('txtUsuario').get_text()
		self.password=self.glade.get_widget('txtPass').get_text()
		self.result=True;
		self.hide();
		print "Iniciando callback..."
		self.parent.conectar(self.host,self.port,self.database,self.user,self.password);
		
	
	def on_btnCancelar_clicked(self,b):
		self.result=False;
		self.hide();
		print "no-conectando..."
		
if __name__ == "__main__":
	p = connection()
	gtk.main()
