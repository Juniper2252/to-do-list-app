
import time
import re
import databaseCode
import os

#items, subitems, sorting, completeness, priority, deadlines
#add to sorting so all completed items can be removed (same sorting algorithm, but have variations for with or without completed tasks)

#maybe repeating tasks?
#sort database now - done, database desgined and created
#in general, should be a buffer from GUI for all data, so the usermanager doesnt need to error check too much, can be adapted

#db -> objects -> GUI

#connect db now - half done
#finish last two methods
#test through making test input class to handle role GUI
#make findItem method, searches for Item in a list of objects - done!
#make InitialiseData method, loads all lists and items from memory -done!""
#each time a change is made, the classes and GUI handle user expwerience, and the DB handles data, not everything needs to be re-fetched again to display



#to do list should create the items, not usermanager
#add control when nothing in the
class ToDoList:
    def __init__(self, description: str, isDone=0, ID=0, root=None):
        self._items = []
        self._description = description
        self._isDone = isDone
        self._ID = ID
        self._selected = False

    def GetSelected(self):
        return self._selected

    def setSelected(self, val:bool):
        self._selected = val

    def addItem(self, I):
        self._items.append(I)
    
    def removeItems(self, I):
        if I in self._items:
            self._items.remove(I)

    def popItem(self):
        return self._items.pop(-1)
        

    def updateValues(self, Values):
        self._description = Values[0]
        self._isDone = Values[1]

    def toggleComplete(self):
        if self._isDone == 0:
            self._isDone = 1
        else:
            self._isDone = 0

    
    def GetItems(self):
        return self._items

    def GetID(self):
        return self._ID
    
    def GetDetails(self):
        return [self._description, self._isDone]


    def toggleComplete(self):
        if self._isDone == 0:
            self._isDone = 1
            if len(self._items) != 0:
                for I in self._items:
                    I.toggleComplete()
        else:
            self._isDone = 0


    #sorting independant of database
    
    def sortByPriority(self):
        itemsWithPrioirty = []
        itemsWithoutPriority = []
        for I in self._items:
            if I.GetDetails()[4] == 0:
                itemsWithoutPriority.append(I)
            else: itemsWithPrioirty.append(I)
        
        TotalItems = itemsWithPrioirty + itemsWithoutPriority
        self._items = TotalItems
    
    def sortByDueDate(self):
        itemsWithDueDate = []
        itemsWithoutDueDate = []
        for I in self._items:
            if I.GetDetails()[2] == -1:
                itemsWithoutDueDate.append(I)
            else:
                itemsWithDueDate.append(I)
        
        sortedItems = sorted(itemsWithDueDate, key=lambda x: x.GetDetails()[2])
        self._items = sortedItems + itemsWithoutDueDate
    
    def sortByTimeCreated(self):
        tempArray = []
        for I in self._items:
            tempArray.append(I)
        
        tempArray = sorted(tempArray, key=lambda x: x.GetDetails()[3])
        self._items = tempArray

    def sortByCompleted(self):
        tempArrayComplete = []
        tempArrayIncomplete = []
        for I in self._items:
            if I.GetDetails()[1] == 1:
                tempArrayComplete.append(I)
            else:
                tempArrayIncomplete.append(I)

        self._items =  tempArrayIncomplete + tempArrayComplete
    def __len__(self):
        return len(self._items)
    
class ToDoListItem(ToDoList):
    def __init__(self, description: str,note: str, dueDate: int, isPriority: int, isDone: int=0, ID: int = 0):
        super().__init__(description, isDone, ID)
        self._dueDate = dueDate
        self._timeCreated = time.time()
        self._isPrioirity = isPriority
        self._note = note


    def updateValues(self, Values):
        self._description = Values[0]
        self._isDone = Values[1]
        self._dueDate = Values[2]
        self._timeCreated = Values[3]
        self._isPrioirity = Values[4]
        self._note = Values[5]


   
    def GetDetails(self):
        return [self._description, self._isDone,  self._dueDate,self._timeCreated, self._isPrioirity, self._note]

