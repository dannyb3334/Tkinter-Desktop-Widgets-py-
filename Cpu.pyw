import tkinter as tk
from tkinter import Menu
import psutil
import json
import sys
import os

class App(tk.Tk):   
    #Write Data to json Function
    def write_var(self, name, value):
        with open("Resources/Settings.json", "w") as f:
            position["Cpu"][name] = value
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
    def display_usage(self, cpu_usage):
        #Declare vars
        cpu_percent = (cpu_usage / 100.0)
        cpu_percent_space = ""
        #Create space on single digit values to avoid changing text length
        if cpu_percent < 0.1:
            cpu_percent_space = " "
        #Update widget
        c = self.label.cget('text')
        c = f"CPU\n{cpu_percent_space}{cpu_usage:.2f}%" 
        self.label.config(text=c)
        #Repeat after 2.000 sec
        self.after(2000, self.display_usage, psutil.cpu_percent())
        
    def create_widget(self, text_color, bg_color):
        #Add background image (fix)
        image1 = tk.PhotoImage(file = "Resources/bg.png")
        #Widget Container (Not Mandatory)
        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)
        #Widget Contents
        self.label = tk.Label(self.frame, text="", font="Consolas " + str(round(8 * size)), justify="center", bg=bg_color, fg=text_color)
        self.label.pack(side="top", fill="both", expand=True)
        self.display_usage(psutil.cpu_percent())
        self.main_menu = Menu(self.frame, tearoff = 0)
        self.sub_menu = Menu(self.main_menu, tearoff=0)
        #Sub-Menu
        self.sub_menu.add_command(label='Large', command=lambda: self.re_size("size", 1.6))
        self.sub_menu.add_command(label='Medium', command=lambda: self.re_size("size", 1.3))
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
            x = position["Cpu"]["x"]
            y = position["Cpu"]["y"]
            size = position["Cpu"]["size"]
            text_color = position["Global"]["text_color"]
            bg_color = position["Global"]["bg_color"]
            opacity = position["Global"]["opacity"]
            topmost = position["Cpu"]["topmost"]
        #Widget General Settings
        self.overrideredirect(True)
        self.wm_attributes('-toolwindow', False) #True only if overriderdirect(False)
        self.wm_attributes('-alpha',opacity)
        self.wm_attributes('-topmost', topmost)
        w = 40 * size #Desired widget width
        h = 40 * size #Desired widget height
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #Build widget contents
        self.create_widget(text_color, bg_color)
        
app = App()
app.mainloop()