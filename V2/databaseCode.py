import sqlite3
import os

class DatabaseManager:
    def __init__(self, Path):
        self._cursor = None
        self._connection = None
        self._basePath = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(self._basePath, Path)
        if not os.path.exists(self._path):
            self.createDatabase()


    def createDatabase(self):
        commands = ["""
        CREATE TABLE "List" (
        "ListID"	INTEGER,
        "Description"	TEXT NOT NULL,
        "IsDone"	INTEGER NOT NULL,
        PRIMARY KEY("ListID")
        )""","""
        CREATE TABLE "ListItem" (
        "ItemID"	INTEGER,
        "ListID"	INTEGER,
        "Description"	TEXT,
        "IsDone"	INTEGER,
        "DueDate"	REAL,
        "TimeCreated"	NUMERIC,
        "IsPriority"	INTEGER,
        "Note"	TEXT,
        PRIMARY KEY("ItemID")
        ) """, """
        CREATE TABLE "SubItem" (
        "SubItemID"	INTEGER,
        "ItemID"	INTEGER,
        "Description"	TEXT,
        "IsDone"	INTEGER,
        PRIMARY KEY("SubItemID")
        )
        """]
       

        self.openConnection()
        for I in commands:
            print(I)
            self._cursor.execute(I)
            #self._connection.commit()
        self.endConnection()
                

                
    
    def openConnection(self):
        self._connection = sqlite3.connect(self._path)
        self._cursor = self._connection.cursor()

    def endConnection(self):
        self._connection.commit()
        self._connection.close()

    #CRUD - R
    def getAllLists(self):
        self.openConnection()
        self._cursor.execute("""SELECT *
                                FROM List""")
        listResult = self._cursor.fetchall()
        self.endConnection()
        return listResult

    def getItemsOfList(self, listID):
        self.openConnection()
        self._cursor.execute(f"""SELECT ListItem.ItemID, ListItem.ListID, ListItem.Description, ListItem.IsDone, ListItem.DueDate, ListItem.TimeCreated, ListItem.IsPriority, ListItem.Note
                                FROM List, ListItem
                                WHERE List.ListID = ListItem.ListID
                                AND List.ListID = {listID}
                            """)
        ItemsResult = self._cursor.fetchall()
        self.endConnection()
        return ItemsResult

    def getSubitemsOfItem(self,ItemID):
        self.openConnection()
        self._cursor.execute(f"""SELECT SubItem.SubitemID, SubItem.ItemID, SubItem.Description, SubItem.IsDone
                                FROM SubItem, ListItem
                                WHERE SubItem.ItemID = ListItem.ItemID
                                AND ListItem.ItemID = {ItemID}
                                    """)
        SubResult = self._cursor.fetchall()
        self.endConnection()
        return SubResult

    #CRUD - C
    #[listID, description]
    def addList(self, Values):
        self.openConnection()
        self._cursor.execute(f"""INSERT INTO List(ListID,Description,IsDone)
                                VALUES({Values[0]},'{Values[1]}', {Values[2]})""")
        self.endConnection()

    #values array in form [ItemID,ListID, Description, IsDone, DueDate, TimeCreated, IsPriority]
    def addItem(self, Values):
        self.openConnection()
        print("VAlues to savwe: ",Values)
        self._cursor.execute(f"""INSERT INTO ListItem(ItemID,ListID, Description,IsDone, DueDate, TimeCreated, IsPriority, Note)
                                VALUES({Values[0]},{Values[1]},'{Values[2]}',{Values[3]},{Values[4]}, {Values[5]},{Values[6]}, '{Values[7]}')""")
        self.endConnection()

    def addSubItem(self,Values):
        self.openConnection()
        self._cursor.execute(f"""INSERT INTO SubItem(SubItemID,ItemID,Description,IsDone)
                                VALUES({Values[0]},{Values[1]},'{Values[2]}', {Values[3]})""")
        self.endConnection()


    #CRUD - D
    def deleteList(self, ListID):
        print("Deleting this list")
        ItemsToDelete = self.getItemsOfList(ListID)
        for I in ItemsToDelete:
            self.deleteItem(I[0])

        self.openConnection()
        self._cursor.execute(f"""DELETE FROM List
                                WHERE ListID = {ListID}""")
        self.endConnection()

    def deleteItem(self, ItemID):
        SubToDelete = self.getSubitemsOfItem(ItemID)
        for S in SubToDelete:
            self.deleteSubitem(S[0])

        self.openConnection()
        self._cursor.execute(f"""DELETE FROM ListItem
                                WHERE ItemID = {ItemID}""")
        self.endConnection()

    def deleteSubitem(self, SubID):
        self.openConnection()
        self._cursor.execute(f"""DELETE FROM SubItem
                                WHERE SubItemID == {SubID}""")
        self.endConnection()

    #CRUD - U

    def updateList(self, ListID, Values):
        self.openConnection()
        self._cursor.execute(f"""UPDATE List
                                SET Description = '{Values[0]}', IsDone= {Values[1]}
                                WHERE  ListID = {ListID}""")

        self.endConnection()

    def updateItem(self, ItemID, newValues):
        self.openConnection()
        self._cursor.execute(f"""UPDATE ListItem
                                SET Description = '{newValues[0]}', IsDone = {newValues[1]}, DueDate={newValues[2]}, TimeCreated = {newValues[3]}, IsPriority = {newValues[4]}, Note = '{newValues[5]}'
                                WHERE ItemID = {ItemID}""")
        self.endConnection()

    def updateSubitem(self, SubID, newValues):
        self.openConnection()
        self._cursor.execute(f"""UPDATE SubItem
                                 SET  Description = '{newValues[0]}', IsDone = {newValues[1]} 
                                 WHERE SubItemID= {SubID}""")
        self.endConnection()

    

if __name__ == "__main__":
    x = DatabaseManager("Data.db")
    x.openConnection()
    print(x.getItemsOfList(1))
  