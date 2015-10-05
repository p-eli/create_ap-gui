#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gettext
import os


class Languge():
    def __init__(self, setting):
        self.setting = setting
        self.setLanguage()

    def setLanguage(self):
        self.language = gettext.translation(self.setting['userSetting'].language['fileName'], os.path.join(self.setting['path'],self.setting['userSetting'].language['path']), fallback=True, languages=[self.setting['userSetting'].language['name']])
        self.gettext = self.language.gettext

    def update(self, setting):
        self.setting = setting
        self.setLanguage()

    def getLanguageList(self):
        return os.listdir(os.path.join(self.setting['path'],self.setting['userSetting'].language['path']))