class SubToDoListItem(ToDoListItem):
    def __init__(self, description,isDone = 0, ID = 0):
        super().__init__(description=description, note="", dueDate=-1, isPriority=0, isDone=isDone, ID=ID)

    def updateValues(self, Values):
        self._description = Values[0]
        self._isDone = Values[1]

    def GetDetails(self):
        return [self._description, self._isDone]


class UserManager:
    #this class handles the users environment, holds the items of currently selected list and its items


    def __init__(self):
        #holds currentListID
        self.__currentList: ToDoList = None
        #holds objects created from all objects
        self.__possibleLists = []
        self.__DB = databaseCode.DatabaseManager("Data.db")
        self._highestID = [0,0,0]
        self._sortingMethod = 0

    #all error checking on GUI side, these functions take an input of data and CRUD it


    def loadLists(self):
        AllLists = self.__DB.getAllLists()
        ListID = 0
        ItemID = 0
        SubID = 0
        for I in AllLists:
           
            if int(I[0]) > ListID:
                ListID = I[0]
            tempList = ToDoList(I[1],I[2],I[0])
            ItemsOfList = self.__DB.getItemsOfList(I[0])
            for J in ItemsOfList:
                if int(J[0]) > ItemID:
                    ItemID = J[0]
                tempItem = ToDoListItem(description=J[2],dueDate=J[4],isPriority=J[6],isDone=J[3], ID=J[0], note=J[7])
                tempList.addItem(tempItem)
                subitemsOfItem = self.__DB.getSubitemsOfItem(J[0])
                for K in subitemsOfItem:
                   
                    if int(K[0]) > SubID:
                        SubID = K[0]
                    tempSub = SubToDoListItem(description=K[2], ID=K[0], isDone=K[3])
                    tempItem.addItem(tempSub)
            self.__possibleLists.append(tempList)
        self._highestID = [ListID, ItemID, SubID]
       
          
    def GetLists(self):
        return self.__possibleLists

    def GetCurrentListitems(self):
        
        if self.__currentList is not None:
            return self.__currentList.GetItems() 

    def GetCurrentList(self):
        return self.__currentList
    #IRRELEVANT TO GUI
    def findCompletion(self, isDone: bool):
        if isDone == True:
            return " | Done!"
        else:
            return " | Incomplete"

    #inconclusive, but probably still index used here
    def changeList(self, ID):
        tempList = self.findItemFromID(self.__possibleLists, ID)
        if tempList is not None:
            if self.__currentList is not None:
                self.__currentList.setSelected(False)

            self.__currentList = tempList
            self.__currentList.setSelected(True)

    #kinda pointless
    def displayDetails(self):
        print("[Lists]: ")
        print("------------------------------")
        

        for i in range(0, len(self.__possibleLists)):
            print(" ",self.__possibleLists[i].GetID(), end=". ")
            tempList = self.__possibleLists[i]
            print(tempList.GetDetails()[0] + self.findCompletion(tempList.GetDetails()[1]))
        
        print("------------------------------")
        print()
        print()
        print("[Current List]: ", self.__currentList.GetDetails()[0] + self.findCompletion(self.__currentList.GetDetails()[1]))
        print("------------------------------")
        if len(self.__currentList) == 0:
            print("no Items")
        for i in range(0, len(self.__currentList)):
            
            tempItem = self.__currentList.GetItems()[i]
            InfoString = " " + str(self.__currentList.GetItems()[i].GetID()) + ". " + tempItem.GetDetails()[0]

            
            
            
            if tempItem.GetDetails()[2] != -1:
                InfoString += f" | {time.ctime(tempItem.GetDetails()[2])}"
            
            InfoString += self.findCompletion(tempItem.GetDetails()[1])
            
            if tempItem.GetDetails()[2] == True:
                InfoString += " | HIGH PRIORITY"
            print(InfoString)
            
            if len(tempItem) > 0:
                for i in range(0,len(tempItem)):
                    tempItem2 = tempItem.GetItems()[i]
                    InfoString2 = "     " + str(tempItem2.GetID()) + ". " + tempItem2.GetDetails()[0]
                    
                    InfoString2 += self.findCompletion(tempItem2.GetDetails()[1])
                    print(InfoString2)
        print("------------------------------")
        print()

    def changeSorting(self, inp):
        sortOptions = {"time Created (default)": 0, "Due Date": 1, "Priority": 2,"Completed": 3}
        match sortOptions[inp]:
            case 0:
                self.__currentList.sortByTimeCreated()
            case 1:
                self.__currentList.sortByDueDate()
            case 2:
                self.__currentList.sortByPriority()
            case 3:
                self.__currentList.sortByCompleted()

    #needs to be called after every transaction
    def update(self):
        self.__currentList.checkForExpiring()
        self.__currentList.checkForCompletion()
        self.__currentList.sortByDueDate()


    def findItemFromID(self, list, itemID):
        for I in list:
            if I.GetID() == itemID:
                return I
        return None

    #[desc, isDone]
    def addList(self, Values):
            #needs to add data to database and instantiate 
            listToAdd = ToDoList(description=Values[0], isDone=Values[1], ID=(self._highestID[0]+1))
            self._highestID[0] = self._highestID[0] + 1
            self.__possibleLists.append(listToAdd)
            self.__DB.addList([listToAdd.GetID(), Values[0], Values[1]])
            return listToAdd
            
        #should take input of list ID
    def deleteList(self, ID):
            #check if ID present
            listToRemove = self.findItemFromID(self.__possibleLists, ID)
            
            if listToRemove is not None:

                self.__possibleLists.remove(listToRemove)
                self.__DB.deleteList(ID)
                if listToRemove == self.__currentList:
                    if len(self.__possibleLists) > 0:
                        self.__currentList = self.__possibleLists[0]
                        return self.__currentList
                    else:
                        self.__currentList = None
                        return self.__currentList
    #description, isDone

    
    def sanitiseUpdateData(self,Old, New):
        for J in range(0,len(New)):
            if New[J] == None:
                New[J] = Old[J]
        return New



    def updateList(self, ID, Values):
        listToEdit: ToDoList = self.findItemFromID(self.__possibleLists, ID)
        newValues = self.sanitiseUpdateData(listToEdit.GetDetails(), Values)
        print(newValues)
        listToEdit.updateValues(newValues)
        self.__DB.updateList(ID, newValues)
    

    #S is a string for Descrtiption
    def addSubitem(self,Values, ItemID: int):

        SubItem = SubToDoListItem(description=Values[0], isDone=Values[1], ID=(self._highestID[2]+1))
        self._highestID[2] = self._highestID[2] + 1
        TempItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
       
        TempItem.addItem(SubItem)

        self.__DB.addSubItem([SubItem.GetID(),ItemID,Values[0], Values[1]])
        return SubItem

    def deleteSubitem(self, ItemID, SubID):
        ItemToDeleteFrom = self.findItemFromID(self.__currentList.GetItems(), ItemID)
        SubToDelete = self.findItemFromID(ItemToDeleteFrom.GetItems(), SubID)
        if SubToDelete is not None:
            ItemToDeleteFrom.removeItems(SubToDelete)
            self.__DB.deleteSubitem(SubID)


    #description, isDone
    def updateSubitem(self, SubID,ItemID, Values):
        itemToEdit: ToDoListItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
        SubToEdit: ToDoListItem = self.findItemFromID(itemToEdit.GetItems(), SubID)
        newValues = self.sanitiseUpdateData(SubToEdit.GetDetails(), Values)
        objectValues = newValues + [-1,-1,0,""]
        
        SubToEdit.updateValues(objectValues)
        dbValues = [newValues[0], newValues[1]]
        print(dbValues)
        self.__DB.updateSubitem(SubID, dbValues)
       


    def deleteItem(self, ItemID):
        ItemToDelete =self.findItemFromID(self.__currentList.GetItems(), ItemID)
        if ItemToDelete is not None:
            self.__currentList.removeItems(ItemToDelete)
            self.__DB.deleteItem(ItemID)

    #Input of Values[ Description, isDone, dueDate, -1,isPriority, note]
    def addItem(self, Values):
        itemToAdd = ToDoListItem(description=Values[0], isDone=Values[1], dueDate=Values[2], isPriority=Values[4], ID=(self._highestID[1]+1), note=Values[5])
        self._highestID[1] = self._highestID[1] + 1
        self.__currentList.addItem(itemToAdd)
        self.__DB.addItem([itemToAdd.GetID(),self.__currentList.GetID(), Values[0], Values[1], Values[2], time.time(), Values[4], Values[5]])
        return itemToAdd

