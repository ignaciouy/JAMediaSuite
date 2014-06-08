#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWebCamVideo.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
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
import gobject
import gst
import gtk

from Gstreamer_Bins import Ogv_out_bin
from Gstreamer_Bins import Video_Efectos_bin
from Gstreamer_Bins import v4l2src_bin
from Gstreamer_Bins import Balance_bin
#from Gstreamer_Bins import Xvimage_bin
#from Gstreamer_Bins import Out_lan_jpegenc_bin
from Gstreamer_Bins import Out_lan_smokeenc_bin
from Gstreamer_Bins import In_lan_udpsrc_bin
#from Gstreamer_Bins import Out_lan_speexenc_bin
from Gstreamer_Bins import Foto_bin

gobject.threads_init()
gtk.gdk.threads_init()

PR = False


class JAMediaWebCamVideo(gobject.GObject):

    __gsignals__ = {
    "stop-rafaga": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, []),
    "update": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, ventana_id, device="/dev/video0",
        formato="ogg", efectos=[]):

        gobject.GObject.__init__(self)

        if PR: print "JAMediaWebCamVideo Iniciada"

        self.actualizador = False
        self.tamanio = 0
        self.estado = None
        self.ventana_id = ventana_id
        self.formato = formato
        self.path_archivo = ""
        self.foto_contador = 0

        self.pipeline = gst.Pipeline()

        camara = v4l2src_bin()

        if "/dev/video" in device:
            camara.set_device(device)

        else:
            camara = In_lan_udpsrc_bin(device)

        self.balance = Balance_bin()

        self.tee = gst.element_factory_make(
            'tee', "tee")
        self.tee.set_property('pull-mode', 1)

        self.pipeline.add(camara)
        self.pipeline.add(self.balance)

        if efectos:
            efectos_bin = Video_Efectos_bin(efectos)
            self.pipeline.add(efectos_bin)
            camara.link(efectos_bin)
            efectos_bin.link(self.balance)

        else:
            camara.link(self.balance)

        self.pipeline.add(self.tee)

        queue = gst.element_factory_make(
            'queue', "queue")
        queue.set_property("max-size-buffers", 1000)
        queue.set_property("max-size-bytes", 0)
        queue.set_property("max-size-time", 0)

        ffmpegcolorspace = gst.element_factory_make(
            'ffmpegcolorspace', "ffmpegcolorspace")
        xvimagesink = gst.element_factory_make(
            'xvimagesink', "xvimagesink")
        xvimagesink.set_property(
            "force-aspect-ratio", True)

        self.pipeline.add(queue)
        self.pipeline.add(ffmpegcolorspace)
        self.pipeline.add(xvimagesink)

        self.balance.link(self.tee)

        self.tee.link(queue)
        queue.link(ffmpegcolorspace)
        ffmpegcolorspace.link(xvimagesink)

        fotobin = Foto_bin()
        self.pipeline.add(fotobin)

        self.tee.link(fotobin)

        # FIXME: Por algún motivo no linkea
        #xvimage = Xvimage_bin()
        #self.tee.link(xvimage)

        self.bus = self.pipeline.get_bus()
        self.bus.set_sync_handler(self.__bus_handler)

    def __bus_handler(self, bus, message):

        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                gtk.gdk.threads_enter()
                gtk.gdk.display_get_default().sync()
                message.src.set_xwindow_id(self.ventana_id)
                gtk.gdk.threads_leave()

        #elif message.type == gst.MESSAGE_EOS:
        #    print "gst.MESSAGE_EOS"

        #elif message.type == gst.MESSAGE_QOS:
        #    print "gst.MESSAGE_QOS"

        elif message.type == gst.MESSAGE_LATENCY:
            self.pipeline.recalculate_latency()

        elif message.type == gst.MESSAGE_ERROR:
            print "JAMediaWebCamVideo ERROR:"
            print message.parse_error()

        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            if self.estado != new:
                self.estado = new
                #FIXME: No lo estoy utilizando
                #if new == gst.STATE_PLAYING:
                #    self.emit("estado", "playing")

                #elif new == gst.STATE_PAUSED:
                #    self.emit("estado", "paused")

                #elif new == gst.STATE_NULL:
                #    self.emit("estado", "None")

                #else:
                #    self.emit("estado", "paused")

        return gst.BUS_PASS

    def __new_handle(self, reset, data):
        """
        Elimina o reinicia la funcion que
        envia los datos de actualizacion.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(
                500, self.__handle)

    def __handle(self):
        """
        Consulta el estado y progreso de la grabacion.
        """

        if os.path.exists(self.path_archivo):
            tamanio = os.path.getsize(self.path_archivo)
            tam = int(tamanio) / 1024.0 / 1024.0

            if self.tamanio != tamanio:
                self.tamanio = tamanio

                texto = os.path.basename(self.path_archivo)
                info = "Grabando: %s %.2f Mb" % (texto, tam)

                self.emit('update', info)

        return True

    def set_rotacion(self, rot):

        if PR: print "\tJAMediaWebCamVideo.set_rotacion", rot
        balance = self.pipeline.get_by_name("Balance_bin")
        balance.set_rotacion(rot)

    def get_rotacion(self):

        if PR: print "\tJAMediaWebCamVideo.get_rotacion"
        balance = self.pipeline.get_by_name("Balance_bin")
        return balance.get_rotacion()

    def get_config(self):

        if PR: print "\tJAMediaWebCamVideo.get_config"
        balance = self.pipeline.get_by_name("Balance_bin")
        return balance.get_config()

    def set_efecto(self, efecto, propiedad, valor):

        if PR: print "\tJAMediaWebCamVideo.set_efecto", efecto, propiedad, valor
        ef = self.pipeline.get_by_name("Efectos_bin")

        if ef:
            ef.set_efecto(efecto, propiedad, valor)

    def rotar(self, valor):

        if PR: print "\tJAMediaWebCamVideo.rotar", valor
        balance = self.pipeline.get_by_name('Balance_bin')
        balance.rotar(valor)

    def play(self):

        if PR: print "\tJAMediaWebCamVideo.play"
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):

        print "\tJAMediaWebCamVideo.stop"
        self.__new_handle(False, [])
        self.pipeline.set_state(gst.STATE_NULL)

    def set_balance(self, brillo=False, contraste=False,
        saturacion=False, hue=False, gamma=False):

        if PR: print "\tJAMediaWebCamVideo.set_balance"
        balance = self.pipeline.get_by_name("Balance_bin")

        balance.set_balance(
            brillo=brillo,
            contraste=contraste,
            saturacion=saturacion,
            hue=hue,
            gamma=gamma)

    def set_formato(self, formato):
        """
        Setea formato de salida [ogv, avi, mpeg, ip]
        """

        if PR: print "\tJAMediaWebCamVideo.set_formato", formato
        self.formato = formato

    def filmar(self, path_archivo):
        """
        Conecta a la salida, sea archivo o ip, para grabar o transmitir.
        self.formato, puede ser:
            "", "192.168.1.2", "ogv", "mpeg", "avi"
        """

        if PR: print "\tJAMediaWebCamVideo.filmar"

        self.pipeline.set_state(gst.STATE_NULL)

        formatos = ["ogv", "avi", "mpeg"]
        if self.formato in formatos:
            self.path_archivo = u"%s.%s" % (
                path_archivo, self.formato)

            if self.formato == "ogv":
                out = Ogv_out_bin(self.path_archivo)
                self.pipeline.add(out)
                self.tee.link(out)
                self.play()
                self.__new_handle(True, [])

            elif self.formato == "avi":
                pass

            elif self.formato == "mpeg":
                pass

        else:
            # "Volcado a red lan"
            video_out = Out_lan_smokeenc_bin(self.formato)
            self.pipeline.add(video_out)

            self.tee.link(video_out)
            self.play()
            self.emit('update', "Emitiendo Hacia: %s" % self.formato)

    def fotografiar(self, dir_path, rafaga):

        if PR: print "\tJAMediaWebCamVideo.fotografiar"

        gdkpixbufsink = self.pipeline.get_by_name("gdkpixbufsink")

        pixbuf = gdkpixbufsink.get_property('last-pixbuf')

        if pixbuf and pixbuf != None:
            fecha = datetime.date.today()
            hora = time.strftime("%H-%M-%S")
            archivo = os.path.join(
                dir_path, "JV_%s-%s-%s.png" % (
                fecha, hora, str(self.foto_contador)))

            pixbuf.save(archivo, "png", options={})
            self.foto_contador += 1

            self.emit('update', "%s" % str(
                os.path.basename(archivo)))

        if rafaga < 1.0:
            # FIXME: La primera vez que fotografía no envía la señal
            self.emit("stop-rafaga")

        else:
            gobject.timeout_add(int(rafaga * 1000),
                self.fotografiar, dir_path, rafaga)

        return False
