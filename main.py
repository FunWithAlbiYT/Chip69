import pygame
import sys
from random import randint

class Chip:
    def __init__(self):
        pygame.init()

        self.vram = [[randint(0, 255)] * 640 for _ in range(320)]
        self.memory = [0] * 4096
        self.registers = [0] * 8
        self.pc = 0x0

        self.opcodes = {
            0x02B6: self.op_02B6, # CLS
            0x07D0: self.op_07D0  # DRW
        }

        self.argcodes = {
            0x0B: self.op_0B, # MV TX
            0x0C: self.op_0C  # MV TY
        }

        self.screen = pygame.display.set_mode((640, 320))
        pygame.display.set_caption("Chip69")

    def op_02B6(self):
        # 02B6: Clears the screen
        self.vram = [[0] * 640 for _ in range(320)]

    def op_07D0(self):
        # 07D0: Draws pixel at X point TX and Y point TY

        x = self.registers[0]
        y = self.registers[1]

        if 0 <= x < 640 and 0 <= y < 320:
            self.vram[y][x] = 1

    def op_0B(self, opcode):
        # 0B: Set register TX to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[0] = value

    def op_0C(self, opcode):
        # 0C: Set register TX to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[1] = value

    def run(self):
        while True:
            opcode = self.fetch_opcode()
            self.execute_opcode(opcode)
            self._check_events()
            self._update_screen()

    def fetch_opcode(self):
        if self.pc >= len(self.memory):
            return 0x0
        
        opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        self.pc += 2
        return opcode
    
    def execute_opcode(self, opcode):
        if opcode in self.opcodes:
            self.opcodes[opcode]()
        elif opcode >> 8 in self.argcodes:
            self.argcodes[opcode >> 8](opcode)
        elif (opcode >> 12) & 0xF in self.argcodes:
            self.argcodes[(opcode >> 12) & 0xF](opcode)
        elif opcode != 0x0:
            print("Invalid instruction: " + hex(opcode))
            return
        
        if opcode != 0x0:
            print("Executed instruction: " + hex(opcode))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        
        for y in range(320):
            for x in range(640):
                if self.vram[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 10, 10))
        
        pygame.display.flip()

    def load_rom(self, filename):
        with open(filename, 'rb') as f:
            rom_data = f.read()
        
        for i, byte in enumerate(rom_data):
            self.memory[0x0 + i] = byte

if __name__ == '__main__':
    if len(sys.argv) > 1:
        game = Chip()
        rom = "./roms/"+sys.argv[1]
        game.load_rom(rom)
        game.run()