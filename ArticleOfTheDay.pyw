import tkinter as tk
from tkinter import Button
from tkinter import Menu
from PIL import ImageTk, Image
from Resources import WikiScrapper
import webbrowser
import json
import sys
import os

class App(tk.Tk):
    #Write Data to json Function
    def write_var(self, name, value):
        with open("Resources/Settings.json", "w") as f:
            position["ArticleOfTheDay"][name] = value
            json.dump(position, f, indent=4)
            
    #Move Event
    def move(self, event):
        x, y = self.winfo_pointerxy()
        self.geometry(f"+{x}+{y}")
        
    #Record Position Event
    def record(self, event):
        x, y = self.winfo_pointerxy()
        self.write_var("x", x)
        self.write_var("y", y)
        
    #Change size
    def re_size(self, name, value):
        self.write_var(name, value)
        self.destroy()
        App().mainloop()
        
    #Popup Menu
    def do_popup(self, event):
        try:
            self.main_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.main_menu.grab_release()
    #Open Browser
    def callback(self, url):
            webbrowser.open_new_tab(url)
        
    def create_widget(self, text_color, bg_color):
        #Open Saved Image, Add to Window
        image_raw = Image.open("Resources/ArticleImage.jpg")
        im_width = round(image_raw.width * size)
        im_height = round(image_raw.height * size)
        pad_default = 15 * size
        #Widget Contents
        self.configure(bg=bg_color)
        self.img = ImageTk.PhotoImage((image_raw).resize((im_width, im_height)))
        self.image = tk.Label(self, image = self.img, bg=bg_color)
        self.image.grid(row=1, column=1, padx=pad_default, pady=15*size)
            #Read Record Of Article, Add to Window
        with open("Resources/ArticleText.json", "r") as jsonFile:
            article_saved = json.load(jsonFile)
        self.text = tk.Label(self, text=article_saved, font="helvetica " + str(round(9 * size)), wraplength=595 * size, justify="left", bg=bg_color, fg=text_color)
        self.text.grid(row=1, column=2, padx=(0, pad_default), pady= pad_default)
        self.text.bind("<Button-1>", lambda e: self.callback("https://en.wikipedia.org/wiki/Main_Page"))
        self.main_menu = Menu(self, tearoff = 0)
        self.sub_menu = Menu(self.main_menu, tearoff=0)
        #Sub-Menu
        self.sub_menu.add_command(label='Large', command=lambda: self.re_size("size", 1.2))
        self.sub_menu.add_command(label='Medium', command=lambda: self.re_size("size", 1.1))
        self.sub_menu.add_command(label='Small', command=lambda: self.re_size("size", 1.0))
        #Main-Menu
        self.main_menu.add_cascade(label="Size", menu=self.sub_menu)
        self.main_menu.add_cascade(label="Settings",command=lambda: os.system('Settings.pyw'))
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Refresh", command=lambda: [self.destroy(),App().mainloop()])
        self.main_menu.add_command(label="Quit", command=self.destroy)
        #KeyBinds
        self.bind('<B1-Motion>', self.move)
        self.bind('<ButtonRelease-1>', self.record)
        self.bind('<Button-3>', self.do_popup)
        
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global size
        global position
        #Get variables from json file
        with open("Resources/Settings.json", "r") as f:
            position = json.load(f)
            x = position["ArticleOfTheDay"]["x"]
            y = position["ArticleOfTheDay"]["y"]
            size = position["ArticleOfTheDay"]["size"]
            text_color = position["Global"]["text_color"]
            bg_color = position["Global"]["bg_color"]
            opacity = position["Global"]["opacity"]
            topmost = position["ArticleOfTheDay"]["topmost"]
        #Widget General Settings
        self.overrideredirect(True)
        self.wm_attributes('-toolwindow', False) #True only if overriderdirect(False)
        self.wm_attributes('-alpha',opacity)
        self.wm_attributes('-topmost', topmost)
        w = 785 * size #Desired widget height
        h = 185 * size #Desired widget width
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #Build widget contents
        self.create_widget(text_color, bg_color)
        
app = App()
app.mainloop()
