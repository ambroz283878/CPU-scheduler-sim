from process import Process
class Queue():
    def __init__(self):
        self.elements = []
        self.length = 0
    
    def listQueue(self):
        lst = []
        for i in self.elements:
            lst.append(i.PID)
        return lst

    def removeElement(self, elem):
        self.length -= 1
        self.elements.remove(elem)
    def addElement(self, pos: int, element: Process):
        self.elements.insert(pos, element)
        self.length += 1

class FcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(self.length, element)

class LcfsQueue(Queue):
    def __init__(self):
        super().__init__()
    def addElement(self, element: Process):
        super().addElement(0, element)
