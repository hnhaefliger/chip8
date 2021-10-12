class RAM:
    memory = [0x00 for i in range(4096)]

    def read(self, addr):
        return self.memory[addr]

    def write(self, addr, value):
        self.memory[addr] = value