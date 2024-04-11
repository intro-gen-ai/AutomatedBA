from src.step import Step
from abc import ABC, abstractmethod

from src.step import Step
from src.util import SnowflakeManager

class BaseSemantics(Step):
    def __init__(self, args=None):
        if args is None:
            args = dict()  # Ensure args is a set, even if None is passed
        size = args.pop('size', 0)
        self.order = -1
        self.args = args
        a = SnowflakeManager()
        self.schema = a.get_schema()
    
    def getRequirements(self):
        return None

