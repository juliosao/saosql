#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import string
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject


import connection
import about

class pyGtkSql:
	count=0
	
	def __init__(self,database=None): 
		builder = gtk.Builder()
		builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ui/main.glade'))
		builder.connect_signals(self) 

		self.window=builder.get_object('main')
		#self.clipboard = gtk.Clipboard(selection="CLIPBOARD")
		self.txtSQL = builder.get_object("txtSQL")
		self.treResultado=builder.get_object("treResult")
		self.txtLog=builder.get_object("txtLogs")
		self.tabPages=builder.get_object("tabPages")
		self.treStructure=builder.get_object("treStructure")
		self.connection=None		
		self.filename=None
		pyGtkSql.count+=1

		if database == None:
			c = connection.Connection(None)
			self.db = c.show()
		else:
			self.db=database

		if self.db != None:
			self.loadDBStructure()
		

	def show(self):
		self.window.set_default_size(800, 600)
		self.window.show()		
	
	def close(self,sender):					
		self.window.destroy()
		pyGtkSql.count-=1
		if pyGtkSql.count==0:
			gtk.main_quit()
	
	def showAbout(self,sender):
		a=about.About(self)
		a.show()

	def log(self,texto):
		buff=self.txtLog.get_buffer()
		buff.insert(buff.get_end_iter(),texto+'\n')
		self.txtLog.scroll_to_iter(buff.get_end_iter(),0,True,0,1)

	def loadDBStructure(self):
		if self.db:
			try:			
				cursor=self.db.cursor(MySQLdb.cursors.Cursor)
				cursor.execute("SHOW TABLES")
				resultado=cursor.fetchall()

				if type(resultado) is tuple:		
					self.store = gtk.TreeStore(str, str, str)

					self.log("Obtenida informacion de estructura de la base de datos");										
							
					for fila in resultado:
						self.log(fila[0])
						self.store.append([fila[0],[]])
									
					self.treStructure.set_model(self.store)
										
					cell = gtk.CellRendererText()
					tables = gtk.TreeViewColumn("Table", cell, text=0)
					cell = gtk.CellRendererText()
					types = gtk.TreeViewColumn("Type", cell, text=0)
					cell = gtk.CellRendererText()
					extras = gtk.TreeViewColumn("Extras", cell, text=0)
					self.treStructure.append_column(tables)
					self.treStructure.append_column(types)
					self.treStructure.append_column(extras)

					self.treStructure.pack_start(cell, True)

					self.tabPages.set_current_page(1)
					self.log("Consulta OK")
				else:
					self.db.commit()
					self.log("La consulta no devolvio resultados")
					self.tabPages.set_current_page(2)
					
				cursor.close

			except Exception, e:
				print(e)
				self.log(str(e))
				self.tabPages.set_current_page(2)

	def runQuery(self,sender):
		pass
	"""
	def msgbox(self,titulo,texto,accept=True,cancel=False):
		dialog = gtk.MessageDialog(	None, gtk.DIALOG_MODAL)
		dialog.set_title(titulo)
		dialog.set_markup(texto)
		dialog.shift=False
		
		if accept:
			dialog.add_button(gtk.STOCK_OK,gtk.RESPONSE_OK)
				
		if cancel:
			dialog.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL)
		
		res=dialog.run()
		dialog.destroy()
		return res
		
	
	def mostrarAcerca(self,sender):
		a=about.about()
		a.show()

	def on_btnConectar_clicked(self,b):
		self.connection=connection.connection(self)
		self.connection.show()
		print "saliendo del dialogo..."
	
	def on_btnDesconectar_clicked(self,b):
		if(self.db):
			self.db.close()
			
		self.db=None
		self.log("desconectado")
		self.msgbox("Desconectado","Desconexion completada")

	def on_btnEjecutar_clicked(self,b):
		if self.db:
			try:			
				buff=self.txtSQL.get_buffer()
				
				sql=''
				bounds=buff.get_selection_bounds()
				if len(bounds) == 2:				
					sql=buff.get_text(bounds[0],bounds[1],True)				
				else:
					start=buff.get_start_iter()
					end=buff.get_end_iter()
					sql=buff.get_text(start,end,True)

				self.log("Ejecutando consulta:"+sql);

				cursor=self.db.cursor(MySQLdb.cursors.Cursor)
				cursor.execute(sql)
				resultado=cursor.fetchall()
				
				for columna in self.treResultado.get_columns():
					self.treResultado.remove_column(columna);

				if resultado:		
					self.log("Consulta ejecutada correctamente");
					
					self.treResultado.set_model(None)
					columnasmodelo=[]						
					i=0
					
					for desc in cursor.description:
						columnasmodelo.append(gobject.TYPE_STRING)
						col=gtk.TreeViewColumn(desc[0],gtk.CellRendererText(),text=i);
						self.treResultado.append_column(col);
						i+=1;
					
					self.store=	gtk.ListStore(*columnasmodelo)						
					
					for fila in resultado:
						valores=self.astrings(fila)		
						self.store.append(valores)	
						
					self.treResultado.set_model(self.store)
					self.tabPaginas.set_current_page(1)
				else:
					self.db.commit()
					self.log("La consulta no devolvio resultados")
					self.tabPaginas.set_current_page(2)
					
				cursor.close

			except Exception, e:
				print(e)
				self.log(str(e))
				self.tabPaginas.set_current_page(2)
		else:
			self.msgbox("Error","Necesita conectarse a una base de datos para poder ejecutar consultas")
				
	def astrings(self,lista):
		lista2=list()
		for s in lista:
			lista2.append(str(s))
		
		return tuple(lista2)
		
	def conectar(self,maquina,puerto,basedatos,usuario,passw):
		try:
			self.log("Iniciando conexion con '"+maquina+"' db='"+basedatos+"'")
			self.db = MySQLdb.connect(host=maquina,user=usuario,passwd=passw,db=basedatos,port=int(puerto))
			if self.db:
				self.log("Conexión realizada")
				dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
											   gtk.MESSAGE_QUESTION,
											   gtk.BUTTONS_OK, "Conexion realizada");
				dialog.run()
				dialog.destroy()
				self.cargaTablas()
				

			else:
				self.log("Conexión fallida:"+str(self.db.error()))
				self.msgbox("Error al conectar","Detalles del error:\n"+str(self.db.error()))
				self.tabPaginas.set_current_page(2)
		except Exception, e:
			self.log(str(e))
			self.tabPaginas.set_current_page(2)
			self.msgbox("Error al conectar","Detalles del error:\n"+str(e))
	
	def salir(self,sender):
		if(self.db):
			self.db.close()
			
		self.ventana.destroy()
		pyGtkSql.contador-=1
		if pyGtkSql.contador==0:
			gtk.main_quit()
	
	
	def log(self,texto):
		buff=self.txtLog.get_buffer()
		buff.insert(buff.get_end_iter(),texto+'\n')
		self.txtLog.scroll_to_iter(buff.get_end_iter(),0,True,0,1)
	
	def copiar(self,sender):
		buff=self.txtSQL.get_buffer()
		bounds = buff.get_selection_bounds()
		if bounds:		
			self.clipboard.set_text(str(buff.get_text(bounds[0],bounds[1])))
		
	def cortar(self,sender):
		buff=self.txtSQL.get_buffer()
		bounds = buff.get_selection_bounds()
		if bounds:		
			self.clipboard.set_text(str(buff.get_text(bounds[0],bounds[1])))
			buff.delete(bounds[0],bounds[1])
		
	def pegar(self,sender):
		self.clipboard.request_text(self.pasteCallback)
		
	def pasteCallback(self, clipboard, text, data):
		buff=self.txtSQL.get_buffer()
		bounds = buff.insert_at_cursor(text);
	
	def nuevo(self,sender):
		n=pyGtkSql()
		n.db=self.db
		
		#self.txtSQL.get_buffer().set_text("")
	
	def cargaTablas(self):
		if self.db:
			try:			
				cursor=self.db.cursor(MySQLdb.cursors.Cursor)
				cursor.execute("SHOW TABLES")
				resultado=cursor.fetchall()

				if resultado:		
					list_store=gtk.ListStore(gobject.TYPE_STRING)
					self.log("Obtenida informacion de estructura de la base de datos");										
					listaTablas=list()
		
					for fila in resultado:
						self.log(fila[0])
						list_store.append([fila[0]])
									
					self.cmbTabla.set_model(list_store)
					self.cmbTabla.set_text_column(0)
					
					cell = gtk.CellRendererText()
					self.cmbTabla.pack_start(cell, True)

					self.tabPaginas.set_current_page(1)
					self.log("Consulta OK")
				else:
					self.db.commit()
					self.log("La consulta no devolvio resultados")
					self.tabPaginas.set_current_page(2)
					
				cursor.close

			except Exception, e:
				print(e)
				self.log(str(e))
				self.tabPaginas.set_current_page(2)
	
	def datosTabla(self,sender):
		#self.log(self.cmbTabla.entry.get_text())
		activo= self.cmbTabla.get_active()
		if activo < 0:
			return
		
		m= self.cmbTabla.get_model()
		sql="SHOW FIELDS FROM "+m[activo][0];
		
		try:
			cursor=self.db.cursor(MySQLdb.cursors.Cursor)
			cursor.execute(sql)
			resultado=cursor.fetchall()
			
			for columna in self.treTabla.get_columns():
				self.treTabla.remove_column(columna);

			if resultado:						
				self.treTabla.set_model(None)
				columnasmodelo=[]						
				i=0
				
				for desc in cursor.description:
					columnasmodelo.append(gobject.TYPE_STRING)
					col=gtk.TreeViewColumn(desc[0],gtk.CellRendererText(),text=i);
					self.treTabla.append_column(col);
					i+=1;
				
				store=gtk.ListStore(*columnasmodelo)						
				
				for fila in resultado:
					valores=self.astrings(fila)		
					store.append(valores)	
					
				self.treTabla.set_model(store)
			else:
				self.log("La consulta no devolvio resultados")
				self.tabPaginas.set_current_page(2)
				
			cursor.close

		except Exception, e:
			print(e)
			self.log(str(e))
			self.tabPaginas.set_current_page(2)
	
	def abrir(self,sender):
		dlg=gtk.FileChooserDialog("Abrir SQL",self.ventana,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		filter=gtk.FileFilter()
		filter.set_name("Archivos SQL")
		filter.add_pattern("*.sql")
		dlg.add_filter(filter)
		
		filter=gtk.FileFilter()
		filter.set_name("Todos los archivos")
		filter.add_pattern("*")
		dlg.add_filter(filter)
		
		res=dlg.run()
		if res==gtk.RESPONSE_OK:
			self.filename=dlg.get_filename()
			buff=self.txtSQL.get_buffer()
			try:
				f=open(self.filename,"r")
				s=f.read()
				f.close()
				buff.set_text(s)
			except:
				self.msgbox("Error","Error al guardar el fichero")
				
		dlg.destroy()
	
	def guardar_como(self,sender):
		dlg=gtk.FileChooserDialog("Guardar SQL como",self.ventana,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		filter=gtk.FileFilter()
		filter.set_name("Archivos SQL")
		filter.add_pattern("*.sql")
		dlg.add_filter(filter)
		
		res=dlg.run()
		if res==gtk.RESPONSE_OK:
			self.filename=dlg.get_filename()
			buff=self.txtSQL.get_buffer()
			start=buff.get_start_iter()
			end=buff.get_end_iter()
			sql=buff.get_text(start,end,True)
			try:
				f=open(self.filename,"w")
				f.write(sql)
				f.close()
				self.log("Guardado correctamente en "+self.filename)
			except Exception, e:
				self.msgbox("Error","Error al guardar el fichero:\n"+str(e))
				self.log("Error al guardar:" +str(e))
		dlg.destroy()
		
	def guardar(self,sender):
		if self.filename:
			try:
				buff=self.txtSQL.get_buffer()
				start=buff.get_start_iter()
				end=buff.get_end_iter()
				sql=buff.get_text(start,end,True)
				f=open(self.filename,"w")
				f.write(sql)
				f.close()
				self.log("Guardado correctamente en "+self.filename)
			except Exception, e:
				self.msgbox("Error","Error al guardar el fichero")
				self.log("Error al guardar:" +str(e))		
		else:
			self.guardar_como(sender)
	"""
		
if __name__ == "__main__":
	p = pyGtkSql()
	p.show()
	gtk.main()
