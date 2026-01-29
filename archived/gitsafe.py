#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Safe Setup - Interfaz Gráfica
Autor: nilsonmorales
Licencia: GPLv3
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango, GdkPixbuf
import subprocess
import os
import threading
import webbrowser
import locale
import warnings
import sys
import tempfile
import json


warnings.filterwarnings("ignore", category=DeprecationWarning)

# === 🌍 Sistema de Traducción ===
try:
    sys.path.insert(0, '/usr/local/bin')
    from pymenupuplang import TranslationManager
    TR = TranslationManager(app_name="gitsafe") 
except Exception as e:
    print(f"⚠️  pymenupuplang not found: {e}")
    class FallbackTranslator:
        def __init__(self):
            self.translations = {}  
        
        def __getitem__(self, key):
            return key
        
        def get(self, key, default=None):
            return default or key
        
        def get_category_map(self):
            return {}
    
    TR = FallbackTranslator()


class GitConfigGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title=TR["Git Safe Setup"])
        self.set_default_size(700, 650)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # ========== AGREGAR ESTILOS CSS PARA BOTONES PELIGROSOS ==========
        css = """
        .destructive-action {
            background-color: #ff6b6b;
            color: white;
            font-weight: bold;
        }
        .destructive-action:hover {
            background-color: #ff5252;
        }
        .suggested-action {
            background-color: #4ecdc4;
            color: white;
            font-weight: bold;
        }
        """
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        
        screen = Gdk.Screen.get_default()
        style_context = self.get_style_context()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # ========== CONFIGURAR ICONO DE LA VENTANA ==========
        icon_paths = [
            "/usr/local/lib/X11/pixmaps/utility48.png",  
            "/usr/share/pixmaps/git.png",
            "/usr/share/icons/hicolor/48x48/apps/git.png"
        ]
        
        icon_set = False
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
                    self.set_icon(pixbuf)
                    icon_set = True
                    break
                except Exception:
                    pass
        
        if not icon_set:
            self.set_icon_name("preferences-system")
    
        # Verificar si Git está instalado antes de continuar
        if not self.check_git_installed():
            return
        
        # Contenedor principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Header
        header = self.create_header()
        main_box.pack_start(header, False, False, 0)
        
        # Notebook para pestañas
        self.notebook = Gtk.Notebook()
        main_box.pack_start(self.notebook, True, True, 0)
        
        # Pestaña 1: Configuración de Usuario
        user_page = self.create_user_page()
        label = Gtk.Label(label=TR["👤 User"])
        self.notebook.append_page(user_page, label)
        
        # Pestaña 2: Configuraciones
        config_page = self.create_config_page()
        label = Gtk.Label(label=TR["⚙️ Configuration"])
        self.notebook.append_page(config_page, label)
        
        # Pestaña 3: Alias
        alias_page = self.create_alias_page()
        label = Gtk.Label(label=TR["🔖 Alias"])
        self.notebook.append_page(alias_page, label)
        
        # Pestaña 4: SSH
        ssh_page = self.create_ssh_page()
        label = Gtk.Label(label=TR["🔐 SSH"])
        self.notebook.append_page(ssh_page, label)
        
        # Pestaña 5: Repositorio
        repo_page = self.create_repo_page()
        label = Gtk.Label(label=TR["📦 Repository"])
        self.notebook.append_page(repo_page, label)
        
        # Pestaña 6: Tags
        tags_page = self.create_tags_page()
        label = Gtk.Label(label=TR["🏷️ Tags & Releases"])
        self.notebook.append_page(tags_page, label)
        
        # Footer con botones
        footer = self.create_footer()
        main_box.pack_start(footer, False, False, 0)
        
        self.load_current_config()
        
        # 🔹 NUEVO: Cargar último repositorio usado
        self.load_last_repo_on_startup()
        
    def create_header(self):
        """Crear header de la aplicación"""
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        header_box.set_margin_top(10)
        header_box.set_margin_bottom(10)
        
        title = Gtk.Label()
        title.set_markup(f'<span size="x-large" weight="bold">🐙 {TR["Git Safe Setup"]}</span>')
        header_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(label=TR["Configure Git without breaking existing configurations"])
        header_box.pack_start(subtitle, False, False, 0)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.pack_start(separator, False, False, 5)
        
        return header_box
    
    def create_user_page(self):
        """Crear página de configuración de usuario"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        # Nombre de usuario
        name_label = Gtk.Label()
        name_label.set_markup(f'<b>👤 {TR["Username"]}</b>')
        name_label.set_halign(Gtk.Align.START)
        content.pack_start(name_label, False, False, 0)
        
        name_box = Gtk.Box(spacing=10)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text(TR["Your full name"])
        name_box.pack_start(self.name_entry, True, True, 0)
        
        self.name_current = Gtk.Label()
        self.name_current.set_halign(Gtk.Align.START)
        name_box.pack_start(self.name_current, False, False, 0)
        
        content.pack_start(name_box, False, False, 0)
        
        # Email
        email_label = Gtk.Label()
        email_label.set_markup(f'<b>📧 {TR["Email"]}</b>')
        email_label.set_halign(Gtk.Align.START)
        content.pack_start(email_label, False, False, 0)
        
        email_box = Gtk.Box(spacing=10)
        self.email_entry = Gtk.Entry()
        self.email_entry.set_placeholder_text(TR["you@email.com"])
        email_box.pack_start(self.email_entry, True, True, 0)
        
        self.email_current = Gtk.Label()
        self.email_current.set_halign(Gtk.Align.START)
        email_box.pack_start(self.email_current, False, False, 0)
        
        content.pack_start(email_box, False, False, 0)
        
        # Botón guardar
        save_btn = Gtk.Button(label=f"💾 {TR['Save User']}")
        save_btn.connect("clicked", self.save_user_config)
        content.pack_start(save_btn, False, False, 10)
        
        scroll.add(content)
        return scroll
    
    def create_config_page(self):
        """Crear página de configuraciones generales"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        # Editor
        editor_label = Gtk.Label()
        editor_label.set_markup(f'<b>📝 {TR["Default Editor"]}</b>')
        editor_label.set_halign(Gtk.Align.START)
        content.pack_start(editor_label, False, False, 0)
        
        self.editor_combo = Gtk.ComboBoxText()
        editors = ["geany", "nano", "vim", "code", "gedit"]
        for editor in editors:
            self.editor_combo.append_text(editor)
        self.editor_combo.set_active(0)
        content.pack_start(self.editor_combo, False, False, 0)
        
        # Rama por defecto
        branch_label = Gtk.Label()
        branch_label.set_markup(f'<b>🌿 {TR["Default Branch"]}</b>')
        branch_label.set_halign(Gtk.Align.START)
        content.pack_start(branch_label, False, False, 0)
        
        self.branch_entry = Gtk.Entry()
        self.branch_entry.set_text("main")
        content.pack_start(self.branch_entry, False, False, 0)
        
        # Color UI
        self.color_check = Gtk.CheckButton(label=f"🎨 {TR['Enable colors in Git']}")
        self.color_check.set_active(True)
        content.pack_start(self.color_check, False, False, 0)
        
        # Push default
        push_label = Gtk.Label()
        push_label.set_markup(f'<b>⬆️ {TR["Push Strategy"]}</b>')
        push_label.set_halign(Gtk.Align.START)
        content.pack_start(push_label, False, False, 0)
        
        self.push_combo = Gtk.ComboBoxText()
        push_options = ["simple", "current", "matching"]
        for option in push_options:
            self.push_combo.append_text(option)
        self.push_combo.set_active(0)
        content.pack_start(self.push_combo, False, False, 0)
        
        # Pull rebase con explicación
        rebase_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        self.rebase_check = Gtk.CheckButton(label=f"🔄 {TR['Use rebase when pulling']}")
        rebase_box.pack_start(self.rebase_check, False, False, 0)
        
        # Botón de información sobre rebase
        info_btn = Gtk.Button.new_with_label(f"❓ {TR['What is git pull --rebase?']}")
        info_btn.connect("clicked", self.show_rebase_info)
        info_btn.set_margin_start(20)
        rebase_box.pack_start(info_btn, False, False, 0)
        content.pack_start(rebase_box, False, False, 0)
        
        # Credential helper
        cred_label = Gtk.Label()
        cred_label.set_markup(f'<b>🔑 {TR["Credential Cache"]}</b>')
        cred_label.set_halign(Gtk.Align.START)
        content.pack_start(cred_label, False, False, 0)
        
        cred_box = Gtk.Box(spacing=10)
        cred_box.pack_start(Gtk.Label(label=f"{TR['Timeout (seconds)']}:"), False, False, 0)
        self.cred_spin = Gtk.SpinButton()
        self.cred_spin.set_range(0, 86400)
        self.cred_spin.set_increments(300, 3600)
        self.cred_spin.set_value(3600)
        cred_box.pack_start(self.cred_spin, False, False, 0)
        content.pack_start(cred_box, False, False, 0)
        
        # Botón aplicar
        apply_btn = Gtk.Button(label=f"✅ {TR['Apply Configuration']}")
        apply_btn.connect("clicked", self.apply_config)
        content.pack_start(apply_btn, False, False, 10)
        
        scroll.add(content)
        return scroll
    
    def create_alias_page(self):
        """Crear página de alias"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        info_label = Gtk.Label()
        info_label.set_markup(f'<b>🔖 {TR["Recommended Git Aliases"]}</b>')
        info_label.set_halign(Gtk.Align.START)
        content.pack_start(info_label, False, False, 0)
        
        # Lista de alias
        self.alias_checks = {}
        aliases = {
            'st': 'status',
            'co': 'checkout',
            'br': 'branch',
            'cm': 'commit',
            'lg': 'log --graph --oneline --decorate --all',
            'last': 'log -1 HEAD',
            'unstage': 'reset HEAD --',
            'amend': 'commit --amend'
        }
        
        for alias, command in aliases.items():
            check = Gtk.CheckButton()
            check.set_active(True)
            label = Gtk.Label()
            label.set_markup(f'<tt>git {alias}</tt> → <i>{command}</i>')
            label.set_halign(Gtk.Align.START)
            
            box = Gtk.Box(spacing=10)
            box.pack_start(check, False, False, 0)
            box.pack_start(label, True, True, 0)
            
            content.pack_start(box, False, False, 0)
            self.alias_checks[alias] = (check, command)
        
        # Botón aplicar alias
        alias_btn = Gtk.Button(label=f"📌 {TR['Apply Selected Aliases']}")
        alias_btn.connect("clicked", self.apply_aliases)
        content.pack_start(alias_btn, False, False, 10)
        
        scroll.add(content)
        return scroll
    
    def create_ssh_page(self):
        """Crear página de configuración SSH"""
        scroll = Gtk.ScrolledWindow()
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        title = Gtk.Label()
        title.set_markup(f'<b>🔐 {TR["SSH Configuration for GitHub"]}</b>')
        title.set_halign(Gtk.Align.START)
        content.pack_start(title, False, False, 0)
        
        # Estado SSH
        self.ssh_status = Gtk.Label()
        self.ssh_status.set_halign(Gtk.Align.START)
        content.pack_start(self.ssh_status, False, False, 0)
        
        # Botón generar clave
        gen_btn = Gtk.Button(label=f"🔑 {TR['Generate New SSH Key']}")
        gen_btn.connect("clicked", self.generate_ssh_key)
        content.pack_start(gen_btn, False, False, 0)
        
        # Botón para abrir GitHub Settings
        self.github_btn = Gtk.Button(label=f"🌐 {TR['Open GitHub SSH Settings']}")
        self.github_btn.connect("clicked", self.open_github_settings)
        self.github_btn.set_sensitive(False)  # Inicialmente deshabilitado
        content.pack_start(self.github_btn, False, False, 0)
        
        # Área de texto para mostrar la clave pública
        key_label = Gtk.Label()
        key_label.set_markup(f'<b>📋 {TR["Public SSH Key"]}</b>')
        key_label.set_halign(Gtk.Align.START)
        content.pack_start(key_label, False, False, 0)
        
        scroll_text = Gtk.ScrolledWindow()
        scroll_text.set_min_content_height(150)
        
        self.ssh_textview = Gtk.TextView()
        self.ssh_textview.set_editable(False)
        self.ssh_textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scroll_text.add(self.ssh_textview)
        content.pack_start(scroll_text, True, True, 0)
        
        # Botón copiar
        copy_btn = Gtk.Button(label=f"📋 {TR['Copy to Clipboard']}")
        copy_btn.connect("clicked", self.copy_ssh_key)
        content.pack_start(copy_btn, False, False, 0)
        
        # Verificar si ya existe clave
        self.check_ssh_status()
        
        scroll.add(content)
        return scroll
    
    def create_repo_page(self):
        """Crear página para clonar repositorios"""
        scroll = Gtk.ScrolledWindow()
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        title = Gtk.Label()
        title.set_markup(f'<b>📦 {TR["Clone Repository"]}</b>')
        title.set_halign(Gtk.Align.START)
        content.pack_start(title, False, False, 0)
        
        # URL del repositorio
        url_label = Gtk.Label(label=f"{TR['Repository URL']}:")
        url_label.set_halign(Gtk.Align.START)
        content.pack_start(url_label, False, False, 0)
        
        self.repo_entry = Gtk.Entry()
        self.repo_entry.set_placeholder_text(TR["https://github.com/user/repository.git"])
        content.pack_start(self.repo_entry, False, False, 0)
        
        # Directorio destino
        dest_label = Gtk.Label(label=f"{TR['Destination Directory']}:")
        dest_label.set_halign(Gtk.Align.START)
        content.pack_start(dest_label, False, False, 0)
        
        dest_box = Gtk.Box(spacing=10)
        self.dest_entry = Gtk.Entry()
        self.dest_entry.set_text(os.path.expanduser("~"))
        dest_box.pack_start(self.dest_entry, True, True, 0)
        
        browse_btn = Gtk.Button(label="📁")
        browse_btn.connect("clicked", self.browse_directory)
        dest_box.pack_start(browse_btn, False, False, 0)
        content.pack_start(dest_box, False, False, 0)
        
        # Botón clonar
        clone_btn = Gtk.Button(label=f"⬇️ {TR['Clone Repository']}")
        clone_btn.connect("clicked", self.clone_repository)
        content.pack_start(clone_btn, False, False, 10)
        
        # Log de salida
        log_label = Gtk.Label()
        log_label.set_markup(f'<b>📋 {TR["Output"]}</b>')
        log_label.set_halign(Gtk.Align.START)
        content.pack_start(log_label, False, False, 0)
        
        scroll_log = Gtk.ScrolledWindow()
        scroll_log.set_min_content_height(150)
        
        self.log_textview = Gtk.TextView()
        self.log_textview.set_editable(False)
        self.log_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scroll_log.add(self.log_textview)
        content.pack_start(scroll_log, True, True, 0)
        
        scroll.add(content)
        return scroll
        
    def select_repository(self, button=None):
            """Seleccionar un directorio de repositorio Git"""
            dialog = Gtk.FileChooserDialog(
                title=TR["Select Git Repository Directory"],
                parent=self,
                action=Gtk.FileChooserAction.SELECT_FOLDER
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
            
            # 🔹 NUEVO: Cargar último directorio si existe
            last_repo = self.load_last_repository()
            if last_repo and os.path.exists(last_repo):
                dialog.set_current_folder(last_repo)
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                selected_dir = dialog.get_filename()
                os.chdir(selected_dir)  # Cambiar al directorio seleccionado
                
                # 🔹 NUEVO: Guardar el repositorio seleccionado
                self.save_last_repository(selected_dir)
                
                self.update_repo_status()  # Actualizar estado
                self.update_status(f"📁 {TR['Working in']}: {selected_dir}")
            dialog.destroy()         
        
    def create_tags_page(self):
        """Crear página para gestión de Tags y Releases"""
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        title = Gtk.Label()
        title.set_markup(f'<b>🏷️ {TR["Tags &amp; Releases Management"]}</b>')
        title.set_halign(Gtk.Align.START)
        content.pack_start(title, False, False, 0)
        
        # Notebook interno para Tags y Releases
        inner_notebook = Gtk.Notebook()
        
        # Tab 1: Tags
        tags_tab = self.create_tags_tab()
        inner_notebook.append_page(tags_tab, Gtk.Label(label=TR["🏷️ Tags"]))
        
        # Tab 2: Releases
        releases_tab = self.create_releases_tab()
        inner_notebook.append_page(releases_tab, Gtk.Label(label=TR["🚀 Releases"]))
        
        content.pack_start(inner_notebook, True, True, 0)
        
        scroll.add(content)
        return scroll

    def create_tags_tab(self):
        """Crear pestaña de Tags"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        # ========== INDICADOR DE ESTADO DEL REPOSITORIO ==========
        repo_status_box = Gtk.Box(spacing=10)
        self.repo_status_label = Gtk.Label()
        self.repo_status_label.set_halign(Gtk.Align.START)
        repo_status_box.pack_start(self.repo_status_label, False, False, 0)
        box.pack_start(repo_status_box, False, False, 5)
        
        # Agregar botón para seleccionar repositorio
        select_btn = Gtk.Button(label="📂 " + TR["Select Repository"])
        select_btn.connect("clicked", self.select_repository)
        repo_status_box.pack_start(select_btn, False, False, 0)
        
        # ========== SECCIÓN DE LISTAR TAGS ==========
        list_label = Gtk.Label()
        list_label.set_markup(f'<b>📋 {TR["Existing Tags"]}</b>')
        list_label.set_halign(Gtk.Align.START)
        box.pack_start(list_label, False, False, 0)
        
        # Botón para listar tags con opciones de ordenamiento
        list_box = Gtk.Box(spacing=10)
        list_btn = Gtk.Button(label=f"🔄 {TR['List Tags']}")
        list_btn.connect("clicked", self.list_tags)
        list_box.pack_start(list_btn, False, False, 0)
        
        self.tags_sort_combo = Gtk.ComboBoxText()
        self.tags_sort_combo.append_text(TR["Sort by: date"])
        self.tags_sort_combo.append_text(TR["Sort by: name"])
        self.tags_sort_combo.append_text(TR["Sort by: version"])
        self.tags_sort_combo.set_active(0)
        list_box.pack_start(self.tags_sort_combo, False, False, 0)
        
        # Botón para actualizar estado del repositorio
        refresh_btn = Gtk.Button(label="♻️")
        refresh_btn.set_tooltip_text(TR["Refresh repository status"])
        refresh_btn.connect("clicked", lambda b: self.update_repo_status())
        list_box.pack_start(refresh_btn, False, False, 0)
        
        box.pack_start(list_box, False, False, 0)
        
        # Área para mostrar tags
        self.tags_textview = Gtk.TextView()
        self.tags_textview.set_editable(False)
        self.tags_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.tags_textview.set_monospace(True)
        
        tags_scroll = Gtk.ScrolledWindow()
        tags_scroll.set_min_content_height(150)
        tags_scroll.add(self.tags_textview)
        box.pack_start(tags_scroll, True, True, 0)
        
        # Separador
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, False, False, 10)
        
        # ========== SECCIÓN DE CREAR NUEVO TAG ==========
        create_label = Gtk.Label()
        create_label.set_markup(f'<b>✨ {TR["Create New Tag"]}</b>')
        create_label.set_halign(Gtk.Align.START)
        box.pack_start(create_label, False, False, 0)
        
        # Nombre del tag
        tag_name_box = Gtk.Box(spacing=10)
        tag_name_box.pack_start(Gtk.Label(label=f"{TR['Name']}:"), False, False, 0)
        
        self.tag_name_entry = Gtk.Entry()
        self.tag_name_entry.set_placeholder_text("v1.0.0")
        tag_name_box.pack_start(self.tag_name_entry, True, True, 0)
        box.pack_start(tag_name_box, False, False, 0)
        
        # Mensaje del tag
        tag_msg_box = Gtk.Box(spacing=10)
        tag_msg_box.pack_start(Gtk.Label(label=f"{TR['Message']}:"), False, False, 0)
        
        self.tag_msg_entry = Gtk.Entry()
        self.tag_msg_entry.set_placeholder_text(TR["Release v1.0.0"])
        tag_msg_box.pack_start(self.tag_msg_entry, True, True, 0)
        box.pack_start(tag_msg_box, False, False, 0)
        
        # Botones para crear tag
        tag_buttons_box = Gtk.Box(spacing=10)
        
        create_lightweight_btn = Gtk.Button(label=f"🏷️ {TR['Lightweight Tag']}")
        create_lightweight_btn.connect("clicked", self.create_lightweight_tag)
        create_lightweight_btn.set_tooltip_text(TR["Create a simple tag pointing to a commit"])
        tag_buttons_box.pack_start(create_lightweight_btn, False, False, 0)
        
        create_annotated_btn = Gtk.Button(label=f"📝 {TR['Annotated Tag']}")
        create_annotated_btn.connect("clicked", self.create_annotated_tag)
        create_annotated_btn.set_tooltip_text(TR["Create a tag with message and metadata"])
        tag_buttons_box.pack_start(create_annotated_btn, False, False, 0)
        
        box.pack_start(tag_buttons_box, False, False, 0)
        
        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator2, False, False, 10)
        
        # ========== SECCIÓN DE GESTIÓN LOCAL ==========
        local_label = Gtk.Label()
        local_label.set_markup(f'<b>💻 {TR["Local Management"]}</b>')
        local_label.set_halign(Gtk.Align.START)
        box.pack_start(local_label, False, False, 0)
        
        # Campo para especificar tag a eliminar
        local_delete_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        
        # Label de advertencia
        warning_local = Gtk.Label()
        warning_local.set_markup(f'<small><span color="red">⚠️ {TR["WARNING: This action cannot be undone"]}</span></small>')
        warning_local.set_halign(Gtk.Align.START)
        local_delete_box.pack_start(warning_local, False, False, 0)
        
        # Campo para escribir el tag
        local_tag_box = Gtk.Box(spacing=10)
        local_tag_box.pack_start(Gtk.Label(label=f"{TR['Tag to delete']}:"), False, False, 0)
        
        self.delete_local_entry = Gtk.Entry()
        self.delete_local_entry.set_placeholder_text(TR["Enter exact tag name"])
        self.delete_local_entry.set_width_chars(20)
        local_tag_box.pack_start(self.delete_local_entry, True, True, 0)
        local_delete_box.pack_start(local_tag_box, False, False, 0)
        
        # Botón eliminar
        delete_local_btn = Gtk.Button(label=f"🗑️ {TR['Delete Local']}")
        delete_local_btn.get_style_context().add_class("destructive-action")
        delete_local_btn.connect("clicked", self.delete_local_tag)
        delete_local_btn.set_tooltip_text(TR["Delete tag from local repository"])
        local_delete_box.pack_start(delete_local_btn, False, False, 5)
        
        box.pack_start(local_delete_box, False, False, 0)
        
        # Separador
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator3, False, False, 10)
        
        # ========== SECCIÓN DE GESTIÓN REMOTA ==========
        remote_label = Gtk.Label()
        remote_label.set_markup(f'<b>🌐 {TR["Remote Management"]}</b>')
        remote_label.set_halign(Gtk.Align.START)
        box.pack_start(remote_label, False, False, 0)
        
        # Campo para especificar tag a eliminar del remoto
        remote_delete_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        
        # Label de advertencia aún más fuerte
        warning_remote = Gtk.Label()
        warning_remote.set_markup(f'<small><span color="darkred"><b>🚨 {TR["DANGER: This affects ALL collaborators"]}</b></span></small>')
        warning_remote.set_halign(Gtk.Align.START)
        remote_delete_box.pack_start(warning_remote, False, False, 0)
        
        # Campo para escribir el tag
        remote_tag_box = Gtk.Box(spacing=10)
        remote_tag_box.pack_start(Gtk.Label(label=f"{TR['Tag to delete']}:"), False, False, 0)
        
        self.delete_remote_entry = Gtk.Entry()
        self.delete_remote_entry.set_placeholder_text(TR["Enter exact tag name"])
        self.delete_remote_entry.set_width_chars(20)
        remote_tag_box.pack_start(self.delete_remote_entry, True, True, 0)
        remote_delete_box.pack_start(remote_tag_box, False, False, 0)
        
        # Botones remotos en una fila
        remote_buttons_box = Gtk.Box(spacing=10)
        
        push_single_btn = Gtk.Button(label=f"⬆️ {TR['Push Tag']}")
        push_single_btn.connect("clicked", self.push_single_tag)
        push_single_btn.set_tooltip_text(TR["Push selected tag to remote"])
        remote_buttons_box.pack_start(push_single_btn, False, False, 0)
        
        push_all_btn = Gtk.Button(label=f"🚀 {TR['Push All']}")
        push_all_btn.connect("clicked", self.push_all_tags)
        push_all_btn.set_tooltip_text(TR["Push all local tags to remote"])
        remote_buttons_box.pack_start(push_all_btn, False, False, 0)
        
        delete_remote_btn = Gtk.Button(label=f"🗑️ {TR['Delete Remote']}")
        delete_remote_btn.get_style_context().add_class("destructive-action")
        delete_remote_btn.connect("clicked", self.delete_remote_tag)
        delete_remote_btn.set_tooltip_text(TR["Delete tag from remote repository"])
        remote_buttons_box.pack_start(delete_remote_btn, False, False, 0)
        
        remote_delete_box.pack_start(remote_buttons_box, False, False, 5)
        box.pack_start(remote_delete_box, False, False, 0)
        
        box.pack_start(remote_buttons_box, False, False, 0)
        
        # Separador informativo
        info_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(info_separator, False, False, 10)
        
        # ========== INFORMACIÓN ÚTIL ==========
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        info_title = Gtk.Label()
        info_title.set_markup(f'<small><b>💡 {TR["Useful Information"]}</b></small>')
        info_title.set_halign(Gtk.Align.START)
        info_box.pack_start(info_title, False, False, 0)
        
        info_text = Gtk.Label()
        info_text.set_markup(f'''<small>
        • {TR["Tags are like bookmarks for specific commits"]}
        • {TR["Annotated tags contain metadata and are recommended for releases"]}
        • {TR["Lightweight tags are simple pointers to commits"]}
        • {TR["Push tags to share them with collaborators"]}
        </small>''')
        info_text.set_halign(Gtk.Align.START)
        info_text.set_line_wrap(True)
        info_box.pack_start(info_text, False, False, 0)
        
        box.pack_start(info_box, False, False, 0)
        
        return box
    
    def create_releases_tab(self):
        """Crear pestaña de Releases"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        # --- TEXTO INFORMATIVO (CORREGIDO) ---
        info_label = Gtk.Label()
        
        # Texto en inglés por defecto
        default_info = """<b>🚀 What is a Release?</b>

