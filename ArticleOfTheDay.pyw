import tkinter as tk
from tkinter import Button
from PIL import ImageTk, Image
from Resources import WikiScrapper
import json

class App(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Create Window Base
        #self.update_idletasks(1)
        self.overrideredirect(1)
        
        #End Application When Referenced
        def close(event):
            self.quit()
        def move(event):
            x, y = self.winfo_pointerxy()
            self.geometry(f"+{x}+{y}")
        
        
        #Place Window
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        w = 785 #Desired widget height
        h = 195 #Desired widget width
        x = (ws-w)  
        y = (hs-h-48) #Account for taskbar size
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #Go to website
        import webbrowser
        def callback(url):
            webbrowser.open_new_tab(url)
        #Create A Frame
        
        #Open Saved Image, Add to Window
        self.img = ImageTk.PhotoImage(Image.open("Resources/ArticleImage.jpg"))
        self.image = tk.Label(self, image = self.img, justify="right").grid(row=1, column=1, padx=(15, 15), pady=2.5)
        #Read Record Of Article, Add to Window
        with open("Resources/ArticleText.json", "r") as jsonFile:
            article_saved = json.load(jsonFile)
        self.text = tk.Label(self, text=article_saved, font="helvetica 10", wraplength=600, justify="left")
        self.text.grid(row=1, column=2, padx=(10, 0), pady= (15, 15))
        
        
        '''Add hyperlink grab for specific article'''
        
        self.text.bind("<Button-1>", lambda e: callback("https://en.wikipedia.org/wiki/Main_Page"))
        self.bind('<B1-Motion>',move)
        self.bind('<Button-3>', close)
app = App()
app.mainloop()