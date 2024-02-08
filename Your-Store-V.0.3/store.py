import tkinter as tk
from tkinter import StringVar, OptionMenu
from tkinter import ttk
import customtkinter
from functools import partial
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO
import subprocess
import platform
import threading

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    # Download new Database
    try:
        url = "https://raw.githubusercontent.com/The-Bumble-BEE/Your-Store/main/store_data.json"
        response = requests.get(url)
        if response.status_code == 200:
            with open("data/store.json", 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    
    except:
        print("Something went wrong!")    
        
    with open('data/store.json', 'r') as file:
        app_info = json.load(file)
    

    frames = {}
    current = None

    def __init__(self):
        super().__init__()
        self.title("Download Store")
        self.geometry("800x600")
        self.nav_buttons = [] 
        # root!
        main_container = customtkinter.CTkFrame(self, corner_radius=8, fg_color=self.cget("fg_color"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Einstellungsbutton
        settings_button = customtkinter.CTkButton(main_container, text="Settings", command=self.open_settings)
        settings_button.place(relx=0.034, rely=0.01)  # Angenommene relative Position

        # Dropdown-Menü
        options = ["All", "Office", "Communication", "Multimedia", "Creativity", "Browser", "Games", "Coding"]
        self.selected_option = customtkinter.StringVar(value="All")
        combobox = customtkinter.CTkComboBox(master=main_container,  # use root as the master
                                             values=options,
                                             command=self.on_dropdown_change,
                                             variable=self.selected_option)
        
        combobox.place(relx=0.22, rely=0.01)
        
        # self.selected_option = StringVar(self)
        # self.selected_option.set(options[0])
        # dropdown_menu = OptionMenu(main_container, self.selected_option, *options, command=self.on_dropdown_change)
        # dropdown_menu.place(relx=0.22, rely=0.01)  # Angenommene relative Position

        # Search bar
        self.search_var = tk.StringVar()
        search_entry = customtkinter.CTkEntry(main_container, textvariable=self.search_var, placeholder_text="Search", placeholder_text_color="white")
        search_entry.place(relx=0.4, rely=0.01, relwidth=0.5)  # Angenommene Position und Breite
        search_entry.bind("<KeyRelease>", self.filter_apps)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkScrollableFrame(main_container, width=200, corner_radius=8, fg_color=self.cget("fg_color"))
        self.left_side_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=18, pady=40)

        # right side panel -> to show the frame1 or frame 2, or ... frame + n where n <= 5
        self.right_side_panel = customtkinter.CTkFrame(main_container, corner_radius=8, fg_color="#212121")
        self.right_side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=40)
        self.right_side_panel.configure(border_width=1)
        self.right_side_panel.configure(border_color="#323232")

        # Initialisierung der Anwendung
        self.initialize_app()
        
    def destroy_nav_buttons(self):
        for button in self.nav_buttons:
            button.destroy()
        self.nav_buttons = [] 

    def on_dropdown_change(self, *args):
        # Diese Funktion wird aufgerufen, wenn sich die Dropdown-Auswahl ändert
        #print("Dropdown-Auswahl geändert")
        self.initialize_app()

    def initialize_app(self):
        selected_value = self.selected_option.get()
        print(selected_value)
        self.destroy_nav_buttons()
        for app in App.app_info:
            if selected_value == app["category"] or selected_value == "All":
                self.create_nav(self.left_side_panel, app["name"], app["Install_Befehl"], app["Beschreibung"], app["Image"], app["state"])

        # Hier kannst du die Logik für die Initialisierung der Anwendung mit den neuen Daten durchführen
        
        print("Initialisiere Anwendung mit ausgewählter Option:", selected_value)
        # Hier kannst du die Schleife for app in App.aa_info ausführen und die Anwendung aktualisieren


    def update_system_thread(self):
        if platform.system().lower() == "linux":
            self.progress_bar.start()
            try:
                # Der Befehl, den du ausführen möchtest
                befehl_liste = ["sudo apt-get update", "sudo apt-get upgrade"]
                
                # Verwende subprocess, um den Befehl auszuführen
                for befehl in befehl_liste:
                    result = subprocess.run(befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print("Rückgabewert:", result.returncode)
                    print("Ausgabe:", result.stdout)
                    print("Fehlermeldungen:", result.stderr)
            except subprocess.CalledProcessError as e:
                print("Fehler aufgetreten:", e)
            finally:
                # Stoppe die Statusleiste nach Abschluss des Updates oder im Fehlerfall
                self.progress_bar.stop()

    def update_system(self):
        update_thread = threading.Thread(target=self.update_system_thread)
        self.progress_bar.pack() 
        update_thread.start()
    
    def open_settings(self):
        settings_window = customtkinter.CTkToplevel(self)
        settings_window.title("Einstellungen")
        settings_window.geometry("400x300")
        
        # Beispiel: Button im Einstellungsfenster
        example_button = customtkinter.CTkButton(settings_window, text="System updaten", command=self.update_system)
        example_button.pack(pady=10, padx=0)
        
        self.progress_bar = ttk.Progressbar(settings_window)
        self.progress_bar.pack(pady=10)
    
    def create_frame(self, app_name, app_befehl, image, app_description, install):
        App.frames[app_name] = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        App.frames[app_name].configure(corner_radius=8)
        App.frames[app_name].configure(fg_color="white")
        App.frames[app_name].configure(border_width=2)
        App.frames[app_name].configure(border_color="#323232")
        App.frames[app_name].padx = 8
        
        bt_titel = customtkinter.CTkLabel(App.frames[app_name], text=app_name, font=customtkinter.CTkFont(size=30, weight="bold"), text_color="black")
        bt_titel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        bt_install = customtkinter.CTkButton(App.frames[app_name], text="Installieren", command=partial(self.install_app, app_name, app_befehl, install))
        if self.is_app_installed(app_name):
            bt_install.place_forget()  # Versteckt den Installationsbutton
        else:
            bt_install.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
        
        app_description_text = customtkinter.CTkLabel(App.frames[app_name], 
                                              text=app_description, 
                                              font=customtkinter.CTkFont(size=12), 
                                              text_color="black",
                                              wraplength=200)  # Passen Sie wraplength an die Breite Ihres Fensters an
        app_description_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        # Laden Sie das Bild erst, wenn die Seite geöffnet wird
        App.frames[app_name].bind("<Visibility>", lambda event: self.load_image(event, app_name, image))
    
    def is_app_installed(self, app_name):
        """Überprüft, ob eine App bereits installiert ist."""
        try:
            with open("data/installed_programs.txt", "r") as file:
                installed_apps = file.read().splitlines()
            return app_name in installed_apps
        except FileNotFoundError:
            return False
    
    def save_installed_app(self, app_name):
        """Speichert den Namen der installierten App."""
        with open("data/installed_programs.txt", "a") as file:
            file.write(app_name + "\n")

    
    
    def load_image(self, event, app_name, image_url):
            try:
                response = requests.get(image_url)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
            
                # Festlegen der gewünschten Größe für das Bild
                target_size = (100, 100)  # Beispielgröße, anpassen nach Bedarf
                image = image.resize(target_size, Image.LANCZOS)
            
                # Konvertieren des Bildes für die Anzeige in tkinter
                tk_image = ImageTk.PhotoImage(image)
            
                # Anzeigen des Bildes in einem Label
                image_label = customtkinter.CTkLabel(App.frames[app_name], image=tk_image, text="")
                image_label.image = tk_image  # Behält eine Referenz, um das Bild vor dem Garbage Collection zu schützen
                image_label.place(relx=0.7, rely=0.3, anchor=tk.CENTER)
            except Exception as e:
                print(f"Error loading image for {app_name}: {e}")

    def install_app(self, app_name, befehl_liste, install):
        if install == "apt-get":
            try:
                # Verwende subprocess, um den Befehl auszuführen
                for befehl in befehl_liste:
                    result = subprocess.run(befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print("Rückgabewert:", result.returncode)
                    print("Ausgabe:", result.stdout)
                    print("Fehlermeldungen:", result.stderr)
                self.save_installed_app(app_name)    
            except subprocess.CalledProcessError as e:
                print("Fehler aufgetreten:", e)
        
        elif install == "create_webapp":
            try:
                desktop_file_contents = f"""[Desktop Entry]
                Version=1.0
                Name={app_name}
                Comment="Webapp, created with YStore"
                Exec=chromium --app='{befehl_liste}'
                Terminal=false
                Type=Application
                Icon=""
                """
                
                desktop_file_path = f'{app_name}.desktop'
                
                with open(desktop_file_path, 'w') as desktop_file:
                    desktop_file.write(desktop_file_contents)
                
                print(f'Die .desktop-Datei wurde erfolgreich erstellt: {desktop_file_path}')
            except:
                print("Fehler aufgetreten: Webapp konnte nicht erstellt werden")
        else:
            print("Installer existiert nicht")
                
            
        messagebox.showinfo("Installation", f"{befehl_liste} wird installiert:\n{app_name}")

    def create_nav(self, parent, app_name, app_befehl, Beschreibung, image, install):
        bt_frame = customtkinter.CTkButton(parent)
        bt_frame.configure(height=40)
        bt_frame.configure(text=app_name)
        bt_frame.configure(command=partial(self.toggle_frame, app_name))
        bt_frame.grid(pady=3, row=len(self.nav_buttons), column=0)  # Verwende len(self.nav_buttons) als Zeilennummer
        self.create_frame(app_name, app_befehl, image, Beschreibung, install)
    
        # Füge die Referenz zur Nav Button-Liste hinzu
        self.nav_buttons.append(bt_frame)


    def toggle_frame(self, app_name):
        if App.frames[app_name] is not None:
            if App.current is App.frames[app_name]:
                App.current.pack_forget()
                App.current = None
            elif App.current is not None:
                App.current.pack_forget()
                App.current = App.frames[app_name]
                App.current.pack(in_=self.right_side_panel, side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
            else:
                App.current = App.frames[app_name]
                App.current.pack(in_=self.right_side_panel, side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)

    def filter_apps(self, event):
        search_term = self.search_var.get().lower()
        for app_name, frame in App.frames.items():
            if search_term == "":
                frame.pack_forget()
            elif search_term in app_name.lower():
                frame.pack(in_=self.right_side_panel, side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
            else:
                frame.pack_forget()

if __name__ == "__main__":
    a = App()
    a.mainloop()
