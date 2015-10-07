#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from createApGui.terminalInterface import TerminalInterface
import threading
from gi.repository import GObject

class RunningAp():
    def __init__(self, setting, tray=None, statusWindow=None):
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.updatingPage = {'tray':tray, 'statusWindow':statusWindow}
        self.lock = threading.Lock()
        self.mysignal = GObject.GObject()
        GObject.signal_new("newMsg", self.mysignal, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())
        GObject.signal_new("updateStatistic", self.mysignal, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())
        self.mysignal.connect('newMsg', self.newCmdMsg)
        self.reInit()


    def reInit(self):
        self.lock.acquire()
        self.__activeAp = {'name':'None', 'passwd':'None', 'interface1':'None', 'interface2':'None'}
        self.__status = {'active':False,'text':self._('No active AP'),'button':self._('Connect')}
        self.errorMsg = {'newMsg':False,'title':None, 'text':None}
        self.interface = TerminalInterface(self.mysignal,'newMsg')
        self.lock.release()

    def runAp(self):
        if self.__status['active']:
            self.stopAp()
        if self.errorMsg['newMsg']:
            self.reInit()
        self.lock.acquire()
        if self.__activeAp['name']!='None':
            self.interface.command = ['create_ap'+' '+self.__activeAp['interface1']+' '+self.__activeAp['interface2']+' '+self.__activeAp['name']+' '+self.__activeAp['passwd']]
            self.interface.start()
            self.__status['text'] = self._('Creating AP...')
            self.__status['button'] = self._('Disconnect')
            self.__status['active'] = True

        self.lock.release()
        self.updatingStatus()

    def stopAp(self):
        self.interface.stop()
        self.reInit()

    def newCmdMsg(self, signal=None):
        self.lock.acquire()
        msg = self.interface.read()
        if 'ERROR:' in msg or 'command not found' in msg:
            self.errorMsg['newMsg'] = True
            self.errorMsg['title'] = self._('Create failed')
            self.errorMsg['text'] = msg
            self.__status['text'] = self._('AP Error')
            self.__status['button'] = self._('Error details')
            self.__status['active'] = False
        elif 'AP-ENABLED' in msg:
            self.__status['text'] = self._('AP is active')
            self.__status['button'] = self._('Disconnect')
        elif 'INTERFACE-DISABLED' in msg:
            self.__status['text'] = self._('INTERFACE-DISABLED')
      #  elif 'AP-DISABLED' in msg or 'done' in msg:
        #    self.reInit()
      #  else:
       #     self.lock.release()
        #    return

        self.lock.release()
        self.updatingStatus()

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

    @property
    def status(self):
        self.lock.acquire()
        value = self.__status
        self.lock.release()
        return value
