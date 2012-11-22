#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGlobals.py por:
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
import commands
import urllib
import shelve

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GdkX11

if not os.path.exists(os.path.join(os.environ["HOME"], "JAMediaDatos")):
    os.mkdir(os.path.join(os.environ["HOME"], "JAMediaDatos"))
    os.chmod(os.path.join(os.environ["HOME"], "JAMediaDatos"), 0755)
    
'''
# unificar directorios de JAMedia, JAMediaVideo y JAMediaImagenes
directorio_viejo = os.path.join(os.environ["HOME"], ".JAMediaDatos")
directorio_nuevo = os.path.join(os.environ["HOME"], "JAMediaDatos")
if os.path.exists(directorio_viejo):
    for elemento in os.listdir(directorio_viejo):
        commands.getoutput('mv %s %s' % (os.path.join(directorio_viejo,
            elemento), directorio_nuevo))
    commands.getoutput('rm -r %s' % (directorio_viejo))'''

# Directorios JAMedia
DIRECTORIO_MIS_ARCHIVOS = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "MisArchivos")
    
DIRECTORIO_DATOS = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "Datos")
    
if not os.path.exists(DIRECTORIO_MIS_ARCHIVOS):
    os.mkdir(DIRECTORIO_MIS_ARCHIVOS)
    os.chmod(DIRECTORIO_MIS_ARCHIVOS, 0755)
    
if not os.path.exists(DIRECTORIO_DATOS):
    os.mkdir(DIRECTORIO_DATOS)
    os.chmod(DIRECTORIO_DATOS, 0755)

# Directorio JAMediaTube
DIRECTORIO_YOUTUBE = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "YoutubeVideos")
    
if not os.path.exists(DIRECTORIO_YOUTUBE):
    os.mkdir(DIRECTORIO_YOUTUBE)
    os.chmod(DIRECTORIO_YOUTUBE, 0755)

# Directorios JAMediaVideo
AUDIO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "Audio")
    
if not os.path.exists(AUDIO_JAMEDIA_VIDEO):
    os.mkdir(AUDIO_JAMEDIA_VIDEO)
    os.chmod(AUDIO_JAMEDIA_VIDEO, 0755)
    
VIDEO_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "Videos")
    
if not os.path.exists(VIDEO_JAMEDIA_VIDEO):
    os.mkdir(VIDEO_JAMEDIA_VIDEO)
    os.chmod(VIDEO_JAMEDIA_VIDEO, 0755)
    
IMAGENES_JAMEDIA_VIDEO = os.path.join(os.environ["HOME"],
    "JAMediaDatos", "Fotos")
    
if not os.path.exists(IMAGENES_JAMEDIA_VIDEO):
    os.mkdir(IMAGENES_JAMEDIA_VIDEO)
    os.chmod(IMAGENES_JAMEDIA_VIDEO, 0755)

GRIS = Gdk.Color(60156, 60156, 60156)
AMARILLO = Gdk.Color(65000,65000,40275)
NARANJA = Gdk.Color(65000,26000,0)
BLANCO = Gdk.Color(65535, 65535, 65535)
NEGRO = Gdk.Color(0, 0, 0)

def get_pixels(centimetros):
    """ Recibe un tamaño en centimetros y
    devuelve el tamaño en pixels que le corresponde,
    según tamaño del monitor que se está utilizando.
    
    # 1 px = 0.026458333 cm #int(centimetros/0.026458333)
    # 1 Pixel = 0.03 Centimetros = 0.01 Pulgadas. """

    screen = GdkX11.X11Screen()
    
    res_w = screen.width()
    res_h = screen.height()
    
    mm_w = screen.width_mm()
    mm_h = screen.height_mm()
    
    ancho = int (float(res_w) / float(mm_w) * 10.0 * centimetros)
    alto = int (float(res_h) / float(mm_h) * 10.0 * centimetros)
    
    return int(min([ancho, alto]))

def get_separador(draw = False, ancho = 0, expand = False):
    """ Devuelve un separador generico."""
    
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador

def get_boton(archivo, flip = False,
    color = Gdk.Color(65000, 65000, 65000), rotacion = None, pixels = 0):
    """ Devuelve un toolbutton generico."""
    
    if not pixels:
        pixels = get_pixels(1)
        
    boton = Gtk.ToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixels, pixels)
    if flip: pixbuf = pixbuf.flip(True)
    if rotacion: pixbuf = pixbuf.rotate_simple(rotacion)
    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    return boton

def get_togle_boton(archivo, flip = False,
    color = Gdk.Color(65000, 65000, 65000), pixels = 0):
    """ Devuelve un toggletoolbutton generico."""
    
    if not pixels:
        pixels = get_pixels(1.5)
        
    boton = Gtk.ToggleToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixels, pixels)
    if flip: pixbuf = pixbuf.flip(True)
    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    return boton


# >>> JAMedia
canales = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/canales'
radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/radios'

def descarga_lista_de_streamings(url):
    """Recibe la web donde se publican los streamings
    de radio o televisión de JAMedia y devuelve la lista
    de streamings. Un streaming se representa por una lista:
    [nombre, url]"""
    
    try:
        streamings = []
        
        web = urllib.urlopen(url)
        lineas = web.readlines()
        web.close()
        
        for linea in lineas:
            if 'table' in linea:
                l = linea.split('table')
                
                for x in l:
                    if '<div>' in x:
                        xx = x.split('<div>')
                        
                        for z in xx:
                            if "," in z:
                                s = z.split('</div>')[0]
                                stream = s.split(",")
                                streamings.append(stream)
                                
        return streamings
    
    except:
        return []
    
