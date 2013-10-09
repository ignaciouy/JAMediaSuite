#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay
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

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GdkPixbuf

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

from JAMediaObjects.JAMFileSystem import describe_archivo

class ToolbarPreviews(Gtk.Toolbar):
    
    __gtype_name__ = 'JAMediaImagenesToolbarPreviews'
    
    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'switch_to': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'ver': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'camara': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self, path):
        
        Gtk.Toolbar.__init__(self)
        
        self.path = path
        
        self.buttons_back = []
        self.buttons_visor = []
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "play.png")
        boton = get_boton(
            archivo, flip = True,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Anterior")
        boton.connect("clicked", self.__emit_switch)
        self.insert(boton, -1)
        self.buttons_back.append(boton)
        
        separador = get_separador(draw = True,
            expand = False)
        self.insert(separador, -1)
        self.buttons_back.append(separador)
        
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "foto.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Cámara")
        boton.connect("clicked", self.__emit_camara)
        self.insert(boton, -1)
        
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "ver.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Visor de Imágenes")
        boton.connect("clicked", self.__emit_visor)
        self.insert(boton, -1)
        #boton.set_no_show_all(True)
        self.buttons_visor.append(boton)
        
        self.insert(get_separador(draw = True,
            expand = False), -1)
            
        self.insert(get_separador(draw = False,
            ancho = 15, expand = False), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","JAMediaImagenes.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1.2),
            tooltip_text = "Autor.")
        boton.connect("clicked", self.__show_credits)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","JAMedia-help.svg")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Ayuda.")
        boton.connect("clicked", self.__show_help)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = True,
            expand = False), -1)
            
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "salir.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 5, expand = False), -1)
        
        self.show_all()
        
    def set_modo(self, modo):
        
        if modo == "noback":
            map(self.__ocultar, self.buttons_back)
            
        elif modo == "novisor":
            map(self.__ocultar, self.buttons_visor)
            
        elif modo == "visor":
            map(self.__mostrar, self.buttons_visor)
            
    def __mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
    def __ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def __emit_camara(self, widget):
        
        self.emit("camara")
        
    def __emit_visor(self, widget):
        
        self.emit("ver", self.path)
        
    def __show_credits(self, widget):
        
        dialog = Credits(parent = self.get_toplevel())
        response = dialog.run()
        dialog.destroy()
        
    def __show_help(self, widget):
        
        dialog = Help(parent = self.get_toplevel())
        response = dialog.run()
        dialog.destroy()
        
    def __emit_switch(self, widget):
        
        self.emit("switch_to", os.path.dirname(self.path))
        
    def __salir(self, widget):
        
        self.emit("salir")
        
