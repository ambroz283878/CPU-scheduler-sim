from cpu import CPU, Dispatcher
from process import Process, processNamePool
import json

with open("procData.json", "r") as f:
    processes = json.load(f)

dispatcher = Dispatcher("fcfs")
cpu = CPU(dispatcher)

for i in processes:
    proc = processes[i]
    processes[i] = Process(proc["PID"], proc["name"], proc["cpuBursts"], proc["ioBursts"])
    print(processes[i].processStats())
