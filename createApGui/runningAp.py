#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from createApGui.terminalInterface import TerminalInterface
import threading
class RunningAp():
    def __init__(self, setting, tray=None, statusWindow=None):
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.__activeAp = {'name':'None', 'passwd':'None', 'interface1':'None', 'interface2':'None'}
        self.status = {'active':False,'text':self._('No active AP'),'button':self._('Connect')}
        self.errorMsg = {'newMsg':False,'title':None, 'text':None}
        self.interface = TerminalInterface(self.newCmdMsg)
        self.updatingPage = {'tray':tray, 'statusWindow':statusWindow}
        self.lock = threading.Lock()

    def runAp(self):
        if self.__activeAp['name']!='None':
            self.interface.command = ['create_ap'+' '+self.__activeAp['interface1']+' '+self.__activeAp['interface2']+' '+self.__activeAp['name']+' '+self.__activeAp['passwd']]
            self.interface.start()
            self.status['text'] = self._('Creating AP...')
            self.status['button'] = self._('Disconnect')
            self.status['active'] = True
        self.updatingStatus()

    def createNew(self):
        self.setting['runningAp'] = RunningAp(self.setting, tray=self.updatingPage['tray'],statusWindow=self.updatingPage['statusWindow'])

    def stopAp(self):
        self.lock.acquire()
        self.interface.stop()
        self.interface.stop()
        self.createNew()
        self.lock.release()

    def newCmdMsg(self):
        self.lock.acquire()
        msg = self.interface.read()
        if 'ERROR:' in msg or 'command not found' in msg:
            self.errorMsg['newMsg'] = True
            self.errorMsg['title'] = self._('Create failed')
            self.errorMsg['text'] = msg
            self.status['text'] = self._('AP Error')
            self.status['button'] = self._('Error details')
            self.status['active'] = False
        elif 'AP-ENABLED' in msg:
            self.status['text'] = self._('AP is active')
            self.status['button'] = self._('Disconnect')
        elif 'INTERFACE-DISABLED' in msg:
            self.status['text'] = self._('INTERFACE-DISABLED')
        self.updatingStatus()
        self.lock.release()

    def updatingStatus(self):
        if self.updatingPage['statusWindow']:
            self.updatingPage['statusWindow']()
        elif self.updatingPage['tray']:
             self.updatingPage['tray']()

    @property
    def activeAp(self):
        return self.__activeAp

    @activeAp.setter
    def activeAp(self, data):
        self.__activeAp['name'] = data[0]
        self.__activeAp['passwd'] = data[1]
        self.__activeAp['interface1'] = data[2]
        self.__activeAp['interface2'] = data[3]
