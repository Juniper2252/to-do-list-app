import tkinter as tk
from tkinter import ttk
import json
import os 

#dark mode :)

CONFIG = {
     "autocompleteObjects": True,
     "sortingType": "time Created (default)"
}




class CustomManager:
    def __init__(self, root):
        self._root = root
        self._basePath = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(self._basePath, "config\\userDefaults.JSON")

        self._theme = {}
        self._config = {}
        self._customtheme = ttk.Style(self._root)
        self._customtheme.theme_use("clam")
        self.getDefaults()
   
        self.setStyle()

    def getDefaults(self):
        with open(self._path, "r") as f:
            rawData = f.read()
            parsedData =  json.loads(rawData)
            self._theme = parsedData["THEME"]
            self._config = parsedData["CONFIG"]
           

    def getTheme(self):
        return self._theme

    def getConfig(self):
            return self._config 

    def getTypeOfTheme(self):
        return self._config["themeType"]

    def setStyle(self):

        self._customtheme.configure("Default.TButton", background = self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], font=(self._theme["defaultFont"],10))
        self._customtheme.map("Default.TButton", background=[("active", self._theme["hoveringObjectBG"])])

        #needs some work, especially when clicked
        self._customtheme.configure("Default.TCheckbutton", background=self._theme["defaultObjectBG"],margin = 0, padding=0, indicatorbackground=self._theme["defaultObjectBG"], indicatorforeground=self._theme["defaultObjectFG"])
        self._customtheme.map("Default.TCheckbutton", background=[("active", self._theme["defaultObjectBG"])])

        self._customtheme.configure("incompleteList.TButton", background=self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], font=(self._theme["defaultFont"], 12))
        self._customtheme.map("incompleteList.TButton", background=[("active", self._theme["hoveringObjectBG"])])
        
        self._customtheme.configure("completeList.TButton", background=self._theme["completedObjectBG"], foreground=self._theme["completedObjectFG"], font=(self._theme["defaultFont"], 12))
        self._customtheme.map("completeList.TButton", background=[("active", self._theme["hoveringObjectBG"])])
                
        self._customtheme.configure("incompleteItem.TFrame", background=self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], font=(self._theme["defaultFont"], 18), borderwidth=1, relief="ridge")
        self._customtheme.configure("completeItem.TFrame", background=self._theme["completedObjectBG"], foreground=self._theme["completedObjectFG"], font=(self._theme["defaultFont"], 18), borderwidth=1, relief="ridge")
        self._customtheme.configure("incompleteItem.TLabel", background=self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], font=(self._theme["defaultFont"], 18))
        self._customtheme.configure("completeItem.TLabel", background=self._theme["completedObjectBG"], foreground=self._theme["completedObjectFG"], font=(self._theme["defaultFont"], 18))
                             
        self._customtheme.configure("selectedList.TButton", background=self._theme["selectedListBG"], foreground=self._theme["selectedListFG"], font=(self._theme["defaultFont"], 12))
        self._customtheme.map("selectedList.TButton", background=[("active", self._theme["hoveringObjectBG"])])

        
        self._customtheme.configure("hoveringItemIncomplete.TLabel", foreground=self._theme["hoveringObjectBG"], background = self._theme["defaultObjectBG"],font=(self._theme["defaultFont"], 18))
        self._customtheme.configure("hoveringItemComplete.TLabel", foreground=self._theme["hoveringObjectBG"], background = self._theme["completedObjectBG"],font=(self._theme["defaultFont"], 18))

        self._customtheme.configure("hoveringSubIncomplete.TLabel", foreground=self._theme["hoveringObjectBG"], background = self._theme["defaultObjectBG"], font=(self._theme["defaultFont"], 18))
        self._customtheme.configure("hoveringSubComplete.TLabel", foreground=self._theme["hoveringObjectBG"], background = self._theme["completedObjectBG"], font=(self._theme["defaultFont"], 18))


        self._customtheme.configure("popupFrame.TFrame", background = self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"])
        self._customtheme.configure("popupLabel.TLabel", background = self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"],font=(self._theme["defaultFont"], 18))
        self._customtheme.configure("popupEntry.TEntry", fieldbackground  = self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], insertcolor= self._theme["defaultObjectFG"], lightcolor =  self._theme["completedObjectBG"], font=(self._theme["defaultFont"], 18))
        self._customtheme.configure("calendar.DateEntry",fieldbackground=self._theme["defaultObjectBG"], background= self._theme["defaultObjectBG"],foreground=self._theme["defaultObjectFG"], arrowcolor =self._theme["defaultObjectFG"], font=(self._theme["defaultFont"],10))
        self._customtheme.map("calendar.DateEntry", background=[("active", self._theme["defaultObjectBG"])])
        self._customtheme.map("calendar.DateEntry", arrowcolor =[("active", self._theme["defaultObjectFG"])])
        self._customtheme.configure("sortingChoice.TCombobox",fieldbackground=self._theme["defaultObjectBG"], background= self._theme["defaultObjectBG"],foreground=self._theme["defaultObjectFG"], arrowcolor =self._theme["defaultObjectFG"], font=("Impact",10))
        self._customtheme.map("sortingChoice.TCombobox", background=[("active", self._theme["defaultObjectBG"])])
        self._customtheme.map("sortingChoice.TCombobox", arrowcolor =[("active", self._theme["defaultObjectFG"])])


        self._customtheme.configure("datetime.TSpinbox",background= self._theme["defaultObjectBG"], foreground=self._theme["defaultObjectFG"], font=(self._theme["defaultFont"],10), fieldbackground=self._theme["defaultObjectBG"])
        self._customtheme.configure("sidebar.TFrame", background=self._theme["sideTabBG"])
        self._customtheme.configure("mainWindow.TFrame", background=self._theme["mainWindowBG"])

        self._customtheme.configure("scrollBar.Vertical.TScrollbar", troughcolor=self._theme["defaultObjectBG"], background=self._theme["defaultObjectBG"], arrowcolor = self._theme["defaultObjectFG"])
        self._customtheme.map("scrollBar.Vertical.TScrollbar", background=[("disabled",self._theme["defaultObjectBG"])] )
        self._customtheme.map("scrollBar.Vertical.TScrollbar", background=[("active",self._theme["defaultObjectBG"])] )

        self._customtheme.configure("Default.TFrame", background=self._theme["defaultObjectBG"])

    def saveTheme(self):
        with open(self._path, "w") as f:
           
           data = {
               "THEME" : self._theme,
               "CONFIG" : self._config
           }
           writingdata =json.dumps(data)
         
           f.write(writingdata) 

    def copyDict(self, dict1, dict2):
        for I in list(dict1.keys()):
            dict1[I] = dict2[I]

        return dict1

    def applyTheme(self,type, theme):
        if type == "Custom":
            self._theme = self.copyDict(self._theme, theme)
        else:
            self.applyDefaultTheme(type)

        self._config["themeType"] = type
        self.setStyle()
        self.saveTheme()
        print(self._config)
        print(self._theme)

    def applyConfig(self, config):
        self._config = self.copyDict(self._config, config)
        self.saveTheme()

    def getDefaultThemes(self):
        themePath = os.path.join(self._basePath, "config\\defaultThemes.JSON")
        with open(themePath, "r") as f:
            x = f.read()
            themeData = json.loads(x)
            return themeData

    def getDefaultThemeNames(self):
        return self.getDefaultThemes().keys()


    def saveCustomTheme(self, theme, name):
        path = os.path.join(self._basePath,"config\\defaultThemes.JSON")
        with open(path, "r") as f:
            currentData = f.read()
            parsedData = json.loads(currentData)
        
            parsedData[str(name)] = theme
          
        with open(path, "w") as f:
            f.write("")
            f.write(json.dumps(parsedData))
    

    def applyDefaultTheme(self, default):
        themes = self.getDefaultThemes()
        currentTheme = themes[default]
        self._theme = currentTheme
        self.setStyle()
        self.saveTheme()

    def changeSorting(self,choice):
        self._config["sortingType"] = choice
        self.saveTheme()

    def getSorting(self):
        return self._config["sortingType"]

if __name__ =="__main__":
    root = tk.Tk()
    x = CustomManager(root)
    print(x.getDefaults())