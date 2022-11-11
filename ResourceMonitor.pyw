import tkinter as tk
import psutil

class App(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(1)
        #Move Event
        def move(event):
            x, y = self.winfo_pointerxy()
            self.geometry(f"+{x}+{y}")
        #Close Event  
        def close(event):
            self.quit()
        
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenwidth() # height of the screen
        w = 280 #Desired widget width
        h = 110 #Desired widget height
        x = (1536-w)  
        y = (hs-hs) #Account for taskbar size
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.label = tk.Label(self, text="", font="Consolas 10", width=41, anchor="e")
        self.label.pack(side="top",fill="both",expand=True)
        self.bind('<B1-Motion>', move)
        self.bind('<Button-3>', close)
        self.display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent, 30)
        
    def display_usage(self, cpu_usage, ram_usage, bars=50):
        cpu_percent = (cpu_usage / 100.0)
        cpu_percent_space = ""
        if cpu_percent < 0.1:
            cpu_percent_space = " "
        cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
        ram_percent = (ram_usage / 100.0)
        ram_percent_space = ""
        if ram_percent < 0.1:
            ram_percent_space = " "
        ram_bar = ('█' * int(ram_percent * bars)) + '-' * (bars - int(ram_percent * bars))
        c = self.label.cget('text')
        c = f"CPU Usage\n {cpu_percent_space}{cpu_usage:.2f}% |{cpu_bar}|\n\nRAM Usage\n {ram_percent_space}{ram_usage:.2f}% |{ram_bar}|" 
        self.label.config(text=c)
        self.after(3000, self.display_usage, psutil.cpu_percent(), psutil.virtual_memory().percent, 30)
        
app = App()
app.mainloop()