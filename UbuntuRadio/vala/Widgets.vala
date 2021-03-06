/*
   Widgets.vala por:
   Flavio Danesse <fdanesse@gmail.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/


public class MenuUbuntuRadio : Gtk.MenuBar{
    /*
    Menú Principal de la aplicación
    */

    public signal void radios();
    public signal void configurar();
    public signal void creditos();
    public signal void actualizar();
    public signal void salir();

    public MenuUbuntuRadio(){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Menú");

		Gtk.Menu menu = new Gtk.Menu ();
		item1.set_submenu(menu);

		Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Radios");
        item2.activate.connect(this.emit_listar_radios);
        menu.append(item2);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Configurar...");
        item3.activate.connect(this.emit_configurar);
        menu.append(item3);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Creditos...");
        item4.activate.connect(this.emit_creditos);
        menu.append(item4);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Actualizar Lista");
        item5.activate.connect(this.emit_actualizar);
        menu.append(item5);

        Gtk.MenuItem item6 = new Gtk.MenuItem.with_label("Salir");
        item6.activate.connect(this.emit_salir);
        menu.append(item6);

		this.add (item1);
        this.show_all();
    }

    private void emit_listar_radios(){
        this.radios();
    }

    private void emit_configurar(){
        this.configurar();
    }

    private void emit_creditos(){
        this.creditos();
    }

    private void emit_actualizar(){
        this.actualizar();
    }

    private void emit_salir(){
        this.salir();
    }
}


public class MenuStreamList : Gtk.Menu{
    /*
    Menú Contextual para la lista de Streamings
    */

    public signal void accion(string acc, string val1,
        string val2, string val3);

    private Gtk.ListStore lista;
    private Gtk.TreePath pathstream;
    private Gtk.TreeIter iter;
    private string _val1;
    private string _val2;
    private string _val3;

    public MenuStreamList(Gtk.Widget widget, Gtk.TreePath _path,
        Gtk.ListStore _model){

        this.lista = _model;
        this.pathstream = _path;

	    GLib.Value val1;
	    GLib.Value val2;
	    GLib.Value val3;

	    this.lista.get_iter(out this.iter, this.pathstream);

        this.lista.get_value(iter, 0, out val1);
	    this.lista.get_value(iter, 1, out val2);
	    this.lista.get_value(iter, 2, out val3);

	    this._val1 = (string) val1;
	    this._val2 = (string) val2;
	    this._val3 = (string) val3;

		Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Reproducir");
        item2.activate.connect(this.emit_play);
        this.append(item2);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Quitar de la Lista");
        item3.activate.connect(this.remove_item);
        this.append(item3);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Borrar Streaming");
        item4.activate.connect(this.borrar_item);
        this.append(item4);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Grabar");
        item5.activate.connect(this.emit_record);
        this.append(item5);

        this.show_all();

        this.attach_to_widget(widget, null);
    }

    private void borrar_item(){

        this.lista.remove(this.iter);
    }

    private void remove_item(){

        this.lista.remove(this.iter);
        this.accion("borrar", this._val1, this._val2, this._val3);
    }

    private void emit_play(){

        this.accion("play", this._val1, this._val2, this._val3);
    }

    private void emit_record(){

        this.accion("record", this._val1, this._val2, this._val3);
    }
}


public class ItemPlayer : Gtk.Frame{
    /*
    Widget con Reproductor de Streaming
    */

    private Gtk.Button stop_button = new Gtk.Button();
    private Gtk.Image image_button = new Gtk.Image();
    private UbuntuRadioPlayer player = new UbuntuRadioPlayer();
    private Gtk.Label label = new Gtk.Label("Nada para Reproducir");

    public ItemPlayer(){

        this.set_label(" Reproduciendo . . . ");

        Gtk.EventBox eventbox = new Gtk.EventBox();
        eventbox.set_border_width(5);
        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        eventbox.add(hbox);
        this.add(eventbox);

        Gtk.VolumeButton control_volumen = new Gtk.VolumeButton();

        hbox.pack_start(this.label,
            false, true, 0);
        hbox.pack_end(this.stop_button,
            false, true, 0);
        hbox.pack_end(control_volumen,
            false, true, 0);

        this.image_button.set_from_stock(
            Gtk.Stock.MEDIA_PLAY, Gtk.IconSize.BUTTON);
        this.stop_button.set_image(this.image_button);

        control_volumen.set_value(0.10);

        this.show_all();

        this.player.estado.connect(this.update_estado);
        //FIXME: No parece funcionar
        this.player.endfile.connect(this.endfile);
        control_volumen.value_changed.connect(this.player.set_volumen);
        this.stop_button.clicked.connect(this.play_stop);
    }

