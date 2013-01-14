#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
'''
from JAMediaObjects.JAMediaWidgets import ToolbarcontrolValores
from JAMediaObjects.JAMediaWidgets import JAMediaButton

import JAMediaObjects.JAMFileSystem as JAMF'''
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class Toolbar(Gtk.Toolbar):
    """Toolbar principal de JAMedia."""
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        '''
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "configurar.png")
        self.configurar = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        self.configurar.set_tooltip_text("Configuraciones.")
        self.configurar.connect("clicked", self.emit_config)
        self.insert(self.configurar, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)'''
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@gmail.com")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def salir(self, widget):
        
        self.emit('salir')
        
class TextView(Gtk.TextView):
    
    def __init__(self):
        
        Gtk.TextView.__init__(self)
        
        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        
        self.set_buffer(Gtk.TextBuffer())
        
        self.show_all()

class TreeStoreModel(Gtk.TreeStore):
    
    def __init__(self):
        
        Gtk.TreeStore.__init__(self, GObject.TYPE_STRING, GObject.TYPE_STRING)
        
class Lista(Gtk.TreeView):
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)
        
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.valor_select = None
        
        self.modelo = TreeStoreModel()
        
        self.setear_columnas()
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        
        self.set_model(self.modelo)
        
        self.show_all()
        
        self.connect("row-activated", self.activar, None)
        
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.TOUCH_MASK)
            
        #self.connect("button-press-event", self.handler_click)
        self.connect("key-press-event", self.keypress)
        
    def keypress(self, widget, event):
        
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        path = self.modelo.get_path(iter)
        
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        
        return False
    
    def activar (self, treeview, path, view_column, user_param1):
        
        iter = self.modelo.get_iter(path)
        
        if self.row_expanded(path):
            self.collapse_row(path)
            
        elif not self.row_expanded(path):
            self.expand_to_path(path)
        
    def setear_columnas(self):
        
        self.append_column(self.construir_columa('Plugins', 0, True))
        self.append_column(self.construir_columa('Descripción', 1, True))
        
    def construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna
    
    def selecciones(self, treeselection, model, path, is_selected, listore):
        """Cuando se selecciona un item en la lista."""
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor =  model.get_value(iter, 0)
        
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            
        return True
    