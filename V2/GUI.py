import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import logicCode
import time
import datetime
import customisingConfig
from tkinter import colorchooser

#carry on adding to THEME
#upgrade Item objects
#add  subitems

#connected now to logic
#can swap lists
#soooooo now
#1. R done, now C, create lists and items
#2. create subwindow classes to offer edits to the lists and items -done
#3. add subitems as a tab - done



#TO DOOOOOOOO
#1. add note to bottom of subitems
#2. start adding items, lists and subitems
#3. make windows for editing
#https://stackoverflow.com/questions/31599824/tkinter-label-how-do-i-know-that-the-text-is-too-long-for-it
#MY SAVIOUR!!!!!

#https://www.tutorialkart.com/python/tkinter/how-to-set-auto-scroll-for-text-widget-in-tkinter-python/
#for entry validation


#HARD LIMIT 48 FOR LIST NAMES

#split addNewObject into addNewObjectInit and addNewObjectApply
#then should all be fairly connected together
#work on getting to db, changing it
#CRUD SORTED!!!!
#YAY!!!
#need to adds themes
"""THEME = {
    "defaultObjectBG": "red",
    "defaultObjectFG": "white",
    "completedObjectBG": "green",
    "completedObjectFG" : "white",
    "defaultObjectFGAdditional": "grey",
    "hoveringObjectBG" : "orange",
    "hoveringObjectFG" : "purple",
    "selectedListBG" : "black",
    "selectedListFG" : "white",

    "defaultFont" : "Garamond",
    "mainWindowBG" : "#c66464",
    "sideTabBG" : "#d9d9d9",
    "optionBarBG": "#d9d9d9",
    "defaultObjectBG" : "yellow"
}"""

global THEME
THEME = {}

CONFIG = {}


class windowFrame:
     def __init__(self, parent):
            self._parent = parent
            self._window = tk.Toplevel(parent)
            self._window.geometry("200x200")
            self._window.attributes('-topmost', 'true')
            self._frame = ttk.Frame(self._window, style="popupFrame.TFrame")
            self._frame.pack(fill="both", expand=True)

            self._window.bind("<Return>", self.returnValues)


     def returnValues(self, event):
           pass

           
     def closeWindow(self):
           self._window.destroy()


