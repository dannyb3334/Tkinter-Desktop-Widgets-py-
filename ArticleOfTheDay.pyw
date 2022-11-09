from tkinter import *
from tkinter import Button
from PIL import ImageTk, Image
import Resources.WikiScrapper
import json

#Create Window Base
win = Tk()
win.update_idletasks()
win.overrideredirect(1)
#Place Window
ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen
w = 825 #Desired widget height
h = 200 #Desired widget width
x = (ws-w)  
y = (hs-h-48) #Account for taskbar size
win.geometry('%dx%d+%d+%d' % (w, h, x, y))
#End Application When Referenced
def close():
   win.quit()
#Create A Close Button "x"  
close_win = Button(win, text= " x ", font=("helvetica 9 bold"), command=close, borderwidth=0).pack(anchor = "ne", side = "right")

#Go to website
import webbrowser
def callback(url):
    webbrowser.open_new_tab(url)
#Create A Frame
frame = Frame(win)
#Open Saved Image, Add to Window
img = ImageTk.PhotoImage(Image.open("Resources/ArticleImage.jpg"))
image = Label(frame, image = img, justify="right").grid(row=1, column=1, padx=(15, 15), pady=2.5)
#Read Record Of Article, Add to Window
with open("Resources/ArticleText.json", "r") as jsonFile:
    article_saved = json.load(jsonFile)
text = Label(frame, text=article_saved, font="helvetica 10", wraplength=600, justify="left")
text.grid(row=1, column=2, padx=(10, 0), pady= (15, 15))
text.bind("<Button-1>", lambda e: callback("https://en.wikipedia.org/wiki/Main_Page"))
frame.pack()

win.mainloop()