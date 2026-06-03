from cpu import CPU, rrCPU, Dispatcher
from process import Process
import json

scheduler = input("Select scheduling algorithm (fcfs/lcfs/rr): ")
if scheduler not in ["fcfs", "lcfs", "rr"]:
    raise ValueError(f"Provided algorithm '{scheduler}' is not supported or is invalid.")

with open("procData.json", "r") as f:
    procData = json.load(f)

dispatcher = Dispatcher(scheduler)
if scheduler == "rr":
    cpu = rrCPU(dispatcher, 50)
else: 
    cpu = CPU(Dispatcher)

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