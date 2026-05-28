import json
from process import Process
import random

def makeProcess():
    numOfCPUBursts = random.randint(5,15)
    cpuBursts = [random.randint(15,40)]
    ioBursts = []
    for i in range(numOfCPUBursts):
        cpuBursts.append(random.randint(15,55))
        ioBursts.append(random.randint(30,90))

    proc = Process("firefox", cpuBursts, ioBursts)

    print(proc.processStats())

makeProcess()