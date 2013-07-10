#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
#       Flavio Danesse      <fdanesse@gmail.com>

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
import commands
import Pep8
from pyflakes.scripts import pyflakes

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango

#BASEPATH = os.path.dirname(__file__)
FUENTES_GLOBAL = Gtk.Window().get_pango_context().list_families()

def get_boton(stock, tooltip):
    """
    Devuelve un botón generico.
    """

    boton = Gtk.ToolButton.new_from_stock(stock)
    boton.set_tooltip_text(tooltip)
    boton.TOOLTIP = tooltip
    
    return boton

def get_boton_icon(icon, tooltip):
    """
    Devuelve un botón con un icono específico.
    """
    
    boton = Gtk.ToolButton()
    boton.set_tooltip_text(tooltip)
    boton.TOOLTIP = tooltip
    boton.set_icon_name(icon)
    
    return boton

def get_separador(draw = False, ancho = 0, expand = False):
    """
    Devuelve un separador generico.
    """
    
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    
    return separador

LICENCIAS = ['GPL2', 'GPL3', 'LGPL 2.1', 'LGPL 3', 'BSD', 'MIT X11']

class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """
    
    __gtype_name__ = 'Menu'
    
    __gsignals__ = {
    'accion_proyecto': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'accion_archivo': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'accion_ver': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'accion_codigo': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        self.dict_archivo = {}
        self.dict_proyecto = {}
        
        item_proyectos = Gtk.MenuItem('Proyecto')
        item_archivos = Gtk.MenuItem('Archivo')
        item_edicion = Gtk.MenuItem('Edición')
        item_ver = Gtk.MenuItem('Ver')
        item_codigo = Gtk.MenuItem('Código')
        #item_ayuda = Gtk.MenuItem('Ayuda')

        menu_proyectos = Gtk.Menu()
        menu_archivos = Gtk.Menu()
        menu_edicion = Gtk.Menu()
        menu_ver = Gtk.Menu()
        menu_codigo = Gtk.Menu()
        #menu_ayuda = Gtk.Menu()

        item_proyectos.set_submenu(menu_proyectos)
        item_archivos.set_submenu(menu_archivos)
        item_edicion.set_submenu(menu_edicion)
        item_ver.set_submenu(menu_ver)
        item_codigo.set_submenu(menu_codigo)
        #item_ayuda.set_submenu(menu_ayuda)

        self.append(item_proyectos)
        self.append(item_archivos)
        self.append(item_edicion)
        self.append(item_ver)
        self.append(item_codigo)
        #self.append(item_ayuda)

        ### Items del Menú Proyectos
        item = Gtk.MenuItem('Nuevo . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Nuevo Proyecto")
        menu_proyectos.append(item)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Abrir Proyecto")
        menu_proyectos.append(item)

        item = Gtk.MenuItem('Editar . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Editar Proyecto")
        self.dict_proyecto["Editar Proyecto"] = item
        menu_proyectos.append(item)

        item = Gtk.MenuItem('Cerrar')
        item.connect("activate", self.__emit_accion_proyecto, "Cerrar Proyecto")
        self.dict_proyecto["Cerrar Proyecto"] = item
        menu_proyectos.append(item)

        item = Gtk.MenuItem('Guardar')
        item.connect("activate", self.__emit_accion_proyecto, "Guardar Proyecto")
        self.dict_proyecto["Guardar Proyecto"] = item
        menu_proyectos.append(item)

        item = Gtk.MenuItem('Construir')
        item.connect("activate", self.__emit_accion_proyecto, "Construir")
        self.dict_proyecto["Construir"] = item
        menu_proyectos.append(item)
        
        ### Items del Menú Archivos
        item = Gtk.MenuItem('Nuevo')
        item.connect("activate", self.__emit_accion_archivo, "Nuevo Archivo")
        menu_archivos.append(item)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_archivo, "Abrir Archivo")
        menu_archivos.append(item)

        item = Gtk.MenuItem('Cerrar')
        item.connect("activate", self.__emit_accion_archivo, "Cerrar Archivo")
        self.dict_archivo['Cerrar'] = item
        menu_archivos.append(item)
        
        item = Gtk.MenuItem('Guardar')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Archivo")
        menu_archivos.append(item)
        self.dict_archivo['Guardar'] = item
        
        item = Gtk.MenuItem('Guardar Como ...')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Como")
        self.dict_archivo['Guardar Como'] = item
        menu_archivos.append(item)
        
        ### Items del Menú Edición
        item = Gtk.MenuItem('Deshacer')
        item.connect("activate", self.__emit_accion_archivo, "Deshacer")
        menu_edicion.append(item)
        self.dict_archivo['Deshacer'] = item
        
        item = Gtk.MenuItem('Rehacer')
        item.connect("activate", self.__emit_accion_archivo, "Rehacer")
        menu_edicion.append(item)
        self.dict_archivo['Rehacer'] = item
        
        item = Gtk.MenuItem('Cortar')
        item.connect("activate", self.__emit_accion_archivo, "Cortar")
        menu_edicion.append(item)
        self.dict_archivo['Cortar'] = item
        
        item = Gtk.MenuItem('Copiar')
        item.connect("activate", self.__emit_accion_archivo, "Copiar")
        menu_edicion.append(item)
        self.dict_archivo['Copiar'] = item
        
        item = Gtk.MenuItem('Pegar')
        item.connect("activate", self.__emit_accion_archivo, "Pegar")
        self.dict_archivo['Pegar'] = item
        menu_edicion.append(item)
        
        item = Gtk.MenuItem('Seleccionar Todo')
        item.connect("activate", self.__emit_accion_archivo, "Seleccionar Todo")
        self.dict_archivo['Seleccionar Todo'] = item
        menu_edicion.append(item)
        
        ### Items del menú Ver
        item = Gtk.MenuItem("Numeros de línea")
        item.connect("activate", self.__emit_accion_ver, "Numeracion")
        self.dict_archivo['Numeracion'] = item
        menu_ver.append(item)
        
        item = Gtk.MenuItem("Panel inferior")
        item.connect("activate", self.__emit_accion_ver, "Panel inferior")
        menu_ver.append(item)

        item = Gtk.MenuItem("Panel Lateral")
        item.connect("activate", self.__emit_accion_ver, "Panel Lateral")
        menu_ver.append(item)
        
        ### Items del Menú Código
        item = Gtk.MenuItem('Aumentar')
        item.connect("activate", self.__emit_accion_codigo, "Aumentar")
        self.dict_archivo['Aumentar'] = item
        menu_codigo.append(item)
        
        item = Gtk.MenuItem('Disminuir')
        item.connect("activate", self.__emit_accion_codigo, "Disminuir")
        self.dict_archivo['Disminuir'] = item
        menu_codigo.append(item)
        
        item = Gtk.MenuItem('Formato de Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Formato")
        self.dict_archivo['Formato'] = item
        menu_codigo.append(item)
       
        #item = Gtk.MenuItem('Ejecutar archivo')
        #item.connect("activate", self.__emit_accion, "Ejecutar archivo")
        #menu_codigo.append(item)

        #item = Gtk.MenuItem('Ejecutar proyecto')
        #item.connect("activate", self.__emit_accion, "Ejecutar proyecto")
        #menu_codigo.append(item)

        #item = Gtk.MenuItem('Detener')
        #item.connect("activate", self.__emit_accion, "Detener")
        #menu_codigo.append(item)

        #item = Gtk.MenuItem('Remover espacios en blanco')
        #item.connect("activate", self.__emit_accion, "Remover espacios en blanco")
        #menu_codigo.append(item)
        
        item = Gtk.MenuItem('Identar')
        item.connect("activate", self.__emit_accion_codigo, "Identar")
        self.dict_archivo['Identar'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('De Identar')
        item.connect("activate", self.__emit_accion_codigo, "De Identar")
        self.dict_archivo['De Identar'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('Identar con Espacios')
        item.connect("activate", self.__emit_accion_codigo, "Identar con Espacios")
        self.dict_archivo['Identar con Espacios'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('Identar con Tabulaciones')
        item.connect("activate", self.__emit_accion_codigo, "Identar con Tabulaciones")
        self.dict_archivo['Identar con Tabulaciones'] = item
        menu_codigo.append(item)
        
        item = Gtk.MenuItem('Buscar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Buscar Texto")
        self.dict_archivo['Buscar Texto'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('Reemplazar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Reemplazar Texto")
        self.dict_archivo['Reemplazar Texto'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('Chequear la sintaxis')
        item.connect("activate", self.__emit_accion_codigo, "Chequear")
        self.dict_archivo['Chequear'] = item
        menu_codigo.append(item)

        item = Gtk.MenuItem('Valorar')
        item.connect("activate", self.__emit_accion_codigo, "Valorar")
        self.dict_archivo['Valorar'] = item
        menu_codigo.append(item)

        # Items del Menú Ayuda
        #item = Gtk.MenuItem('Créditos')
        #item.connect("activate", self.__emit_accion, "Créditos")
        #menu_ayuda.append(item)

        self.show_all()
        
        for item in self.dict_archivo.keys():
            self.dict_archivo[item].set_sensitive(False)
            
    def __emit_accion_codigo(self, widget, accion):
        
        self.emit('accion_codigo', accion)
        
    def __emit_accion_ver(self, widget, accion):
        
        self.emit('accion_ver', accion)
        
    def __emit_accion_archivo(self, widget, accion):

        self.emit('accion_archivo', accion)
        
    def __emit_accion_proyecto(self, widget, accion):

        self.emit('accion_proyecto', accion)
        
    def activar_proyecto(self, visibility):
        """
        Activa o desactiva opciones.
        """
        
        submenus = []
        
        for option in self.dict_proyecto.keys():
            submenus.append(self.dict_proyecto[option])
            
        if visibility:
            map(self.__activar, submenus)
            
        else:
            map(self.__desactivar, submenus)
            
    def update_archivos(self, visibility, options):
        """
        Activa o desactiva opciones.
        """
        
        submenus = []
        
        for option in options:
            if self.dict_archivo.get(option, False):
                submenus.append(self.dict_archivo[option])
            
        if visibility:
            map(self.__activar, submenus)
            
        else:
            map(self.__desactivar, submenus)
            
    def __activar(self, option):
        
        if not option.get_sensitive(): option.set_sensitive(True)
        
    def __desactivar(self, option):
        
        if option.get_sensitive(): option.set_sensitive(False)
        
class DialogoProyecto(Gtk.Dialog):
    """
    Diálogo para crear un nuevo proyecto.
    """

    __gtype_name__ = 'DialogoProyecto'
    
    def __init__(self, parent_window = None,
        title = "Crear Proyecto Nuevo", accion = "nuevo"):

        Gtk.Dialog.__init__(self,
            title = title,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
        
        if accion == "nuevo":
            self.set_size_request(600, 150)
            
        else:
            self.set_size_request(600, 450)
            
        self.set_border_width(15)
        
        ### Entradas de datos.
        self.nombre = Gtk.Entry()
        self.main = Gtk.ComboBoxText()
        self.path = Gtk.Label()
        self.version = Gtk.Entry()
        
        self.descripcion = Gtk.TextView()
        self.descripcion.set_editable(True)
        self.descripcion.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        scroll_descripcion = Gtk.ScrolledWindow()
        
        scroll_descripcion.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll_descripcion.add_with_viewport(self.descripcion)
        
        scroll_descripcion.set_size_request(200, 100)
        
        self.licencia = Gtk.ComboBoxText()
        self.url = Gtk.Entry()
        self.icon_path = Gtk.Label()

        ### Box para despues agregarlo a un scroll
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        ### Scroll
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add_with_viewport(self.box)

        self.vbox.pack_start(scroll, True, True, 0)

        ### Autores
        self.autores = WidgetAutores()
        
        boton = Gtk.Button("Ver más Opciones . . .")
        boton.connect("clicked", self.__show_options)
        
        self.internal_widgets = [
            self.__get_pack_box(
                [self.__get_label('Nombre:'), self.nombre] ),
            self.__get_pack_box(
                [boton] ),
            self.__get_pack_box(
                [self.__get_label('Archivo Principal:'),
                self.main] ),
            self.__get_pack_box(
                [self.__get_label('Directorio del proyecto:'),
                self.path] ),
            self.__get_pack_box(
                [self.__get_label('Versión:'), self.version] ),
            self.__get_pack_box(
                [self.__get_label('Licencia:'), self.licencia] ),
            self.__get_pack_box(
                [self.__get_label('Web:'), self.url] ),
            self.__get_pack_box(
                [self.__get_label("Autores:"),
                self.autores] ),
            self.__get_pack_box(
                [self.__get_label('Descripción:'), scroll_descripcion] )]
        
        for widget in self.internal_widgets:
            self.box.pack_start(widget, False, False, 3)

        for licencia in LICENCIAS:
            self.licencia.append_text(licencia)
            
        self.licencia.set_active(0)
        
        self.show_all()
        
        if accion == "nuevo":
            for widget in self.internal_widgets[2:]:
                widget.hide()
            
        self.nombre.connect("key_release_event", self.__check_nombre)
        
        ### Si se abre para editar, no se le puede cambiar el nombre.
        if accion == "editar":
            self.nombre.set_sensitive(False)
        
        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                button.set_sensitive(False)
                break
        
    def __show_options(self, widget):
        
        for widget in self.internal_widgets[2:]:
            
            if widget.get_visible():
                widget.hide()
                self.set_size_request(600, 150)
                self.queue_draw()
                
            else:
                self.set_size_request(600, 450)
                widget.show()
        
    def __check_nombre(self, widget, event):
        """
        Activa y Desactiva el boton aceptar, según
        tenga nombre el proyecto o no.
        """
        
        boton = None
        
        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                boton = button
                break
            
        nombre = self.nombre.get_text()
        if nombre: nombre = nombre.strip()
        
        if nombre:
            boton.set_sensitive(True)
            
        else:
            boton.set_sensitive(False)
    
    def __get_label(self, text):
        """
        Recibe un texto y
        devuelve un Gtk.Label con él.
        """
        
        label = Gtk.Label(text)
        
        return label
    
    def __get_pack_box(self, widgets):
        """
        Recibe una lista de Widgets y
        devuelve un box, con esos widgets empaquetados.
        """
        
        box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        box.pack_start(widgets[0], False, False, 5)
        
        for widget in widgets[1:]:
            box.pack_start(widget, True, True, 5)
            
        return box
        
    def get_proyecto(self):
        """
        Devuelve un diccionario con la definición
        del proyecto.
        """
        
        buffer = self.descripcion.get_buffer()
        
        nombre = self.nombre.get_text()
        main = self.main.get_active_text()
        path = self.path.get_text()
        
        buffer = buffer.get_text(
            buffer.get_start_iter(),
            buffer.get_end_iter(), True)
        
        version = self.version.get_text()
        licencia = self.licencia.get_active_text()
        url = self.url.get_text()
        
        if nombre: nombre = nombre.strip()
        if main: main = main.strip()
        if path: path = path.strip()
        if buffer: buffer = buffer.strip()
        if version: version = version.strip()
        if not version: version = "1"
        if licencia: licencia = licencia.strip()
        if url: url = url.strip()
        
        dict = {
            "nombre": nombre,
            "main": main,
            "path": path,
            "descripcion": buffer,
            "version": version,
            "licencia": licencia,
            "url": url,
            "autores": self.autores.get_autores()
            }
            
        return dict

    def set_proyecto(self, diccionario):
        """
        Establece los datos del diccionario introducido
        """

        self.nombre.set_text(diccionario["nombre"])
        self.path.set_text(diccionario["path"])
        self.version.set_text(diccionario["version"])
        self.descripcion.get_buffer().set_text(diccionario["descripcion"])
        self.licencia.set_active(LICENCIAS.index(diccionario["licencia"]))
        self.url.set_text(diccionario["url"])
        self.autores.set_autores(diccionario["autores"])
        
        ### Setear Combo para archivo Main.
        if diccionario.get("path", False):
            import glob
            
            arch = glob.glob("%s/*.py" % diccionario["path"])
            self.main.remove_all()
            
            for archivo in arch:
                self.main.append_text(os.path.basename(archivo))
                
        model = self.main.get_model()
        item = model.get_iter_first()
        
        count = 0
        
        while item:
            if model.get_value(item, 0) == diccionario["main"]:
                self.main.set_active(count)
                break
            
            item = model.iter_next(item)
            count += 1
            
        ### Setear sensibilidad en el boton aceptar.
        for button in self.get_action_area().get_children():
            if self.get_response_for_widget(button) == Gtk.ResponseType.ACCEPT:
                
                nombre = self.nombre.get_text()
                if nombre: nombre.strip()
                
                if not nombre:
                    button.set_sensitive(False)
                    
                else:
                    button.set_sensitive(True)
                    
                break

class DialogoBuscar(Gtk.Dialog):

    def __init__(self, view, parent_window = None,
        title = "Buscar Texto", texto = None):

        Gtk.Dialog.__init__(self,
            title = title,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL)

        self.set_border_width(15)
        
        self.view = view
        self.entrada = Gtk.Entry()
        
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.entrada, False, False, 0)
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 3)
        
        self.boton_anterior = Gtk.Button('Buscar anterior')
        self.boton_siguiente = Gtk.Button('Buscar siguiente')
        self.boton_cerrar = Gtk.Button('Cerrar')
        
        hbox = Gtk.HBox()
        hbox.pack_start(self.boton_anterior, True, True, 3)
        hbox.pack_start(self.boton_siguiente, True, True, 3)
        hbox.pack_start(self.boton_cerrar, True, True, 0)
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 0)
        
        self.boton_anterior.set_sensitive(False)
        self.boton_siguiente.set_sensitive(False)
        
        self.boton_anterior.connect('clicked', self.__buscar, 'Atras')
        self.boton_siguiente.connect('clicked', self.__buscar, 'Adelante')
        self.boton_cerrar.connect('clicked', self.__destroy)
        self.entrada.connect("changed", self.__changed)

        self.seleccion = False
        if texto:
            self.entrada.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            self.seleccion = True
            GObject.idle_add(self.__update, texto, seleccion)

    def __update(self, texto, selection):
        buffer = self.view.get_buffer()
        
        start, end = buffer.get_bounds()
        _texto = buffer.get_text(start, end, 0)
        numero = len(_texto)

        if end.get_offset() == numero and not selection:
            inicio = buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')

        else:
            inicio, fin = selection
            buffer.select_range(inicio, fin)
        
    def __changed(self, widget):
        """
        Habilita y deshabilita los botones de busqueda y reemplazo.
        """
        
        self.boton_anterior.set_sensitive(bool(self.entrada.get_text()))
        self.boton_siguiente.set_sensitive(bool(self.entrada.get_text()))
        
    def __buscar(self, widget, direccion):
        """
        Busca el texto en el buffer.
        """

        texto = self.entrada.get_text()
        buffer = self.view.get_buffer()
        inicio, fin = buffer.get_bounds()
        
        texto_actual = buffer.get_text(inicio, fin, 0)
        
        posicion = buffer.get_iter_at_mark(buffer.get_insert())

        if texto:
            if texto in texto_actual:
                inicio = posicion

                if direccion == 'Adelante':
                    if inicio.get_offset() == buffer.get_char_count():
                        inicio = buffer.get_start_iter()

                elif direccion == 'Atras':
                    if buffer.get_selection_bounds():
 
                        start, end = buffer.get_selection_bounds()
                        _texto = buffer.get_text(start, end, 0)
                        numero = len(_texto)

                        if end.get_offset() == numero:
                            inicio = buffer.get_end_iter()

                        else:
                            inicio = buffer.get_selection_bounds()[0]

                self.__seleccionar_texto(texto, inicio, direccion)

            else:
                buffer.select_range(posicion, posicion)

        if self.seleccion:
            self.seleccion = False
            if direccion == "Atras":
                self.boton_anterior.clicked()
            else:
                self.boton_siguiente.clicked()


    def __seleccionar_texto(self, texto, inicio, direccion):
        """
        Selecciona el texto solicitado,
        y mueve el scrolled sí es necesario
        """

        buffer = self.view.get_buffer()

        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)

        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)

        if match:
            match_start, match_end = match
            buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 1)

        else:
            if direccion == 'Adelante':
                inicio = buffer.get_start_iter()

            elif direccion == 'Atras':
                inicio = buffer.get_end_iter()

            self.__seleccionar_texto(texto, inicio, direccion)

    def __destroy(self, widget):

        self.destroy()


class DialogoReemplazar(Gtk.Dialog):

    def __init__(self, view, parent_window = None,
        title = "Reemplazar Texto", texto = None):

        Gtk.Dialog.__init__(self,
            title = title,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL)
            
        self.set_border_width(15)
        
        self.view = view
        
        ### Entries.
        self.buscar_entry = Gtk.Entry()
        self.reemplazar_entry = Gtk.Entry()
        
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.buscar_entry, False, False, 0)
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 3)
        
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Reemplazar:"), True, True, 3)
        hbox.pack_start(self.reemplazar_entry, False, False, 0)
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 10)
        
        ### Buttons.
        cerrar = Gtk.Button("Cerrar")
        self.reemplazar = Gtk.Button("Reemplazar")
        self.button_buscar = Gtk.Button("Saltear")
        
        hbox = Gtk.HBox()
        hbox.pack_start(self.reemplazar, True, True, 3)
        hbox.pack_start(self.button_buscar, True, True, 3)
        hbox.pack_start(cerrar, True, True, 0)
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 0)
        
        self.reemplazar.set_sensitive(False)
        self.button_buscar.set_sensitive(False)

        cerrar.connect("clicked", self.__destroy)
        self.button_buscar.connect('clicked', self.__buscar, 'Adelante')
        self.reemplazar.connect("clicked", self.__reemplazar)
        
        if texto:
            self.buscar_entry.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            self.seleccion = True
            GObject.idle_add(self.__update, texto, seleccion)

        GObject.idle_add(self.__changed)
        
    def __update(self, texto, selection):
        buffer = self.view.get_buffer()
        
        start, end = buffer.get_bounds()
        _texto = buffer.get_text(start, end, 0)
        numero = len(_texto)

        if end.get_offset() == numero and not selection:
            inicio = buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')

        else:
            inicio, fin = selection
            buffer.select_range(inicio, fin)

    def __changed(self):
        """
        Habilita y deshabilita los botones de busqueda y reemplazo.
        """
        
        self.button_buscar.set_sensitive(bool(self.buscar_entry.get_text()))
        buffer = self.view.get_buffer()
        select = buffer.get_selection_bounds()
        
        if len(select) == 2:
            select = True
        else:
            select = False

        self.reemplazar.set_sensitive(select and \
            bool(self.buscar_entry.get_text()) and \
            bool(self.reemplazar_entry.get_text()))

        return True

    def __buscar(self, widget, direccion):
        """
        Busca el texto en el buffer.
        """

        texto = self.buscar_entry.get_text()
        buffer = self.view.get_buffer()
        inicio, fin = buffer.get_bounds()
        
        texto_actual = buffer.get_text(inicio, fin, 0)

        posicion = buffer.get_iter_at_mark(buffer.get_insert())

        if texto:
            if texto in texto_actual:
                inicio = posicion

                if direccion == 'Adelante':
                    if inicio.get_offset() == buffer.get_char_count():
                        inicio = buffer.get_start_iter()

                elif direccion == 'Atras':
                    if buffer.get_selection_bounds():
 
                        start, end = buffer.get_selection_bounds()
                        _texto = buffer.get_text(start, end, 0)
                        numero = len(_texto)

                        if end.get_offset() == numero:
                            inicio = buffer.get_end_iter()

                        else:
                            inicio = buffer.get_selection_bounds()[0]

                self.__seleccionar_texto(texto, inicio, direccion)

            else:
                buffer.select_range(posicion, posicion)

        if self.seleccion:
            self.seleccion = False
            self.button_buscar.clicked()
    
    def __destroy(self, widget, event=None):
        
        self.destroy()

    def __reemplazar(self, widget):
        
        buffer = self.view.get_buffer()
        inicio_s, fin_s = buffer.get_selection_bounds()
        texto_reemplazo = self.reemplazar_entry.get_text()

        buffer.delete(inicio_s, fin_s)
        buffer.insert_at_cursor(texto_reemplazo)

        self.seleccion = False

        self.button_buscar.clicked()
    
    def __seleccionar_texto(self, texto, inicio, direccion):
        """
        Selecciona el texto solicitado,
        y mueve el scrolled sí es necesario.
        """

        buffer = self.view.get_buffer()

        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)

        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)

        if match:
            match_start, match_end = match
            buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 1)

        else:
            if direccion == 'Adelante':
                inicio = buffer.get_start_iter()

            elif direccion == 'Atras':
                inicio = buffer.get_end_iter()

            self.__seleccionar_texto(texto, inicio, direccion)


class My_FileChooser(Gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio y poder
    hacer "guardar como" sobre un archivo abierto.
    """
    
    __gsignals__ = {
    'load':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}
        
    def __init__(self,
        parent_window = None,
        action_type = None,
        filter_type = None,
        title = None,
        path = None,
        mime_type = None):
        
        Gtk.FileChooserDialog.__init__(self,
            parent = parent_window,
            action = action_type,
            flags = Gtk.DialogFlags.MODAL,
            title = title)
            
        self.set_default_size( 640, 480 )
        self.set_select_multiple(False)

        if os.path.isfile(path):
            self.set_filename(path)

        else:
            self.set_current_folder_uri("file://%s" % path)
        
        if filter_type != None:
            filter = Gtk.FileFilter()
            filter.set_name(filter_type)
            filter.add_pattern(filter_type)
            self.add_filter(filter)
            
        if mime_type != None:
            filter = Gtk.FileFilter()
            filter.set_name("Archivos de texto")
            filter.add_mime_type(mime_type)
            self.add_filter(filter)
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        texto = ""
        if action_type == Gtk.FileChooserAction.OPEN or \
            action_type == Gtk.FileChooserAction.SELECT_FOLDER:
            texto = "Abrir"
        
        elif action_type == Gtk.FileChooserAction.SAVE:
            texto = "Guardar"
            
        abrir = Gtk.Button(texto)
        salir = Gtk.Button("Salir")
        
        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)
        
        self.set_extra_widget(hbox)
        
        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)
        
        self.show_all()
        
        self.connect("file-activated", self.__file_activated)
        
    def __file_activated(self, widget):
        """
        Cuando se hace doble click sobre un archivo.
        """
        
        self.__abrir(None)
        
    def __abrir(self, widget):
        """
        Emite el path del archivo seleccionado.
        """
        
        if not self.get_filename():
            self.__salir(None)
            return
        
        direccion = str(self.get_filename()).replace("//", "/")
        
        # FIXME: Para abrir solo archivos, de lo contrario el filechooser
        # se está utilizando para "guardar como".
        if os.path.exists(direccion) and not os.path.isfile(direccion):
            self.__salir(None)
            return
    
        self.emit('load', direccion)
        
        self.__salir()

    def __salir(self, widget=None):
        """
        Se auto destruye.
        """
        
        self.destroy()

