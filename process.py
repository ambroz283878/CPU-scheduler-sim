class Process():
    def __init__(self, name, cpuBursts, ioBursts):
        self.name = name
        self.cpuBursts = cpuBursts
        self.ioBursts = ioBursts
        self.cpuBurstID = 0
        self.ioBurstID = 0
    def nextCPUBurst(self):
        return self.cpuBursts[self.cpuBurstID]
    def nextIOBurst(self):
        return self.ioBursts[self.ioBurstID]
    def processStats(self):
        return f"""---------
Process stats:
    name: {self.name}
    CPU Bursts: {self.cpuBursts}
        Total CPU time: {sum(self.cpuBursts)}
    IO Bursts: {self.ioBursts}
        Total IO wait time: {sum(self.ioBursts)}
---------
"""
    def jsonFormat(self):
        return {
            "name":self.name,
            "cpuBursts":self.cpuBursts,
            "ioBursts":self.ioBursts
        }