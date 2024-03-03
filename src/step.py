from abc import ABC, abstractmethod

class Step(ABC):
    """
    All steps require an order
    """
    def __init__(self):
        self.order = None
    
    @abstractmethod
    def run(self, args):
        pass

    def getOrder(self):
        if self.order is None:
            raise ValueError("There is not an order defined for this object!")
        return self.order