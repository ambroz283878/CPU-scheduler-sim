from queues import Queue, fcfsQueue, lcfsQueue, waitingQueue
from process import Process

class CPU():
    def __init__(self, dispatcher: Dispatcher):
        self.currentProcess : Process = None
        self.timeRemaining = 0
        self.dispatcher = dispatcher
    def advanceTime(self):
        pass
    def run(self):
        if self.currentProcess != None:
            self.currentProcess.updateRemainingCPUTime()
            if self.currentProcess.remainingCPUTBurstTime == 0:
                self.dispatcher.addWaiting(self.currentProcess)
                self.currentProcess = None
            return 0
        try:
            self.currentProcess = self.dispatcher.readyQueue[0]
            print(f"PROCESS LOADED\n    PID: {self.currentProcess.PID}")
        except IndexError:
            print("CPU IDLE")
        return 0

class Dispatcher():
    def __init__(self, schedulingAlgorithm):
        self.waiting = waitingQueue()
        match schedulingAlgorithm:
            case "fcfs":
                self.readyQueue = fcfsQueue()
            case "lcfs":
                self.readyQueue = lcfsQueue()
    
    def addWaiting(self, proc):
        self.waiting.addElement(self.waiting.length, proc)

    def dispatch(self):
        for proc in self.waiting:
            proc.updateRemainingIOTime()
            if proc.remainingIOBurstTime == 0:
                proc.ioBurstID += 1
                proc.cpuBurstID += 1
                self.readyQueue.addElement(proc)