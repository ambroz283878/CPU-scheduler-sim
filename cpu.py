processNamePool = ["firefox", "terminal", "vscode", "discord", "tailscale", "virtualbox",
"openssh", "nginx", "docker", "postgresql"]
class Process():
    def __init__(self,PID: int, name: str, cpuBursts: list, ioBursts: list):
        self.PID = PID
        self.name = name
        self.cpuBursts = cpuBursts # array with lengths of process' cpu bursts
        self.ioBursts = ioBursts # array with lengths of process' io bursts
        self.cpuBurstID = 0 # current cpu burst index
        self.ioBurstID = 0 # current io burst index
        self.readyWaitTime = 0 # time spent waiting in ready queue
        self.responseTime = [0]*len(self.cpuBursts)
        self.remainingCPUBurstTime = self.cpuBursts[self.cpuBurstID] # time remaining in current cpu burst
        self.remainingIOBurstTime = self.ioBursts[self.ioBurstID] # time remaining in current io burst
        self.interrupted=False
    def interrupt(self):
        self.interrupted=True
    def updateRemainingCPUTime(self):
        self.remainingCPUBurstTime -= 1
    def updateRemainingIOTime(self):
        self.remainingIOBurstTime -= 1
    def updateReadyWaitTime(self):
        self.readyWaitTime += 1
    def updateBurstWaitTime(self):
        self.responseTime[self.cpuBurstID] += 1
    def setPID(self, pid):
        self.pid = pid
    def nextCPUBurst(self): # move to next cpu burst
        self.cpuBurstID += 1
        self.remainingCPUBurstTime = self.cpuBursts[self.cpuBurstID]
        self.interrupted=False
        return self.remainingCPUBurstTime
    def nextIOBurst(self): # move to next io burst
        self.ioBurstID += 1
        try:
            self.remainingIOBurstTime = self.ioBursts[self.ioBurstID]
            return self.remainingIOBurstTime
        except IndexError:
            return None
    def processStats(self):
        return f"""---------
Process stats:
    PID: {self.PID}
    name: {self.name}
    CPU Bursts: {self.cpuBursts}
        Total CPU time: {sum(self.cpuBursts)}
    IO Bursts: {self.ioBursts}
        Total IO wait time: {sum(self.ioBursts)}
    Minimal execution time: {sum(self.cpuBursts)+sum(self.ioBursts)}
    Observed execution time: {self.readyWaitTime}
    Average response time: {sum(self.responseTime)/len(self.responseTime)}
---------
"""
    def jsonFormat(self): # process info in JSON format
        return {
            "PID":self.PID,
            "name":self.name,
            "cpuBursts":self.cpuBursts,
            "ioBursts":self.ioBursts,
            "avgBurstWaitTime":sum(self.responseTime)/len(self.responseTime)
        }

class Queue():
    def __init__(self):
        self.elements = []
    
    def listQueue(self):
        lst = []
        for i in self.elements:
            lst.append(i.PID)
        return lst

    def len(self):
        return len(self.elements)

    def removeElement(self, pos: int):
        return self.elements.pop(pos)
    def addElement(self, pos: int, element: Process):
        self.elements.insert(pos, element)

class FcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process): # add element at the end of array of processes
        super().addElement(self.len(), element)

class LcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process): # add element at the beggining of array of processes
        super().addElement(0, element)

