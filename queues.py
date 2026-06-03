from process import Process
class Queue():
    def __init__(self):
        self.elements = []
    
    def listQueue(self):
        lst = []
        for i in self.elements:
            lst.append(i.PID)
        return lst

    def len(self):
        return len(self.elements)

    def removeElement(self, pos: int):
        return self.elements.pop(pos)
    def addElement(self, pos: int, element: Process):
        self.elements.insert(pos, element)

class FcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(self.len(), element)

class LcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(0, element)