    public void stop(){
        /*
        Se usa para detener el reproductor al cerrar la aplicación
        */

        if (this.player._estado == "playing"){
            this.player.stop();
            }
    }

    public void load(string bandera, string _name, string uri){
        /*
        Carga un streaming en el Reproductor.
        */

        this.label.set_text(_name);
        this.player.load(uri);
    }

    private void update_estado(string estado){
        /*
        Recibe el estado del reproductor cada vez que este cambia
        */

        if (estado == "playing"){
            Idle.add (() => {
                this.image_button.set_from_stock(
                Gtk.Stock.MEDIA_STOP, Gtk.IconSize.BUTTON);
                return false;});
        }
        else{
            Idle.add (() => {
                this.image_button.set_from_stock(
                Gtk.Stock.MEDIA_PLAY, Gtk.IconSize.BUTTON);
                return false;});
        }
    }

    private void play_stop(){
        /*
        Cuando se hace click en el botón stop
        */

        if (this.player._estado == "playing"){
            this.player.stop();
            }

        else{
            this.player.play();
            }
    }

    private void endfile(){
        /*
        Cuando termina la reproducción
        */

        Idle.add (() => {
            this.image_button.set_from_stock(
            Gtk.Stock.MEDIA_PLAY, Gtk.IconSize.BUTTON);
            return false;});
    }

}


public class ItemRecord : Gtk.Frame{
    /*
    Widget con Grabador de Streaming
    */

    private Gtk.Button stop_button = new Gtk.Button();
    private Gtk.Image image_button = new Gtk.Image();
    private UbuntuRadioRecord player = new UbuntuRadioRecord("", "", "");
    private Gtk.Label infolabel = new Gtk.Label("Grabación Detenida");
    private Gtk.Label label = new Gtk.Label("Nada para Grabar");

    public ItemRecord(){

        this.set_label(" Grabando . . . ");

        Gtk.EventBox eventbox = new Gtk.EventBox();
        eventbox.set_border_width(5);
        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
        eventbox.add(vbox);
        this.add(eventbox);

        hbox.pack_start(this.label,
            false, true, 0);
        hbox.pack_end(this.stop_button,
            false, true, 0);

        vbox.pack_start(hbox,
            false, true, 0);
        vbox.pack_start(this.infolabel,
            false, true, 0);

        this.image_button.set_from_stock(
            Gtk.Stock.MEDIA_STOP, Gtk.IconSize.BUTTON);
        this.stop_button.set_image(this.image_button);

        this.show_all();

        this.stop_button.clicked.connect(this.play_stop);
    }

    public void stop(){
        /*
        Se usa para detener el reproductor al cerrar la aplicación
        */

        if (this.player._estado == "playing"){
            this.player.stop();
            }
    }

    public void load(string bandera, string _name, string uri){
        /*
        Carga un streaming en el Reproductor.
        */

        if (this.player._estado == "playing"){
            this.player.stop();
            }

        this.player = null;
        this.player = new UbuntuRadioRecord(_name, uri, "ogg");
        this.label.set_text(_name);
        this.player.estado.connect(this.update_estado);
        //this.player.update.connect(this.update_info);
        //FIXME: No parece funcionar
        this.player.endfile.connect(this.endfile);
    }

    private void update_estado(string estado){
        /*
        Recibe el estado del reproductor cada vez que este cambia
        */

        //stdout.printf ("%s\n", estado);
        if (estado == "playing"){
            Idle.add (() => {
                this.infolabel.set_text("Grabando . . .");
                this.image_button.set_from_stock(
                Gtk.Stock.MEDIA_STOP, Gtk.IconSize.BUTTON);
                return false;});
        }
        else{
            Idle.add (() => {
                this.infolabel.set_text("Grabación Detenida");
                this.image_button.set_from_stock(
                Gtk.Stock.MEDIA_RECORD, Gtk.IconSize.BUTTON);
                return false;});
        }
    }