class ToolbarImagen(Gtk.Toolbar):
    """
    Toolbar para visor de imágenes.
    """
    
    __gtype_name__ = 'JAMediaImagenesToolbarImagen'
    
    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'switch_to': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "activar":(GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self, path):
        
        Gtk.Toolbar.__init__(self)
        
        self.path = path
        self.buttons_player = []
        self.buttons_escala_rotacion = []
        self.buttons_config = []
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "play.png")
        boton = get_boton(
            archivo, flip = True,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Anterior")
        boton.connect("clicked", self.__emit_switch)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = True,
            expand = False), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "escalaoriginal.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Original")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_escala_rotacion.append(boton)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Alejar")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_escala_rotacion.append(boton)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Acercar")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_escala_rotacion.append(boton)
        
        separador = get_separador(draw = True,
            expand = False)
        self.insert(separador, -1)
        self.buttons_escala_rotacion.append(separador)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Rotar Izquierda")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_escala_rotacion.append(boton)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        boton = get_boton(
            archivo, flip = True,
            pixels = get_pixels(1),
            tooltip_text = "Rotar Derecha")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_escala_rotacion.append(boton)
        
        separador = get_separador(draw = True,
            expand = False)
        self.insert(separador, -1)
        self.buttons_escala_rotacion.append(separador)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "configurar.png")
        button = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Configurar Presentación")
        button.connect("clicked", self.__activar)
        self.insert(button, -1)
        self.buttons_config.append(button)
        
        separador = get_separador(draw = True,
            expand = False)
        self.insert(separador, -1)
        self.buttons_player.append(separador)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "siguiente.png")
        boton = get_boton(
            archivo, flip = True,
            pixels = get_pixels(1),
            tooltip_text = "Anterior")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_player.append(boton)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "play.png")
        self.botonplay = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Reproducir")
        self.botonplay.connect("clicked", self.__activar)
        self.insert(self.botonplay, -1)
        self.buttons_player.append(self.botonplay)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "siguiente.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Siguiente")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_player.append(boton)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "stop.png")
        boton = get_boton(
            archivo, flip = False,
            pixels = get_pixels(1),
            tooltip_text = "Detener")
        boton.connect("clicked", self.__activar)
        self.insert(boton, -1)
        self.buttons_player.append(boton)
        
        separador = get_separador(draw = True,
            expand = False)
        self.insert(separador, -1)
        self.buttons_config.append(separador)
        
        self.insert(get_separador(draw = False,
            expand = True), -1)
        
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos", "salir.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(1),
            tooltip_text = "Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def set_modo(self, modo):
        
        if modo == "edit":
            map(self.__ocultar, self.buttons_player)
            map(self.__mostrar, self.buttons_escala_rotacion)
            
        elif modo == "player":
            map(self.__mostrar, self.buttons_player)
            map(self.__ocultar, self.buttons_escala_rotacion)
            
        elif modo == "noconfig":
            map(self.__ocultar, self.buttons_config)
            
    def __mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
    def __ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def set_paused(self):
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "play.png")
        pixel = get_pixels(1)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixel, pixel)
        img = self.botonplay.get_children()[0].get_children()[0].get_children()[0]
        
        img.set_from_pixbuf(pixbuf)
        
    def set_playing(self):
        
        archivo = os.path.join(JAMediaObjectsPath, "Iconos", "pausa.png")
        pixel = get_pixels(1)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixel, pixel)
        img = self.botonplay.get_children()[0].get_children()[0].get_children()[0]
        
        img.set_from_pixbuf(pixbuf)
        
    def __activar(self, widget = None, event = None):
        
        self.emit("activar", widget.TOOLTIP)
        
    def __emit_switch(self, widget):
        
        self.emit("switch_to", self.path)
        
    def __salir(self, widget):
        
        self.emit("salir")
        
class ToolbarTry(Gtk.Toolbar):
    
    __gtype_name__ = 'JAMediaImagenesToolbarTry'
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        item.set_expand(False)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False,
            expand = True), -1)
            
        self.show_all()
        
    def set_info(self, path, size):
        
        self.label.set_text("Archivo: %s    Tamaño: %s x %s pixeles." % (path, size[0], size[1]))
        
class ToolbarConfig(Gtk.Toolbar):
    """
    Toolbar con opciones de configuracion para
    modo presentacion de diapositivas.
    """
    
    __gtype_name__ = 'JAMediaImagenesToolbarConfig'
    
    __gsignals__ = {
    "run":(GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT, ))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.intervalo = 1.0
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(0.8),
            tooltip_text = "Disminuir")
        boton.connect("clicked", self.__menos_intervalo)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label(
            "Cambiar Imagen cada: %s Segundos" % (self.intervalo))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(0.8),
            tooltip_text = "Aumentar")
        boton.connect("clicked", self.__mas_intervalo)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "play.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(0.8),
            tooltip_text = "Aceptar")
        boton.connect("clicked", self.__run_presentacion)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "salir.png")
        boton = get_boton(
            archivo, flip = False,
            rotacion = None,
            pixels = get_pixels(0.8),
            tooltip_text = "Cancelar")
        boton.connect("clicked", self.__cancelar)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        self.show_all()
        
    def __mas_intervalo(self, widget= None):
        
        self.intervalo += 0.1
        self.label.set_text(
            "Cambiar Imagen cada: %s Segundos" % (self.intervalo))

    def __menos_intervalo(self, widget= None):
        
        if self.intervalo > 0.3:
            self.intervalo -= 0.1
            self.label.set_text(
                "Cambiar Imagen cada: %s Segundos" % (self.intervalo))

    def __run_presentacion(self, widget= None):
        
        self.hide()
        self.emit("run", int(self.intervalo*1000))
        
    def __cancelar(self, widget= None):
        
        self.hide()
        
