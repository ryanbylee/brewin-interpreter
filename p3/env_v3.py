# The EnvironmentManager class keeps a mapping between each variable name (aka symbol)
# in a brewin program and the Value object, which stores a type, and a value.
class EnvironmentManager:
    def __init__(self):
        self.environment = [{}]
        self.ref_environment = [{}]

    # returns a VariableDef object
    def get(self, symbol):
        for env in reversed(self.environment):
            if symbol in env:
                return env[symbol]

        return None

    def get_ref(self, local):
        if local in self.ref_environment[-1]:
            return self.ref_environment[-1][local]
        
        return None

    def set(self, symbol, value):
        for env in reversed(self.environment):
            if symbol in env:
                env[symbol] = value
                return

        # symbol not found anywhere in the environment
        self.environment[-1][symbol] = value

    def ref_set(self, local, value):
        if local in self.ref_environment[-1]: 
            self.environment[-3][self.get_ref(local)] = value
            return
    # create a new symbol in the top-most environment, regardless of whether that symbol exists
    # in a lower environment
    def create(self, symbol, value):
        self.environment[-1][symbol] = value

    def ref_create(self, local, ref):
        self.ref_environment[-1][local] = ref
    # used when we enter a nested block to create a new environment for that block
    def push(self):
        self.environment.append({})  # [{}] -> [{}, {}]

    # used when we exit a nested block to discard the environment for that block
    def pop(self):
        self.environment.pop()

    def ref_push(self):
        self.ref_environment.append({})
    
    def ref_pop(self):
        self.ref_environment.pop()