class WidgetAutores(Gtk.Box):
    """
    Box para agregar datos de los Autores
    """

    def __init__(self):
        
        Gtk.Box.__init__(self,
            orientation = Gtk.Orientation.VERTICAL)
            
        self.__agregar(None)
        
        self.show_all()

    def __agregar(self, widget):
        """
        Función para agregar información de un autor.
        """

        box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        entry1 = Gtk.Entry()
        entry2 = Gtk.Entry()
        
        remover = get_boton(Gtk.STOCK_REMOVE, "Eliminar")
        agregar = get_boton(Gtk.STOCK_ADD, "Agregar")
        
        box.pack_start(entry1, False, False, 5)
        box.pack_start(entry2, False, False, 0)
        box.pack_start(remover, False, False, 0)
        box.pack_end(agregar, False, False, 0)
        
        self.pack_start(box, False, False, 0)
        
        agregar.connect("clicked", self.__agregar)
        remover.connect("clicked", self.__quitar)
        
        self.show_all()

    def __quitar(self, widget):
        """
        Función para eliminar informacion de un autor.
        """
        
        if len(self.get_children()) == 1:
            widget.get_parent().get_children()[0].set_text("")
            widget.get_parent().get_children()[1].set_text("")
            
        else:
            widget.get_parent().destroy()

    def get_autores(self):
        """
        Devuelve una lista de tuplas (nombre, mail),
        con todos los autores definidos.
        """

        autores = []
        
        for autor in self.get_children():
            nombre = autor.get_children()[0]
            mail = autor.get_children()[1]
            
            nombre = nombre.get_text()
            nombre = nombre.strip()
            
            mail = mail.get_text()
            mail = mail.strip()
            
            if nombre and mail:
                autores.append( (nombre, mail) )

        return autores

    def set_autores(self, autores):
        """
        Setea los autores.
        """
        
        for x in range(len(autores)-1):
            self.__agregar(None)
            
        for autor in autores:
            nombre, mail = autor
            linea = self.get_children()[autores.index(autor)]
            linea.get_children()[0].set_text(nombre)
            linea.get_children()[1].set_text(mail)

