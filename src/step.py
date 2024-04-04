from abc import ABC, abstractmethod
from src.util import validate_file_exists

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
   
    @abstractmethod
    def getRequirements(self):
        pass

    
    def checkRequirements(self):
        for i in self.getRequirements():
            if not validate_file_exists(self.getRequirements()):
                return False
        return True