def clear_lista_de_streamings(path):
    """Limpia la lista de streamings en un archivo."""
    
    archivo = shelve.open(path)
    archivo.clear()
    archivo.close()
    
def guarda_lista_de_streamings(path, items):
    """Recibe el path a un archivo de lista de streamings
    de JAMedia y una lista de items [nombre, url] y los almacena
    en el archivo."""
    
    archivo = shelve.open(path)
    for item in items:
        archivo[item[0]] = item[1]
    archivo.close()
    
def get_streamings(path):
    """Recibe el path a un archivo de streamings
    y devuelve la lista de streamings que contiene."""
    
    archivo = shelve.open(path)
    items = archivo.items()
    archivo.close()
    
    return items

def set_listas_default():
    """ Crea las listas para JAMedia si es que no existen y
    llena las default en caso de estar vacías."""

    listas = [
        os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
        ]
        
    for archivo in listas:
        if not os.path.exists(archivo):
            jamedialista = shelve.open(archivo)
            jamedialista.close()
            os.chmod(archivo, 0666)
            
    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"))
    lista = archivo.items()
    archivo.close()
    
    if not lista:
        try:
            # Streamings JAMediatv
            lista_canales = descarga_lista_de_streamings(canales)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"), lista_canales)
            
        except:
            print "Error al descargar Streamings de TV."
            
    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    archivo = shelve.open(os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"))
    lista = archivo.items()
    archivo.close()
    
    if not lista:
        try:
            # Streamings JAMediaradio
            lista_radios = descarga_lista_de_streamings(radios)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"), lista_radios)

        except:
            print "Error al descargar Streamings de Radios."
    
def get_streaming_default():
    """ Descarga los streaming desde la web de JAMedia
    cuando el usuario lo solicita."""
    
    try:
        # Streamings JAMediatv
        lista_canales = descarga_lista_de_streamings(canales)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"), lista_canales)
        
    except:
        print "Error al descargar Streamings de TV."
        
    try:
        # Streamings JAMediaradio
        lista_radios = descarga_lista_de_streamings(radios)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"), lista_radios)
        
    except:
        print "Error al descargar Streamings de Radios."
        
def add_stream(tipo, item):
    """Agrega un streaming a la lista correspondiente de jamedia."""
    
    if "TV" in tipo or "Tv" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
        
    elif "Radio" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")
        
    else:
        return
    
    archivo = shelve.open(path)
    archivo[item[0]] = item[1]
    archivo.close()

def eliminar_streaming(url, lista):
    """Elimina un Streaming de una lista de jamedia."""
    
    if lista == "Radios":
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")
        
    elif lista == "TVs":
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
        
    elif lista == "JAM-Radio":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia")
        
    elif lista == "JAM-TV":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia")
        
    else:
        return
    
    archivo = shelve.open(path)
    items = archivo.items()
    
    for item in items:
        if url == str(item[1]):
            del (archivo[item[0]])
            
    archivo.close()

def stream_en_archivo(streaming, path):
    """Verifica si un streaming está en
    un archivo de lista de jamedia determinado."""
    
    archivo = shelve.open(path)
    items = archivo.values()
    
    for item in items:
        if streaming == item:
            archivo.close()
            return True
        
    archivo.close()
    return False
# <<< JAMedia

# >>> JAMediaTube
def set_shelve_lista(archivo, videos):
    """Recibe un nombre de archivo para almacenar datos
    de videos de JAMediaTube.
    
    datos es una lista de diccionarios que representan videos."""
    
    archivo = "%s.tube" % archivo
    archivo = os.path.join(DIRECTORIO_DATOS, archivo)
    
    lista = shelve.open(archivo)
    
    for elemento in videos:
        lista[elemento["id"]] = elemento
    
    lista.close()
    
def get_shelve_lista(archivo):
    """Recibe un nombre de archivo shelve que contiene
    videos de JAMediaTube y los devuelve."""
    
    lista = shelve.open(archivo)
    
    keys = lista.keys()
    videos = []
    
    for item in keys:
        videos.append(lista[item])
    
    lista.close()
    
    return videos
# <<< JAMediaTube

# >>> JAMediaVideo
VIDEOEFECTOS = [
    'agingtv',
    'bulge',
    #'burn',            # FIXME: No percibo ningún efecto
    'chromium',
    'dicetv',
    #'diffuse',         # FIXME: Demasiado lento
    #'dilate',          # FIXME: No percibo ningún efecto
    #'dodge',           # FIXME: No percibo ningún efecto
    'edgetv',
    'exclusion',        # FIXME: Lento
    'fisheye',
    'funnel',
    'frei0r-filter-cartoon',
    'frei0r-filter-distort0r',
    'frei0r-filter-edgeglow',
    'frei0r-filter-nervous',
    'frei0r-filter-primaries',
    'frei0r-filter-rgb-parade',
    'frei0r-filter-sobel',
    'marble',
    #'gaussianblur',    # FIXME: Demasiado lento
    'optv',
    #'quarktv',         # Muy Lento, pero buenisimo
    'radioactv',
    'rippletv',
    'revtv',
    'shagadelictv',
    'solarize',
    'streaktv',
    'vertigotv',
    'warptv',
    ]
    # clockoverlay
    # circle
    # fpsdisplaysink
    # InputSelector
    
# <<< JAMediaVideo

'''
Anotaciones para describir las clases de JAMedia:
    import pydoc
    import JAMediaObjects
    from JAMediaObjects.JAMediaReproductor import JAMediaReproductor

    pydoc.writedoc(JAMediaReproductor)'''
    