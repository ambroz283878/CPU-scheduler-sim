from queues import Queue, fcfsQueue, lcfsQueue, waitingQueue

class CPU():
    def __init__(self, schedulingAlgorithm):
        self.currentProcess = None
        self.timeRemaining = 0
        self.waiting = waitingQueue()
        match schedulingAlgorithm:
            case "fcfs":
                self.readyQueue = fcfsQueue()
            case "lcfs":
                self.readyQueue = lcfsQueue()
        
    def dispatcher(self):
        self.currentProcess
    def advanceTime(self):
        if self.currentProcess == None:
            self.currentProcess = self.readyQueue.advanceElement()