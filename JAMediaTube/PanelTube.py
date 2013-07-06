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
from gi.repository import GObject

import JAMediaObjects

#import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

#JAMediaObjectsPath = JAMediaObjects.__path__[0]

from Widgets import Mini_Toolbar
from Widgets import ToolbarAccionListasVideos
from Widgets import Toolbar_Videos_Izquierda
from Widgets import Toolbar_Videos_Derecha
from Widgets import Toolbar_Guardar

TipDescargas = "Arrastra Hacia La Izquierda para Quitarlo de Descargas."
TipEncontrados = "Arrastra Hacia La Derecha para Agregarlo a Descargas"

class PanelTube(Gtk.Paned):
    """
    Panel de JAMediaTube.
    """
    
    __gsignals__ = {
    'download':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'open_shelve_list':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_PYOBJECT))}
    
    def __init__(self):
        
        Gtk.Paned.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.toolbar_encontrados = None
        self.encontrados = None
        self.toolbar_guardar_encontrados = None
        self.toolbar_videos_izquierda = None
        self.toolbar_accion_izquierda = None
        
        self.toolbar_descargar = None
        self.descargar = None
        self.toolbar_guardar_descargar = None
        self.toolbar_videos_derecha = None
        self.toolbar_accion_derecha = None
        
        self.setup_init()
        
    def setup_init(self):
        """
        Crea y Empaqueta todo.
        """
        
        self.toolbar_encontrados = Mini_Toolbar("Videos Encontrados")
        self.toolbar_guardar_encontrados = Toolbar_Guardar()
        self.encontrados = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.toolbar_accion_izquierda = ToolbarAccionListasVideos()
        self.toolbar_videos_izquierda = Toolbar_Videos_Izquierda()
        
        self.toolbar_descargar = Mini_Toolbar("Videos Para Descargar")
        self.toolbar_guardar_descargar = Toolbar_Guardar()
        self.descargar = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.toolbar_accion_derecha = ToolbarAccionListasVideos()
        self.toolbar_videos_derecha = Toolbar_Videos_Derecha()
        
        # Izquierda
        scroll = self.get_scroll()
        scroll.add_with_viewport (self.encontrados)
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.pack_start(self.toolbar_encontrados, False, False, 0)
        box.pack_start(self.toolbar_guardar_encontrados, False, False, 0)
        box.pack_start(scroll, True, True, 0)
        box.pack_start(self.toolbar_accion_izquierda, False, False, 0)
        box.pack_end(self.toolbar_videos_izquierda, False, False, 0)
        self.pack1(box, resize = False, shrink = False)
        
        # Derecha
        scroll = self.get_scroll()
        scroll.add_with_viewport (self.descargar)
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.pack_start(self.toolbar_descargar, False, False, 0)
        box.pack_start(self.toolbar_guardar_descargar, False, False, 0)
        box.pack_start(scroll, True, True, 0)
        box.pack_start(self.toolbar_accion_derecha, False, False, 0)
        box.pack_end(self.toolbar_videos_derecha, False, False, 0)
        self.pack2(box, resize = False, shrink = False)
        
        self.show_all()
        
        self.toolbar_videos_izquierda.connect('mover_videos', self.mover_videos)
        self.toolbar_videos_derecha.connect('mover_videos', self.mover_videos)
        self.toolbar_videos_izquierda.connect('borrar', self.set_borrar)
        self.toolbar_videos_derecha.connect('borrar', self.set_borrar)
        self.toolbar_accion_izquierda.connect('ok', self.ejecutar_borrar)
        self.toolbar_accion_derecha.connect('ok', self.ejecutar_borrar)
        self.toolbar_encontrados.connect('abrir', self.abrir_lista_shelve)
        self.toolbar_encontrados.connect('guardar', self.show_toolbar_guardar)
        self.toolbar_guardar_encontrados.connect('ok', self.guardar_lista_shelve)
        self.toolbar_descargar.connect('abrir', self.abrir_lista_shelve)
        self.toolbar_descargar.connect('guardar', self.show_toolbar_guardar)
        self.toolbar_guardar_descargar.connect('ok', self.guardar_lista_shelve)
        self.toolbar_videos_derecha.connect("comenzar_descarga",
            self.comenzar_descarga)
        
        GObject.timeout_add(300, self.update)
        
    def abrir_lista_shelve(self, widget, archivo):
        """
        Agrega a la lista, todos los videos almacenados en
        un archivo shelve.
        """
        
        archivo = os.path.join(G.DIRECTORIO_DATOS, archivo)
        videos = G.get_shelve_lista(archivo)
        
        self.emit('open_shelve_list', videos, widget)
        
    def show_toolbar_guardar(self, widget):
        """
        Muestra la toolbar para escribir nombre de archivo
        donde se guardarán los videos de la lista correspondiente.
        """
        
        if widget == self.toolbar_encontrados:
            self.toolbar_guardar_encontrados.show()
            
        elif widget == self.toolbar_descargar:
            self.toolbar_guardar_descargar.show()
    
    def guardar_lista_shelve(self, widget, texto):
        """
        Guarda todos los videos de la lista en un archivo shelve.
        """
        
        origen = False
        
        if widget == self.toolbar_guardar_encontrados:
            origen = self.encontrados
            
        elif widget == self.toolbar_guardar_descargar:
            origen = self.descargar
            
        videos = []
        if origen:
            video_items = origen.get_children()
            
            if video_items:
                for video in video_items:
                    videos.append(video.videodict)
        
        if videos: G.set_shelve_lista(texto, videos)
        
    def comenzar_descarga(self, widget):
        """
        Envia la señal descargar para comenzar la
        descarga de un video en la lista, cuando el
        usuario hace click en el boton descargar.
        """
        
        self.emit('download')
        
    def mover_videos(self, widget):
        """
        Pasa todos los videos de una lista a otra.
        """
        
        self.toolbar_accion_izquierda.cancelar()
        self.toolbar_accion_derecha.cancelar()
        
        if widget == self.toolbar_videos_izquierda:
            origen = self.encontrados
            destino = self.descargar
            text = TipDescargas
            
        elif widget == self.toolbar_videos_derecha:
            origen = self.descargar
            destino = self.encontrados
            text = TipEncontrados
            
        elementos = origen.get_children()
        
        GObject.idle_add(
            self.ejecutar_mover_videos,
            origen,
            destino,
            text,
            elementos)
    
    def ejecutar_mover_videos(self, origen, destino, text, elementos):
        """
        Ejecuta secuencia que pasa videos desde una lista a otra.
        """
        
        if not elementos: return False
    
        if elementos[0].get_parent() == origen:
            origen.remove(elementos[0])
            destino.pack_start(elementos[0], False, False, 1)
            elementos[0].set_tooltip_text(text)
            
        elementos.remove(elementos[0])
        
        if elementos:
            GObject.idle_add(
                self.ejecutar_mover_videos,
                origen,
                destino,
                text,
                elementos)
            
    def set_vista_inicial(self):
        """
        Las toolbar accion deben estar ocultas inicialmente.
        """
        
        self.toolbar_accion_izquierda.cancelar()
        self.toolbar_accion_derecha.cancelar()
        
    def ejecutar_borrar(self, widget, objetos):
        """
        Elimina una lista de videos.
        """
        
        for objeto in objetos:
            objeto.destroy()
        
    def set_borrar(self, widget, objetos = None):
        """
        Llama a toolbar accion para pedir confirmacion
        sobre borrar un video o una lista de videos de la lista.
        
        Esta funcion se puede utilizar para borrar un solo video
        llamandola directamente. No es necesario que se ejecute
        a causa de la señal de la toolbar correspondiente, pero
        en este caso debe pasarse como parámetro widget,
        la toolbar que corresponde a la lista en que se
        encuentra el o los videos a borrar.
        """
        
        if widget == self.toolbar_videos_izquierda:
            if not objetos or objetos == None:
                objetos = self.encontrados.get_children()
                
            if not objetos or objetos == None: return # No se abre confirmacion.
            self.toolbar_accion_izquierda.set_accion(objetos)
            
        elif widget == self.toolbar_videos_derecha:
            if not objetos or objetos == None:
                objetos = self.descargar.get_children()
                
            if not objetos or objetos == None: return # No se abre confirmacion.
            self.toolbar_accion_derecha.set_accion(objetos)
            
        else:
            print "Caso imprevisto en run_accion de PanelTube."
        
    def update(self):
        """
        Actualiza información en toolbars de
        videos encontrados y en descaga.
        """
        
        encontrados = len(self.encontrados.get_children())
        endescargas = len(self.descargar.get_children())
        self.toolbar_encontrados.set_info(encontrados)
        self.toolbar_descargar.set_info(endescargas)
        
        return True
    
    def get_scroll(self):
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        return scroll
