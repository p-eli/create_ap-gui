import subprocess
import threading
import os
import signal


class TerminalInterface(threading.Thread):

    def __init__(self, aten=None):
        threading.Thread.__init__(self)
        self.aten = aten
        self.output = ''
        self.errOutput = ''
        self.p1 = None
        self.lock = threading.Lock()
        self.command = []
        self.daemon = True

    def run(self):
        self.bashCommunicate()

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
            if self.aten != None:
                self.aten()

    def bashCommunicate1(self):
        self.p1 = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        for line in self.p1.stdout:
            self.lock.acquire()
            self.output = self.output+'\n'+line.rstrip().decode('utf-8')
            self.lock.release()
            if self.aten != None:
                self.aten()

    def stop(self):
        if self.p1 != None:
            os.kill(self.p1.pid, signal.SIGINT)
            self.p1 = None