class ToolbarProyecto(Gtk.Toolbar):
    """
    Toolbar para el proyecto.
    """
    
    __gtype_name__ = 'ToolbarProyecto'
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.dict_proyecto = {}
        
        nuevo_proyecto = get_boton(Gtk.STOCK_NEW, "Nuevo Proyecto")
        abrir_proyecto = get_boton(Gtk.STOCK_OPEN, "Abrir Proyecto")
        cerrar_proyecto = get_boton(Gtk.STOCK_CLOSE, "Cerrar Proyecto")
        editar_proyecto = get_boton(Gtk.STOCK_EDIT, "Editar Proyecto")
        guardar_proyecto = get_boton(Gtk.STOCK_SAVE, "Guardar Proyecto")
        ejecutar_proyecto = get_boton(Gtk.STOCK_MEDIA_PLAY, "Ejecutar Proyecto")
        detener = get_boton(Gtk.STOCK_MEDIA_STOP, "Detener Ejecución")

        self.dict_proyecto["Cerrar Proyecto"] = cerrar_proyecto
        self.dict_proyecto["Editar Proyecto"] = editar_proyecto
        self.dict_proyecto["Guardar Proyecto"] = guardar_proyecto
        self.dict_proyecto["Ejecutar Proyecto"] = ejecutar_proyecto
        self.dict_proyecto["Detener Ejecución"] = detener
        
        self.insert(nuevo_proyecto, -1)
        self.insert(abrir_proyecto, -1)
        self.insert(editar_proyecto, -1)
        self.insert(guardar_proyecto, -1)
        self.insert(cerrar_proyecto, -1)
        self.insert(get_separador(draw = True, ancho = 0, expand = False), -1)
        self.insert(ejecutar_proyecto, -1)
        self.insert(detener, -1)
        
        self.insert(get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
        botones = [
            nuevo_proyecto,
            abrir_proyecto,
            cerrar_proyecto,
            editar_proyecto,
            guardar_proyecto,
            ejecutar_proyecto,
            detener]
            
        for boton in botones:
            boton.connect("clicked", self.__emit_accion)
            
        for boton in self.dict_proyecto.keys():
            self.dict_proyecto[boton].set_sensitive(False)
            
    def __emit_accion(self, widget):
        
        self.emit("accion", widget.TOOLTIP)
        
    def activar(self, visibility):
        """
        Activa o desactiva oopciones.
        """
        
        submenus = []
        
        for option in self.dict_proyecto.keys():
            submenus.append(self.dict_proyecto[option])
            
        if visibility:
            map(self.__activar, submenus)
            
        else:
            map(self.__desactivar, submenus)
            
    def __activar(self, option):
        
        if not option.get_sensitive(): option.set_sensitive(True)
        
    def __desactivar(self, option):
        
        if option.get_sensitive(): option.set_sensitive(False)

class ToolbarArchivo(Gtk.Toolbar):
    """
    Toolbar para el archivo
    """
    
    __gtype_name__ = 'ToolbarArchivo'
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.dict_archivo = {}
        
        nuevo_archivo = get_boton(Gtk.STOCK_NEW, "Nuevo Archivo")
        abrir_archivo = get_boton(Gtk.STOCK_OPEN, "Abrir Archivo")
        guardar_archivo = get_boton(Gtk.STOCK_SAVE, "Guardar Archivo")
        guardar_como = get_boton(Gtk.STOCK_SAVE_AS, "Guardar Como")
        ejecutar = get_boton(Gtk.STOCK_MEDIA_PLAY, "Ejecutar Archivo")
        detener = get_boton(Gtk.STOCK_MEDIA_STOP, "Detener Ejecución")
        deshacer = get_boton(Gtk.STOCK_UNDO, "Deshacer")
        rehacer = get_boton(Gtk.STOCK_REDO, "Rehacer")
        copiar = get_boton(Gtk.STOCK_COPY, "Copiar")
        cortar = get_boton(Gtk.STOCK_CUT, "Cortar")
        pegar = get_boton(Gtk.STOCK_PASTE, "Pegar")
        seleccionar_todo = get_boton(Gtk.STOCK_SELECT_ALL, "Seleccionar Todo")

        self.dict_archivo["Guardar"] = guardar_archivo
        self.dict_archivo["Guardar Como"] = guardar_como
        self.dict_archivo["Deshacer"] = deshacer
        self.dict_archivo["Rehacer"] = rehacer
        self.dict_archivo["Copiar"] = copiar
        self.dict_archivo["Cortar"] = cortar
        self.dict_archivo["Pegar"] = pegar
        self.dict_archivo["Seleccionar Todo"] = seleccionar_todo
        self.dict_archivo["Ejecutar Archivo"] = ejecutar
        self.dict_archivo["Detener Ejecución"] = detener
        
        self.insert(get_separador(draw = False, ancho = 10, expand = False), -1)
        
        self.insert(nuevo_archivo, -1)
        self.insert(abrir_archivo, -1)
        self.insert(guardar_archivo, -1)
        self.insert(guardar_como, -1)
        self.insert(get_separador(draw = True, ancho = 0, expand = False), -1)
        self.insert(ejecutar, -1)
        self.insert(detener, -1)
        self.insert(get_separador(draw = True, ancho = 0, expand = False), -1)
        self.insert(deshacer,-1)
        self.insert(rehacer,-1)
        self.insert(get_separador(draw = True, ancho = 0, expand = False), -1)
        self.insert(copiar,-1)
        self.insert(cortar,-1)
        self.insert(pegar,-1)
        self.insert(get_separador(draw = True, ancho = 0, expand = False), -1)
        self.insert(seleccionar_todo,-1)
        
        self.insert(get_separador(draw = False, ancho = 0, expand = True), -1)

        self.show_all()
        
        botones = [
            nuevo_archivo,
            abrir_archivo,
            guardar_archivo,
            guardar_como,
            ejecutar,
            detener,
            deshacer,
            rehacer,
            copiar,
            cortar,
            pegar,
            seleccionar_todo]
            
        for boton in botones:
            boton.connect("clicked", self.__emit_accion)
            
        for boton in self.dict_archivo.keys():
            self.dict_archivo[boton].set_sensitive(False)

    def __emit_accion(self, widget):
        
        self.emit("accion", widget.TOOLTIP)
        
    def update(self, visibility, options):
        """
        Activa o desactiva oopciones.
        """
        
        submenus = []
        
        for option in options:
            if self.dict_archivo.get(option, False):
                submenus.append(self.dict_archivo[option])
            
        if visibility:
            map(self.__activar, submenus)
            
        else:
            map(self.__desactivar, submenus)
            
    def __activar(self, option):
        
        if not option.get_sensitive(): option.set_sensitive(True)
        
    def __desactivar(self, option):
        
        if option.get_sensitive(): option.set_sensitive(False)
        
class ToolbarBusquedas(Gtk.Toolbar):
    
    __gtype_name__ = 'ToolbarBusquedas'
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, GObject.TYPE_STRING)),
    "buscar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        boton = get_boton(Gtk.STOCK_GO_BACK, "Anterior")
        boton.connect("clicked", self.__emit_accion)
        self.insert(boton, -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        
        self.entry = Gtk.Entry()
        self.entry.show()
        
        item.add(self.entry)
        self.insert(item, -1)
        
        boton = get_boton(Gtk.STOCK_GO_FORWARD, "Siguiente")
        boton.connect("clicked", self.__emit_accion)
        self.insert(boton, -1)
        
        self.entry.connect("changed", self.__emit_buscar)
        self.show_all()
        
    def __emit_accion(self, widget):
        """
        Cuando se hace click en anterior y siguiente.
        """
        
        self.emit("accion", widget.TOOLTIP, self.entry.get_text())

    def __emit_buscar(self, widget):
        """
        Cuando cambia el texto a buscar.
        """
        
        self.emit("buscar", widget.get_text())
        
class DialogoAlertaSinGuardar(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario al cerrar un archivo
    que contiene cambios sin guardar.
    """

    __gtype_name__ = 'DialogoAlertaSinGuardar'
    
    def __init__(self, parent_window = None):

        Gtk.Dialog.__init__(self,
            title = "ATENCION !",
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cerrar sin Guardar", Gtk.ResponseType.CLOSE,
                "Cancelar", Gtk.ResponseType.CANCEL])
        
        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label("""
            ¿No se han Guardado los Últimos Cambios en
            El Archivo, Desea Guardarlo Antes de Cerrar?
            """)
            
        label.show()
        self.vbox.add(label)
        
class DialogoSobreEscritura(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario sobre la
    reescritura de un archivo existente.
    """

    __gtype_name__ = 'DialogoSobreEscritura'
    
    def __init__(self, parent_window = None):

        Gtk.Dialog.__init__(self,
            title = "ATENCION !",
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
        
        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label("""
            El Archivo ya Existe.
            ¿Deseas Sobre Escribirlo?
            """)
            
        label.show()
        self.vbox.add(label)
        
class DialogoFormato(Gtk.Dialog):
    """
    Selector de tipografía + fuente
    """

    def __init__(self, parent_window = None):

        Gtk.Dialog.__init__(self,
            title = "Seleccione una tipografía",
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Aceptar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
                
        self.tamano = "10"
        self.fuente = "Monospace"

        self.textoprueba = self.__get_box_prueba()
        self.tree_fuentes = self.__get_treeview_fuentes()
        self.tree_tamanos = self.__get_treeview_tamano()

        self.fuentes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.fuentes.pack_start(self.tree_fuentes, True, True, 0)
        self.fuentes.pack_start(self.tree_tamanos, True, True, 0)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.pack_start(self.fuentes, True, True, 0)
        self.main_box.pack_start(self.textoprueba, False, False, 2)

        self.vbox.pack_start(self.main_box, True, True, 0)
        
        self.set_size_request(400, 400)
        self.set_border_width(15)

        self.show_all()

    def __get_treeview_fuentes(self):
        """
        Devuelve un scroll el cual contiene el treeview
        de las tipografías.
        """

        tree = Gtk.TreeView(Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING))
        columna = Gtk.TreeViewColumn("Tipografía", Gtk.CellRendererText(), markup=0)
        tree.append_column(columna)

        seleccion = tree.get_selection()
        seleccion.set_mode(Gtk.SelectionMode.SINGLE)
        
        seleccion.set_select_function(
            self.__tipografia_tamano_cambiado,
            "Fuente")
            
        scroll = Gtk.ScrolledWindow()
        scroll.add(tree)
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        
        fuentes = []
       
        for family in FUENTES_GLOBAL:
            name = family.get_name()
            fuentes.append(name)

        fuentes.sort()

        for fuente in fuentes:
            modelo = tree.get_model()
            texto = '<span font="%s">%s</span>' % (fuente, fuente)
            modelo.insert(-1, [texto, fuente])

        return scroll

    def __get_treeview_tamano(self):
        """
        Devuelve un scroll el cual contiene el treeview
        de tamaño.
        """

        tree = Gtk.TreeView(Gtk.ListStore(GObject.TYPE_INT))
        columna = Gtk.TreeViewColumn("Tamaño", Gtk.CellRendererText(), text=0)
        tree.append_column(columna)

        seleccion = tree.get_selection()
        seleccion.set_mode(Gtk.SelectionMode.SINGLE)
        
        seleccion.set_select_function(
            self.__tipografia_tamano_cambiado,
            "Tamaño")
            
        scroll = Gtk.ScrolledWindow()
        scroll.add(tree)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        tamanos = [8, 9, 10, 11, 12,
            14, 16, 20, 22, 24, 26,
            28, 36, 48, 72]
            
        for tam in tamanos:
            modelo = tree.get_model()
            modelo.insert(-1, [tam])

        return scroll

    def __get_box_prueba(self):
        """
        Texto para probar la tipografía actualmente
        seleccionada.
        """

        self.texto = Gtk.Label("Texto")
        fuente = Pango.FontDescription("Monospace 10")
        self.texto.modify_font(fuente)

        box = Gtk.EventBox()
        box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        box.add(self.texto)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.add_with_viewport(box)
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.set_size_request(-1, 100)
        
        return scroll

    def __tipografia_tamano_cambiado(self, seleccion, modelo, path, data, tipo):
        """
        Cuando se cambia el tamaño/fuente de la tipografía
        se actualiza el texto con la nueva tipografía.
        """

        iter_sel = modelo.get_iter(path)

        if tipo == "Tamaño":
            self.tamano = modelo.get_value(iter_sel, 0)
            
        elif tipo == "Fuente":
            self.fuente = modelo.get_value(iter_sel, 1)
            
        fuente = Pango.FontDescription("%s %s" % (self.fuente, self.tamano))
        self.texto.modify_font(fuente)

        return True
        
    def obtener_fuente(self):
        """
        Devuelve la fuente y el tamaño seleccionada.
        """

        return [self.fuente, self.tamano]

class DialogoErrores(Gtk.Dialog):
    """
    Diálogo para chequear errores
    """

    def __init__(self, view, parent_window = None, tipo = "pep8"):

        Gtk.Dialog.__init__(self,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = ["Aceptar", Gtk.ResponseType.ACCEPT])

        self.set_size_request(600, 250)
        self.set_border_width(15)
        
        flakerrores = ErroresTreeview(view, tipo)

        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add(flakerrores)
        
        label = Gtk.Label("Errores")
        
        label.show()
        scroll.show_all()
        
        self.vbox.pack_start(label, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 3)
        
class ErroresTreeview(Gtk.TreeView):

    def __init__(self, view, tipo):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_STRING,
            GObject.TYPE_STRING))

        self.view = view
        
        seleccion = self.get_selection()
        seleccion.set_mode(Gtk.SelectionMode.SINGLE)
        seleccion.set_select_function(self.__clicked, self.get_model())
        
        columna = Gtk.TreeViewColumn("Línea", Gtk.CellRendererText(), text=0)
        self.append_column(columna)

        columna = Gtk.TreeViewColumn("Error", Gtk.CellRendererText(), text=1)
        self.append_column(columna)
        
        buffer = view.get_buffer()
        start, end = buffer.get_bounds()

        texto = buffer.get_text(start, end, True)
        
        if tipo == "pep8":
            errores = Pep8.run_check("", texto)
            items = []
            
            for linea in errores:
                if ":" in str(linea):
                    dat = str(linea).split(":")
                    
                    if len(dat) == 4:
                        item = [dat[1].strip(), dat[3].strip()]
                        
                        if not item in items:
                            items.append(item)
                            
                    else:
                        newdat = items[-1]
                        item = [newdat[0].strip(), dat[0].strip()]
                        
                        if not item in items:
                            items.append(item)
                            
            for item in items:
                self.get_model().append(item)
                
        elif tipo == "pyflakes":
            errores = pyflakes.check(texto, "")

            if not type(errores) == int:
            # FIXME: Casos como $%%&$% solo devuelve el Nº de linea.
                for error in errores:
                    dat = str(error).split(":")
                    self.get_model().append([dat[1], dat[2]])
        
    def __clicked(self, treeselection, model, path, is_selected, listore):
        
        iter_sel = model.get_iter(path)
        linea = model.get_value(iter_sel, 0)
        
        self.view._marcar_error(int(linea))
        
        return True
    
class Estructura_Menu(Gtk.Menu):
    """
    Menu con opciones para treeview de Estructura.
    """
    
    __gsignals__ = {
    'accion':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}
    
    def __init__(self, widget, boton, pos, tiempo, path, modelo, accion_previa):
        
        Gtk.Menu.__init__(self)
        
        iterfirst = modelo.get_iter_first()
        iter = modelo.get_iter(path)
        filepath = modelo.get_value(iter, 2)
        
        lectura, escritura, ejecucion = self.__verificar_permisos(filepath)
        
        if os.path.exists(filepath):
            
            if os.path.isfile(filepath):
                import commands
                datos = commands.getoutput('file -ik %s%s%s' % ("\"", filepath, "\""))
                
                if "text" in datos or "x-python" in datos and lectura:
                    self.__get_item(widget, path, "abrir")
                    
                if lectura:
                    self.__get_item(widget, path, "copiar")
 
                if escritura:
                    self.__get_item(widget, path, "cortar")
                
                if escritura:
                    self.__get_item(widget, path, "suprimir")
                    
                if "text" in datos or "x-python" in datos and lectura:
                    self.__get_item(widget, path, "buscar")
                
            elif os.path.isdir(filepath):
                if filepath == modelo.get_value(iterfirst, 2):
                    self.__get_item(widget, path, "eliminar proyecto")
                    
                    self.__get_item(widget, path, "Crear Directorio")
                    
                    if escritura and "copiar" in accion_previa or "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")
                    
                    self.__get_item(widget, path, "buscar")
                    
                else:
                    if lectura:
                        self.__get_item(widget, path, "copiar")
                        
                    if escritura and lectura:
                        self.__get_item(widget, path, "cortar")

                    if escritura and "copiar" in accion_previa or "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")

                    if escritura:
                        self.__get_item(widget, path, "suprimir")
                        self.__get_item(widget, path, "Crear Directorio")
                    
                    if lectura:
                        self.__get_item(widget, path, "buscar")
            
        self.show_all()
        
        self.attach_to_widget(widget, self.__null)

    def __verificar_permisos(self, path):
        # verificar:
        # 1- Si es un archivo o un directorio
        # 2- Si sus permisos permiten la copia, escritura y borrado

        # Comprobar existencia y permisos http://docs.python.org/library/os.html?highlight=os#module-os
        # os.access(path, mode)
        # os.F_OK # si existe la direccion
        # os.R_OK # Permisos de lectura
        # os.W_OK # Permisos de escritura
        # os.X_OK # Permisos de ejecucion
        
        if not os.path.exists(path): return False, False, False
    
        try:
            if  os.access(path, os.F_OK):
                return os.access(path, os.R_OK), os.access(path, os.W_OK), os.access(path, os.X_OK)
            
            else:
                return False, False, False
            
        except:
            return False, False, False
   
    def __null(self):
        pass
    
    def __get_item(self, widget, path, accion):
        """
        Agrega un item al menu.
        """
        
        item = Gtk.MenuItem("%s%s" % (accion[0].upper(), accion[1:]))
        
        self.append(item)
        
        item.connect_object(
            "activate",
            self.__set_accion,
            widget,
            path,
            accion)
            
    def __set_accion(self, widget, path, accion):
        """
        Responde a la seleccion del usuario sobre el menu.
        
        Recibe la lista de sobre la que ha hecho click,
        una accion a realizar sobre el elemento seleccionado en ella y
        el elemento seleccionado y emite una señal con todo para pedir
        confirmacion al usuario sobre la accion a realizar.
        """
        
        iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, iter)