class CPU(): # standard CPU
    def __init__(self, dispatcher: Dispatcher):
        self.currentProcess : Process = None # address register (program counter)
        self.timeRemaining = 0 # time remaining in current burst
        self.dispatcher = dispatcher
        self.totalCPUtime = 0 # CPU time counter
        self.idleTime = 0
        self.completedProcesses = 0 # completed processes counter

    def run(self): # every tick:
        self.totalCPUtime +=1
        if self.currentProcess != None: # if there is a process in address register - keep executing and check remaining burst time
            self.currentProcess.updateRemainingCPUTime()
            if self.currentProcess.remainingCPUBurstTime == 0: # if finished burst:
                if (self.currentProcess.cpuBurstID+1 == len(self.currentProcess.cpuBursts)): # if process finished execution, add it to terminated processes list
                    self.dispatcher.addTerminated(self.currentProcess)
                    self.completedProcesses += 1
                else: # tell the process to move to next burst and add it to waiting queue
                    self.dispatcher.addWaiting(self.currentProcess)
                self.currentProcess = None
            else:
                return 0
        try: # if register is empty - load process from ready queue
            self.currentProcess = self.dispatcher.execReady()
            print(f"PROCESS LOADED\n    PID: {self.currentProcess.PID}")
        except IndexError: # except when ready queue is empty:
            self.idleTime+=1
            print("CPU IDLE")
        return 0
    def cpuStats(self):
        waiting = 0.
        responseTime = 0.
        for proc in self.dispatcher.terminated.elements:
            waiting += proc.readyWaitTime
            responseTime += sum(proc.responseTime)/len(proc.responseTime)
        print(f"""CPU STATS:
    {self.completedProcesses} processes completed in {self.totalCPUtime} ms CPU time
    Idle time: {self.idleTime}
    Average total ready wait time: {waiting/self.completedProcesses}
    Average response time: {responseTime/self.completedProcesses}
    Throughput (proc/1000ms): {1000*(self.completedProcesses/self.totalCPUtime)}
    """)

class rrCPU(CPU): #Round Robin CPU
    def __init__(self, dispatcher: Dispatcher, quantum: int):
        super().__init__(dispatcher)
        self.interruptionCount = 0
        self.quantum = quantum
        self.timeRemaining = quantum

    def run(self): # every tick:
        self.totalCPUtime +=1
        if self.currentProcess != None: # if there is a process in address register - keep executing and check remaining burst time
            self.currentProcess.updateRemainingCPUTime()
            self.timeRemaining -= 1
            if self.currentProcess.remainingCPUBurstTime == 0: # if process finished burst faster than time quantum:
                if (self.currentProcess.cpuBurstID+1 == len(self.currentProcess.cpuBursts)): # if process finished execution, add it to terminated processes list
                    self.dispatcher.addTerminated(self.currentProcess)
                    self.completedProcesses += 1
                else: # tell the process to move to next burst and add it to waiting queue
                    self.dispatcher.addWaiting(self.currentProcess)
                self.timeRemaining = self.quantum # reset remaining RR time to time quantum
                self.currentProcess = None # remove process from registry
                return 0
            elif self.timeRemaining == 0: # if RR time is up:
                self.currentProcess.interrupt()
                self.dispatcher.addReady(self.currentProcess) # add interrupted process to ready queue
                self.currentProcess = None  # remove process from registry
                self.interruptionCount +=1 # register RR interuption
                self.timeRemaining = self.quantum # reset remaining RR time to time quantum
            return 0
        try:
            self.currentProcess = self.dispatcher.execReady()
            print(f"PROCESS LOADED\n    PID: {self.currentProcess.PID}")
        except IndexError:
            print("CPU IDLE")
            self.idleTime+=1
        return 0
    def cpuStats(self):
        super().cpuStats()
        print(f"""
    Round Robin time quantum: {self.quantum} ms
    Number of RR interruptions: {self.interruptionCount}""")

class Dispatcher():
    def __init__(self, schedulingAlgorithm: str):
        self.waiting = Queue()
        self.terminated = Queue()
        self.algorithm = schedulingAlgorithm
        match self.algorithm: # create ready queue matching selected algorithm
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
        finished_io = [proc for proc in self.waiting.elements
                   if proc.remainingIOBurstTime <= 1]
        for proc in finished_io:
            proc.updateRemainingIOTime()
            proc.nextCPUBurst() # update CPU burst indicator 
            proc.nextIOBurst() # update IO burst indicator
            self.readyQueue.addElement(proc) # add process to ready queue
            self.waiting.removeElement(self.waiting.elements.index(proc)) # remove process from waiting queue
        for proc in self.waiting.elements:
            proc.updateRemainingIOTime()
        for proc in self.readyQueue.elements:
            proc.updateReadyWaitTime()
            if not proc.interrupted:
                proc.updateBurstWaitTime()