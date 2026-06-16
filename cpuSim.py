from cpu import CPU, rrCPU, Dispatcher, Process
import json

scheduler = input("Select scheduling algorithm (fcfs/lcfs/rr): ") # choose scheduler
if scheduler not in ["fcfs", "lcfs", "rr"]:
    raise ValueError(f"Provided algorithm '{scheduler}' is not supported or is invalid.")

with open("procData.json", "r") as f: # load process Data form json file
    procData = json.load(f) 

dispatcher = Dispatcher(scheduler) # initialize Dispatcher and CPU
if scheduler == "rr":
    cpu = rrCPU(dispatcher, 60)
else: 
    cpu = CPU(dispatcher)

processes = {}

for i in procData: # map Process object to it's PID
    proc = procData[i]
    processes.update({proc["PID"]:Process(proc["PID"], proc["name"], proc["cpuBursts"], proc["ioBursts"])})
    print(processes[proc["PID"]].processStats())

for i in processes: # add all processes to the ready queue
    dispatcher.addReady(processes[i])

while (dispatcher.readyQueue.len()+dispatcher.waiting.len() > 0 or cpu.currentProcess != None): # do if there are processes in ready and waiting queues or in CPU registry 
    dispatcher.dispatch()
    cpu.run()

#for i in dispatcher.terminated.elements: # display process stats of all terminated processes
#    print(i.processStats())

#dispatcher.qStatus() # display dispatcher stats
cpu.cpuStats() # display cpu stats