A <b>Release</b> is more than just a tag:
• Includes binaries
• Includes changelogs
• Can be marked as pre-release or stable version

It's the official way to deliver finished software."""
        
        # Intentar obtener la traducción
        translated_info = TR.get('RELEASE_INFO_TEXT', default_info)
        
        # Limpiar solo si es necesario
        if '\\n' in translated_info:
            clean_info = translated_info.replace('\\n', '\n')
        else:
            clean_info = translated_info
        
        info_label.set_markup(clean_info)
        info_label.set_line_wrap(True)
        info_label.set_halign(Gtk.Align.START)
        box.pack_start(info_label, False, False, 0)
        
        # Área para changelog
        changelog_label = Gtk.Label()
        changelog_label.set_markup(f'<b>📝 {TR.get("Changelog (Markdown)", "Changelog (Markdown)")}</b>')
        changelog_label.set_halign(Gtk.Align.START)
        box.pack_start(changelog_label, False, False, 0)
        
        self.changelog_textview = Gtk.TextView()
        self.changelog_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        
        # --- TEXTO POR DEFECTO DEL CHANGELOG (CORREGIDO) ---
        default_changelog = """## 🚀 New Features

- ✅ Functionality implemented
- 🔧 Performance improvement
- 🐛 Bug fixes

## 📋 Technical Changes

- Code refactoring
- Documentation improvements

## 🙏 Acknowledgments

Thanks to all contributors!"""
        
        # Intentar obtener la traducción
        translated_changelog = TR.get('DEFAULT_CHANGELOG', default_changelog)
        
        # Limpiar solo si es necesario
        if '\\n' in translated_changelog:
            clean_changelog = translated_changelog.replace('\\n', '\n')
        else:
            clean_changelog = translated_changelog
        
        buffer = self.changelog_textview.get_buffer()
        buffer.set_text(clean_changelog)
        
        changelog_scroll = Gtk.ScrolledWindow()
        changelog_scroll.set_min_content_height(200)
        changelog_scroll.add(self.changelog_textview)
        box.pack_start(changelog_scroll, True, True, 0)
        
        # Botones de acción
        buttons_box = Gtk.Box(spacing=10)
        
        # Generar changelog automático
        gen_changelog_btn = Gtk.Button(label=f"📊 {TR.get('Generate Changelog', 'Generate Changelog')}")
        gen_changelog_btn.connect("clicked", self.generate_changelog)
        buttons_box.pack_start(gen_changelog_btn, False, False, 0)
        
        # Crear tag preparatorio
        prep_release_btn = Gtk.Button(label=f"🏷️ {TR.get('Create Preparatory Tag', 'Create Preparatory Tag')}")
        prep_release_btn.connect("clicked", self.create_preparatory_release)
        buttons_box.pack_start(prep_release_btn, False, False, 0)
        
        # Exportar información
        export_btn = Gtk.Button(label=f"📤 {TR.get('Export Release Info', 'Export Release Info')}")
        export_btn.connect("clicked", self.export_release_info)
        buttons_box.pack_start(export_btn, False, False, 0)
        
        box.pack_start(buttons_box, False, False, 0)
        
        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator2, False, False, 10)
        
        # Abrir interfaz web
        web_label = Gtk.Label()
        web_label.set_markup(f'<b>🌐 {TR.get("Create Release on GitHub/GitLab", "Create Release on GitHub/GitLab")}</b>')
        web_label.set_halign(Gtk.Align.START)
        box.pack_start(web_label, False, False, 0)
        
        web_buttons_box = Gtk.Box(spacing=10)
        
        # Obtener URL del repositorio
        self.repo_url = ""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.repo_url = result.stdout.strip()
        except:
            pass
            
        if self.repo_url:
            # GitHub Releases
            github_btn = Gtk.Button(label=f"🐙 {TR.get('GitHub Releases', 'GitHub Releases')}")
            github_btn.connect("clicked", lambda b: self.open_releases_page("github"))
            web_buttons_box.pack_start(github_btn, False, False, 0)
            
            # GitLab Releases
            gitlab_btn = Gtk.Button(label=f"🦊 {TR.get('GitLab Releases', 'GitLab Releases')}")
            gitlab_btn.connect("clicked", lambda b: self.open_releases_page("gitlab"))
            web_buttons_box.pack_start(gitlab_btn, False, False, 0)
        else:
            no_repo_label = Gtk.Label(label=f"⚠️ {TR.get('No remote repository detected', 'No remote repository detected')}")
            web_buttons_box.pack_start(no_repo_label, False, False, 0)
            
        box.pack_start(web_buttons_box, False, False, 0)
        
        return box
        
    def create_release_tag(self, button):
        """Crear tag anotado para el release (Paso 1)"""
        version = self.release_version_entry.get_text().strip()
        title = self.release_title_entry.get_text().strip()
        
        if not version:
            self.show_info_dialog(TR.get("Please enter a version", "Por favor introduce una versión"))
            return
        
        # Validar que estamos en un repositorio Git
        if not self.is_git_repository():
            self.show_info_dialog(TR.get("Not in a Git repository", "No estás en un repositorio Git"))
            return
        
        tag_name = f"v{version}"
        
        if not title:
            title = f"Release {tag_name}"
        
        # Obtener changelog
        buffer = self.changelog_textview.get_buffer()
        changelog = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        
        # Mensaje completo del tag
        tag_message = f"{title}\n\n{changelog}"
    
    def create_release_tag(self, button):
            """Crear tag anotado para el release (Paso 1)"""
            version = self.release_version_entry.get_text().strip()
            title = self.release_title_entry.get_text().strip()
            
            if not version:
                self.show_info_dialog(TR.get("Please enter a version", "Por favor introduce una versión"))
                return
            
            # Validar que estamos en un repositorio Git
            if not self.is_git_repository():
                self.show_info_dialog(TR.get("Not in a Git repository", "No estás en un repositorio Git"))
                return
            
            tag_name = f"v{version}"
            
            if not title:
                title = f"Release {tag_name}"
            
            # Obtener changelog
            buffer = self.changelog_textview.get_buffer()
            changelog = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
            
            # Mensaje completo del tag
            tag_message = f"{title}\n\n{changelog}"
            
            # ✅ CAPTURAR self en una variable local
            parent_self = self
            
            def create_tag_thread():
                log_buffer = parent_self.release_log_textview.get_buffer()
                GLib.idle_add(log_buffer.set_text, f"🏷️ {TR.get('Creating tag', 'Creando tag')} {tag_name}...\n")
                
                try:
                    # Verificar si el tag ya existe
                    check_result = subprocess.run(
                        ["git", "tag", "-l", tag_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if tag_name in check_result.stdout:
                        GLib.idle_add(log_buffer.set_text, 
                            f"⚠️ {TR.get('Tag already exists', 'El tag ya existe')}: {tag_name}\n\n"
                            f"{TR.get('Please use a different version or delete the existing tag', 'Por favor usa una versión diferente o elimina el tag existente')}\n"
                        )
                        GLib.idle_add(parent_self.update_status, f"⚠️ {TR.get('Tag already exists', 'El tag ya existe')}")
                        return
                    
                    # Crear tag anotado
                    result = subprocess.run(
                        ["git", "tag", "-a", tag_name, "-m", tag_message],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        output = f"✅ {TR.get('Tag created successfully', 'Tag creado exitosamente')}: {tag_name}\n\n"
                        
                        # Mostrar información del tag
                        tag_info = subprocess.run(
                            ["git", "show", "--quiet", tag_name],
                            capture_output=True,
                            text=True
                        )
                        
                        if tag_info.returncode == 0:
                            output += f"📋 {TR.get('Tag information', 'Información del tag')}:\n"
                            output += "=" * 60 + "\n"
                            output += tag_info.stdout + "\n"
                        
                        output += f"\n✨ {TR.get('Next step', 'Siguiente paso')}: {TR.get('Push tag to remote', 'Subir tag al remoto')}\n"
                        
                        GLib.idle_add(log_buffer.set_text, output)
                        GLib.idle_add(parent_self.update_status, f"✅ {TR.get('Tag created', 'Tag creado')}: {tag_name}")
                    else:
                        error_msg = f"❌ {TR.get('Error creating tag', 'Error creando tag')}:\n{result.stderr}"
                        GLib.idle_add(log_buffer.set_text, error_msg)
                        GLib.idle_add(parent_self.update_status, f"❌ {TR.get('Error creating tag', 'Error creando tag')}")
                        
                except Exception as e:
                    error_msg = f"❌ {TR.get('Error', 'Error')}: {str(e)}"
                    GLib.idle_add(log_buffer.set_text, error_msg)
                    GLib.idle_add(parent_self.update_status, f"❌ {TR.get('Error', 'Error')}")
            
            thread = threading.Thread(target=create_tag_thread)
            thread.daemon = True
            thread.start()

    def push_release_tag(self, button):
            """Subir tag al remoto (Paso 2)"""
            version = self.release_version_entry.get_text().strip()
            
            if not version:
                self.show_info_dialog(TR.get("Please enter a version first", "Por favor introduce primero una versión"))
                return
            
            tag_name = f"v{version}"
            
            # ✅ CAPTURAR self en una variable local
            parent_self = self
            
            def push_tag_thread():
                log_buffer = parent_self.release_log_textview.get_buffer()
                GLib.idle_add(log_buffer.set_text, f"⬆️ {TR.get('Pushing tag to remote', 'Subiendo tag al remoto')}: {tag_name}...\n")
                
                try:
                    # Verificar que el tag existe localmente
                    check_result = subprocess.run(
                        ["git", "tag", "-l", tag_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if tag_name not in check_result.stdout:
                        GLib.idle_add(log_buffer.set_text, 
                            f"❌ {TR.get('Tag not found locally', 'Tag no encontrado localmente')}: {tag_name}\n\n"
                            f"{TR.get('Create the tag first (Step 1)', 'Crea primero el tag (Paso 1)')}\n"
                        )
                        GLib.idle_add(parent_self.update_status, f"❌ {TR.get('Tag not found', 'Tag no encontrado')}")
                        return
                    
                    # Subir tag
                    result = subprocess.run(
                        ["git", "push", "origin", tag_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        output = f"✅ {TR.get('Tag pushed successfully', 'Tag subido exitosamente')}: {tag_name}\n\n"
                        output += f"📤 {TR.get('Output', 'Salida')}:\n"
                        output += result.stdout + result.stderr + "\n"
                        output += f"\n✨ {TR.get('Next step', 'Siguiente paso')}: {TR.get('Create release on web', 'Crear release en la web')}\n"
                        output += f"   {TR.get('Click GitHub or GitLab button', 'Haz clic en el botón de GitHub o GitLab')}\n"
                        
                        GLib.idle_add(log_buffer.set_text, output)
                        GLib.idle_add(parent_self.update_status, f"✅ {TR.get('Tag pushed', 'Tag subido')}: {tag_name}")
                    else:
                        error_msg = f"❌ {TR.get('Error pushing tag', 'Error subiendo tag')}:\n{result.stderr}"
                        GLib.idle_add(log_buffer.set_text, error_msg)
                        GLib.idle_add(parent_self.update_status, f"❌ {TR.get('Error pushing tag', 'Error subiendo tag')}")
                        
                except Exception as e:
                    error_msg = f"❌ {TR.get('Error', 'Error')}: {str(e)}"
                    GLib.idle_add(log_buffer.set_text, error_msg)
                    GLib.idle_add(parent_self.update_status, f"❌ {TR.get('Error', 'Error')}")
            
            thread = threading.Thread(target=push_tag_thread)
            thread.daemon = True
            thread.start()

    def export_release_info(self, button):
        """Exportar información del release a archivo Markdown"""
        version = self.release_version_entry.get_text().strip()
        title = self.release_title_entry.get_text().strip()
        
        if not version:
            self.show_info_dialog(TR.get("Please enter a version", "Por favor introduce una versión"))
            return
        
        tag_name = f"v{version}"
        
        if not title:
            title = f"Release {tag_name}"
        
        buffer = self.changelog_textview.get_buffer()
        changelog = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        
        release_type = self.release_type_combo.get_active_text()
        is_prerelease = "Pre-release" in release_type or "Beta" in release_type
        
        # Crear contenido del archivo
        release_info = f"""# Release {tag_name}: {title}
    
    ## 📋 Información Básica
    
    - **Versión:** {version}
    - **Tag:** {tag_name}
    - **Tipo:** {release_type}
    - **Fecha:** {subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip()}
    - **Pre-release:** {"Sí" if is_prerelease else "No"}
    
    ---
    
    ## 📝 Changelog
    
    {changelog}
    
    ---
    
    ## 📦 Archivos Recomendados para Incluir
    
    Considera adjuntar estos archivos al release en GitHub/GitLab:
    
    - [ ] Binarios compilados (.exe, .AppImage, .deb, .rpm)
    - [ ] Código fuente (.tar.gz, .zip)
    - [ ] Documentación (README.pdf, manual.pdf)
    - [ ] Checksums (SHA256SUMS)
    - [ ] Firmas digitales (.sig, .asc)
    
    ---
    
    ## 🚀 Comandos Git Usados
    
    ```bash
    # Crear tag anotado
    git tag -a {tag_name} -m "{title}"
    
    # Subir tag al remoto
    git push origin {tag_name}
    
    # Ver información del tag
    git show {tag_name}
    ```
    
    ---
    
    ## 🌐 Crear Release en GitHub/GitLab
    
    ### GitHub:
    1. Ir a: https://github.com/USUARIO/REPO/releases/new?tag={tag_name}
    2. El tag {tag_name} ya debería estar seleccionado
    3. Copiar el changelog de arriba
    4. Subir archivos binarios/assets
    5. {"Marcar como pre-release" if is_prerelease else "Publicar como release estable"}
    
    ### GitLab:
    1. Ir a: https://gitlab.com/USUARIO/REPO/-/releases/new
    2. Seleccionar tag {tag_name}
    3. Copiar el changelog de arriba
    4. Subir assets
    5. Crear release
    
    ---
    
    *Generado por Git Safe Setup*
    """
        
        try:
            filename = f"RELEASE_{tag_name}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(release_info)
            
            # Actualizar log
            log_buffer = self.release_log_textview.get_buffer()
            log_buffer.set_text(
                f"✅ {TR.get('Release information exported', 'Información del release exportada')}\n\n"
                f"📄 {TR.get('File', 'Archivo')}: {os.path.abspath(filename)}\n\n"
                f"{TR.get('You can use this file as reference when creating the release', 'Puedes usar este archivo como referencia al crear el release')}\n"
            )
            
            self.update_status(f"✅ {TR.get('Exported to', 'Exportado a')} {filename}")
            self.show_info_dialog(
                f"{TR.get('Release information exported to', 'Información del release exportada a')}:\n\n{os.path.abspath(filename)}"
            )
            
        except Exception as e:
            self.update_status(f"❌ {TR.get('Error exporting', 'Error exportando')}: {str(e)}")
            self.show_error_dialog(f"{TR.get('Error exporting file', 'Error exportando archivo')}: {str(e)}")        
        
    def update_status(self, message):
        """Actualizar mensaje de estado"""
        if hasattr(self, 'status_label'):
            self.status_label.set_text(message)     
            
    def open_releases_page(self, platform):
        """Abrir página de releases en GitHub/GitLab"""
        if not hasattr(self, 'repo_url') or not self.repo_url:
            self.show_info_dialog(TR["No remote repository URL detected"])
            return
        
        try:
            if platform == "github":
                url = self.repo_url
                # Convertir SSH URL a HTTPS si es necesario
                if url.startswith("git@"):
                    url = url.replace(":", "/").replace("git@", "https://")
                
                # Remover .git si existe
                url = url.replace(".git", "")
                
                # Construir URL de releases
                if "/releases" not in url:
                    url = url + "/releases"
                
                webbrowser.open(url)
                self.update_status(f"🌐 {TR['Opening GitHub Releases...']}")
                
            elif platform == "gitlab":
                url = self.repo_url
                # Convertir SSH URL a HTTPS si es necesario
                if url.startswith("git@"):
                    url = url.replace(":", "/").replace("git@", "https://")
                
                # Remover .git si existe
                url = url.replace(".git", "")
                
                # Construir URL de releases para GitLab
                if "/-/releases" not in url:
                    url = url + "/-/releases"
                
                webbrowser.open(url)
                self.update_status(f"🌐 {TR['Opening GitLab Releases...']}")
                
        except Exception as e:
            self.update_status(f"❌ {TR['Error opening browser']}: {str(e)}")                
    
    def create_footer(self):
        """Crear footer con estado y botones"""
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        footer.set_margin_top(5)
        footer.set_margin_bottom(5)
        footer.set_margin_start(5)
        footer.set_margin_end(5)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        
        footer_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        footer_container.pack_start(separator, False, False, 0)
        footer_container.pack_start(footer, False, False, 0)
        
        self.status_label = Gtk.Label(label=f"✨ {TR['Ready to configure']}")
        self.status_label.set_halign(Gtk.Align.START)
        footer.pack_start(self.status_label, True, True, 0)
        
        about_btn = Gtk.Button(label=f"ℹ️ {TR['About']}")
        about_btn.connect("clicked", self.show_about)
        footer.pack_start(about_btn, False, False, 0)
        
        return footer_container
    
    # ========== MÉTODOS DE FUNCIONALIDAD ==========
    
    def check_git_installed(self):
        """Verificar si Git está instalado"""
        try:
            # En Puppy Linux es mejor usar 'which' para verificar binarios
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def load_current_config(self):
        """Cargar configuración actual de Git"""
        try:
            # Nombre
            name = subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True, text=True
            ).stdout.strip()
            if name:
                self.name_current.set_markup(f'<i>{TR["Current"]}: {name}</i>')
                self.name_entry.set_text(name)
            
            # Email
            email = subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True, text=True
            ).stdout.strip()
            if email:
                self.email_current.set_markup(f'<i>{TR["Current"]}: {email}</i>')
                self.email_entry.set_text(email)
            
            # Editor
            editor = subprocess.run(
                ["git", "config", "--global", "core.editor"],
                capture_output=True, text=True
            ).stdout.strip()
            if editor:
                # Buscar el editor en la lista
                editors = ["geany", "nano", "vim", "code", "gedit"]
                for i, e in enumerate(editors):
                    if e in editor:
                        self.editor_combo.set_active(i)
                        break
            
            # Rama por defecto
            branch = subprocess.run(
                ["git", "config", "--global", "init.defaultBranch"],
                capture_output=True, text=True
            ).stdout.strip()
            if branch:
                self.branch_entry.set_text(branch)
            
            # Color UI
            color = subprocess.run(
                ["git", "config", "--global", "color.ui"],
                capture_output=True, text=True
            ).stdout.strip()
            self.color_check.set_active(color != "false")
            
            # Push strategy
            push = subprocess.run(
                ["git", "config", "--global", "push.default"],
                capture_output=True, text=True
            ).stdout.strip()
            if push:
                push_options = ["simple", "current", "matching"]
                for i, option in enumerate(push_options):
                    if option == push:
                        self.push_combo.set_active(i)
                        break
            
            # Pull rebase
            rebase = subprocess.run(
                ["git", "config", "--global", "pull.rebase"],
                capture_output=True, text=True
            ).stdout.strip()
            self.rebase_check.set_active(rebase == "true")
            
            # Credential timeout
            cred = subprocess.run(
                ["git", "config", "--global", "credential.helper"],
                capture_output=True, text=True
            ).stdout.strip()
            if "timeout=" in cred:
                try:
                    timeout = cred.split("timeout=")[1].split()[0]
                    self.cred_spin.set_value(int(timeout))
                except:
                    pass
            
            # Verificar si hay alias configurados
            for alias in self.alias_checks.keys():
                exists = subprocess.run(
                    ["git", "config", "--global", f"alias.{alias}"],
                    capture_output=True, text=True
                ).stdout.strip()
                if exists:
                    self.alias_checks[alias][0].set_active(True)
            
            self.update_status(f"✅ {TR['Current configuration loaded']}")
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    def run_git_command(self, args):
        """Ejecutar comando de git"""
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def save_user_config(self, button):
        """Guardar configuración de usuario"""
        name = self.name_entry.get_text().strip()
        email = self.email_entry.get_text().strip()
        
        if name:
            success, _ = self.run_git_command(["git", "config", "--global", "user.name", name])
            if success:
                self.name_current.set_markup(f'<i>{TR["Current"]}: {name}</i>')
        
        if email:
            success, _ = self.run_git_command(["git", "config", "--global", "user.email", email])
            if success:
                self.email_current.set_markup(f'<i>{TR["Current"]}: {email}</i>')
        
        self.update_status(f"✅ {TR['User configuration saved']}")
    
    def apply_config(self, button):
        """Aplicar configuraciones generales"""
        # Editor
        editor = self.editor_combo.get_active_text()
        self.run_git_command(["git", "config", "--global", "core.editor", editor])
        
        # Rama por defecto
        branch = self.branch_entry.get_text()
        self.run_git_command(["git", "config", "--global", "init.defaultBranch", branch])
        
        # Color
        color = "auto" if self.color_check.get_active() else "false"
        self.run_git_command(["git", "config", "--global", "color.ui", color])
        
        # Push
        push_strategy = self.push_combo.get_active_text()
        self.run_git_command(["git", "config", "--global", "push.default", push_strategy])
        
        # Rebase
        rebase = "true" if self.rebase_check.get_active() else "false"
        self.run_git_command(["git", "config", "--global", "pull.rebase", rebase])
        
        # Credential helper
        timeout = int(self.cred_spin.get_value())
        self.run_git_command([
            "git", "config", "--global", "credential.helper",
            f"cache --timeout={timeout}"
        ])
        
        self.update_status(f"✅ {TR['Configuration applied successfully']}")
    
    def show_rebase_info(self, button):
            """Mostrar información sobre git pull --rebase"""
            dialog = Gtk.Dialog(
                title=TR.get("About git pull --rebase", "Sobre git pull --rebase"),
                transient_for=self,
                flags=0,
                modal=True
            )
            dialog.set_default_size(530, 450)
            
            content_area = dialog.get_content_area()
            content_area.set_spacing(15)
            
            # Título con icono
            title = Gtk.Label()
            title.set_markup('<span size="large" weight="bold">🔄 Git Pull --rebase</span>')
            content_area.pack_start(title, False, False, 10)
            
            # OBTENER Y LIMPIAR TEXTO
            raw_text = TR.get('REBASE_INFO_TEXT', 'Info not found')
            
            # Paso 1: Convertir \\n en saltos reales
            # Paso 2: Eliminar cualquier barra invertida suelta (\) que cause el error
            # Paso 3: Limpiar espacios al inicio y final
            clean_text = raw_text.replace('\\n', '\n').replace('\\', '').strip()
            
            explanation = Gtk.Label()
            explanation.set_markup(clean_text)
            explanation.set_line_wrap(True)
            explanation.set_max_width_chars(65)
            explanation.set_justify(Gtk.Justification.LEFT)
            explanation.set_xalign(0.0)
            
            # Scroll con margen
            scroll = Gtk.ScrolledWindow()
            scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scroll.set_min_content_height(350)
            
            # Añadir un contenedor para dar margen interno (padding)
            viewport = Gtk.Viewport()
            viewport.set_border_width(15)
            viewport.add(explanation)
            scroll.add(viewport)
            
            content_area.pack_start(scroll, True, True, 10)
            
            # Botón de cierre
            close_btn = dialog.add_button(TR.get("Close", "Cerrar"), Gtk.ResponseType.CLOSE)
            close_btn.get_style_context().add_class("suggested-action")
            
            dialog.show_all()
            dialog.run()
            dialog.destroy()    
    
    def apply_aliases(self, button):
        """Aplicar alias seleccionados"""
        count = 0
        for alias, (check, command) in self.alias_checks.items():
            if check.get_active():
                success, _ = self.run_git_command([
                    "git", "config", "--global", f"alias.{alias}", command
                ])
                if success:
                    count += 1
        
        self.update_status(f"✅ {count} {TR['aliases configured']}")
    
    def check_ssh_status(self):
        """Verificar estado de SSH"""
        ssh_key_path = os.path.expanduser("~/.ssh/id_ed25519.pub")
        if os.path.exists(ssh_key_path):
            self.ssh_status.set_markup(f'<span color="green">✅ {TR["SSH key found"]}</span>')
            try:
                with open(ssh_key_path, 'r') as f:
                    key = f.read()
                    buffer = self.ssh_textview.get_buffer()
                    buffer.set_text(key)
                    
                    # Habilitar botón de GitHub si hay una clave
                    self.github_btn.set_sensitive(True)
            except:
                pass
        else:
            # También buscar claves RSA tradicionales
            rsa_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
            if os.path.exists(rsa_key_path):
                self.ssh_status.set_markup(f'<span color="green">✅ {TR["SSH key (RSA) found"]}</span>')
                try:
                    with open(rsa_key_path, 'r') as f:
                        key = f.read()
                        buffer = self.ssh_textview.get_buffer()
                        buffer.set_text(key)
                        self.github_btn.set_sensitive(True)
                except:
                    self.ssh_status.set_markup(f'<span color="orange">⚠️ {TR["No SSH key found"]}</span>')
            else:
                self.ssh_status.set_markup(f'<span color="orange">⚠️ {TR["No SSH key found"]}</span>')
    
    def generate_ssh_key(self, button):
        """Generar nueva clave SSH"""
        email = subprocess.run(
            ["git", "config", "--global", "user.email"],
            capture_output=True, text=True
        ).stdout.strip()
        
        if not email:
            email_dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=TR["Email not configured"]
            )
            email_dialog.format_secondary_text(TR.get('EMAIL_NOT_CONFIGURED_TEXT',
                "You don't have an email configured in Git.\n"
                "Do you want to configure it now?"
            ))
            response = email_dialog.run()
            email_dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
                # Cambiar a pestaña de usuario
                self.notebook.set_current_page(0)
                self.update_status(f"{TR['Please configure your email first']}")
                return
            else:
                # Preguntar por email para la clave SSH
                dialog = Gtk.Dialog(
                    title=TR["Email for SSH key"],
                    transient_for=self,
                    flags=0
                )
                dialog.add_button(TR["Cancel"], Gtk.ResponseType.CANCEL)
                dialog.add_button(TR["Generate"], Gtk.ResponseType.OK)
                
                content = dialog.get_content_area()
                email_entry = Gtk.Entry()
                email_entry.set_placeholder_text(TR["you@email.com"])
                content.pack_start(email_entry, True, True, 10)
                
                dialog.show_all()
                response = dialog.run()
                email = email_entry.get_text().strip()
                dialog.destroy()
                
                if response != Gtk.ResponseType.OK or not email:
                    return
    
    # ... resto del código sin cambios
        
        def generate():
            try:
                # Crear directorio .ssh si no existe
                ssh_dir = os.path.expanduser("~/.ssh")
                os.makedirs(ssh_dir, exist_ok=True)
                
                # Generar clave
                subprocess.run(
                    ["ssh-keygen", "-t", "ed25519", "-C", email, "-f",
                     os.path.expanduser("~/.ssh/id_ed25519"), "-N", ""],
                    check=True
                )
                GLib.idle_add(self.check_ssh_status)
                GLib.idle_add(self.update_status, f"✅ {TR['SSH key generated']}")
            except Exception as e:
                GLib.idle_add(self.update_status, f"❌ {TR['Error']}: {str(e)}")
        
        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()
    
    def copy_ssh_key(self, button):
        """Copiar clave SSH al portapapeles"""
        buffer = self.ssh_textview.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        
        if text.strip():
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(text, -1)
            self.update_status(f"📋 {TR['Key copied to clipboard']}")
        else:
            self.update_status(f"❌ {TR['No key to copy']}")
    
    def open_github_settings(self, button):
        """Abrir la página de configuración SSH de GitHub"""
        url = "https://github.com/settings/keys"
        try:
            webbrowser.open(url)
            self.update_status(f"🌐 {TR['Opening GitHub SSH Settings...']}")
        except Exception as e:
            self.update_status(f"❌ {TR['Could not open browser']}: {str(e)}")
    
    def browse_directory(self, button):
        """Seleccionar directorio"""
        dialog = Gtk.FileChooserDialog(
            title=TR["Select directory"],
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dest_entry.set_text(dialog.get_filename())
        dialog.destroy()
    
    def clone_repository(self, button):
        """Clonar repositorio"""
        url = self.repo_entry.get_text().strip()
        dest = self.dest_entry.get_text().strip()
        
        if not url:
            self.show_info_dialog(TR["Please enter a URL"])
            return
        
        def clone():
            buffer = self.log_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Cloning']} {url}...\n")
            
            try:
                result = subprocess.run(
                    ["git", "clone", url],
                    cwd=dest,
                    capture_output=True,
                    text=True
                )
                
                output = result.stdout + result.stderr
                GLib.idle_add(buffer.set_text, output)
                
                if result.returncode == 0:
                    GLib.idle_add(self.update_status, f"✅ {TR['Repository cloned successfully']}")
                else:
                    GLib.idle_add(self.update_status, f"❌ {TR['Error cloning repository']}")
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"{TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error cloning']}")
        
        thread = threading.Thread(target=clone)
        thread.daemon = True
        thread.start()
        
    def is_git_repository(self):
        """Verificar si el directorio actual es un repositorio Git"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def update_repo_status(self):
        """Actualizar el estado del repositorio actual"""
        if self.is_git_repository():
            try:
                # Obtener ruta del repositorio
                repo_path = subprocess.run(
                    ["git", "rev-parse", "--show-toplevel"],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                
                repo_name = os.path.basename(repo_path) if repo_path else TR["Repository"]
                
                # Obtener rama actual
                branch_result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True
                )
                branch = branch_result.stdout.strip() if branch_result.returncode == 0 else TR["No branch"]
                
                # Obtener número de tags
                tags_result = subprocess.run(
                    ["git", "tag", "-l"],
                    capture_output=True,
                    text=True
                )
                tags_count = len(tags_result.stdout.strip().split('\n')) if tags_result.stdout.strip() else 0
                
                if hasattr(self, 'repo_status_label'):
                    status_text = f"📁 {repo_name} | 🌿 {branch} | 🏷️ {tags_count}"
                    self.repo_status_label.set_markup(f'<span color="green"><b>{status_text}</b></span>')
                    
            except Exception as e:
                if hasattr(self, 'repo_status_label'):
                    self.repo_status_label.set_markup(f'<span color="orange">⚠️ {TR["Git repository"]} ({str(e)[:30]})</span>')
        else:
            if hasattr(self, 'repo_status_label'):
                self.repo_status_label.set_markup(f'<span color="red"><b>❌ {TR["Not a Git repository"]}</b></span>')        
        
    def list_tags(self, button):
        """Listar tags del repositorio"""
        def list_tags_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Listing tags...']}\n\n")
            
            try:
                # Primero verificar que estamos en un repositorio Git
                if not self.is_git_repository():
                    GLib.idle_add(buffer.set_text, 
                        f"❌ {TR['Not a Git repository']}\n\n"
                        f"{TR['Please navigate to a Git repository first']}.\n"
                        f"{TR['You can clone one in the Repository tab']}."
                    )
                    GLib.idle_add(self.update_status, f"❌ {TR['Not in Git repository']}")
                    return
                
                # Obtener el método de ordenamiento
                sort_method = self.tags_sort_combo.get_active_text()
                
                # Configurar comando según método de ordenamiento
                if sort_method == TR["Sort by: date"]:
                    cmd = ["git", "tag", "-l", "--sort=-creatordate"]
                elif sort_method == TR["Sort by: name"]:
                    cmd = ["git", "tag", "-l", "--sort=refname"]
                else:  # Sort by: version
                    cmd = ["git", "tag", "-l", "--sort=version:refname"]
                
                # Obtener tags
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    tags = result.stdout.strip().split('\n')
                    
                    # Formatear salida SIN HTML
                    output = f"🏷️ {TR['Tags found']}: {len(tags)}\n"
                    output += "=" * 60 + "\n\n"
                    
                    for i, tag in enumerate(tags, 1):
                        output += f"{i:3}. {tag}\n"  # ❌ SIMPLE, SIN <b>
                        
                        # Intentar obtener información del tag (para tags anotados)
                        tag_info_cmd = ["git", "show", "--no-patch", "--format=%ci | %s", tag]
                        tag_info = subprocess.run(
                            tag_info_cmd,
                            capture_output=True,
                            text=True
                        )
                        
                        if tag_info.returncode == 0 and tag_info.stdout.strip():
                            info = tag_info.stdout.strip()
                            output += f"     📅 {info}\n"
                            output += f"     📝 {TR['Annotated tag']}\n"
                        else:
                            # Para tags ligeros, obtener información del commit
                            commit_info_cmd = ["git", "log", "-1", "--format=%ci | %s", tag, "--"]
                            commit_info = subprocess.run(
                                commit_info_cmd,
                                capture_output=True,
                                text=True
                            )
                            
                            if commit_info.returncode == 0 and commit_info.stdout.strip():
                                info = commit_info.stdout.strip()
                                output += f"     📅 {info}\n"
                                output += f"     📍 {TR['Lightweight tag']}\n"
                            else:
                                output += f"     ℹ️ {TR['No detailed info available']}\n"
                        
                        output += "\n"
                    
                    GLib.idle_add(lambda: self.display_tags_output(output, len(tags)))
                    
                else:
                    GLib.idle_add(buffer.set_text, 
                        f"📭 {TR['No tags found in this repository']}\n\n"
                        f"{TR['You can create your first tag using the form above']}.\n"
                        f"{TR['Recommended format']}: v1.0.0, release-2024, etc."
                    )
                    GLib.idle_add(self.update_status, f"ℹ️ {TR['No tags found']}")
                    
            except Exception as e:
                error_msg = f"❌ {TR['Error']}: {str(e)}\n\n{TR['Make sure Git is properly installed and configured']}"
                GLib.idle_add(buffer.set_text, error_msg)
                GLib.idle_add(self.update_status, f"❌ {TR['Error listing tags']}")
        
        thread = threading.Thread(target=list_tags_thread)
        thread.daemon = True
        thread.start()
    
    def display_tags_output(self, output, count):
        """Mostrar la salida de tags en el TextView"""
        buffer = self.tags_textview.get_buffer()
        buffer.set_text(output)
        self.update_status(f"✅ {TR['Found']} {count} {TR['tags']}")
        self.update_repo_status()  # Actualizar el contador en el estado
        
    def is_git_repository(self):
        """Verificar si el directorio actual es un repositorio Git"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False        
    
    def create_lightweight_tag(self, button):
        """Crear un tag ligero"""
        tag_name = self.tag_name_entry.get_text().strip()
        
        if not tag_name:
            self.show_info_dialog(TR["Please enter a name for the tag"])
            return
        
        def create_tag_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Creating lightweight tag']} '{tag_name}'...\n")
            
            try:
                result = subprocess.run(
                    ["git", "tag", tag_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['Lightweight tag']} '{tag_name}' {TR['created successfully']}\n\n"
                    # Listar tags actualizados
                    result_list = subprocess.run(
                        ["git", "tag", "-l"],
                        capture_output=True,
                        text=True
                    )
                    output += f"{TR['Current tags']}:\n"
                    output += result_list.stdout
                    
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Tag']} '{tag_name}' {TR['created']}")
                else:
                    GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {result.stderr}")
                    GLib.idle_add(self.update_status, f"❌ {TR['Error creating tag']}")
                    
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error creating tag']}")
        
        thread = threading.Thread(target=create_tag_thread)
        thread.daemon = True
        thread.start()
    
    def create_annotated_tag(self, button):
        """Crear un tag anotado con mensaje"""
        tag_name = self.tag_name_entry.get_text().strip()
        tag_message = self.tag_msg_entry.get_text().strip()
        
        if not tag_name:
            self.show_info_dialog(TR["Please enter a name for the tag"])
            return
        
        if not tag_message:
            tag_message = f"Release {tag_name}"
        
        def create_tag_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Creating annotated tag']} '{tag_name}'...\n")
            
            try:
                result = subprocess.run(
                    ["git", "tag", "-a", tag_name, "-m", tag_message],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['Annotated tag']} '{tag_name}' {TR['created successfully']}\n"
                    output += f"📝 {TR['Message']}: {tag_message}\n\n"
                    
                    # Mostrar información del tag
                    tag_info = subprocess.run(
                        ["git", "show", tag_name],
                        capture_output=True,
                        text=True
                    )
                    
                    if tag_info.returncode == 0:
                        output += tag_info.stdout
                    
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Annotated tag']} '{tag_name}' {TR['created']}")
                else:
                    GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {result.stderr}")
                    GLib.idle_add(self.update_status, f"❌ {TR['Error creating tag']}")
                    
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error creating tag']}")
        
        thread = threading.Thread(target=create_tag_thread)
        thread.daemon = True
        thread.start()
    
    def push_single_tag(self, button):
        """Subir un tag específico al remoto"""
        tag_name = self.tag_name_entry.get_text().strip()
        
        if not tag_name:
            self.show_info_dialog(TR["Please enter the name of the tag to push"])
            return
        
        def push_tag_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Pushing tag']} '{tag_name}' {TR['to remote...']}\n")
            
            try:
                result = subprocess.run(
                    ["git", "push", "origin", tag_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['Tag']} '{tag_name}' {TR['pushed to remote successfully']}\n"
                    output += result.stdout + result.stderr
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Tag']} '{tag_name}' {TR['pushed to remote']}")
                else:
                    GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {result.stderr}")
                    GLib.idle_add(self.update_status, f"❌ {TR['Error pushing tag']}")
                    
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error pushing tag']}")
        
        thread = threading.Thread(target=push_tag_thread)
        thread.daemon = True
        thread.start()
    
    def push_all_tags(self, button):
        """Subir todos los tags al remoto"""
        def push_tags_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Pushing all tags to remote...']}\n")
            
            try:
                result = subprocess.run(
                    ["git", "push", "origin", "--tags"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['All tags pushed to remote successfully']}\n"
                    output += result.stdout + result.stderr
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Tags pushed to remote']}")
                else:
                    GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {result.stderr}")
                    GLib.idle_add(self.update_status, f"❌ {TR['Error pushing tags']}")
                    
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error pushing tags']}")
        
        thread = threading.Thread(target=push_tags_thread)
        thread.daemon = True
        thread.start()
    
    def delete_local_tag(self, button):
        """Eliminar un tag local con múltiples confirmaciones"""
        tag_name = self.delete_local_entry.get_text().strip()
        
        if not tag_name:
            self.show_info_dialog(TR["Please enter the EXACT name of the tag to delete"])
            return
        
        # PRIMERA CONFIRMACIÓN: Diálogo simple
        dialog1 = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"{TR['Confirm local deletion']}"
        )
        dialog1.format_secondary_text(
            f"{TR['You are about to delete the local tag']}:\n\n"
            f"<b>'{tag_name}'</b>\n\n"
            f"{TR['This action cannot be undone']}.\n"
            f"{TR['Are you sure you want to continue']}?"
        )
        response1 = dialog1.run()
        dialog1.destroy()
        
        if response1 != Gtk.ResponseType.YES:
            return
        
        # SEGUNDA CONFIRMACIÓN: Verificar que el tag existe
        try:
            check_result = subprocess.run(
                ["git", "tag", "-l", tag_name],
                capture_output=True,
                text=True
            )
            
            if tag_name not in check_result.stdout:
                self.show_error_dialog(f"{TR['Tag not found']}: '{tag_name}'")
                return
            
        except Exception as e:
            self.show_error_dialog(f"{TR['Error checking tag']}: {str(e)}")
            return
        
        # TERCERA CONFIRMACIÓN: Diálogo final con verificación
        dialog2 = Gtk.Dialog(
            title=TR["FINAL CONFIRMATION"],
            transient_for=self,
            flags=0,
            modal=True
        )
        dialog2.set_default_size(450, 200)
        
        content = dialog2.get_content_area()
        content.set_spacing(15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        # Título con icono de advertencia
        title_label = Gtk.Label()
        title_label.set_markup(f'<span size="large" weight="bold">⚠️ {TR["LAST CHANCE TO CANCEL"]}</span>')
        content.pack_start(title_label, False, False, 0)
        
        # Información del tag
        info_label = Gtk.Label()
        info_label.set_markup(
            f'<b>{TR["You are deleting"]}:</b>\n'
            f'<span size="larger"><b>{tag_name}</b></span>\n\n'
            f'<small>{TR["This will be permanently removed from your local repository"]}</small>'
        )
        info_label.set_line_wrap(True)
        content.pack_start(info_label, False, False, 0)
        
        # Checkbox de confirmación
        confirm_check = Gtk.CheckButton(label=TR["I understand this action cannot be undone"])
        content.pack_start(confirm_check, False, False, 0)
        
        # Botones
        cancel_btn = dialog2.add_button(TR["Cancel"], Gtk.ResponseType.CANCEL)
        delete_btn = dialog2.add_button(TR["DELETE"], Gtk.ResponseType.OK)
        delete_btn.get_style_context().add_class("destructive-action")
        delete_btn.set_sensitive(False)  # Inicialmente deshabilitado
        
        # Habilitar botón solo cuando el checkbox esté marcado
        def on_checkbox_toggled(check):
            delete_btn.set_sensitive(check.get_active())
        
        confirm_check.connect("toggled", on_checkbox_toggled)
        
        dialog2.show_all()
        response2 = dialog2.run()
        dialog2.destroy()
        
        if response2 != Gtk.ResponseType.OK:
            self.update_status(f"❌ {TR['Deletion cancelled']}")
            return
        
        # FINALMENTE: Eliminar el tag
        def delete_tag_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Deleting local tag']} '{tag_name}'...\n")
            
            try:
                result = subprocess.run(
                    ["git", "tag", "-d", tag_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['Local tag']} '{tag_name}' {TR['deleted successfully']}\n\n"
                    output += f"{TR['Output']}: {result.stdout}\n"
                    
                    # Actualizar lista de tags
                    tags_result = subprocess.run(
                        ["git", "tag", "-l"],
                        capture_output=True,
                        text=True
                    )
                    
                    if tags_result.stdout.strip():
                        output += f"\n{TR['Remaining tags']}:\n"
                        output += tags_result.stdout
                    else:
                        output += f"\n📭 {TR['No tags remaining in repository']}"
                    
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Tag']} '{tag_name}' {TR['deleted locally']}")
                    GLib.idle_add(self.delete_local_entry.set_text, "")  # Limpiar campo
                else:
                    error_msg = f"❌ {TR['Error']}: {result.stderr}"
                    GLib.idle_add(buffer.set_text, error_msg)
                    GLib.idle_add(self.update_status, f"❌ {TR['Error deleting tag']}")
                    
            except Exception as e:
                error_msg = f"❌ {TR['Error']}: {str(e)}"
                GLib.idle_add(buffer.set_text, error_msg)
                GLib.idle_add(self.update_status, f"❌ {TR['Error deleting tag']}")
        
        thread = threading.Thread(target=delete_tag_thread)
        thread.daemon = True
        thread.start()
    
    def delete_remote_tag(self, button):
        """Eliminar un tag del remoto con protección máxima"""
        tag_name = self.delete_remote_entry.get_text().strip()
        
        if not tag_name:
            self.show_info_dialog(TR["Please enter the EXACT name of the tag to delete from remote"])
            return
        
        # VERIFICACIÓN 1: El tag debe existir localmente primero
        try:
            local_check = subprocess.run(
                ["git", "tag", "-l", tag_name],
                capture_output=True,
                text=True
            )
            
            if tag_name not in local_check.stdout:
                # Preguntar si quiere proceder de todos modos
                dialog_force = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.YES_NO,
                    text=TR["Tag not found locally"]
                )
                dialog_force.format_secondary_text(
                    f"{TR['The tag']} '{tag_name}' {TR['was not found in your local repository']}.\n\n"
                    f"{TR['This could mean']}:\n"
                    f"• {TR['The tag does not exist']}\n"
                    f"• {TR['You spelled it wrong']}\n"
                    f"• {TR['You need to fetch from remote first']}\n\n"
                    f"{TR['Do you want to attempt deletion anyway']}?"
                )
                response_force = dialog_force.run()
                dialog_force.destroy()
                
                if response_force != Gtk.ResponseType.YES:
                    return
        except Exception as e:
            self.show_error_dialog(f"{TR['Error checking local tags']}: {str(e)}")
            return
        
        # CONFIRMACIÓN MÁXIMA - Diálogo en rojo
        dialog = Gtk.Dialog(
            title="🚨 " + TR["DANGER: DELETE REMOTE TAG"],
            transient_for=self,
            flags=0,
            modal=True
        )
        dialog.set_default_size(500, 300)
        
        # Establecer color de fondo de advertencia
        dialog.get_content_area().override_background_color(
            Gtk.StateFlags.NORMAL,
            Gdk.RGBA(0.9, 0.1, 0.1, 0.1)  # Rojo muy suave
        )
        
        content = dialog.get_content_area()
        content.set_spacing(20)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        
        # Icono y título grande
        title_box = Gtk.Box(spacing=15)
        warning_icon = Gtk.Label(label="🚨")
        warning_icon.set_markup('<span size="xx-large">🚨</span>')
        title_box.pack_start(warning_icon, False, False, 0)
        
        title_text = Gtk.Label()
        title_text.set_markup(f'<span size="large" weight="bold" color="darkred">{TR["DANGER ZONE"]}</span>')
        title_box.pack_start(title_text, False, False, 0)
        content.pack_start(title_box, False, False, 0)
        
        # Mensaje principal
        main_msg = Gtk.Label()
        main_msg.set_markup(
            f'<b>{TR["You are about to DELETE from ALL COLLABORATORS"]}:</b>\n\n'
            f'<span size="larger" weight="bold">"{tag_name}"</span>\n\n'
            f'<small>{TR["This action will affect EVERYONE pulling from this repository"]}</small>'
        )
        main_msg.set_line_wrap(True)
        content.pack_start(main_msg, False, False, 0)
        
        # Checkboxes de confirmación múltiple
        confirm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        check1 = Gtk.CheckButton(label=TR["I understand this affects ALL collaborators"])
        check2 = Gtk.CheckButton(label=TR["I have notified other team members"])
        check3 = Gtk.CheckButton(label=TR["This tag is definitely incorrect or obsolete"])
        check4 = Gtk.CheckButton(label=TR["I accept full responsibility for this action"])
        
        confirm_box.pack_start(check1, False, False, 0)
        confirm_box.pack_start(check2, False, False, 0)
        confirm_box.pack_start(check3, False, False, 0)
        confirm_box.pack_start(check4, False, False, 0)
        
        content.pack_start(confirm_box, False, False, 0)
        
        # Campo para escribir el nombre del tag como verificación final
        verify_box = Gtk.Box(spacing=10)
        verify_box.pack_start(Gtk.Label(label=f"{TR['Type the tag name to confirm']}:"), False, False, 0)
        
        verify_entry = Gtk.Entry()
        verify_entry.set_placeholder_text(tag_name)
        verify_box.pack_start(verify_entry, True, True, 0)
        content.pack_start(verify_box, False, False, 0)
        
        # Botones
        cancel_btn = dialog.add_button(TR["ABORT MISSION"], Gtk.ResponseType.CANCEL)
        delete_btn = dialog.add_button(TR["NUKE FROM ORBIT"], Gtk.ResponseType.OK)
        
        # Estilos para los botones
        cancel_btn.get_style_context().add_class("suggested-action")
        delete_btn.get_style_context().add_class("destructive-action")
        delete_btn.set_sensitive(False)  # Inicialmente deshabilitado
        
        def update_delete_button():
            """Habilitar botón solo cuando TODAS las condiciones se cumplan"""
            all_checked = all([
                check1.get_active(),
                check3.get_active(),
                check4.get_active(),
                verify_entry.get_text().strip() == tag_name
            ])
            delete_btn.set_sensitive(all_checked)
        
        # Conectar eventos
        for check in [check1, check2, check3, check4]:
            check.connect("toggled", lambda w: update_delete_button())
        verify_entry.connect("changed", lambda w: update_delete_button())
        
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.OK:
            self.update_status(f"✅ {TR['Remote deletion wisely cancelled']}")
            return
        
        # FINALMENTE proceder con la eliminación remota
        def delete_remote_thread():
            buffer = self.tags_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"🚨 {TR['Deleting remote tag']} '{tag_name}'...\n")
            
            try:
                result = subprocess.run(
                    ["git", "push", "origin", "--delete", tag_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = f"✅ {TR['Remote tag']} '{tag_name}' {TR['deleted successfully']}\n\n"
                    output += f"{TR['Output']}:\n{result.stdout}\n"
                    
                    # Sugerir también eliminar localmente
                    output += f"\n💡 {TR['Recommendation']}: {TR['You should also delete the local tag']}\n"
                    output += f"   <tt>git tag -d {tag_name}</tt>"
                    
                    GLib.idle_add(buffer.set_text, output)
                    GLib.idle_add(self.update_status, f"✅ {TR['Tag']} '{tag_name}' {TR['deleted from remote']}")
                    GLib.idle_add(self.delete_remote_entry.set_text, "")  # Limpiar campo
                else:
                    error_msg = f"❌ {TR['Error']}: {result.stderr}"
                    GLib.idle_add(buffer.set_text, error_msg)
                    GLib.idle_add(self.update_status, f"❌ {TR['Error deleting remote tag']}")
                    
            except Exception as e:
                error_msg = f"❌ {TR['Error']}: {str(e)}"
                GLib.idle_add(buffer.set_text, error_msg)
                GLib.idle_add(self.update_status, f"❌ {TR['Error deleting remote tag']}")
        
        thread = threading.Thread(target=delete_remote_thread)
        thread.daemon = True
        thread.start()
        
    def generate_changelog(self, button):
        """Generar changelog automático desde los commits"""
        def generate_changelog_thread():
            buffer = self.changelog_textview.get_buffer()
            GLib.idle_add(buffer.set_text, f"{TR['Generating changelog...']}\n")
            
            try:
                # Obtener último tag
                result = subprocess.run(
                    ["git", "describe", "--tags", "--abbrev=0"],
                    capture_output=True,
                    text=True
                )
                
                last_tag = result.stdout.strip() if result.returncode == 0 else ""
                
                # Obtener commits desde el último tag
                if last_tag:
                    cmd = ["git", "log", f"{last_tag}..HEAD", "--oneline", "--format=%h | %s | %an"]
                else:
                    cmd = ["git", "log", "--oneline", "--format=%h | %s | %an"]
                
                commits_result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )
                
                if commits_result.returncode == 0 and commits_result.stdout.strip():
                    commits = commits_result.stdout.strip().split('\n')
                    
                    # Generar changelog organizado
                    changelog = f"## 📋 {TR['Changelog from']} {'last release' if last_tag else 'start'}\n\n"
                    
                    # Categorizar commits
                    features = []
                    fixes = []
                    docs = []
                    other = []
                    
                    for commit in commits:
                        if commit:
                            if "feat:" in commit.lower() or "feature:" in commit.lower():
                                features.append(commit)
                            elif "fix:" in commit.lower() or "bug:" in commit.lower():
                                fixes.append(commit)
                            elif "doc:" in commit.lower() or "docs:" in commit.lower():
                                docs.append(commit)
                            else:
                                other.append(commit)
                    
                    if features:
                        changelog += f"### 🚀 {TR['New Features']}\n"
                        for feat in features:
                            changelog += f"- {feat}\n"
                        changelog += "\n"
                    
                    if fixes:
                        changelog += f"### 🐛 {TR['Bug Fixes']}\n"
                        for fix in fixes:
                            changelog += f"- {fix}\n"
                        changelog += "\n"
                    
                    if docs:
                        changelog += f"### 📖 {TR['Documentation']}\n"
                        for doc in docs:
                            changelog += f"- {doc}\n"
                        changelog += "\n"
                    
                    if other:
                        changelog += f"### 🔧 {TR['Other Changes']}\n"
                        for oth in other:
                            changelog += f"- {oth}\n"
                    
                    if last_tag:
                        changelog += f"\n*{TR['Compared with tag']}: {last_tag}*\n"
                    
                    GLib.idle_add(buffer.set_text, changelog)
                    GLib.idle_add(self.update_status, f"✅ {TR['Changelog generated']}")
                else:
                    GLib.idle_add(buffer.set_text, f"❌ {TR['No new commits found']}")
                    GLib.idle_add(self.update_status, f"❌ {TR['No commits for changelog']}")
                    
            except Exception as e:
                GLib.idle_add(buffer.set_text, f"❌ {TR['Error']}: {str(e)}")
                GLib.idle_add(self.update_status, f"❌ {TR['Error generating changelog']}")
        
        thread = threading.Thread(target=generate_changelog_thread)
        thread.daemon = True
        thread.start()
    
    def create_preparatory_release(self, button):
        """Crear tag y preparar todo para un release"""
        version = self.release_version_entry.get_text().strip()
        title = self.release_title_entry.get_text().strip()
        
        if not version:
            self.show_info_dialog(TR["Please enter a version for the release"])
            return
        
        if not title:
            title = f"Release v{version}"
        
        # Crear tag anotado
        tag_name = f"v{version}"
        buffer = self.changelog_textview.get_buffer()
        changelog = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        
        release_type = "pre-release" if "Pre-release" in self.release_type_combo.get_active_text() else "stable"
        
        def create_release_thread():
            output = f"🚀 {TR['Preparing release']} {tag_name} ({release_type})\n"
            output += "=" * 50 + "\n\n"
            
            GLib.idle_add(self.tags_textview.get_buffer().set_text, output)
            
            try:
                # 1. Crear tag anotado
                result = subprocess.run(
                    ["git", "tag", "-a", tag_name, "-m", f"{title}\n\n{changelog}"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    output += f"❌ {TR['Error creating tag']}: {result.stderr}\n"
                    GLib.idle_add(self.tags_textview.get_buffer().set_text, output)
                    return
                
                output += f"✅ {TR['Tag']} '{tag_name}' {TR['created']}\n"
                
                # 2. Obtener información del tag
                tag_info = subprocess.run(
                    ["git", "show", "--quiet", tag_name],
                    capture_output=True,
                    text=True
                )
                
                if tag_info.returncode == 0:
                    output += f"\n📋 {TR['Tag information']}:\n"
                    output += tag_info.stdout + "\n"
                
                # 3. Exportar información para GitHub/GitLab
                release_info = f"""# {TR['Release']} {tag_name}
    
    **{TR['Title']}:** {title}
    **{TR['Type']}:** {release_type}
    **{TR['Tag']}:** {tag_name}
    **{TR['Date']}:** {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
    
    ## {TR['Changelog']}
    
    {changelog}
    
    ## {TR['Commands to publish']}
    
    ```bash
    # {TR['Push tag to remote']}
    git push origin {tag_name}
    
    # {TR['Then create the release in the web interface']}
    # {TR['GitHub']}: https://github.com/USER/REPO/releases/new?tag={tag_name}
    # {TR['GitLab']}: https://gitlab.com/USER/REPO/-/releases/new
    ```"""
                
                # Guardar en archivo
                with open(f"RELEASE_{tag_name}.md", "w") as f:
                    f.write(release_info)
                
                output += f"\n📄 {TR['Information saved in']}: RELEASE_{tag_name}.md\n"
                output += f"🌐 {TR['Use this file to create the release on GitHub/GitLab']}\n"
                
                GLib.idle_add(self.tags_textview.get_buffer().set_text, output)
                GLib.idle_add(self.update_status, f"✅ {TR['Release']} {tag_name} {TR['prepared']}")
                
            except Exception as e:
                output += f"❌ {TR['Error']}: {str(e)}\n"
                GLib.idle_add(self.tags_textview.get_buffer().set_text, output)
                GLib.idle_add(self.update_status, f"❌ {TR['Error preparing release']}")
        
        thread = threading.Thread(target=create_release_thread)
        thread.daemon = True
        thread.start()
    
    def export_release_info(self, button):
        """Exportar información del release a archivo"""
        version = self.release_version_entry.get_text().strip()
        title = self.release_title_entry.get_text().strip()
        
        if not version:
            self.show_info_dialog(TR["Please enter a version"])
            return
        
        tag_name = f"v{version}"
        
        buffer = self.changelog_textview.get_buffer()
        changelog = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        
        release_type = "pre-release" if "Pre-release" in self.release_type_combo.get_active_text() else "stable"
        
        # Crear información del release
        release_info = f"""# {TR['Release']} {tag_name}
    
    ## {TR['Basic Information']}
    
    - **{TR['Version']}:** {version}
    - **{TR['Tag']}:** {tag_name}
    - **{TR['Title']}:** {title if title else f"Release v{version}"}
    - **{TR['Type']}:** {release_type}
    - **{TR['Date']}:** {subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip()}
    
    ## {TR['Changelog']}
    
    {changelog}
    
    ## {TR['Assets to Include (optional)']}
    
    - [ ] {TR['Compiled binaries']}
    - [ ] {TR['PDF documentation']}
    - [ ] {TR['SHA256 checksums']}
    - [ ] {TR['Source code .zip']}
    
    ## {TR['Git Commands']}
    
    ```bash
    # {TR['Create tag']}
    git tag -a {tag_name} -m "{title if title else f'Release v{version}'}"
    
    # {TR['Push tag']}
    git push origin {tag_name}
    
    # {TR['Create release from existing tag']}
    # ({TR['use GitHub/GitLab web interface']})
    ```"""
        
        try:
            # Guardar en archivo
            filename = f"RELEASE_{tag_name}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(release_info)
            
            self.update_status(f"✅ {TR['Information exported to']} {filename}")
            self.show_info_dialog(f"{TR['Release information exported to']}:\n{os.path.abspath(filename)}")
            
        except Exception as e:
            self.update_status(f"❌ {TR['Error exporting']}: {str(e)}")
    
    def show_info_dialog(self, message):
        """Mostrar diálogo de información"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def show_about(self, widget):
        """Muestra el diálogo de información"""
        # Crear un diálogo personalizado en lugar de usar Gtk.AboutDialog
        dialog = Gtk.Dialog(
            title=TR["About Git Safe Setup"],
            transient_for=self,
            flags=0,
            modal=True
        )
        dialog.set_default_size(600, 500)
        dialog.set_border_width(10)
        
        content_area = dialog.get_content_area()
        content_area.set_spacing(15)
        
        # --- INFORMACIÓN PRINCIPAL (CENTRADA) ---
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        info_box.set_halign(Gtk.Align.CENTER)
        
        # Icono centrado
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        icon_box.set_halign(Gtk.Align.CENTER)
        
        icon_paths = [
            "/usr/local/lib/X11/pixmaps/utility48.png",  
            "/usr/share/pixmaps/git.png",
            "/usr/share/icons/hicolor/48x48/apps/git.png"
        ]
        
        icon_set = False
        for path in icon_paths:
            if os.path.exists(path):
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
                    pixbuf_scaled = pixbuf.scale_simple(48, 48, GdkPixbuf.InterpType.BILINEAR)
                    icon = Gtk.Image.new_from_pixbuf(pixbuf_scaled)
                    icon_box.pack_start(icon, False, False, 0)
                    icon_set = True
                    break
                except Exception:
                    pass
        
        if not icon_set:
            icon = Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.DIALOG)
            icon_box.pack_start(icon, False, False, 0)
        
        info_box.pack_start(icon_box, False, False, 0)
        
        # Título centrado
        title = Gtk.Label()
        title.set_markup(f'<span size="large" weight="bold">{TR["Git Safe Setup"]}</span>')
        title.set_halign(Gtk.Align.CENTER)
        info_box.pack_start(title, False, False, 0)
        
        # Información centrada
        version = Gtk.Label(label="Version 1.0")
        version.set_halign(Gtk.Align.CENTER)
        info_box.pack_start(version, False, False, 0)
        
        author = Gtk.Label(label="Author: nilsonmorales")
        author.set_halign(Gtk.Align.CENTER)
        info_box.pack_start(author, False, False, 0)
        
        description = Gtk.Label(label=TR["Graphical tool to configure Git on Puppy Linux"])
        description.set_line_wrap(True)
        description.set_halign(Gtk.Align.CENTER)
        description.set_max_width_chars(50)
        info_box.pack_start(description, False, False, 0)
        
        content_area.pack_start(info_box, False, False, 10)
        
        # Separador
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        content_area.pack_start(separator1, False, False, 10)
        
        # --- LICENCIA CON SCROLL ---
        license_label = Gtk.Label()
        license_label.set_markup(f'<b>License: WTFPL (Do What The Fuck You Want To Public License)</b>')
        license_label.set_halign(Gtk.Align.START)
        content_area.pack_start(license_label, False, False, 0)
        
        # Área de texto con scroll para la licencia
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(250)
        
        license_textview = Gtk.TextView()
        license_textview.set_editable(False)
        license_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        license_textview.set_cursor_visible(False)
        license_textview.set_monospace(True)
        
        # Texto de la licencia (versión corta para legibilidad)
        license_text = """DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO."""
        
        buffer = license_textview.get_buffer()
        buffer.set_text(license_text)
        
        scroll.add(license_textview)
        content_area.pack_start(scroll, True, True, 10)
        
        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        content_area.pack_start(separator2, False, False, 10)
        
        # --- BOTÓN DE CERRAR ---
        close_btn = dialog.add_button(TR.get("Close", "Close"), Gtk.ResponseType.CLOSE)
        close_btn.get_style_context().add_class("suggested-action")
        
        dialog.show_all()
        dialog.run()
        dialog.destroy()
    
    def show_error_dialog_and_exit(self, message):
        """Mostrar diálogo de error y cerrar la aplicación"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=TR["Fatal Error"]
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
        Gtk.main_quit()
    
    def show_error_dialog(self, message):
        """Mostrar diálogo de error"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
        
    def save_last_repository(self, path):
        """Guardar el último repositorio usado"""
        config_path = os.path.join(tempfile.gettempdir(), "gitsafe_last_repo.json")
        try:
            with open(config_path, 'w') as f:
                json.dump({"last_repo": path}, f)
        except:
            pass

    def load_last_repository(self):
        """Cargar el último repositorio usado"""
        config_path = os.path.join(tempfile.gettempdir(), "gitsafe_last_repo.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    return data.get("last_repo")
        except:
            pass
        return None
    
    def load_last_repo_on_startup(self):
        """Cargar automáticamente el último repositorio usado"""
        last_repo = self.load_last_repository()
        if last_repo and os.path.exists(last_repo):
            try:
                # Cambiar al directorio del último repo
                os.chdir(last_repo)
                
                # Verificar si realmente es un repositorio Git
                if self.is_git_repository():
                    self.update_repo_status()
                    self.update_status(f"✅ {TR['Loaded last repository']}: {os.path.basename(last_repo)}")
                else:
                    # Si no es repo Git, no hacer nada
                    pass
            except Exception as e:
                # Si falla, simplemente no cargar nada
                print(f"No se pudo cargar último repositorio: {e}")        

def main():
    # Verificar Git antes de crear la ventana
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except:
        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=TR["Fatal Error"]
        )
        dialog.format_secondary_text(TR.get('GIT_NOT_INSTALLED_TEXT', '''Git is not installed on the system.

Please install Git first:
• Puppy Linux: pkg install git
• Debian/Ubuntu: apt-get install git
• Fedora: dnf install git'''))
        dialog.run()
        dialog.destroy()
        return
    
    app = GitConfigGUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
