processNamePool = ["firefox", "terminal", "vscode", "discord", "tailscale", "virtualbox",
"openssh", "nginx", "docker", "postgresql"]
class Process():
    def __init__(self,PID: int, name: str, cpuBursts: list, ioBursts: list):
        self.PID = PID
        self.name = name
        self.cpuBursts = cpuBursts
        self.ioBursts = ioBursts
        self.cpuBurstID = 0
        self.ioBurstID = 0
        self.readyWaitTime = 0
        self.remainingCPUBurstTime = self.cpuBursts[self.cpuBurstID]
        self.remainingIOBurstTime = self.ioBursts[self.ioBurstID]

    def updateRemainingCPUTime(self):
        self.remainingCPUBurstTime -= 1
    def updateRemainingIOTime(self):
        self.remainingIOBurstTime -= 1
    def updateReadyWaitTime(self):
        self.readyWaitTime += 1

    def setPID(self, pid):
        self.pid = pid
    def nextCPUBurst(self):
        self.cpuBurstID += 1
        self.remainingCPUBurstTime = self.cpuBursts[self.cpuBurstID]
        return self.remainingCPUBurstTime
    def nextIOBurst(self):
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
---------
"""
    def jsonFormat(self):
        return {
            "PID":self.PID,
            "name":self.name,
            "cpuBursts":self.cpuBursts,
            "ioBursts":self.ioBursts
        }