    private void play_stop(){
        /*
        Cuando se hace click en el botón stop
        */

        if (this.player._estado == "playing"){
            this.player.stop();
            }

        else{
            this.player.play();
            }
    }

    private void endfile(){
        /*
        Cuando termina la reproducción
        */

        Idle.add (() => {
            this.infolabel.set_text("Grabación Detenida");
            this.image_button.set_from_stock(
            Gtk.Stock.MEDIA_RECORD, Gtk.IconSize.BUTTON);
            return false;});
    }
}


public class Streaming : GLib.Object{
    /*
    Un Elemento para la lista de Streamings es una lista
    de 3 elementos que contiene:
        path al icono de la bandera
        nombre del streamings
        url del streaming
    */

    public string icono;
    public string nombre;
    public string url;

    public Streaming(string icono, string nombre, string url){
        this.icono = icono;
        this.nombre = nombre;
        this.url = url;
    }
}


public class Lista : Gtk.TreeView{

    private Gtk.ListStore lista = new Gtk.ListStore(
        3, typeof (string), typeof (string), typeof (string));

    public signal void play(string val1, string val2, string val3);
    public signal void record(string val1, string val2, string val3);

    public Lista(){

        this.set_model(this.lista);

        this.insert_column_with_attributes(
            -1, "", new Gtk.CellRendererText(), "text", 0);
        this.insert_column_with_attributes(
            -1, "Emisora", new Gtk.CellRendererText(), "text", 1);
        this.insert_column_with_attributes(
            -1, "", new Gtk.CellRendererText(), "text", 2);

        this.lista.set_sort_column_id(1, Gtk.SortType.DESCENDING);
        this.set("headers_visible", true);
        this.set("activate_on_single_click", true);
        this.set("headers_clickable", true);
        this.show_all();

        this.row_activated.connect(this.clicked);
    }

    private void clicked(Gtk.TreePath _path, Gtk.TreeViewColumn column){

        MenuStreamList menu = new MenuStreamList(this, _path, this.lista);
        menu.accion.connect(this.set_accion);
        menu.popup(null, null, null, 1, Gtk.get_current_event_time());
    }

    private void set_accion(string accion, string val1,
        string val2, string val3){
        /*
        Responde a selecciones del usuario en el
        menú contextual de los streamings.
        */

        if (accion == "play"){
            this.play(val1, val2, val3);
            }
        else if (accion == "record"){
            this.record(val1, val2, val3);
            }
        else if (accion == "borrar"){
            }
    }

    public void set_lista(SList<Streaming> list){

        this.lista.clear();

        foreach (Streaming streaming in list){
            Gtk.TreeIter iter;
            this.lista.append (out iter);
            this.lista.set (iter, 0, streaming.icono,
                1, streaming.nombre, 2, streaming.url);
        }
    }

}


public class Creditos : Gtk.Dialog{

    public Creditos(Gtk.Window parent, string title){

        this.set("title", title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set("border_width", 15);

        this.set_decorated(false);
        this.set_resizable(false);

        Gtk.Image imagen = new Gtk.Image();
        imagen.set_from_file("Iconos/creditos.svg");

        Gtk.Box Box = this.get_content_area ();
        Box.pack_start(imagen, true, true, 0);
        Box.show_all();

        this.add_button ("Cerrar", Gtk.ResponseType.OK);
    }
}


public class Descargas : Gtk.Dialog{

    public Descargas(Gtk.Window parent, string title){

        this.set("title", title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set("border_width", 15);

        this.set_decorated(false);
        this.set_resizable(false);

        Gtk.Label label = new Gtk.Label("*** Descargando Streamings ***");

        Gtk.Box Box = this.get_content_area();
        Box.pack_start(label, true, true, 0);
        Box.show_all();

        this.realize.connect(this.realized);
    }

    private void realized(){

        GLib.Timeout.add(500, this.descargar);
    }

    private bool descargar(){

        get_streaming_default();

        this.destroy();

        return false;
    }
}