class optionsPopup(windowFrame):
     def __init__(self, parent):
          super().__init__(parent)
          self._window.geometry("700x600")
          self._window.resizable(False, False)

          ttk.Label(self._frame, text="AutoComplete Items?", style="popupLabel.TLabel").pack()
          self._autoVar = tk.IntVar()
          self._auto = ttk.Checkbutton(self._frame, onvalue=1, offvalue=0, variable=self._autoVar, style="Default.TCheckbutton")
          self._autoVar.set(CONFIG["autocompleteObjects"])
          self._auto.pack()

          self._current = {
               "defaultObjectBG":THEME["defaultObjectBG"],
               "defaultObjectFG": THEME["defaultObjectFG"],
               "completedObjectBG":THEME["completedObjectBG"],
               "completedObjectFG" : THEME["completedObjectFG"],
               "defaultObjectFGAdditional": THEME["defaultObjectBG"],
               "hoveringObjectBG" : THEME["hoveringObjectBG"],
               "hoveringObjectFG" : THEME["hoveringObjectFG"],
               "selectedListBG" : THEME["selectedListBG"],
               "selectedListFG" : THEME["selectedListFG"],

               "defaultFont" :THEME["defaultFont"],
               "mainWindowBG" :THEME["mainWindowBG"],
               "sideTabBG" :THEME["sideTabBG"],
               "optionBarBG":THEME["optionBarBG"]
               }

          self._themeVar = tk.StringVar()
          themeOptions = tuple(DEFAULTSCONTROLLER.getDefaultThemeNames())
          themeOptions += ("Custom",)
          self._sortChoice = ttk.Combobox(self._frame, textvariable=self._themeVar, values=themeOptions, style="sortingChoice.TCombobox")
          self._sortChoice.current(themeOptions.index(DEFAULTSCONTROLLER.getTypeOfTheme()))
          self._sortChoice.bind("<<ComboboxSelected>>", self.checkCustom)
          self._sortChoice.pack()
         

          self._customFrame = ttk.Frame(self._frame,style="popupFrame.TFrame")
                              
         

          defaultColour = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
         
          BGFrame = ttk.Frame(defaultColour, style="popupFrame.TFrame")
          self.DBG = ttk.Label(BGFrame, text="Default Background: " + str(self._current["defaultObjectBG"]), style="popupLabel.TLabel")
          self.DBG.pack(side=tk.LEFT)
          ttk.Button(BGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("defaultObjectBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          BGFrame.pack(side=tk.TOP, expand=True, fill="x")

          FGFrame = ttk.Frame(defaultColour,style="popupFrame.TFrame")
          self.DFG = ttk.Label(FGFrame, text="Default foreground: " +  str(self._current["defaultObjectFG"]), style="popupLabel.TLabel")
          self.DFG.pack(side=tk.LEFT)
          ttk.Button(FGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("defaultObjectFG", colorchooser.askcolor(title="default foreground"))).pack(side=tk.RIGHT)
          FGFrame.pack(side=tk.TOP, expand=True, fill="x")
          defaultColour.pack(expand=True, fill="x")

          
          defaultComplete = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
         
          BGFrame = ttk.Frame(defaultComplete,style="popupFrame.TFrame")
          self.CBG = ttk.Label(BGFrame, text="Default Completed Background: " + str(self._current["completedObjectBG"]), style="popupLabel.TLabel")
          self.CBG.pack(side=tk.LEFT)
          ttk.Button(BGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("completedObjectBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          BGFrame.pack(side=tk.TOP, expand=True, fill="x")
          
          FGFrame = ttk.Frame(defaultComplete,style="popupFrame.TFrame")
          self.CFG = ttk.Label(FGFrame, text="Default completed foreground: " +  str(self._current["completedObjectFG"]), style="popupLabel.TLabel")
          self.CFG.pack(side=tk.LEFT)
          ttk.Button(FGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("completedObjectFG", colorchooser.askcolor(title="default foreground"))).pack(side=tk.RIGHT)
          FGFrame.pack(side=tk.TOP, expand=True, fill="x")
          defaultComplete.pack(expand=True, fill="x")

          defaultHover = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
                   
          BGFrame = ttk.Frame(defaultHover,style="popupFrame.TFrame")
          self.HBG = ttk.Label(BGFrame, text="Default hovering Background: " + str(self._current["hoveringObjectBG"]), style="popupLabel.TLabel")
          self.HBG.pack(side=tk.LEFT)
          ttk.Button(BGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("hoveringObjectBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          BGFrame.pack(side=tk.TOP, expand=True, fill="x")

          FGFrame = ttk.Frame(defaultHover,style="popupFrame.TFrame")
          self.HFG = ttk.Label(FGFrame, text="Default hovering foreground: " +  str(self._current["hoveringObjectFG"]), style="popupLabel.TLabel")
          self.HFG.pack(side=tk.LEFT)
          ttk.Button(FGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("hoveringObjectFG", colorchooser.askcolor(title="default foreground"))).pack(side=tk.RIGHT)
          FGFrame.pack(side=tk.TOP, expand=True, fill="x")
          defaultHover.pack(expand=True, fill="x")


          defaultList = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
                             
          BGFrame = ttk.Frame(defaultList,style="popupFrame.TFrame")
          self.LBG = ttk.Label(BGFrame, text="Default selected list background: " + str(self._current["selectedListBG"]), style="popupLabel.TLabel")
          self.LBG.pack(side=tk.LEFT)
          ttk.Button(BGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("selectedListBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          BGFrame.pack(side=tk.TOP, expand=True, fill="x")

          FGFrame = ttk.Frame(defaultList,style="popupFrame.TFrame")
          self.LFG = ttk.Label(FGFrame, text="Default selected list foreground: " +  str(self._current["selectedListFG"]), style="popupLabel.TLabel")
          self.LFG.pack(side=tk.LEFT)
          ttk.Button(FGFrame, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("selectedListFG", colorchooser.askcolor(title="default foreground"))).pack(side=tk.RIGHT)
          FGFrame.pack(side=tk.TOP, expand=True, fill="x")
          defaultList.pack(expand=True, fill="x")

          defaultFont = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
                                       
          FontFrame = ttk.Frame(defaultFont,style="popupFrame.TFrame")
          ttk.Label(FontFrame, text="Default font: ", style="popupLabel.TLabel").pack(side=tk.LEFT)
          self._fontVar = tk.StringVar()
          self._fontName = ttk.Entry(FontFrame, textvariable=self._fontVar,style="popupEntry.TEntry")
          self._fontName.pack(side=tk.RIGHT)
          self._fontName.insert(tk.END,str(self._current["defaultFont"]))
          FontFrame.pack(side=tk.TOP, expand=True, fill="x")
          defaultFont.pack(expand=True, fill="x")
          

          defaultMain = ttk.Frame(self._customFrame,style="popupFrame.TFrame")
                             
          optionbarframe = ttk.Frame(defaultMain,style="popupFrame.TFrame")
          self.OBG = ttk.Label(optionbarframe, text="Default option bar: " + str(self._current["optionBarBG"]), style="popupLabel.TLabel")
          self.OBG.pack(side=tk.LEFT)
          ttk.Button(optionbarframe, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("optionBarBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          optionbarframe.pack(side=tk.TOP, expand=True, fill="x")

          sidebarframe = ttk.Frame(defaultMain,style="popupFrame.TFrame")
          self.SBG = ttk.Label(sidebarframe, text="Default side bar: " + str(self._current["sideTabBG"]), style="popupLabel.TLabel")
          self.SBG.pack(side=tk.LEFT)
          ttk.Button(sidebarframe, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("sideTabBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          sidebarframe.pack(side=tk.TOP, expand=True, fill="x")


          
          mainwindowframe = ttk.Frame(defaultMain,style="popupFrame.TFrame")
          self.MBG = ttk.Label(mainwindowframe, text="Default main window: " + str(self._current["mainWindowBG"]), style="popupLabel.TLabel")
          self.MBG.pack(side=tk.LEFT)
          ttk.Button(mainwindowframe, text="Set", style="Default.TButton", command=lambda : self.mapDefaultBG("mainWindowBG", colorchooser.askcolor(title="default background"))).pack(side=tk.RIGHT)
          mainwindowframe.pack(side=tk.TOP, expand=True, fill="x")
          defaultMain.pack(expand=True, fill="x")


          ttk.Label(self._customFrame, text="Theme name", style="incompleteItem.TLabel").pack()
          self._customThemeNameVar = tk.StringVar()
          self._customName = ttk.Entry(self._customFrame, style="popupEntry.TEntry", textvariable=self._customThemeNameVar)
          self._customName.pack()
          ttk.Button(self._customFrame, text="Save custom theme?", style="Default.TButton", command=self.saveCustomTheme).pack()
          

          ttk.Button(self._frame, text="OK", command=self.submitUpdates, style="Default.TButton").pack()
          if self._themeVar.get() == "Custom":
                self._customFrame.pack()

       
     

     def updateLabel(self):
          self.DBG.config( text="Default Background: " + str(self._current["defaultObjectBG"]))
          self.DFG.config(text="Default foreground: " +  str(self._current["defaultObjectFG"]))
          self.CBG.config( text="Default Completed Background: " + str(self._current["completedObjectBG"]))
          self.CFG.config( text="Default Completed Foreground: " + str(self._current["completedObjectFG"]))
          self.HBG.config(text="Default hovering Background: " + str(self._current["hoveringObjectBG"]))
          self.HFG.config(text="Default hovering Foreground: " + str(self._current["hoveringObjectFG"]))
          self.LBG.config( text="Default selected list background: " + str(self._current["selectedListBG"]))
          self.LFG.config( text="Default selected list Foreground: " + str(self._current["selectedListFG"]))
          self.OBG.config(text="Default option bar: " + str(self._current["optionBarBG"]))
          self.SBG.config(text="Default side bar: " + str(self._current["sideTabBG"]))
          self.MBG.config(text="Default main window: " + str(self._current["mainWindowBG"]))


     def saveCustomTheme(self):
          self._current["defaultFont"] = self._fontVar.get() 
          DEFAULTSCONTROLLER.saveCustomTheme(self._current, self._customThemeNameVar.get())
          self.closeWindow()

         
     def checkCustom(self, event):
          if self._themeVar.get() == "Custom":
                 self._customFrame.pack()
          else:
               self._customFrame.pack_forget()
                 



     def submitUpdates(self):
          CONFIG["autocompleteObjects"] = self._autoVar.get()
          DEFAULTSCONTROLLER.applyConfig(CONFIG)
          if self._themeVar.get() == "Custom":
               self._current["defaultFont"] = self._fontVar.get() 

          DEFAULTSCONTROLLER.applyTheme(self._themeVar.get(), self._current)
         
          self._parent.applyOptions()
          self.closeWindow()




     def mapDefaultBG(self,val, Inp):
          self._current[val] = Inp[1]
          print(self._current)
          self.updateLabel()



class deletePopup(windowFrame):
     def __init__(self, parent, Name):
            super().__init__(parent)
            ttk.Label(self._frame, text="Delete "+Name, style="popupLabel.TLabel").pack()
           
            self._optionframe = ttk.Frame(self._frame, style="popupFrame.TFrame")
            self._delete = ttk.Button(self._optionframe, text="delete", command=self.comfirmDelete, style="Default.TButton")
            self._cancel = ttk.Button(self._optionframe, text="cancel", command=self.cancelDelete, style="Default.TButton")

            self._delete.pack(side=tk.LEFT)
            self._cancel.pack(side=tk.RIGHT)
            self._optionframe.pack()

     def comfirmDelete(self):
          self._parent.onDeleteApply()

     def cancelDelete(self):
           self.closeWindow()


class ListPopup(windowFrame):
     def __init__(self, root):
          super().__init__(root)
          self._descriptionLabel = ttk.Label(self._frame, text="List name", style="incompleteItem.TLabel")
          self._descriptionLabel.pack(side=tk.TOP)
          self._nameVar = tk.StringVar()
          self._ListName = ttk.Entry(self._frame, textvariable=self._nameVar,style="popupEntry.TEntry")
     
         
          self._ListName.focus_set()

          self._ListName.pack(pady=10)

          ttk.Label(self._frame, text="Is Done?", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._doneVar = tk.IntVar()
         
          
          self._isDone = ttk.Checkbutton(self._frame, onvalue=1, offvalue=0, variable=self._doneVar, style="Default.TCheckbutton")
          self._isDone.pack()


          self._submit = ttk.Button(self._frame,text="Submit", command= lambda: self.returnValues(None), style="Default.TButton")
          self._submit.pack()
          
     def validateInput(self):
          if len(self._nameVar.get()) > 48:
                messagebox.showerror(title="Invalid name", message="New list name too long")
                self._ListName.focus_set()
                return False
          return True

     def returnValues(self, event):
          if self.validateInput():
               self._parent.addNewObjectApply([str(self._nameVar.get()), int(self._doneVar.get())])
           
class editListPopup(ListPopup):
     def __init__(self, root, currentValues):
            super().__init__(root)
            self._ListName.insert(tk.END,str(currentValues[0]))
            self._doneVar.set(currentValues[1])

     def returnValues(self, event):
               if self.validateInput():
                    self._parent.applyEdit([str(self._nameVar.get()), int(self._doneVar.get())])
                
class itemPopup(windowFrame): #has structure [self._description,  self._dueDate,self._timeCreated, self._isPrioirity, self._note]
     def __init__(self, parent ):
          super().__init__(parent)
          self._window.geometry("700x600")
          self._window.resizable(False, False)
          ttk.Label(self._frame, text="item name", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._nameVar = tk.StringVar()
          self._itemName = ttk.Entry(self._frame, textvariable=self._nameVar, width=350, style="popupEntry.TEntry")
          
          
          self._itemName.focus_set()
          self._itemName.pack()

          ttk.Label(self._frame, text="Is Done?", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._doneVar = tk.IntVar()
          self._doneVar.set(0)
          self._isDone = ttk.Checkbutton(self._frame, onvalue=1, offvalue=0, variable=self._doneVar, style="Default.TCheckbutton")
          self._isDone.pack()
          

          ttk.Label(self._frame, text="Due Date", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._timeControl = ttk.Frame(self._frame, style="popupFrame.TFrame")
          self._addDueDate = tk.IntVar()
          self._addDueDate.set(0)
          self._hasDueDate= ttk.Checkbutton(self._timeControl, command=self.displayDueDate, variable=self._addDueDate, onvalue=1, offvalue=0,style="Default.TCheckbutton")
          self._hasDueDate.pack()
          self._dueDateFrame = ttk.Frame(self._timeControl, style="popupFrame.TFrame")
          ttk.Label(self._dueDateFrame, text="Date", style="incompleteItem.TLabel").pack()
          self._days = tkcalendar.DateEntry(self._dueDateFrame, mindate = datetime.datetime.now(), day=datetime.datetime.now().day, month = datetime.datetime.now().month, year=datetime.datetime.now().year, date_patter="dd/mm/yyyy", style="calendar.DateEntry")
          self._days.pack(side=tk.TOP)
          self._addTime = tk.IntVar()
          self._addTime.set(0)
          ttk.Label(self._dueDateFrame, text="Time", style="incompleteItem.TLabel").pack()
          self._hasTimeOnDueDate = ttk.Checkbutton(self._dueDateFrame, variable=self._addTime, onvalue=1, offvalue=0, command=self.displayTime, style="Default.TCheckbutton" )
          self._hasTimeOnDueDate.pack()
          self._time = ttk.Frame(self._dueDateFrame, style="popupFrame.TFrame")
          
          self._days.bind("<<DateEntrySelected>>", self.updateCalendar)
          
          self._days.pack(side=tk.TOP)
          self._timeControl.pack()
          self._hour = ttk.Spinbox(self._time, from_=0, to=23, style="datetime.TSpinbox")
          self._minute = ttk.Spinbox(self._time, from_=0, to=59, style="datetime.TSpinbox")


          #want default to be nothing
          self._hour.insert(tk.END, datetime.datetime.now().hour)
          self._minute.insert(tk.END, datetime.datetime.now().minute)
          
          self._hour.pack(side=tk.LEFT)
          self._minute.pack(side=tk.RIGHT)
         



          ttk.Label(self._frame, text="High Priority?", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._priorityVar = tk.IntVar()

          self._highPriority = ttk.Checkbutton(self._frame, onvalue=1, offvalue=0, variable=self._priorityVar, style="Default.TCheckbutton")
          self._highPriority.pack()


          ttk.Label(self._frame, text="Note", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._note = tk.Text(self._frame, height=5, fg=THEME["defaultObjectFG"], bg=THEME["defaultObjectBG"],insertbackground=THEME["defaultObjectFG"], font=(THEME["defaultFont"], 10))
          self._note.pack()

          self._submit = ttk.Button(self._frame,text="Submit", command= lambda: self.returnValues(None), style="Default.TButton")
          self._submit.pack()
          
     def displayDueDate(self):
            if self._addDueDate.get() == 1:
               self._dueDateFrame.pack()
            else:
                  self._dueDateFrame.pack_forget()

     def displayTime(self):
          if self._addTime.get() ==1:
               self._time.pack()
          else:
               self._time.pack_forget()


     def updateCalendar(self, event):
          absDate = self.getCurrentInputtedDueDateSeconds()
          if absDate < time.time():
               self._hour.delete(first=0, last="end")
               self._minute.delete(first=0, last="end")

               self._hour.insert(tk.END, datetime.datetime.now().hour)
               self._minute.insert(tk.END, datetime.datetime.now().minute)

          if self._days.get_date().strftime("%d/%m/%Y") == datetime.datetime.now().strftime("%d/%m/%Y"):
                self._hour.configure(from_=datetime.datetime.now().hour)
                self._minute.configure(from_=datetime.datetime.now().minute)
          else:
                self._hour.configure(from_=0)
                self._minute.configure(from_=0)

     def validateInput(self):
               if len(self._nameVar.get()) > 70:
                       messagebox.showerror(title="Invalid name", message="New item name too long")
                       self._itemName.focus_set()
                       return False
               if self._addDueDate.get() == 1:
                    timeGiven = self.getCurrentInputtedDueDateSeconds()
                    if timeGiven < time.time():
                         messagebox.showerror(title="Invalid Due Date", message="Due Date already passed")
                         return False
               return True

     def getCurrentInputtedDueDateSeconds(self):
          if self._addDueDate.get() == 1:
               if self._addTime.get() == 1:
                    hour = int(self._hour.get())
                    minute = int(self._minute.get())
               else:
                    hour = 23
                    minute = 59
               newDueDate =  time.mktime((self._days.get_date().year, self._days.get_date().month, self._days.get_date().day,hour,minute+1,-1,-1,-1, -1))
                                    
                                          
          else:
               newDueDate = -1  

          return newDueDate    

     def returnValues(self, event):
              
               if self.validateInput():
                    newDueDate = self.getCurrentInputtedDueDateSeconds()
                    self._parent.addNewObjectApply([str(self._nameVar.get()),self._doneVar.get(), newDueDate, None, self._priorityVar.get(), self._note.get("1.0", "end-1c")])

class editItemPopup(itemPopup):
      def __init__(self, parent, currentValues):
            super().__init__(parent)
            self._itemName.insert(tk.END,str(currentValues[0]))
            self._doneVar.set(currentValues[1])
            self._priorityVar.set(currentValues[4])
            self._note.insert(tk.END, currentValues[5])

            if currentValues[2] != -1:
               self._addDueDate.set(1)
               self.displayDueDate()
               dueDateString = time.localtime(currentValues[2])
               self._hour.delete(first=0, last="end")
               self._minute.delete(first=0, last="end")
              

               if  (time.strftime("%H",dueDateString) == "23" and time.strftime("%M",dueDateString) == "59"):
                    self._hour.insert(tk.END, datetime.datetime.now().hour)
                    self._minute.insert(tk.END, datetime.datetime.now().minute)
                    self._addTime.set(0)
                    self.displayTime()
               else:
                  
                    self._hour.insert(tk.END, time.strftime("%H",dueDateString))
                    self._minute.insert(tk.END, time.strftime("%M",dueDateString))
                    self._addTime.set(1)
                    self.displayTime()
               dateOfDueDate = datetime.date(year=int(time.strftime("%Y",dueDateString)),month=int(time.strftime("%m",dueDateString)),day=int(time.strftime("%d",dueDateString)))
              
               self._days.set_date(dateOfDueDate)
            self.updateCalendar(None)

      def returnValues(self, event):
                    if self.validateInput() == True:
                         newDueDate = self.getCurrentInputtedDueDateSeconds()    
                         self._parent.applyEdit([str(self._nameVar.get()),self._doneVar.get(), newDueDate, self._priorityVar.get(), self._note.get("1.0", "end-1c")])

class subitemPopup(ListPopup):
     def __init__(self, parent):
          super().__init__(parent)
          self._descriptionLabel.configure(text="Subitem Name")

     def returnValues(self, event):
          if self.validateInput():
               self._parent.createSubitemApply([str(self._nameVar.get()), int(self._doneVar.get())])

class editSubPopup(subitemPopup):
     def __init__(self, parent, currentValues):
            super().__init__(parent)
            self._ListName.insert(tk.END,str(currentValues[0]))
            self._doneVar.set(currentValues[1])

     def returnValues(self, event):
          if self.validateInput():
               self._parent.applyEdit([str(self._nameVar.get()), int(self._doneVar.get())])

      
#general option
#omg for the love of god abstract
class Option(ttk.Frame):
     def __init__(self, root, Object, parent):
          super().__init__(root)
          self._parent = parent
          self._mainFrame = ttk.Frame(self, style="mainWindow.TFrame")
          self._object = Object
          self._defaults = []
          self._isComplete = tk.IntVar()
          self._isComplete.set(self._object.GetDetails()[1])

     
          self._operationFrame = tk.Frame(self._mainFrame)

          self._edit = ttk.Button(self._operationFrame, text="edit", command=self.onEdit, style="Default.TButton")
          self._delete = ttk.Button(self._operationFrame,text="delete", command=self.onDeleteInit, style="Default.TButton")
          self._complete = ttk.Checkbutton(self._mainFrame, takefocus=1, command=self.toggleComplete, variable=self._isComplete, offvalue=0, onvalue=1, style="Default.TCheckbutton")

         
          self._mainFrame.pack(expand=True, fill="both", side=tk.RIGHT)

          self._edit.pack(fill="y", side=tk.TOP, expand=True)
          self._delete.pack(fill="y", side=tk.BOTTOM,expand=True)
          self._operationFrame.pack(side=tk.RIGHT, fill="y")
          self._complete.pack(side=tk.RIGHT)
     

     def toggleComplete(self):
          pass

     def markComplete(self):
          pass

     def markIncomplete(self):
          pass

     def evaluateCompletion(self):
          if len(self._object.GetItems()) == 0:
               return
          Valid = True
          for I in self._object.GetItems():
                if I.GetDetails()[1] == 0:
                      Valid = False

          if Valid:
               self.markComplete()

     def onEdit(self):
          pass

     def applyEdit(self):
          pass

     def onDeleteInit(self):
          self._deletePopup = deletePopup(self, self._object.GetDetails()[0])

     def onDeleteApply(self):
          pass

#individual boxes
class ListOption(Option):
     def __init__(self, root, Object, parent):
          super().__init__(root, Object, parent)
          self.configure(style="sidebar.TFrame")
          self._mainFrame.configure(height=20)
          self._option = ttk.Button(self._mainFrame, text=self._object.GetDetails()[0], command=self.onClick)
          self._option.pack(side=tk.LEFT, fill="both", expand=True)

          
          if self._object.GetDetails()[1]:
               self._defaults = "completeList.TButton"
               self.markComplete()
          else:
               self._defaults = "incompleteList.TButton"
               self.markIncomplete()

     def GetObject(self):
           return self._object
        
     def onClick(self):
          self._parent.changeList(self._object.GetID())
          
 
     def onEdit(self):
           self._window = editListPopup(self, self._object.GetDetails())

     def applyEdit(self, new):
           newValues = new
           self._object.updateValues(newValues)
           self._option.configure(text=newValues[0])
           if newValues[1] == 1:
                 self.markComplete()
           else:
                 self.markIncomplete()
           self._window.closeWindow()
           CONTROLLER.updateList(self._object.GetID(), self._object.GetDetails())


     def onDeleteApply(self):
          self._parent.deleteList(self._object.GetID())
          self.destroy()

     def checkSelected(self):
          if self._object.GetSelected():
               self.markSelected()
          else:
               self.markUnselected()
     
     def markSelected(self):
          self._option.configure(style="selectedList.TButton")
          

     def markUnselected(self):
          self._option.configure(style=self._defaults)
               


     def markComplete(self):
          self._isComplete.set(1)
          self._defaults = "completeList.TButton"
          if not self._object.GetSelected():
               self._option.configure(style=self._defaults)
          

     def markIncomplete(self):
          self._isComplete.set(0)
          self._defaults = "incompleteList.TButton"
          if not self._object.GetSelected():
               self._option.configure(style=self._defaults)
          
     def toggleComplete(self):
         
          if self._object.GetDetails()[1] == 1:
               self._object.updateValues([self._object.GetDetails()[0], 0])
               self.markIncomplete()
          else:
               self._object.updateValues([self._object.GetDetails()[0], 1])
               self.markComplete()
          CONTROLLER.updateList(self._object.GetID(), [None, self._object.GetDetails()[1]])

class ItemOption(Option):

     def __init__(self, root, Object, parent):
          super().__init__(root, Object, parent)
          self._isExpanded = False
          self.configure(height=5,style="mainWindow.TFrame")
          self._mainFrame.configure(height=200)
          self._option = ttk.Label(self._mainFrame, text=str(self._object.GetDetails()[0]))
          
          self._dueDate = ttk.Label(self._mainFrame)
          self.configureTime()

          self._priorityMarker = ttk.Label(self._mainFrame, text="Priority" if self._object.GetDetails()[4] else "")
          self._numSub = ttk.Label(self._mainFrame, text=f"({len(self._object.GetItems())})" if len(self._object.GetItems()) > 0 else "")
         

          self._option.pack(side=tk.LEFT, padx=2)
          self._dueDate.pack(side=tk.LEFT)
          
          #self._complete.pack(side=tk.RIGHT)
          self._addSub = ttk.Button(self._operationFrame, text="Add", command=self.createSubitemInit, style="Default.TButton")
          self._addSub.pack(side=tk.BOTTOM, fill="y", expand=True)
         
          self._numSub.pack(side=tk.RIGHT)
          self._priorityMarker.pack(side=tk.RIGHT)
          self._mainFrame.pack(fill="both", expand=True, side=tk.TOP)
          self._mainFrame.bind("<Button-1>", self.onClick)
          self._option.bind("<Button-1>", self.onClick)

          self._defaults = []
        
          if self._object.GetDetails()[1] == 1:
               self.markComplete()
          else:
               self.markIncomplete()

          self._subitems = ttk.Frame(self, style="mainWindow.TFrame")
          self.bind("<Enter>", self.onEnter)
          self.bind("<Leave>", self.onExit)
          
          if CONFIG["autocompleteObjects"] == 1:
               self.evaluateCompletion()

     def onEnter(self, event):
              if self._object.GetDetails()[1] == 1:
                   self._option.configure(style="hoveringItemComplete.TLabel")
                   self._dueDate.configure(style="hoveringItemComplete.TLabel")

              else:
                    self._option.configure(style="hoveringItemIncomplete.TLabel")
                    self._dueDate.configure(style="hoveringItemIncomplete.TLabel")

     def onExit(self, event):
           self._option.configure(style=self._defaults[1])
           self._dueDate.configure(style=self._defaults[1])


     def configureTime(self):
          if self._object.GetDetails()[2] != -1:
               timeTuple = time.localtime(self._object.GetDetails()[2])
               if timeTuple.tm_hour == 23 and timeTuple.tm_min == 59:
                    parsedString = time.strftime("%d/%m/%Y", timeTuple)
               else:
                    parsedString = time.strftime("%d/%m/%Y %H:%M", timeTuple)
                   
                         
          else:
               parsedString = ""

          self._dueDate.configure(text=str(f"Due date: {parsedString}") if parsedString != "" else "")



     def onDeleteApply(self):

               CONTROLLER.deleteItem(self._object.GetID())
               self.destroy()

     def onEdit(self):
           self._window = editItemPopup(parent=self,currentValues=self._object.GetDetails())
#Input of Values[ Description,isDone dueDate,isPriority, note]
     def applyEdit(self, new):
              
               
               newValues = [new[0], new[1], new[2], self._object.GetDetails()[3], new[3], new[4]] 
               self._object.updateValues(newValues)
               self._option.configure(text=new[0])
               self.configureTime()

               if new[3] == 0:
                     self._priorityMarker.configure(text="")
               else:
                     self._priorityMarker.configure(text="Priority")

               self._window.closeWindow()
               CONTROLLER.updateItem(self._object.GetID(), self._object.GetDetails())

     def onClick(self, event):
               if self._isExpanded:
                    self.deleteSubitems()
                    self._isExpanded = False
               else:
                     self.addSubitems()
                     self._isExpanded = True
                    

     def markComplete(self):
          self._isComplete.set(1)
          self._defaults = ["completeItem.TFrame","completeItem.TLabel"]
          self._mainFrame.configure(style=self._defaults[0])
          self._option.configure(style=self._defaults[1])
          self._dueDate.configure(style=self._defaults[1])
          self._priorityMarker.configure(style=self._defaults[1])
          self._numSub.configure(style=self._defaults[1])
          
          

     def markIncomplete(self):
          self._isComplete.set(0)
          self._defaults = ["incompleteItem.TFrame","incompleteItem.TLabel"]
          self._mainFrame.configure(style=self._defaults[0])
          self._option.configure(style=self._defaults[1])
          self._dueDate.configure(style=self._defaults[1])
          self._priorityMarker.configure(style=self._defaults[1])
          self._numSub.configure(style=self._defaults[1])

          

     def toggleComplete(self):
          if self._object.GetDetails()[1] == 1:
               self._object.updateValues([self._object.GetDetails()[0], 0, self._object.GetDetails()[2],self._object.GetDetails()[3],self._object.GetDetails()[4],self._object.GetDetails()[5]])
               self.markIncomplete()
          else:
               self._object.updateValues([self._object.GetDetails()[0], 1, self._object.GetDetails()[2],self._object.GetDetails()[3],self._object.GetDetails()[4],self._object.GetDetails()[5]])
               self.markComplete()
          
          CONTROLLER.updateItem(self._object.GetID(), [None, self._object.GetDetails()[1],None,None,None,None])

     def addSubitems(self):
          for j in self._subitems.pack_slaves():
                j.destroy()

          self._object.addItem(logicCode.ToDoListItem("buffer", "",-1,0,0,-1))
          for i in self._object.GetItems():
               if i.GetDetails()[0] == "buffer":
                     continue
               x = SubitemOption(self._subitems, i, self)
               x.pack(fill="x", pady=2)
               

          self._object.popItem()
          self._noteFrame = ttk.Frame(self._subitems, style="Default.TFrame")
         
          ####
          ttk.Label(self._noteFrame, text="Note: ", style="incompleteItem.TLabel").pack(side=tk.TOP)
          self._note = tk.Text(self._noteFrame, wrap=tk.WORD, font=(THEME["defaultFont"], 15),bg=THEME["defaultObjectBG"], fg=THEME["defaultObjectFG"], height=5, borderwidth=1)#
          self._note.insert(tk.END, self._object.GetDetails()[5])
          self._note.configure(state="disabled")
          self._note.unbind("<MouseWheel>")
          self._note.pack(side=tk.BOTTOM)
          self._noteFrame.pack(fill="x", pady=5)
          self._subitems.pack(side=tk.BOTTOM, fill="both", expand=True, pady=5)

     def cancelTextScroll(self, event):
           return "break"
     
     def updateSubitem(self, SubID, NewValues):
           CONTROLLER.updateSubitem(SubID,self._object.GetID(),NewValues)

     def createSubitemInit(self):
          self._popup = subitemPopup(self)

     def updateSubitemNum(self):
           self._numSub.configure(text=f"({len(self._object.GetItems())})" if len(self._object.GetItems()) > 0 else "")

     def createSubitemApply(self, Values):
          subToAdd = CONTROLLER.addSubitem(Values, ItemID=self._object.GetID())
          SubitemOption(self._subitems, subToAdd, self).pack(fill="x", pady=2)
          self._popup.closeWindow()
          self.updateSubitemNum()

     def deleteSubitem(self, SubID):
          CONTROLLER.deleteSubitem(SubID=SubID, ItemID=self._object.GetID())
          self.updateSubitemNum()
          
    


          

     def deleteSubitems(self):
          self._subitems.pack_forget()
     

     #from here, needs logic to add and remove 

          #pass up index stored in self._values(0) hopefully and [None, self._values[1], None, None,None, None]

class SubitemOption(Option):
     def __init__(self, root, Object, parent):
          super().__init__(root, Object, parent)
          self.configure(height=5)
          self._buffer = tk.Label(self, text="", width=10, bg=THEME["mainWindowBG"])
          self._buffer.pack(side=tk.LEFT, fill="both")
          self._option = ttk.Label(self._mainFrame, text=self._object.GetDetails()[0])   
         

          self._option.pack(side=tk.LEFT, expand=True)

          self._defaults = []
          if self._object.GetDetails()[1]:
               self.markComplete()
          else:
               self.markIncomplete()
          self.bind("<Enter>", self.onEnter)
          self.bind("<Leave>", self.onExit)
                    


     def onEnter(self, event):
          if self._object.GetDetails()[1] == 1:
               self._option.configure(style="hoveringSubComplete.TLabel")
          else:
               self._option.configure(style="hoveringSubIncomplete.TLabel")
                
     
     def onExit(self, event):
          self._option.configure(style=self._defaults[1])

     def onDeleteApply(self):
               self._parent.deleteSubitem(self._object.GetID())
               self.destroy()

     def markComplete(self):
               self._isComplete.set(1)
               self._defaults = ["completeItem.TFrame", "completeItem.TLabel"]
               self._mainFrame.configure(style=self._defaults[0])
               self._option.configure(style=self._defaults[1])

               if CONFIG["autocompleteObjects"] == 1:
                     self._parent.evaluateCompletion()
                       
     def markIncomplete(self):
               self._isComplete.set(0)
               self._defaults = ["incompleteItem.TFrame", "incompleteItem.TLabel"]
               self._mainFrame.configure(style=self._defaults[0])
               self._option.configure(style=self._defaults[1])

     def toggleComplete(self):
               if self._object.GetDetails()[1] == 1:
                    self._object.updateValues([self._object.GetDetails()[0], 0])
                    
                    self.markIncomplete()
               else:
                    self._object.updateValues([self._object.GetDetails()[0], 1])
                    self.markComplete()
               self._parent.updateSubitem(self._object.GetID(), [None, self._object.GetDetails()[1]])
               

     def onEdit(self):
           self._window = editSubPopup(self, self._object.GetDetails()[0:2])

     def applyEdit(self, new):
          self._object.updateValues(new)
          self._option.configure(text=new[0])
          if new[1] == 1:
               self.markComplete()
          else:
               self.markIncomplete()
          self._window.closeWindow()
          self._parent.updateSubitem(self._object.GetID(), self._object.GetDetails())



               

#main big windows
class listWindow(ttk.Frame):
     def __init__(self, root, parent):
          super().__init__(root)
          self._parent: mainWindow = parent
          self._addBar = ttk.Frame(self,style="incompleteItem.TFrame")
          self._addButton = ttk.Button(self._addBar, text="Add", command=self.addNewObjectInit, style="Default.TButton")
          self._addButton.pack(side=tk.RIGHT, fill="y")
          self._addBar.pack(side=tk.TOP, fill="x")
          self._canvas = tk.Canvas(self, borderwidth=0)
          self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._canvas.yview, style="scrollBar.Vertical.TScrollbar")
          self._frame = ttk.Frame(self._canvas)
          self._canvas.configure(yscrollcommand=self._scrollbar.set)


          self._scrollbar.pack(side=tk.RIGHT, fill="y")
          self._canvas.pack(side=tk.LEFT, fill="both", expand=True)
          self._window = self._canvas.create_window((0,0), window=self._frame, tags="self._frame", anchor="nw")

          self.bind("<Configure>", self.changeBuffer)
          self._frame.bind("<Configure>", self.onFrameChange)
          self._canvas.bind("<Configure>", self.onCanvasChange)
          #self.bind("<Configure>", self.onResize)
          self._frame.bind("<Enter>", self.onEnter)
          self._frame.bind("<Leave>", self.onExit)

        
          self._objectFrame = ttk.Frame(self._frame)
          self._objectFrame.pack(expand=True, fill="both", side=tk.TOP)
          self._buffer = ttk.Frame(self._frame, height=1)
          self._buffer.pack(expand=True, fill="x", side=tk.BOTTOM)
          self.onFrameChange(None)
          self.changeBuffer(None)



     def applyTheme(self):
          pass    


     def onResize(self, event):
          #self._canvas.itemconfig(self._window, height = event.height)
          self._frame.configure(height=event.height)
         
        
          
     def changeBuffer(self,event):
          #would be really cool if i needed
          """total = 0
          for I in self._objectFrame.pack_slaves():
               total += I.winfo_height() + 6

          print("total",total)
          print("window", self.winfo_height())
          if self.winfo_height() < total:
          
          self._buffer.configure(height=self.winfo_height()-150)
          else:
               self._buffer.configure(height=20)
          """
          

          self._buffer.configure(height=self.winfo_height()-150)

     def resetBuffer(self):
          self._buffer.configure(height=1)

         


     def onCanvasChange(self, event):
          newWidth = event.width
          self._canvas.itemconfig(self._window, width = newWidth)
          
         
          

     def onFrameChange(self, event):
          self._canvas.configure(scrollregion=self._canvas.bbox("all"))
          self.changeBuffer(event)
          


     def resize(self, value):
          self.configure(width=value)
          self._frame.configure(width=value)
          self.onFrameChange(None)

     def addNewObjectInit(self):
        pass

     def addNewObjectApply(self, Values):
          pass

          
     def onEnter(self, event):
          self._canvas.bind_all("<MouseWheel>", self.onScroll)

     def onExit(self, event):
       
          self._canvas.unbind_all("<MouseWheel")

     def onScroll(self,event):
          if self._frame.winfo_height()>= self.winfo_height():
               self._canvas.yview_scroll(int(-1*int(event.delta/120)), "units")

     def addItems(self, Items):
          pass

     def resetItems(self):
          for i in self._objectFrame.pack_slaves():
               i.destroy()


#only difference rn is type of object spawned
class Sidebar(listWindow):
     def __init__(self, root, parent):
          super().__init__(root, parent)
          self.configure(style="sidebar.TFrame")
          self._canvas.configure(bg=THEME["sideTabBG"])
          
                   
          self._objectFrame.configure(style="sidebar.TFrame")
          self._buffer.configure(style="sidebar.TFrame")
          
     #going to be out from getdetails in an array
     def addItems(self, Items):

          for I in range(0,len(Items)):
                    
                    temp = ListOption(self._objectFrame,Items[I], parent=self)
                    temp.pack(fill="both", expand=True, pady=3)
          self.changeBuffer(None)
          
     def changeBuffer(self,event):
          pass
          
     def applyTheme(self):
          self.configure(style="sidebar.TFrame")
          self._canvas.configure(bg=THEME["sideTabBG"])

     def changeList(self, ID):
          self._parent.changeList(ID)

     def addNewObjectInit(self):
          self._popup = ListPopup(self)#

     def addNewObjectApply(self, Values):
           #Input of Values[ Description, dueDate]
          itemToAdd = CONTROLLER.addList(Values)
          ListOption(self._objectFrame, Object=itemToAdd, parent=self).pack(fill="both", expand=True, pady=3)
          self._popup.closeWindow()
          
          
     def applyEditToObject(self, ID, Values):
          CONTROLLER.updateList(ID, Values)

    

     def verifySelected(self):
          for i in self._objectFrame.pack_slaves():
               i.checkSelected()

     def deleteList(self, ID):
          for i in self._objectFrame.pack_slaves():
               if i.GetObject().GetID() == ID and CONTROLLER.GetCurrentList().GetID() == ID:
                    self.changeList(self._frame.pack_slaves()[0].GetObject().GetID())
          
          newList = CONTROLLER.deleteList(ID)
          if newList == None:
               self._parent.resetItems()




class itemWindow(listWindow):
     def __init__(self, root, parent):
          super().__init__(root, parent)
          self.configure(style="mainWindow.TFrame")
          self._canvas.configure(bg=THEME["mainWindowBG"])
         
          self._objectFrame.configure(style="mainWindow.TFrame")
          self._buffer.configure(style="mainWindow.TFrame")



          self._sortVar = tk.StringVar()
          self._sortVar.set(CONFIG["sortingType"])
          sortOptions = ("time Created (default)", "Due Date", "Priority","Completed")
          self._sortChoice = ttk.Combobox(self._addBar, textvariable=self._sortVar, values=sortOptions, style="sortingChoice.TCombobox")
          self._sortChoice.current(sortOptions.index(DEFAULTSCONTROLLER.getSorting()))
          self._sortChoice.bind("<<ComboboxSelected>>", self.changeSorting)
          self._sortChoice.pack(side=tk.RIGHT, fill="y")

          self._currentList = ttk.Label(self._addBar, text="TEST", style="incompleteItem.TLabel")
          self._currentList.pack(side=tk.LEFT, pady=3, padx=3)

     def applyTheme(self):
          self.configure(style="mainWindow.TFrame")
          self._canvas.configure(bg=THEME["mainWindowBG"])

     def addItems(self, Items):
          for I in range(len(Items)):
                              temp = ItemOption(self._objectFrame,Items[I], self)
                              temp.pack(fill="x",  pady=3)
          self.changeBuffer(None)

     def addNewObjectInit(self):
          if CONTROLLER.GetCurrentList() is not None:
               self._popup = itemPopup(self)

     def changeList(self, name):
          self._currentList.config(text=name)

     def addNewObjectApply(self, Values):
          objectToAdd = CONTROLLER.addItem(Values)
          ItemOption(self._objectFrame, objectToAdd, self).pack(fill="x",  pady=3)
          self._popup.closeWindow()
          self.changeSorting(None)
          self.changeBuffer(None)

     def changeSorting(self, event):
          CONFIG["sortingType"] = self._sortVar.get()
          CONTROLLER.changeSorting(self._sortVar.get())
          DEFAULTSCONTROLLER.applyConfig(CONFIG)
          self.resetItems()
          self.addItems(CONTROLLER.GetCurrentListitems())

class mainWindow(tk.Frame):
     def __init__(self, parent):
          super().__init__(parent)
          self.configure(bg=THEME["defaultObjectBG"])
          self._optionsBar = ttk.Frame(self,height=5, style="Default.TFrame")
          ttk.Button(self._optionsBar, text="options", command=self.openOptions, style="Default.TButton").pack(side=tk.LEFT)

          self._optionsBar.pack(fill="x")
          
          self._paned = tk.PanedWindow(self, orient="horizontal", bg=THEME["defaultObjectBG"])

          self._sidebar = Sidebar(self._paned, parent=self)
          self._sidebar.pack(side=tk.LEFT,fill="both", expand=True, padx=10, pady=10)
          self._paned.add(self._sidebar, minsize = 300)
          self._mainWindow = itemWindow(self._paned, parent=self)
          self._mainWindow.pack(side=tk.RIGHT, expand=True, fill="both",padx=10, pady=10)
          self._paned.add(self._mainWindow )

          self._paned.pack(fill="both", expand=True)


          Lists = CONTROLLER.GetLists()
          if  Lists != []:
               self.loadLists(Lists)
               self.changeList(Lists[0].GetID())
     
              
          self._mainWindow.changeSorting(None)

   

     def loadLists(self, Values):
          self._sidebar.addItems(Values)

     def loadItems(self, Values ):
          self._mainWindow.addItems(Values)


     def openOptions(self):
          x = optionsPopup(self)

     
     def copyTheme(self, dict1):
        for I in list(dict1.keys()):
            THEME[I] = dict1[I]


     def applyOptions(self):
          self.copyTheme(dict1 = DEFAULTSCONTROLLER.getTheme())
          self.configure(bg=THEME["defaultObjectBG"])
          self._paned.config(bg=THEME["defaultObjectBG"])
          self._sidebar.applyTheme()
          self._mainWindow.applyTheme()
          
          

     def changeList(self, ID):
          CONTROLLER.changeList(ID)
          self.resetItems()
          self.loadItems(CONTROLLER.GetCurrentListitems())
          self._sidebar.verifySelected()
          self._mainWindow.resetBuffer()
          self._mainWindow.changeList(CONTROLLER.GetCurrentList().GetDetails()[0])

     def resetItems(self):
          self._mainWindow.resetItems()

     def resetLists(self):
          self._sidebar.resetItems()




root = tk.Tk()
root.title("To Do V2")
root.geometry("1500x900")
root.minsize(300,1)

DEFAULTSCONTROLLER = customisingConfig.CustomManager(root)


CONTROLLER = logicCode.UserManager()
CONTROLLER.loadLists()
THEME = DEFAULTSCONTROLLER.getTheme()
CONFIG = DEFAULTSCONTROLLER.getConfig()
x = mainWindow(root)
x.pack(expand=True, fill="both")

root.mainloop()