# [Description, IsDone, DueDate, TimeCreasted, IsPriority, Note]
    def updateItem(self, ItemID, Values):
      
        ItemToEdit: ToDoListItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
        newValues = self.sanitiseUpdateData(ItemToEdit.GetDetails(), Values)
      
        ItemToEdit.updateValues(newValues)
        self.__DB.updateItem(ItemID, newValues)
    
    def ItemDetails(self, ItemID):
        TempItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
        print()
        print("ITEM - ", TempItem.GetDetails()[1])
        print("additional notes: ",TempItem.GetDetails()[6])
        for I in TempItem.GetItems(): 
            print(" " +str(I.GetDetails()[0]) + ". " + str(I.GetDetails()[1]))
        print()

    def addNote(self, ItemID, N):
            TempItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
            TempItem.addNote(N)
    
    def toggleComplete(self, SubID, ItemID, Values):
        itemToEdit: ToDoListItem = self.findItemFromID(self.__currentList.GetItems(), ItemID)
        SubToEdit: ToDoListItem = self.findItemFromID(itemToEdit.GetItems(), SubID)
        

#create delete subitem and list
#create edit all items

def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def createItem():
        name = input("Enter name item: ")

        dueDate = input("Add due date? (Y/N): ")
        timeDue = -1
        if dueDate == "Y":
            timeDue = getTime()

        priority = input("is high priority?: Y/N ")

        if priority == "Y":
            priorityToAdd = 1
        else:
            priorityToAdd = 0
        return [name, timeDue, priorityToAdd]

