from assig9 import Iterable, filter

class Repository:
    # Class for holding items in a list with operations on those items
    
    def __init__(self):
        self._list = Iterable()

    def searchByID(self, ID):

        for item in self._list:
            if item.getID() == ID:
                return item
        return None 
    
    def add(self, item):
        self._list.append(item)

    def update(self, id, item):
        self.searchByID(id).update(item)

    def remove(self, id):
        for i in range(len(self._list)):
            if self._list[i].getID() == id:
                item = self.searchByID(id).copy()
                del self._list[i]
                return item

    def getAll(self):
        return self._list

import sys

class TextFileRepository(Repository):
    def __init__(self, item, filename):
        Repository.__init__(self)
        self._fileName = filename
        self._item = item
        self._loadFile()

    def add(self, obj):
        Repository.add(self, obj)
        self._saveFile()

    def update(self, id, item):
        Repository.update(self, id, item)
        self._saveFile()

    def remove(self, id):
        item = Repository.remove(self, id)
        self._saveFile()
        return item

    def _saveFile(self):
        f = open(sys.path[0] + "\\" + self._fileName, 'w')
        for item in self.getAll():
            f.write(item.item2string() + '\n')
        f.close()
        
    def _loadFile(self):
        f = open(sys.path[0] + "\\" + self._fileName, 'r')
        line = f.readline().strip()
        while len(line) > 2:
            item = self._item.string2item(line).copy()
            Repository.add(self, item)
            line = f.readline().strip()
        f.close()

import pickle
import os

class PickleFileRepository(Repository):
    def __init__(self, item, filename):
        Repository.__init__(self)
        self._fileName = filename
        self._item = item
        self._loadFile()

    def add(self, obj):
        Repository.add(self, obj)
        self._saveFile()

    def update(self, id, item):
        Repository.update(self, id, item)
        self._saveFile()

    def remove(self, id):
        item = Repository.remove(self, id)
        self._saveFile()
        return item

    def _saveFile(self):
        f = open(sys.path[0] + "\\" + self._fileName, 'wb')
        pickle.dump(Repository.getAll(self), f)
        f.close()
        
    def _loadFile(self):
        if os.path.getsize(sys.path[0] + "\\" + self._fileName) > 0:
            f = open(sys.path[0] + "\\" + self._fileName, 'rb')
            for item in pickle.load(f):
                Repository.add(self, item)
            f.close()

import json

class JsonFileRepository(Repository):
    def __init__(self, item, filename):
        Repository.__init__(self)
        self._fileName = filename
        self._item = item
        self._loadFile()

    def add(self, obj):
        Repository.add(self, obj)
        self._saveFile()

    def update(self, id, item):
        Repository.update(self, id, item)
        self._saveFile()

    def remove(self, id):
        item = Repository.remove(self, id)
        self._saveFile()
        return item

    def _saveFile(self):
        f = open(sys.path[0] + "\\files\\" + self._fileName, 'w')
        aux = []
        for obj in Repository.getAll(self):
            aux.append(obj.item2string())
        json.dump(aux, f)
        f.close()
        
    def _loadFile(self):
        if os.path.getsize(sys.path[0] + "\\files\\" + self._fileName) > 0:
            f = open(sys.path[0] + "\\files\\" + self._fileName, 'r')
            aux = json.load(f)
            for string in aux:
                item = self._item.string2item(string).copy()
                Repository.add(self, item)
            f.close()

import sqlite3

class SqlFileRepository(Repository):
    def __init__(self, item, filename):
        Repository.__init__(self)
        self._fileName = filename
        self._item = item
        
        self._conn = sqlite3.connect(sys.path[0] + "\\files\\" + self._fileName)
        # Create table
        c = 'CREATE TABLE IF NOT EXISTS ' + self._item.itemType() + '( id, string )'
        self._conn.cursor().execute(c)

        self._loadFile()

    def add(self, obj):
        Repository.add(self, obj)
        self._saveFile()

    def update(self, id, item):
        Repository.update(self, id, item)
        self._saveFile()

    def remove(self, id):
        item = Repository.remove(self, id)
        self._saveFile()
        return item

    def _saveFile(self):
        c = 'DELETE FROM ' + self._item.itemType()
        cursor = self._conn.cursor()
        cursor.execute(c)

        for item in Repository.getAll(self):
            c = "INSERT INTO " + self._item.itemType() + " VALUES (" + str(item.getID()) + ",'" + item.item2string() + "')"
            cursor.execute(c)

        self._conn.commit()
        
    def _loadFile(self):
        cursor = self._conn.cursor()
        cursor.execute('SELECT * FROM ' + self._item.itemType())
        aux = cursor.fetchall()
        
        for obj in aux:
            string = obj[1]
            item = self._item.string2item(string).copy()
            Repository.add(self, item)