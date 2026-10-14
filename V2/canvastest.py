import tkinter as tk
from tkinter import ttk
import platform


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )

    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")




"""root = tk.Tk()
root.geometry("1500x900")
panel = tk.PanedWindow(root, orient=tk.HORIZONTAL)
x = ScrollFrame(panel)
x.configure(width=300)
for I in range(0, 10):
    tk.Label(x.viewPort, text=str(I)).pack()
x.pack(side=tk.LEFT, fill="both", expand=True)
panel.add(x)

y = ScrollFrame(root)
y.configure(width=600)
for I in range(0, 10):
    tk.Label(y.viewPort, text=str(I)).pack()
y.pack(side=tk.RIGHT, fill="both", expand=True)
panel.add(y)

panel.pack(fill="both", expand=True)
root.mainloop()"""


"""
import tkinter as tk

root = tk.Tk()
# Use wrap=tk.WORD to automatically go to the next line at space boundaries
text_widget = tk.Text(root, wrap=tk.WORD, width=30, height=5)
text_widget.pack(padx=10, pady=10)

# Inserting text that is longer than 30 characters
text_widget.insert(tk.END, "This text will automatically jump to a new line once it reaches the width boundary.")

root.mainloop()
"""
"""
import tkinter as tk

root = tk.Tk()
root.geometry("300x100")

# Create the Entry box
my_box = tk.Entry(root)
my_box.pack(pady=20)

# Automatically place the cursor in the box
my_box.focus_set()

root.mainloop()
"""
import tkinter as tk
"""
def open_new_window():
    # 1. Create the separate Toplevel window
    new_window = tk.Toplevel(root)
    new_window.title("Secondary Window")
    new_window.geometry("300x200")
    
    # 2. Add widgets to the new window (pass new_window as the parent)
    label = tk.Label(new_window, text="This is a separate window!", font=("Arial", 12))
    label.pack(pady=20)
    
    close_btn = tk.Button(new_window, text="Close Window", command=new_window.destroy)
    close_btn.pack()

# Create the main application window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")

# Button to trigger the separate window
open_btn = tk.Button(root, text="Open Separate Window", command=open_new_window)
open_btn.pack(pady=50)

root.mainloop()
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Clam Style Example")
root.geometry("300x200")

# Initialize and apply the clam theme
style = ttk.Style()
style.theme_use('clam')

# Example of customizing a button's colors in the clam theme
style.configure('TButton', background='blue',  foreground='white', font=('Helvetica', 12))
style.map('TButton', background=[('active', 'darkblue')])

btn = ttk.Button(root, text="Click Me")
btn.pack(pady=50)

root.mainloop()