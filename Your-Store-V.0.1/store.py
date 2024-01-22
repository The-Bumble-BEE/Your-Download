import tkinter as tk
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
    with open('data/store.json', 'r') as file:
        app_info = json.load(file)
    

    frames = {}
    current = None

    def __init__(self):
        super().__init__()
        self.title("Download Store")
        self.geometry("800x600")
        # root!
        main_container = customtkinter.CTkFrame(self, corner_radius=8, fg_color=self.cget("fg_color"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Einstellungsbutton
        settings_button = customtkinter.CTkButton(main_container, text="Einstellungen", command=self.open_settings)
        settings_button.place(relx=0.034, rely=0.01)  # Angenommene relative Position
        
        # Search bar
        self.search_var = tk.StringVar()
        search_entry = customtkinter.CTkEntry(main_container, textvariable=self.search_var, placeholder_text="Programm Suche", placeholder_text_color="white")
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

        for app in App.app_info:
            self.create_nav(self.left_side_panel, app["name"], app["Befehl"], app["Beschreibung"], app["Image"])
    
    def update_system_thread(self):
        if platform.system().lower() == "linux":
            self.progress_bar.start()
            try:
                result = subprocess.run(['sudo', 'apt-get', 'update'], check=True, text=True, capture_output=True)
                print("Ausgabe:\n", result.stdout)
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
    
    def create_frame(self, app_name, app_befehl, image, app_description):
        App.frames[app_name] = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        App.frames[app_name].configure(corner_radius=8)
        App.frames[app_name].configure(fg_color="white")
        App.frames[app_name].configure(border_width=2)
        App.frames[app_name].configure(border_color="#323232")
        App.frames[app_name].padx = 8
        
        bt_titel = customtkinter.CTkLabel(App.frames[app_name], text=app_name, font=customtkinter.CTkFont(size=30, weight="bold"), text_color="black")
        bt_titel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        bt_install = customtkinter.CTkButton(App.frames[app_name], text="Installieren", command=partial(self.install_app, app_name, app_befehl))
        bt_install.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
        
        app_description_text = customtkinter.CTkLabel(App.frames[app_name], 
                                              text=app_description, 
                                              font=customtkinter.CTkFont(size=12), 
                                              text_color="black",
                                              wraplength=200)  # Passen Sie wraplength an die Breite Ihres Fensters an
        app_description_text.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        # Laden Sie das Bild erst, wenn die Seite geöffnet wird
        App.frames[app_name].bind("<Visibility>", lambda event: self.load_image(event, app_name, image))
    
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

    def install_app(self, app_name, app_befehl):
        if platform.system().lower() == "linux":
            try:
                result = subprocess.run(app_befehl, check=True, text=True, capture_output=True)
                print("Ausgabe:\n", result.stdout)
            except subprocess.CalledProcessError as e:
                print("Fehler aufgetreten:", e)

        messagebox.showinfo("Installation", f"{app_name} wird installiert:\n{app_befehl}")

    def create_nav(self, parent, app_name, app_befehl, Beschreibung, image):
        bt_frame = customtkinter.CTkButton(parent)
        bt_frame.configure(height=40)
        
        bt_frame.configure(text=app_name)
        bt_frame.configure(command=partial(self.toggle_frame, app_name))
        bt_frame.grid(pady=3, row=len(App.frames), column=0)
        self.create_frame(app_name, app_befehl, image, Beschreibung)

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
            if search_term in app_name.lower():
                frame.pack(in_=self.right_side_panel, side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
            else:
                frame.pack_forget()

if __name__ == "__main__":
    a = App()
    a.mainloop()
