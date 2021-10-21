from .display import Display
import random
import threading
import time

class Chip8:
    # CPU
    memory = [0x0 for i in range(4 * 1024)]
    sprites = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,
        0x20, 0x60, 0x20, 0x20, 0x70,
        0xF0, 0x10, 0xF0, 0x80, 0xF0,
        0xF0, 0x10, 0xF0, 0x10, 0xF0,
        0x90, 0x90, 0xF0, 0x10, 0x10,
        0xF0, 0x80, 0xF0, 0x10, 0xF0,
        0xF0, 0x80, 0xF0, 0x90, 0xF0,
        0xF0, 0x10, 0x20, 0x40, 0x40,
        0xF0, 0x90, 0xF0, 0x90, 0xF0,
        0xF0, 0x90, 0xF0, 0x10, 0xF0,
        0xF0, 0x90, 0xF0, 0x90, 0x90,
        0xE0, 0x90, 0xE0, 0x90, 0xE0,
        0xF0, 0x80, 0x80, 0x80, 0xF0,
        0xE0, 0x90, 0x90, 0x90, 0xE0,
        0xF0, 0x80, 0xF0, 0x80, 0xF0,
        0xF0, 0x80, 0xF0, 0x80, 0x80
    ]

    for i in range(len(sprites)):
        memory[i] = sprites[i]

    V = [0x0 for i in range(17)]
    index = 0x0
    pc = 0x0200
    stack = []
    sp = 0x0
    delay_timer = 0
    sound_timer = 0

    # Keyboard
    key = 0

    # Display
    display = Display()

    # Other
    paused = False
    speed = 0.0001

    def __init__(self, rom):
        with open(rom, 'rb') as f:
            for i, byte in enumerate(f.read()):
                self.memory[i + 0x200] = byte

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()
        self.display.mainloop()
        self.display.root.mainloop()

    def run(self):
        while True:
            self.cycle()
            time.sleep(self.speed)

    def cycle(self):
        op_code = (self.memory[self.pc] << 8) | self.memory[self.pc+1]
        #print(hex(op_code))
        x = (0x0F00 & op_code) >> 8
        y = (0x00F0 & op_code) >> 4
        self.pc += 2

        if (0xF000 & op_code) == 0x0000:
            if (0xFFFF & op_code) == 0x00E0:
                self.display.clear()

            elif (0xFFFF & op_code) == 0x00EE:
                self.stack.pop(-1)

            else:
                pass

        elif (0xF000 & op_code) == 0x1000:
            self.pc = (0x0FFF & op_code)

        elif (0xF000 & op_code) == 0x2000:
            self.stack.append(self.pc)
            self.pc = (0x0FFF & op_code)

        elif (0xF000 & op_code) == 0x3000:
            if self.V[x] == (0x00FF & op_code):
                self.pc += 2

        elif (0xF000 & op_code) == 0x4000:
            if self.V[x] != (0x00FF & op_code):
                self.pc += 2

        elif (0xF00F & op_code) == 0x5000:
            if self.V[x] == self.V[y]:
                self.pc += 2

        elif (0xF000 & op_code) == 0x6000:
            self.V[x] = (0x00FF & op_code)

        elif (0xF000 & op_code) == 0x7000:
            self.V[x] += (0x00FF & op_code)

        elif (0xF000 & op_code) == 0x8000:
            if (0x000F & op_code) == 0x0000:
                self.V[x] = self.V[y]

            elif (0x000F & op_code) == 0x0001:
                self.V[x] |= self.V[y]

            elif (0x000F & op_code) == 0x0002:
                self.V[x] &= self.V[y]

            elif (0x000F & op_code) == 0x0003:
                self.V[x] ^= self.V[y]

            elif (0x000F & op_code) == 0x0004:
                sum = self.V[x] + self.V[y]
                
                self.V[0xF] = 0

                if sum > 0xFF:
                    self.V[0xF] = 1

                self.V[x] = sum & 0xFF

            elif (0x000F & op_code) == 0x0005:
                sub = self.V[x] - self.V[y]

                self.V[0xF] = 0

                if sub > 0:
                    self.V[0xF] = 1

                self.V[x] = sub & 0xFF

            elif (0x000F & op_code) == 0x0006:
                self.V[0xF] = self.V[x] & 0x1
                self.V[x] >>= 1

            elif (0x000F & op_code) == 0x000E:
                self.V[0xF] = (self.V[x] & 0x80)
                self.V[x] <<= 1
                self.V[x] &= 0x00FF

        elif (0xF000 & op_code) == 0x9000:
            if self.V[x] != self.V[y]:
                self.pc += 2

        elif (0xF000 & op_code) == 0xA000:
            self.index = (op_code & 0x0FFF)

        elif (0xF000 & op_code) == 0xB000:
            self.pc = self.V[0] + (op_code & 0x0FFF)

        elif (0xF000 & op_code) == 0xC000:
            self.V[x] = (random.randint(0, 255) & (op_code & 0x00FF))

        elif (0xF000 & op_code) == 0xD000:
            # DRW Vx, Vy, nibble 
            width = 8
            height = op_code & 0x000F
            self.V[0xF] = 0

            for row in range(height):
                sprite = self.memory[self.index + row]

                for col in range(width):
                    if (sprite & (0b10000000 >> col)) > 0:
                        if self.display.set_pixel(self.V[x] + col, self.V[y] + row):
                            self.V[0xF] = 1

        elif (0xF000 & op_code) == 0xE000:
            if (0x00FF & op_code) == 0x009E:
                if self.key == self.V[x]:
                    self.pc += 2

            elif (0x00FF & op_code) == 0x00A1:
                if self.key != self.V[x]:
                    self.pc += 2

        elif (0xF000 & op_code) == 0xF000:
            if (0x00FF & op_code) == 0x0007:
                self.V[x] = self.delay_timer

            elif (0x00FF & op_code) == 0x000A:
                self.paused = True

            elif (0x00FF & op_code) == 0x0015:
                self.delay_timer = self.V[x]

            elif (0x00FF & op_code) == 0x0018:
                self.sound_timer = self.V[x]

            elif (0x00FF & op_code) == 0x001E:
                self.index += self.V[x]

            elif (0x00FF & op_code) == 0x0029:
                self.index += self.V[x] * 5

            elif (0x00FF & op_code) == 0x0033:
                self.memory[self.index] = int(self.V[x] / 100)
                self.memory[self.index + 1] = int((self.V[x] % 100)/10)
                self.memory[self.index + 2] = int(self.V[x] % 10)

            elif (0x00FF & op_code) == 0x0055:
                for ri in range(x+1):
                    self.memory[self.index + ri] = self.V[ri]

            elif (0x00FF & op_code) == 0x0065:
                for ri in range(x+1):
                    self.V[ri] = self.memory[self.index + ri]

        if not(self.paused):
            if self.delay_timer > 0:
                self.delay_timer -= 1

            if self.sound_timer > 0:
                self.sound_timer -= 1