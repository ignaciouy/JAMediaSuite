#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMexplorer.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import commands

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

import JAMImagenes
from JAMImagenes.JAMImagenes import JAMImagenes

import JAMedia
from JAMedia.JAMedia import JAMediaPlayer

import JAMediaLector
from JAMediaLector.JAMediaLector import JAMediaLector

from Navegador import Navegador

ICONOS = os.path.join(JAMediaObjects.__path__[0], "Iconos")

JAMediaObjectsPath = JAMediaObjects.__path__[0]

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEstilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class Ventana(Gtk.Window):
    """Ventana Principal de JAMexplorer."""
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMexplorer")
        #self.modify_bg(0, Gdk.Color(49000, 52000, 18000))
        self.set_icon_from_file(os.path.join(ICONOS, "jamexplorer.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(3)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.toolbar = Toolbar()
        self.toolbar_accion = ToolbarAccion()
        self.toolbar_salir = ToolbarSalir()
        self.navegador = Navegador()
        self.toolbar_try = ToolbarTry()
        
        switchbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        switchbox.pack_start(self.navegador, True, True, 0)
        
        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_accion, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(switchbox, True, True, 0)
        vbox.pack_start(self.toolbar_try, False, True, 0)
        
        self.add(vbox)
        
        self.socketimagenes = Gtk.Socket()
        self.socketimagenes.show()
        switchbox.pack_start(self.socketimagenes, True, True, 0)
        self.jamimagenes = JAMImagenes()
        self.socketimagenes.add_id(self.jamimagenes.get_id())
        
        self.socketjamedia = Gtk.Socket()
        self.socketjamedia.show()
        switchbox.pack_start(self.socketjamedia, True, True, 0)
        self.jamediaplayer = JAMediaPlayer()
        self.socketjamedia.add_id(self.jamediaplayer.get_id())
        
        self.socketjamedialector = Gtk.Socket()
        self.socketjamedialector.show()
        switchbox.pack_start(self.socketjamedialector, True, True, 0)
        self.jamedialector = JAMediaLector()
        self.socketjamedialector.add_id(self.jamedialector.get_id())
        
        self.sockets = [
            self.socketimagenes,
            self.socketjamedia,
            self.socketjamedialector]
            
        self.objetos_no_visibles_en_switch = [
            self.toolbar,
            self.toolbar_accion,
            self.toolbar_salir,
            self.navegador,
            self.toolbar_try]
        
        self.show_all()
        self.realize()
        
        self.toolbar_accion.hide()
        self.toolbar_salir.hide()
        
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_accion.connect('borrar', self.ejecutar_borrar)
        self.toolbar_salir.connect('salir', self.salir)
        self.connect("destroy", self.salir)
        
        self.navegador.connect('info', self.get_info)
        self.navegador.connect('cargar', self.switch)
        self.navegador.connect('borrar', self.set_borrar)
        
        self.jamimagenes.connect('salir', self.get_explorador)
        self.jamediaplayer.connect('salir', self.get_explorador)
        self.jamedialector.connect('salir', self.get_explorador)
        
        GObject.idle_add(self.setup_init)
        
    def ejecutar_borrar(self, widget, direccion, modelo, iter):
        """Ejecuta borrar un archivo o directorio."""
        
        if JAMF.borrar(direccion):
            modelo.remove(iter)
        
    def set_borrar(self, widget, direccion, modelo, iter):
        """Setea borrar un archivo en toolbaraccion."""
        
        self.toolbar_salir.hide()
        self.toolbar_accion.set_accion(direccion, modelo, iter)
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_accion.hide()
        self.toolbar_salir.run("JAMexplorer")
        
    def setup_init(self):
        
        self.jamediaplayer.setup_init()
        self.jamedialector.setup_init()
        map(self.ocultar, self.sockets)
        
    def ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
      
    def mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
    def get_explorador(self, widget):
        
        map(self.ocultar, self.sockets)
        map(self.mostrar, self.objetos_no_visibles_en_switch)
        self.toolbar_accion.hide()
        self.toolbar_salir.hide()
        self.jamimagenes.limpiar()
        self.jamedialector.limpiar()
        self.queue_draw()
        
    def switch(self, widget, tipo):
        """Carga una aplicacion embebida de acuerdo
        al tipo de archivo que recibe."""
        
        if 'image' in tipo:
            map(self.ocultar, self.objetos_no_visibles_en_switch)
            self.socketimagenes.show()
            model, iter = self.navegador.directorios.treeselection.get_selected()
            valor = model.get_value(iter, 2)
            items = self.get_items(os.path.dirname(valor), 'image')
            self.jamimagenes.set_lista(items)
            # agregar seleccionar segun valor ?
            
        elif 'video' in tipo or 'audio' in tipo:
            map(self.ocultar, self.objetos_no_visibles_en_switch)
            self.socketjamedia.show()
            model, iter = self.navegador.directorios.treeselection.get_selected()
            valor = model.get_value(iter, 2)
            items = self.get_items(os.path.dirname(valor), 'video')
            items.extend(self.get_items(os.path.dirname(valor), 'audio'))
            self.jamediaplayer.set_nueva_lista(items)
            # agregar seleccionar segun valor ?
            
        elif 'pdf' in tipo or 'text' in tipo:
            map(self.ocultar, self.objetos_no_visibles_en_switch)
            self.socketjamedialector.show()
            model, iter = self.navegador.directorios.treeselection.get_selected()
            valor = model.get_value(iter, 2)
            self.jamedialector.abrir(valor)
            
        else:
            print tipo
            
        self.queue_draw()

    def get_items(self, directorio, tipo):
        
        if not os.path.exists(directorio) \
            or not os.path.isdir(directorio):
                return []
            
        items = []
        
        for archivo in os.listdir(directorio):
            path = os.path.join(directorio, archivo)
            if tipo in JAMF.describe_archivo(path):
                items.append( [archivo,path] )
                
        return items
        
    def get_info(self, widget, path):
        """Recibe el path seleccionado en la estructura
        de directorios, obtiene información sobre el mismo
        y la pasa infowidget para ser mostrada."""
        
        if not path: return
        self.toolbar_try.label.set_text(path)
        unidad, directorio, archivo, enlace = JAMF.describe_uri(path)
        lectura, escritura, ejecucion = JAMF.describe_acceso_uri(path)
        texto = ""
        typeinfo = ""
        if enlace:
            texto = "Enlace.\n"
        else:
            if directorio:
                texto = "Directorio.\n"
            elif archivo:
                texto = "Archivo.\n"
                texto += "Tipo:\n"
                for dato in JAMF.describe_archivo(path).split(";"):
                    texto += "\t%s\n" % (dato.strip())
                    typeinfo += dato
                texto += "Tamaño:\n"
                texto += "\t%s bytes\n" % (JAMF.get_tamanio(path))
        texto += "Permisos: \n"
        texto += "Lactura: %s\n" % (lectura)
        texto += "Escritura: %s\n" % (escritura)
        texto += "Ejecución: %s" % (ejecucion)
        self.navegador.infowidget.set_info(texto, typeinfo)
        
    def salir(self, widget = None, senial = None):
        sys.exit(0)
        
class ToolbarAccion(Gtk.Toolbar):
    """Toolbar para que el usuario confirme
    borrar un archivo."""
    
    __gsignals__ = {
    "borrar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.direccion = None
        self.modelo = None
        self.iter = None
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)
        
        #self.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        #self.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.emit_borrar)
        self.insert(boton, -1)

        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def emit_borrar(self, widget):
        """Cuando se selecciona borrar en el menu de un item."""
        
        self.emit('borrar', self.direccion, self.modelo, self.iter)
        self.cancelar()
        
    def set_accion(self, direccion, modelo, iter):
        """Configura borrar un archivo o directorio."""
        
        self.direccion = direccion
        self.modelo = modelo
        self.iter = iter
        
        self.label.set_text("¿Borrar?: %s" % (self.direccion))
        self.show_all()

    def cancelar(self, widget = None):
        """Cancela la borrar."""
        
        self.label.set_text("")
        
        self.direccion = None
        self.modelo = None
        self.iter = None
        
        self.hide()
        
class Toolbar(Gtk.Toolbar):
    """Toolbar Principal de JAMexplorer."""
    
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "jamexplorer.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@gmail.com")
        #self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(ICONOS,"salir.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.emit_salir)
        self.insert(boton, -1)
        
        self.show_all()
        
    def emit_salir(self, widget):
        
        self.emit('salir')

class ToolbarTry(Gtk.Toolbar):
    """Barra de estado de JAMexplorer."""
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        #self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
        
        
if __name__ == "__main__":
    Ventana()
    Gtk.main()