class NoVarException(Exception):
    pass

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.var_dict = {}

    def has_key(self, name):  # variable name
        return name in self.var_dict

    def get(self, name):         # gets from memory current value of variable <name>
        return self.var_dict[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.var_dict[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.mem_stack = []
        self.size = 0
        if memory:  
            self.mem_stack.append(memory)
            self.size += 1          # = len(self.mem_stack)

    def get(self, name):             # gets from memory stack current value of variable <name>
        mem_stack_it = self.size - 1
        while mem_stack_it >= 0:
            if self.mem_stack[mem_stack_it].has_key(name):
                return self.mem_stack[mem_stack_it].get(name)
            mem_stack_it -= 1
        raise NoVarException(f"No variable {name} in scope!")

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.mem_stack[self.size - 1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        mem_stack_it = self.size - 1
        while mem_stack_it >= 0:
            if self.mem_stack[mem_stack_it].has_key(name):
                self.mem_stack[mem_stack_it].put(name, value)
            mem_stack_it -= 1
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.mem_stack.append(memory)
        self.size += 1

    def pop(self):          # pops the top memory from the stack
        if self.size <= 0:
            raise Exception("Cannot pop from empty memory stack!")
        self.mem_stack.pop()
        self.size -= 1

