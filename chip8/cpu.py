from .ram import RAM
from .display import Display
import random

class CPU:
    op_code = 0x0000
    V = [0x00 for i in range(16)]
    I = 0x000
    PC = 0x200
    stack = [0x000 for i in range(16)]
    SP = 0x0
    key = [0b0 for i in range(16)]

    ram = RAM()
    display = Display()

    delay_timer = 0x0
    sound_timer = 0x0

    def cycle(self):
        op_code = (self.ram.read(self.pc) << 8) | self.ram.read(self.pc+1)
        self.PC += 2

        if (0xF000 & op_code) == 0x0000:
            if (0xFFFF & op_code) == 0x00E0:
                self.display.clear()

            elif (0xFFFF & op_code) == 0x00EE:
                pass ###

            else:
                pass ###

        elif (0xF000 & op_code) == 0x1000:
            self.PC = (0x0FFF & op_code)
            
        elif (0xF000 & op_code) == 0x2000:
            pass ###
            
        elif (0xF000 & op_code) == 0x3000:
            if self.V[(0x0F00 & op_code) >> 8] == (0x00FF & op_code):
                self.PC += 2

        elif (0xF000 & op_code) == 0x4000:
            if self.V[(0x0F00 & op_code) >> 8] != (0x00FF & op_code):
                self.PC += 2

        elif (0xF00F & op_code) == 0x5000:
            if self.V[(0x0F00 & op_code) >> 8] == self.V[(0x00F0 & op_code) >> 4]:
                self.PC += 2

        elif (0xF000 & op_code) == 0x6000:
            self.V[(0x0F00 & op_code) >> 8] = (0x00FF & op_code)

        elif (0xF000 & op_code) == 0x7000:
            self.V[(0x0F00 & op_code) >> 8] += (0x00FF & op_code)
            self.V[(0x0F00 & op_code) >> 8] &= 0xFF

        elif (0xF000 & op_code) == 0x8000:
            if (0x000F & op_code) == 0x0000:
                self.V[(0x0F00 & op_code) >> 8] = self.V[(0x00F0 & op_code) >> 4]

            elif (0x000F & op_code) == 0x0001:
                self.V[(0x0F00 & op_code) >> 8] |= self.V[(0x00F0 & op_code) >> 4]

            elif (0x000F & op_code) == 0x0002:
                self.V[(0x0F00 & op_code) >> 8] &= self.V[(0x00F0 & op_code) >> 4]

            elif (0x000F & op_code) == 0x0003:
                self.V[(0x0F00 & op_code) >> 8] ^= self.V[(0x00F0 & op_code) >> 4]

            elif (0x000F & op_code) == 0x0004:
                self.V[(0x0F00 & op_code) >> 8] += self.V[(0x00F0 & op_code) >> 4]
                self.V[16] = (self.V[(0x0F00 & op_code) >> 8] & 0x0F00)
                self.V[(0x0F00 & op_code) >> 8] &= 0x00FF

            elif (0x000F & op_code) == 0x0005:
                self.V[16] = (self.V[(0x0F00 & op_code) >> 8] & 0x0001)
                self.V[(0x0F00 & op_code) >> 8] >>= 1

            elif (0x000F & op_code) == 0x0006:
                pass

            elif (0x000F & op_code) == 0x000E:
                self.V[16] = (self.V[(0x0F00 & op_code) >> 8] & 0b10000000)
                self.V[(0x0F00 & op_code) >> 8] <<= 1
                self.V[(0x0F00 & op_code) >> 8] &= 0x00FF

        elif (0xF000 & op_code) == 0x9000:
            if self.V[(0x0F00 & op_code) >> 8] != self.V[(0x00F0 & op_code) >> 4]:
                self.PC += 2

        elif (0xF000 & op_code) == 0xA000:
            self.I = (op_code & 0x0FFF)

        elif (0xF000 & op_code) == 0xB000:
            self.PC = self.V[0] + (op_code & 0x0FFF)

        elif (0xF000 & op_code) == 0xC000:
            self.V[(0x0F00 & op_code) >> 8] = (random.randint(0, 255) & (op_code & 0x00FF))

        elif (0xF000 & op_code) == 0xD000:
            self.display.draw(
                self.V[(0x0F00 & op_code) >> 8],
                self.V[(0x00F0 & op_code) >> 4],
                (0x000F & op_code)
            )

        elif (0xF000 & op_code) == 0xE000:
            if (0x00FF & op_code) == 0x009E:
                if self.key == self.V[(0x0F00 & op_code) >> 8]:
                    self.PC += 2

            elif (0x00FF & op_code) == 0x00A1:
                if self.key != self.V[(0x0F00 & op_code) >> 8]:
                    self.PC += 2

        elif (0xF000 & op_code) == 0xF000:
            if (0x00FF & op_code) == 0x0007:
                self.V[(0x0F00 & op_code) >> 8] = self.delay_timer

            elif (0x00FF & op_code) == 0x000A:
                self.V[(0x0F00 & op_code) >> 8] = self.sound_timer

            elif (0x00FF & op_code) == 0x0015:
                pass

            elif (0x00FF & op_code) == 0x0018:
                self.delay_timer = self.V[(0x0F00 & op_code) >> 8]

            elif (0x00FF & op_code) == 0x001E:
                self.sound_timer = self.V[(0x0F00 & op_code) >> 8]

            elif (0x00FF & op_code) == 0x0029:
                self.I += self.V[(0x0F00 & op_code) >> 8]

            elif (0x00FF & op_code) == 0x0033:
                pass

            elif (0x00FF & op_code) == 0x0055:
                pass

            elif (0x00FF & op_code) == 0x0065:
                pass














