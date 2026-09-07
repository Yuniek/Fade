from .errors import FadeRuntimeError

# ##################################
# Environment
# ##################################

class Environment:
    def __init__(self):
        self.environment = {}
    def setVariable(self, var_name:str, var_value:str|int|float|None):
        self.environment[var_name] = var_value
    def getVariable(self, var_name:str):
        if var_name not in self.environment:
            raise FadeRuntimeError(f"Unknown variable {var_name}")
        return self.environment[var_name]