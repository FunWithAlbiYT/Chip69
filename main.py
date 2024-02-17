import pygame
import sys
from random import randint

class Chip:
    def __init__(self):
        pygame.init()

        self.vram = [[randint(0, 255)] * 640 for _ in range(320)]
        self.memory = [0] * 4096
        self.registers = [0] * 5
        self.pc = 0x0

        self.opcodes = {
            0x2B6: self.op_2B6, # CLS
            0x7D0: self.op_7D0, # DRW
        }

        self.argcodes = {
            0xB: self.op_B, # MV TX
            0xC: self.op_C, # MV TY
            0x9: self.op_9, # MV EX
            0xA: self.op_A, # MV EY
            0x1: self.op_1  # DRL
        }

        self.screen = pygame.display.set_mode((640, 320))
        pygame.display.set_caption("Chip69 Emulator")

    def op_2B6(self):
        # 2B6: Clears the screen
        self.vram = [[0] * 640 for _ in range(320)]

    def op_7D0(self):
        # 7D0: Draws pixels from point (TX, TY) to point (EX, EY)

        TX, TY, EX, EY = self.registers[:4]

        for y in range(TY, EY + 1):
            for x in range(TX, EX + 1):
                if 0 <= x < 640 and 0 <= y < 320:
                    self.vram[y][x] = 1

    def op_B(self, opcode):
        # 0B: Set register TX to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[0] = value

    def op_C(self, opcode):
        # C: Set register TY to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[1] = value

    def op_9(self, opcode):
        # 9: Set register EX to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[2] = value

    def op_A(self, opcode):
        # A: Set register EY to last two bytes of opcode
        if opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        else:
            value = opcode & 0xFFF

        self.registers[3] = value

    def op_1(self, opcode):
        # 1: Draws a letter from the built in fontset at Xpos TX and Ypos TY starting position

        # WIP

        pass

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

        draw_commands = []

        for y in range(320):
            for x in range(640):
                if self.vram[y][x] == 1:
                    draw_commands.append((x, y))

        for command in draw_commands:
            pygame.draw.rect(self.screen, (255, 255, 255), (command[0], command[1], 1, 1))

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