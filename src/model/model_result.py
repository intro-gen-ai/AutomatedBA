class ModelResult:
    def __init__(self, execution_time=None, code=None, message=None, confidence=None, log=None):
        self.execution_time = execution_time
        self.code = code
        self.message = message
        self.confidence = confidence
        self.log = log
    
    @classmethod
    def empty(cls):
        return cls()