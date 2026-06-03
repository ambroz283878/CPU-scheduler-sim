import json
from process import Process, processNamePool
import random

nProc = 10
with open("runData.json", "r") as file:
    try:
        assignedPIDs = json.load(file)["usedPID"]
    except json.decoder.JSONDecodeError:
        assignedPIDs = []
    
processes = {}

def distribution(param: tuple = (40, 15), low_cutoff:int = 20):
    avg = param[0]
    sigma = param[1]
    x = int(random.normalvariate(avg,sigma))
    if x < low_cutoff:
        x += abs(x - avg)
    return x

def makeProcess():
    numOfCPUBursts = random.randint(8,20)
    cpuBursts = [distribution()]
    ioBursts = []
    for i in range(numOfCPUBursts):
        cpuBursts.append(distribution())
        ioBursts.append(distribution((80,30),40))
    
    pid = random.randint(100,1000)
    while pid in assignedPIDs:
        pid = random.randint(100,1000)
    assignedPIDs.append(pid)
    with open("runData.json", "w") as f:
        json.dump({"usedPID":assignedPIDs}, f)
    proc = Process(pid,processNamePool[random.randint(0,len(processNamePool)-1)], cpuBursts, ioBursts)
    processes[pid] = proc

for i in range(nProc):
    makeProcess()

with open("procData.json", "w") as f:
    json.dump({pid: processes[pid].jsonFormat() for pid in processes}, f, indent=4)