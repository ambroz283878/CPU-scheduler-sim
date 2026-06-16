import json
from cpu import Process, processNamePool
import random
import matplotlib.pyplot as plt
from collections import Counter

nIOBound = 100
ioBoundDist = [(40,10), 20]
ioBoundDist2 = [(90,30),40]
nCPUBound = 50
cpuBoundDist = [(80,15), 40]
cpuBoundDist2 = [(40,15), 30]
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

def makeProcess(cpuDist: list[tuple,str],ioDist: list[tuple,str]):
    numOfCPUBursts = random.randint(8,20)
    cpuBursts = [distribution(cpuDist[0], cpuDist[1])]
    ioBursts = []
    for i in range(numOfCPUBursts):
        cpuBursts.append(distribution(cpuDist[0], cpuDist[1]))
        ioBursts.append(distribution(ioDist[0],ioDist[1]))
    
    pid = random.randint(100,1000)
    while pid in assignedPIDs:
        pid = random.randint(100,1000)
    assignedPIDs.append(pid)
    with open("runData.json", "w") as f:
        json.dump({"usedPID":assignedPIDs}, f)
    proc = Process(pid,processNamePool[random.randint(0,len(processNamePool)-1)], cpuBursts, ioBursts)
    processes[pid] = proc

for i in range(nCPUBound):
    makeProcess(cpuBoundDist, cpuBoundDist2)
for i in range(nIOBound):
    makeProcess(ioBoundDist, ioBoundDist2)

data = []
for i in processes.values():
    for j in i.cpuBursts:
        data.append(j)

c = Counter(data)
labels = list(c.keys())
values = list(c.values())
plt.bar(labels,values)
plt.xlabel("Długość serii")
plt.ylabel("Liczba wystąpień")

plt.show()
with open("procData.json", "w") as f:
    json.dump({pid: processes[pid].jsonFormat() for pid in processes}, f, indent=4)