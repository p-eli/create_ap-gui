#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import pickle
import os
from createApGui import __version__

class UserSetting():
    def __init__(self):
        self.version = {'version':__version__, 'autoCheck':True}
        self.language = {'name':'English_en', 'fileName':'lang', 'path':'lang'}
        self.saveAp = []
        try:
            self.saveFile = {'path':os.path.join(os.path.expanduser("~"+os.getenv("PKEXEC_UID")),'.crateApGui'), 'fileName':'userSetting'}
        except:
            self.saveFile = {'path':os.path.join(os.path.expanduser("~"+os.getlogin()),'.crateApGui'), 'fileName':'userSetting'}
      #  self.newAP = {'name':'','passwd':'','interface':None,'interface1':None}

    def addAp(self, name, passwd, interface1, interface2):
        self.saveAp.append({'name':name,'passwd':passwd,'interface1':interface1,'interface2':interface2})
        self.save()

    def removeAp(self, name, interface1, interface2):
        if self.saveAp != []:
            for item in self.saveAp:
                if item['name']==name and item['interface1']==interface1 and item['interface2']==interface2:
                    self.saveAp.remove(item)
        self.save()

    def searchAp(self, name, interface1=None, interface2=None):
        if self.saveAp != []:
                for item in self.saveAp:
                    if (interface1 == interface2 == None and item['name']==name) or (item['name']==name and item['interface1']==interface1 and item['interface2']==interface2):
                        return [item['name'], item['passwd'], item['interface1'], item['interface2']]

    def getApStore(self, store):
        if self.saveAp != []:
            for item in self.saveAp:
                store.append([item['name'],item['interface1'],item['interface2']])

    def save(self):
        with open(os.path.join(self.saveFile['path'],self.saveFile['fileName']), 'wb') as file:
            pickle.dump(self,file)

    def load(self):
        try:
            with open(os.path.join(self.saveFile['path'],self.saveFile['fileName']), 'rb') as file:
                loadSetting = pickle.load(file)
                try:
                    if loadSetting.version == __version__:
                        return loadSetting
                    else:
                        self.saveAp = loadSetting.saveAp
                        self.language = loadSetting.language
                        self.version = loadSetting.version
                        self.save()
                        return self
                except:
                    self.saveAp = loadSetting.saveAp
                    self.save()
                    return self

        except FileNotFoundError:
            return self
