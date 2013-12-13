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
from gi.repository import GLib

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
from JAMexplorer import Toolbar
from JAMexplorer import ToolbarTry

from sugar3.activity import activity

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

class JAMexplorer(activity.Activity):
    
    def __init__(self, handle):
        
        activity.Activity.__init__(self, handle, False)

        self.set_border_width(3)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.navegador = Navegador()
        self.toolbar_try = ToolbarTry()
        
        switchbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        switchbox.pack_start(self.navegador, True, True, 0)
        
        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.toolbar_salir, False, True, 0)
        vbox.pack_start(switchbox, True, True, 0)
        vbox.pack_start(self.toolbar_try, False, True, 0)
        
        self.set_canvas(vbox)
        
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
            self.navegador,
            self.toolbar_try]
        
        self.show_all()
        self.realize()
        
        self.toolbar_salir.hide()
        
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.salir)
        self.connect("destroy", self.salir)
        
        self.navegador.connect('info', self.get_info)
        self.navegador.connect('cargar', self.switch)
        self.jamimagenes.connect('salir', self.get_explorador)
        self.jamediaplayer.connect('salir', self.get_explorador)
        self.jamedialector.connect('salir', self.get_explorador)
        
        GLib.idle_add(self.setup_init)
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
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
            # FIXME: and not 'iso' in tipo es un hack para que no tome
            # imagenes iso como imagenes gráficas.
            descripcion = JAMF.describe_archivo(path)
            if tipo in descripcion and not 'iso' in descripcion:
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
        