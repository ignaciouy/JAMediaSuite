#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central

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

import gi
from gi.repository import WebKit

class Navegador(WebKit.WebView):
    """Navegador Web."""
    
    def __init__(self):
        
        WebKit.WebView.__init__(self)
        
        self.show_all()
        
        self.open('https://www.google.com/')
        
        self.set_zoom_level(1.0)
        
        print self.get_settings() # WebKit.WebSettings()
        
    def do_choose_file(self):
        print 'do_choose_file'
        
    def do_close_web_view(self):
        print 'do_close_web_view'
        
    def do_console_message(self, uno, dos, tres):
        
        print 'do_console_message',
        print "*", uno
        print "*",dos
        print "*",tres
        
        """
        do_console_message
        * The page at https://sites.google.com/site/flaviodanesse/ displayed insecure content from http://activities.sugarlabs.org/en-US/sugar/images/t/540/1292037530.
        * 0
        *
        """

    def do_copy_clipboard(self):
        print 'do_copy_clipboard'

    def do_cut_clipboard(self):
        print 'do_cut_clipboard'

    def do_move_cursor(self):
        print 'do_move_cursor'

    def do_navigation_requested(self, webwrame, networkrequest):
        print 'do_navigation_requested', webwrame, networkrequest

    def do_paste_clipboard(self):
        print 'do_paste_clipboard'

    def do_redo(self):
        print 'do_redo'

    def do_script_alert(self):
        print 'do_script_alert'

    def do_script_confirm(self):
        print 'do_script_confirm'

    def do_script_prompt(self):
        print 'do_script_prompt'
        
    def do_select_all(self):
        print 'do_select_all'
        
    def do_set_scroll_adjustments(self):
        print 'do_set_scroll_adjustments'

    #def do_should_allow_editing_action(self):
    #    """Cuando se hace click en el frame, o
    #    cuando se escribe en el buscador."""
        
    #    print 'do_should_allow_editing_action'

    def do_undo(self):
        print 'do_undo'
        
    def do_web_view_ready(self):
        print 'do_web_view_ready'
