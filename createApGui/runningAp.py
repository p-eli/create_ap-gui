#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from createApGui.terminalInterface import TerminalInterface, Statistic
import threading
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject

signalNewMsg = 'newMsg'
signalUpdateStatistic = 'updateStatistic'
regexRX = re.compile('RX[^\(]*[^\)]*\)')
regexTX = re.compile('TX[^\(]*[^\)]*\)')
regexBrackets = re.compile('[^\(]*\(([^\)]*)\)')

class RunningAp():
    GObject.signal_new(signalNewMsg, GObject.GObject, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())
    GObject.signal_new(signalUpdateStatistic, GObject.GObject, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())

    def __init__(self, setting, tray=None, statusWindow=None):
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.updatingPage = {'tray':tray, 'statusWindow':statusWindow}
        self.interfaceLock = threading.Lock()
        self.statisticLock = threading.Lock()

        self.mysignal = GObject.GObject()
        self.mysignal.connect(signalNewMsg, self.newCmdMsg)
        self.mysignal.connect(signalUpdateStatistic, self.updateStatistic)
        self.reInit()


    def reInit(self):
        self.interfaceLock.acquire()
        self.__activeAp = {'name':'None', 'passwd':'None', 'interface1':'None', 'interface2':'None'}
        self.__status = {'active':False,'text':self._('No active AP'),'button':self._('Connect')}
        self.errorMsg = {'newMsg':False,'title':None, 'text':None}
        self.__statistic = {'startReceived':None,'startSending':None,'receiving':'0', 'totalReceived':'0', 'sending':'0', 'totalSent':'0'}
        #init Thread
        self.interfaceThread = TerminalInterface(self.mysignal,signalNewMsg)
        self.statisticThread = Statistic(self.mysignal,signalUpdateStatistic)
        self.interfaceLock.release()

    def runAp(self):
        if self.__status['active']:
            self.stopAp()
        if self.errorMsg['newMsg']:
            self.reInit()
        self.interfaceLock.acquire()
        if self.__activeAp['name']!='None':
            self.interfaceThread.command = ['create_ap'+' '+self.__activeAp['interface1']+' '+self.__activeAp['interface2']+' '+self.__activeAp['name']+' '+self.__activeAp['passwd']]
            self.interfaceThread.start()
            self.__status['text'] = self._('Creating AP...')
            self.__status['button'] = self._('Disconnect')
            self.__status['active'] = True
        self.interfaceLock.release()
        self.runStatistic()
        self.updatingStatus()

    def stopAp(self):
        self.interfaceThread.stop()
        self.stopStatistic()
        self.reInit()
       # self.updatingStatus()

    def newCmdMsg(self, signal=None):
        self.interfaceLock.acquire()
        msg = self.interfaceThread.read()
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
     #   else:
      #      self.interfaceLock.release()
       #     return

        self.interfaceLock.release()
        self.updatingStatus()

    def runStatistic(self):
        if self.__status['active']:
            self.statisticThread.command = ['ifconfig'+' '+self.__activeAp['interface1']]
            self.statisticThread.start()

    def updateStatistic(self, signal=None):
        msg = self.statisticThread.read()
        if 'error' in msg:
            self.stopStatistic()
            #todo some error msg
        else:
            if 'RX' in msg and 'bytes' in msg:
                self.statisticLock.acquire()
                line = re.search(regexRX, msg).group(0)
                line = re.sub(regexBrackets,'\\1', line)
                self.__statistic['totalReceived'] = line
                self.statisticLock.release()
            if 'TX' in msg and 'bytes' in msg:
                self.statisticLock.acquire()
                line = re.search(regexTX, msg).group(0)
                line = re.sub(regexBrackets,'\\1', line)
                self.__statistic['totalSent'] = line
                self.statisticLock.release()
            self.updatingStatus()

    def stopStatistic(self):
        self.statisticThread.stop()

    def updatingStatus(self):
        if self.updatingPage['statusWindow']:
            self.updatingPage['statusWindow']()
        elif self.updatingPage['tray']:
             self.updatingPage['tray']()

    def registerPage(self, page):
        self.updatingPage['statusWindow'] = page
        self.runStatistic()

    def unregisterPage(self):
        self.updatingPage['statusWindow'] = None
        self.stopStatistic()

    @property
    def activeAp(self):
        return self.__activeAp

    @activeAp.setter
    def activeAp(self, data):
        self.__activeAp['name'] = data[0]
        self.__activeAp['passwd'] = data[1]
        if data[2] != None:
            self.__activeAp['interface1'] = data[2]
        else:
            self.__activeAp['interface1'] = ''
        if data[3] != None:
            self.__activeAp['interface2'] = data[3]
        else:
            self.__activeAp['interface2'] = ''

    @property
    def status(self):
        self.interfaceLock.acquire()
        value = self.__status
        self.interfaceLock.release()
        return value

    @status.setter
    def status(self, data):
        pass

    @property
    def totalReceived(self):
        return self.__statistic['totalReceived']

    @property
    def receiving(self):
        return self.__statistic['receiving']

    @property
    def sending(self):
        return self.__statistic['sending']

    @property
    def totalSent(self):
        return self.__statistic['totalSent']




