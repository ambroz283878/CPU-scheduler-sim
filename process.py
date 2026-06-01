processNamePool = ["firefox", "terminal", "vscode", "discord", "tailscale", "virtualbox",
"openssh", "nginx", "docker", "postgresql"]
class Process():
    def __init__(self,PID, name, cpuBursts, ioBursts):
        self.PID = PID
        self.name = name
        self.cpuBursts = cpuBursts
        self.ioBursts = ioBursts
        self.cpuBurstID = 0
        self.ioBurstID = 0
    def setPID(self, pid):
        self.pid = pid
    def nextCPUBurst(self):
        return self.cpuBursts[self.cpuBurstID]
    def nextIOBurst(self):
        return self.ioBursts[self.ioBurstID]
    def processStats(self):
        return f"""---------
Process stats:
    PID: {self.PID}
    name: {self.name}
    CPU Bursts: {self.cpuBursts}
        Total CPU time: {sum(self.cpuBursts)}
    IO Bursts: {self.ioBursts}
        Total IO wait time: {sum(self.ioBursts)}
---------
"""
    def jsonFormat(self):
        return {
            "PID":self.PID,
            "name":self.name,
            "cpuBursts":self.cpuBursts,
            "ioBursts":self.ioBursts
        }