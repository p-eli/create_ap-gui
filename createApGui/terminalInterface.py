import subprocess
import threading
import os
import signal
import time
class TerminalInterface(threading.Thread):
    def __init__(self, mySignal, signalName):
        threading.Thread.__init__(self)
        self.signalName = signalName
        self.mySignal = mySignal
        self.output = ''
        self.p1 = None
        self.lock = threading.Lock()
        self.command = []

    def run(self):
        self.bashCommunicate()
        self.lock.acquire()
        if self.output != '':
            self.lock.release()
            time.sleep(0.3)

    def read(self):
        self.lock.acquire()
        output = self.output
        self.output = ''
        self.lock.release()
        return output

    def bashCommunicate(self):
        self.p1 = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        for line in self.p1.stdout:
            self.lock.acquire()
            self.output = self.output+'\n'+line.rstrip().decode('utf-8')
            self.lock.release()
            self.mySignal.emit(self.signalName)

    def stop(self):
        if self.p1 != None:
            os.kill(self.p1.pid, signal.SIGINT)
            self.p1 = None



class Statistic(threading.Thread):
    def __init__(self, mySignal, signalName):
        threading.Thread.__init__(self)
        self.__mySignal = mySignal
        self.__signalName = signalName
        self.__running = True
        self.command = ''
        self.__output = []
        self.__lock = threading.Lock()

    def read(self):
        self.__lock.acquire()
        if self.__output != '':
            output = self.__output[0].decode('utf-8')
        else:
            output = ''
        self.__output = ''
        self.__lock.release()
        return output

    def run(self):
        while self.__running:
            p = subprocess.Popen(self.command, stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
            self.__lock.acquire()
            try:
                self.__output = p.communicate()
            except:
                self.__output = ''
            finally:
                self.__lock.release()
                self.__mySignal.emit(self.__signalName)
                time.sleep(2)

    def stop(self):
        self.__running = False