class DialogoEliminar(Gtk.Dialog):
    """
    Diálogo para confirmar la eliminación
    del archivo/directorio seleccionado
    """

    def __init__(self, tipo = "Archivo", parent_window = None):

        Gtk.Dialog.__init__(self,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Si, eliminar!", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
        
        self.set_size_request(300, 100)
        self.set_border_width(15)
        
        label = Gtk.Label("Estás Seguro de que Deseas Eliminar\nel %s Seleccionado?" % tipo)
        
        label.show()
        self.vbox.pack_start(label, True, True, 0)

class BusquedaGrep(Gtk.Dialog):
    """
    Dialogo con un TreeView para busquedas con Grep
    """

    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
        
    def __init__(self, path = None, parent_window = None):

        Gtk.Dialog.__init__(self,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Cerrar", Gtk.ResponseType.ACCEPT])
                
        self.path = path
        
        self.set_size_request(600, 250)
        self.set_border_width(15)
        
        self.treeview = TreeViewBusquedaGrep()
        self.entry = Gtk.Entry()
        buscar = Gtk.Button("Buscar")
        
        hbox = Gtk.HBox()
        hbox.pack_start(self.entry, False, False, 0)
        hbox.pack_start(buscar, False, False, 0)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add(self.treeview)
        
        scroll.show_all()
        hbox.show_all()
        
        self.vbox.pack_start(hbox, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 0)
        
        buscar.connect("clicked", self.__buscar)
        self.treeview.connect("nueva-seleccion", self.__re_emit_nueva_seleccion)
        
    def __re_emit_nueva_seleccion(self, widget, valor):
        
        self.emit("nueva-seleccion", valor)
        
    def __buscar(self, widget):
        """
        Realiza la búsqueda solicitada.
        """
        
        text = self.entry.get_text().strip()
        
        if text:
            import commands
            
            if os.path.isdir(self.path):
                result = commands.getoutput("less | grep -R -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()
                
            elif os.path.isfile(self.path):
                result = commands.getoutput("less | grep -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()
        
            items = []
            for line in result:
                dat = line.split(":")
                
                if os.path.isdir(self.path):
                    if len(dat) == 3: items.append([dat[0], dat[1], dat[2].strip()])
                
                elif os.path.isfile(self.path):
                    if len(dat) == 2: items.append([self.path, dat[0], dat[1].strip()])
                    
            self.treeview.limpiar()
            self.treeview.agregar_items(items)
        
class TreeViewBusquedaGrep(Gtk.TreeView):
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self, Gtk.ListStore(
            GObject.TYPE_STRING, GObject.TYPE_STRING,
            GObject.TYPE_STRING))
        
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)
        
        self.__setear_columnas()
        
        self.treeselection = self.get_selection()
        
        self.show_all()
    
    def do_row_activated(self, path, treviewcolumn):
        
        model = self.get_model()
        iter = model.get_iter(path)
        
        valor = [
            model.get_value(iter, 0),
            model.get_value(iter, 1),
            model.get_value(iter, 2)]
        
        self.emit("nueva-seleccion", valor)
    
    def __setear_columnas(self):
        
        self.append_column(self.__construir_columa('Archivo', 0, True))
        self.append_column(self.__construir_columa('N° de línea', 1, True))
        self.append_column(self.__construir_columa('Línea', 2, True))
        
    def __construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        return columna
    
    def limpiar(self):
        
        self.get_model().clear()
        
    def agregar_items(self, elementos):
        
        GObject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        
    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """
        
        if not elementos:
            self.seleccionar_primero()
            return False
        
        self.get_model().append(elementos[0])
        
        elementos.remove(elementos[0])
        
        GObject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        
    def seleccionar_primero(self, widget = None):
        
        self.treeselection.select_path(0)
