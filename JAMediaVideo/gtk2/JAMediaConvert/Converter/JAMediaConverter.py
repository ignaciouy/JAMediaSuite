#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaConverter.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay
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
import time
import datetime
import gst
import gobject

from Bins import wav_bin
from Bins import mp3_bin
from Bins import ogg_bin

def borrar(origen):

    try:
        import os
        import shutil

        if os.path.isdir(origen):
            shutil.rmtree("%s" % (os.path.join(origen)))

        elif os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)))

        else:
            return False

        return True

    except:
        print "ERROR Al Intentar Borrar un Archivo"
        return False

PR = True

gobject.threads_init()


class JAMediaConverter(gobject.GObject):
    """
    Recibe un archivo de audio o un archivo de video y un codec de salida:
        Procesa dicho archivo de la siguiente forma:
            Si recibe un archivo de Video:
                Extraer sus imágenes si codec es uno de: ["jpg", "png"]
                Extraer su audio si codec es uno de: ["ogg", "mp3", "wav"]
                Convierte el archivo a uno de: ["ogv", "mpeg", "avi"]

            Si Recibe un archivo de audio:
                Convierte el archivo a uno de: ["ogg", "mp3", "wav"]
    """

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "newposicion": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "info": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, origen, codec, dirpath_destino):

        gobject.GObject.__init__(self)

        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.actualizador = False
        self.timer = 0
        self.tamanio = 0
        self.origen = origen
        self.dirpath_destino = dirpath_destino
        self.codec = codec
        self.newpath = ""

        self.player = gst.element_factory_make(
            "playbin2", "playbin2")

        if self.codec == "wav":
            self.__run_wav_out()

        elif self.codec == "mp3":
            self.__run_mp3_out()

        elif self.codec == "ogg":
            self.__run_ogg_out()

        self.player.set_property("uri", "file://" + self.origen)

        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __run_wav_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        self.newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(self.newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            self.newpath = os.path.join(self.dirpath_destino, location)

        wavenc = wav_bin(self.newpath)
        self.player.set_property('audio-sink', wavenc)

    def __run_mp3_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        self.newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(self.newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            self.newpath = os.path.join(self.dirpath_destino, location)

        lamemp3enc = mp3_bin(self.newpath)
        self.player.set_property('audio-sink', lamemp3enc)

    def __run_ogg_out(self):

        videoconvert = gst.element_factory_make(
            "fakesink", "video-out")
        self.player.set_property('video-sink', videoconvert)

        # path de salida
        location = os.path.basename(self.origen)

        if "." in location:
            extension = ".%s" % self.origen.split(".")[-1]
            location = location.replace(extension, ".%s" % self.codec)

        else:
            location = "%s.%s" % (location, self.codec)

        self.newpath = os.path.join(self.dirpath_destino, location)

        if os.path.exists(self.newpath):
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            location = "%s_%s_%s" % (fecha, hora, location)
            self.newpath = os.path.join(self.dirpath_destino, location)

        oggenc = ogg_bin(self.newpath)
        self.player.set_property('audio-sink', oggenc)

    def __bus_handler(self, bus, mensaje):

        if mensaje.type == gst.MESSAGE_EOS:
            self.__new_handle(False)
            self.emit("endfile")

        elif mensaje.type == gst.MESSAGE_ERROR:
            err, debug = mensaje.parse_error()
            self.__new_handle(False)
            if PR:
                print "JAMediaConverter ERROR:"
                print "\t%s ==> %s" % (self.origen, self.codec)
                print "\t%s" % err
                print "\t%s" % debug
            self.emit("endfile")

        return gst.BUS_PASS

    def __new_handle(self, reset):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Envia los datos de actualizacion para
        la barra de progreso del reproductor.
        """

        valor1 = None
        valor2 = None
        pos = None
        duracion = None

        # Control de archivo de salida
        if os.path.exists(self.newpath):
            tamanio = os.path.getsize(self.newpath)
            #tam = int(tamanio) / 1024.0 / 1024.0

            if self.tamanio != tamanio:
                self.timer = 0
                self.tamanio = tamanio

            else:
                self.timer += 1

        if self.timer > 60:
            self.stop()
            self.emit("endfile")
            if PR:
                print "JAMediaConverter No Pudo Procesar:", self.newpath
            if os.path.exists(self.newpath):
                borrar(self.newpath)
            return False

        # Control de progreso
        try:
            valor1, bool1 = self.player.query_duration(gst.FORMAT_TIME)
            valor2, bool2 = self.player.query_position(gst.FORMAT_TIME)

        except:
            if PR:
                print "JAMediaConverter ERROR en HANDLER"
            return True

        if valor1 != None:
            duracion = valor1 / 1000000000

        if valor2 != None:
            posicion = valor2 / 1000000000

        if duracion == 0 or duracion == None:
            return True

        pos = int(posicion * 100 / duracion)

        #if pos < 0 or pos > self.duracion:
        #    return True

        if self.duracion != duracion:
            self.duracion = duracion

        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)

        return True

    def play(self):
        self.emit("info", "Procesando ==> %s" % self.codec)

        #if PR:
        #    print "JAMediaConverter Iniciado: %s ==> %s" % (
        #        os.path.basename(self.origen), self.codec)

        self.player.set_state(gst.STATE_PLAYING)
        self.__new_handle(True)

    def stop(self):
        self.__new_handle(False)
        self.player.set_state(gst.STATE_NULL)
        self.emit("info", "  Progreso  ")

        #if PR:
        #    print "JAMediaConverter Detenido: %s" % (
        #        os.path.basename(self.origen))
