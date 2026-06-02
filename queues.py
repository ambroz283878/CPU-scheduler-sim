from process import Process
class Queue():
    def __init__(self):
        self.elements = []
        self.length = 0
        return self
    def advanceElement(self):
        self.length -= 1
        return self.elements.pop(0)
    def addElement(self, pos: int, element: Process):
        self.elements.insert(pos, element)
        self.length += 1

class fcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(self.length, element)

class lcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(0, element)

class waitingQueue(Queue):
    def __init__(self):
        super().__init__()
    def advanceTime(self):
        readyProcesses = []
        for element in self.elements:
            element.updateIOBurstTime()
            if element.remainingIOBurstTime == 0:
                readyProcesses.append(element)
        return readyProcesses