class Credits(Gtk.Dialog):
    
    __gtype_name__ = 'JAMediaImagenesCredits'
    
    def __init__(self, parent = None):

        Gtk.Dialog.__init__(self,
            parent = parent,
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Cerrar", Gtk.ResponseType.ACCEPT])
        
        self.set_border_width(15)
        
        tabla1 = Gtk.Table(columns=5, rows=1, homogeneous=False)
        
        jamedia = Gtk.Image()
        jamedia.set_from_file(
            os.path.join(JAMediaObjectsPath,
                "Iconos", "JAMediaImagenes.svg"))
        tabla1.attach_defaults(jamedia, 0, 1, 0, 1)
        
        jam = Gtk.Image()
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "ceibaljam-o.png"),-1, 25)
        jam.set_from_pixbuf(pix)
        tabla1.attach_defaults(jam, 1, 2, 0, 1)

        jam = Gtk.Image()
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "licencia.png"),-1, 25)
        jam.set_from_pixbuf(pix)
        tabla1.attach_defaults(jam, 2, 3, 0, 1)

        jam = Gtk.Image()
        pix = GdkPixbuf.Pixbuf.new_from_file_at_size(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "uruguay-o.png"),-1, 25)
        jam.set_from_pixbuf(pix)
        tabla1.attach_defaults(jam, 3, 4, 0, 1)
        
        tabla2 = Gtk.Table(columns=3, rows=2, homogeneous=False)
        
        credits = Gtk.Image()
        credits.set_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "credits.png"))
        tabla2.attach_defaults(credits, 0, 5, 0, 2)
        
        self.vbox.pack_start(tabla1, True, True, 0)
        self.vbox.pack_start(tabla2, True, True, 0)
        
        from gi.repository import Pango
        label = Gtk.Label("Flavio Danesse  -  fdanesse@gmail.com")
        label.modify_font(Pango.FontDescription('Monospace 8'))
        self.vbox.pack_start(
            label,
            True, True, 0)
            
        label = Gtk.Label(
            "https://sites.google.com/site/sugaractivities/jamediaobjects/")
        label.modify_font(Pango.FontDescription('Monospace 8'))
        self.vbox.pack_start(
            label,
            True, True, 0)
            
        self.vbox.show_all()
        
class Help(Gtk.Dialog):
    
    __gtype_name__ = 'JAMediaImagenesHelp'
    
    def __init__(self, parent = None):

        Gtk.Dialog.__init__(self,
            parent = parent,
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Cerrar", Gtk.ResponseType.ACCEPT])
        
        self.set_border_width(15)
        
        tabla1 = Gtk.Table(columns=5, rows=2, homogeneous=False)
        
        vbox = Gtk.HBox()
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "play.png")
        self.anterior = get_boton(
            archivo, flip = True,
            pixels = get_pixels(0.8),
            tooltip_text = "Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "play.png")
        self.siguiente = get_boton(
            archivo,
            pixels = get_pixels(0.8),
            tooltip_text = "Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)
        
        tabla1.attach_defaults(vbox, 0, 5, 0, 1)
        
        self.helps = []
        
        for x in range(1, 2):
            help = Gtk.Image()
            help.set_from_file(
                os.path.join(JAMediaObjectsPath,
                    "Iconos", "JAMedia-help%s.png" % x))
            tabla1.attach_defaults(help, 0, 5, 1, 2)
            
            self.helps.append(help)
        
        self.vbox.pack_start(tabla1, True, True, 0)
        self.vbox.show_all()
        
        self.__switch(None)
        
    def __ocultar(self, objeto):
        
        if objeto.get_visible():
            objeto.hide()
            
    def __switch(self, widget):
        
        if not widget:
            map(self.__ocultar, self.helps[1:])
            self.anterior.hide()
            self.helps[0].show()
    
        else:
            index = self.__get_index_visible()
            helps = list(self.helps)
            new_index = index
            
            if widget == self.siguiente:
                if index < len(self.helps)-1:
                    new_index += 1
                
            elif widget == self.anterior:
                if index > 0:
                    new_index -= 1
                    
            helps.remove(helps[new_index])
            map(self.__ocultar, helps)
            self.helps[new_index].show()
            
            if new_index > 0:
                self.anterior.show()
                
            else:
                self.anterior.hide()
                
            if new_index < self.helps.index(self.helps[-1]):
                self.siguiente.show()
                
            else:
                self.siguiente.hide()
            
    def __get_index_visible(self):
        
        for help in self.helps:
            if help.get_visible():
                return self.helps.index(help)
            