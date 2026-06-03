from cpu import CPU, Dispatcher
from process import Process
import json

with open("procData.json", "r") as f:
    procData = json.load(f)

dispatcher = Dispatcher("fcfs")
cpu = CPU(dispatcher)

processes = {}

for i in procData:
    proc = procData[i]
    processes.update({proc["PID"]:Process(proc["PID"], proc["name"], proc["cpuBursts"], proc["ioBursts"])})
    print(processes[proc["PID"]].processStats())

for i in processes:
    dispatcher.addReady(processes[i])

while (dispatcher.readyQueue.len()+dispatcher.waiting.len() > 0 or cpu.currentProcess != None):
    dispatcher.dispatch()
    cpu.run()

dispatcher.qStatus()  
for i in dispatcher.terminated.elements:
    print(i.processStats())