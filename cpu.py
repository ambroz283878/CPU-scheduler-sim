from queues import Queue, FcfsQueue, LcfsQueue
from process import Process

class CPU():
    def __init__(self, dispatcher: Dispatcher):
        self.currentProcess : Process = None
        self.timeRemaining = 0
        self.dispatcher = dispatcher

    def run(self):
        if self.currentProcess != None:
            self.currentProcess.updateRemainingCPUTime()
            if self.currentProcess.remainingCPUBurstTime == 0:
                if (self.currentProcess.cpuBurstID+1 == len(self.currentProcess.cpuBursts)):
                    self.dispatcher.addTerminated(self.currentProcess)
                else:
                    self.dispatcher.addWaiting(self.currentProcess)
                self.currentProcess = None
            return 0
        try:
            self.currentProcess = self.dispatcher.execReady()
            print(f"PROCESS LOADED\n    PID: {self.currentProcess.PID}")
        except IndexError:
            print("CPU IDLE")
        return 0

class rrCPU(CPU):
    def __init__(self, dispatcher: Dispatcher, quantum: int):
        super().__init__(dispatcher)
        self.quantum = quantum
        self.timeRemaining = quantum

    def run(self):
        if self.currentProcess != None:
            self.currentProcess.updateRemainingCPUTime()
            if self.currentProcess.remainingCPUBurstTime == 0:
                if (self.currentProcess.cpuBurstID+1 == len(self.currentProcess.cpuBursts)):
                    self.dispatcher.addTerminated(self.currentProcess)
                else:
                    self.dispatcher.addWaiting(self.currentProcess)
                self.currentProcess = None
            elif self.timeRemaining == 0:
                self.dispatcher.addReady(self.currentProcess)
                self.currentProcess = None
                self.timeRemaining = self.quantum
            return 0
        try:
            self.currentProcess = self.dispatcher.execReady()
            print(f"PROCESS LOADED\n    PID: {self.currentProcess.PID}")
        except IndexError:
            print("CPU IDLE")
        return 0

class Dispatcher():
    def __init__(self, schedulingAlgorithm: str):
        self.waiting = Queue()
        self.terminated = Queue()
        self.algorithm = schedulingAlgorithm
        match self.algorithm:
            case "fcfs":
                self.readyQueue = FcfsQueue()
            case "lcfs":
                self.readyQueue = LcfsQueue()
            case "sjf":
                pass
            case "rr":
                self.readyQueue = FcfsQueue()
            case _:
                raise ValueError(f"Provided algorithm '{self.algorithm}' is not supported or is invalid.")
    
    def addTerminated(self, proc: Process):
        self.terminated.addElement(self.terminated.len(), proc)

    def addWaiting(self, proc: Process):
        self.waiting.addElement(self.waiting.len(), proc)

    def addReady(self, proc: Process):
        self.readyQueue.addElement(proc)

    def execReady(self):
        return self.readyQueue.removeElement(0)

    def qStatus(self):
        print(f"""
DISPATCHER STATUS:
    Terminated processes (n {self.terminated.len()}):
        {self.terminated.listQueue()}
    Waiting processes (n: {self.waiting.len()}):
        {self.waiting.listQueue()}
    Ready processes (n: {self.readyQueue.len()}):
        {self.readyQueue.listQueue()}
""")

    def dispatch(self):
        for proc in self.waiting.elements:
            proc.updateRemainingIOTime()
            if proc.remainingIOBurstTime == 0:
                proc.nextCPUBurst()
                proc.nextIOBurst()
                self.readyQueue.addElement(proc)
                self.waiting.removeElement(self.waiting.elements.index(proc))
        for proc in self.readyQueue.elements:
            proc.updateReadyWaitTime()