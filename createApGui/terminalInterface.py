import subprocess
import threading
import os
import signal

class TerminalInterface(threading.Thread):
    def __init__(self, mySignal, signalMsg):
        threading.Thread.__init__(self)
        self.signalMsg = signalMsg
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
            import time
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
            self.mySignal.emit(self.signalMsg)

    def stop(self):
        if self.p1 != None:
            os.kill(self.p1.pid, signal.SIGINT)
            self.p1 = None