def getTime():
        #error checking of input
        #using re
        #if no input time for given, input 23:59
        #with GUI this can be selected and just re-inputted
        #easier to loop on CLI

        validTime = False
        while not validTime:
            validTime = True
            TimeToAdd = input("enter time: (format of dd/mm/yyyy hh:mm):  ")
            TimeToAdd = TimeToAdd.strip(" ")

        #regex error checking
            dateResult = re.search(r"[0-3][1-9]\/(0[1-9]|1[0-2])\/[0-9]{4}", TimeToAdd)
            timeResult = re.search(r"([0-1][0-9]|2[0-3]):[0-5][0-9]", TimeToAdd)
            if dateResult and not timeResult:
                TimeToAdd += " 23:59"
            elif timeResult and not dateResult:
                currentDate = time.localtime()
                currentDateFormatted = str(currentDate.tm_mday) + "/" + str(currentDate.tm_mon) +"/"+ str(currentDate.tm_year) 
                TimeToAdd = currentDateFormatted + " " + TimeToAdd
            elif not dateResult and not timeResult:
                print("not a valid date")
                validTime = False
            #add error checking
            TimeOutput = time.strptime(TimeToAdd, "%d/%m/%Y %H:%M")
            if time.mktime(TimeOutput) < time.time():
                print("date already passed")
                validTime = False

            if validTime == False:
                choice = input("Try again? (Y/N): ")
                if choice != "Y":
                    return -1
            
        return time.mktime(TimeOutput)

