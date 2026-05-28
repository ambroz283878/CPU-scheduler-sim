class Queue():
    def __init__(self):
        self.elements = []
    def advanceElement(self):
        return self.elements.pop(0)
    def addElement(self, element):
        self.elements.insert(len(self.elements),element)

   