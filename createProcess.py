import json
from cpu import Process, processNamePool
import random

nIOBound = 100
ioBoundDist = [(40,10), 20]
nCPUBound = 50
cpuBoundDist = [(80,15), 40]
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

def makeProcess(dist):
    numOfCPUBursts = random.randint(8,20)
    cpuBursts = [distribution(dist[0], dist[1])]
    ioBursts = []
    for i in range(numOfCPUBursts):
        cpuBursts.append(distribution(dist[0], dist[1]))
        ioBursts.append(distribution((80,30),40))
    
    pid = random.randint(100,1000)
    while pid in assignedPIDs:
        pid = random.randint(100,1000)
    assignedPIDs.append(pid)
    with open("runData.json", "w") as f:
        json.dump({"usedPID":assignedPIDs}, f)
    proc = Process(pid,processNamePool[random.randint(0,len(processNamePool)-1)], cpuBursts, ioBursts)
    processes[pid] = proc

for i in range(nCPUBound):
    makeProcess(cpuBoundDist)
for i in range(nIOBound):
    makeProcess(ioBoundDist)

with open("procData.json", "w") as f:
    json.dump({pid: processes[pid].jsonFormat() for pid in processes}, f, indent=4)