def displayChoices():

    print("1. Delete Item")
    print("2. Add Item")
    print("3. print Items again")
    print("4. Change List")
    print("5. add List")
    print("6. Remove List")
    print("7. add sub item")
    print("10. delete subitem")
    print("11. view item details")
    print("12. add note")
    print("13. update Item")
    print("14. toggle complete Item")
    print("15. update list")
    print("16. toggle complete list")
    print("17. update subitem")
    print("18. toggle complete subitem")
    print()

def getInput():
    valid = False
    while not valid:
        valid = True
        choice = int(input("enter choice: "))
        if choice not in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]:
            valid = False
           
    return choice

if __name__ == "__main__":
    x = UserManager()
    x.loadLists()
    clearTerminal()
    while True:
        x.displayDetails()
        displayChoices()
        option = getInput()
        if option == 1:
            IndexToChange = int(input("Item to remove: "))
            x.deleteItem(IndexToChange)
        elif option == 2:
            itemToAdd = createItem()
            x.addItem(itemToAdd)
        elif option == 3:
            x.displayDetails()
        elif option == 4:
            IndexToChange = int(input("new list number: "))
            x.changeList(IndexToChange)
        elif option == 5:
            ListName = input("name of list: ")
            x.addList(ListName)
        elif option == 6:
            IndexToChange = int(input("new list number: "))
            x.removeList(IndexToChange)
        elif option == 7:
            IndexToChange = int(input("Item to add to: "))
            SubName = input("name of Subitem: ")
            x.addSubitem(SubName, IndexToChange)
        elif option == 8:
            IndexToChange = int(input("Item to mark as complete: ")) 
            x.toggleCompleteItem(IndexToChange)
        elif option == 9:
            IndexToChange = int(input("Item: ")) 
            IndexToChange2 = int(input("Subitem: "))
            x.toggleCompleteSubitem(IndexToChange, IndexToChange2)
        elif option == 10:
            IndexToChange = int(input("Item: ")) 
            IndexToChange2 = int(input("Subitem: "))
            x.deleteSubitem(IndexToChange,IndexToChange2)
        elif option == 11:
            IndexToChange = int(input("Item: ")) 
            x.ItemDetails(IndexToChange)
            input()
        elif option == 12:
            IndexToChange = int(input("Item: ")) 
            x.ItemDetails(IndexToChange)
            Note = input("new note: ")
            x.addNote(IndexToChange, Note)
        elif option == 13:
            IndexToChange = int(input("Item: ")) 
            newItem = createItem()
            x.updateItem(IndexToChange, [newItem[0],None,newItem[1], None, newItem[2],None])
        elif option == 14:
            IndexToChange = int(input("Item: ")) 
            choice = int(input("complete or not?: 0/1: "))
            x.updateItem(IndexToChange,[None,choice,None,None,None,None])

        elif option == 15:
            listToUpdate = int(input("list: "))
            listName = input("enter new list name: ")
            x.updateList(listToUpdate, [listName, None])

        elif option == 16:
            IndexToChange = int(input("List: ")) 
            choice = int(input("complete or not?: 0/1: "))
            x.updateList(IndexToChange,[None,choice])

        elif option == 17:
            IndexToChange = int(input("Item: ")) 
            IndexToChange2 = int(input("Subitem: "))
            newSub = input("new subitem name: ")
            x.updateSubitem(IndexToChange2, IndexToChange, [newSub, None])

        elif option == 18:
            IndexToChange = int(input("Item: ")) 
            IndexToChange2 = int(input("Subitem: "))
            choice = int(input("complete or not?: 0/1: "))
            x.updateSubitem(IndexToChange2, IndexToChange, [None, choice])

       
        clearTerminal()
        



