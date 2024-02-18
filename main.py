from random import randint
from time import time
import fontset
import sys

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class Chip:
    def __init__(self):
        pygame.init()

        self.waitTime = time()

        self.vram = [[randint(0, 255) for _ in range(640)] for _ in range(320)]
        self.memory = [0] * 4096
        self.registers = [0] * 5
        self.pc = 0xFF

        self.opcodes = {
            0x2B6: self.op_2B6, # CLS
            0x1A4: self.op_1A4, # CLR
            0x7D0: self.op_7D0, # DRW
            0x3E7: self.op_3E7, # EXT
            0x1EC: self.op_1EC, # SLP
        }

        self.argcodes = {
            0xB: self.op_B,    # MV TX
            0xC: self.op_C,    # MV TY
            0x9: self.op_9,    # MV EX
            0xA: self.op_A,    # MV EY
            0x1: self.op_1,    # MV TF
            0x45: self.op_45,  # DRL
            0x50: self.op_50,  # DRN
            0x5: self.op_5,    # SE
            0x10: self.op_10,  # SNE
            0x8: self.op_8,    # CMP
        }

        self.screen = pygame.display.set_mode((640, 320))
        pygame.display.set_caption("Chip69 Emulator")

    def scale(self, character, scale_x, scale_y):
        scaled = []
        for row in character:
            scaled_row = []
            for pixel in row:
                scaled_row.extend([pixel] * scale_x)
            scaled.extend([scaled_row] * scale_y)
        return scaled

    def op_2B6(self):
        # 2B6: Clears the screen
        self.vram = [[0] * 640 for _ in range(320)]

    def op_1A4(self):
        # 1A4: Sets the value of all registers to 0
        self.registers = [0] * 5

    def op_7D0(self):
        # 7D0: Draws pixels from point (TX, TY) to point (EX, EY)
        TX, TY, EX, EY = self.registers[:4]

        for y in range(TY, EY + 1):
            for x in range(TX, EX + 1):
                if 0 <= x < 640 and 0 <= y < 320:
                    self.vram[y][x] = 1

    def op_3E7(self):
        # 3E7: Exits the currently loaded ROM
        self.vram = [[0] * 640 for _ in range(320)]
        self.memory = [0] * 4096

        letters = "UNLOADED ROM"
        spaceCalc = 25

        for letter in letters:
            if letter == ' ':
                spaceCalc += 10
                continue
            else:
                spaceCalc += 8
            original_letter = fontset.letters[letter]
            scaled_letter = self.scale(original_letter, 2, 2)
            for y, row in enumerate(scaled_letter):
                for x, pixel in enumerate(row):
                    if pixel == 1:
                        if 0 <= spaceCalc + x < 640 and 0 <= 25 + y < 320:
                            self.vram[25 + y][spaceCalc + x] = 1
            spaceCalc += 2


    def op_1EC(self):
        # 1EC: Stops the program for a TF amount of time
        self.waitTime = time()

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
        # 1: Set register TF to last two bytes of 
        value = 0x0

        if (opcode & 0xF0) >> 4 in self.argcodes:
            value = opcode & 0xF
        elif opcode >> 8 in self.argcodes:
            value = opcode & 0xFF
        elif (opcode >> 12) & 0xFFF in self.argcodes:
            value = opcode & 0xFFF

        self.registers[4] = value

    def op_45(self, opcode):
        # 45: Draws a letter from the built-in fontset at Xpos TX and Ypos TY starting position
        #     And multiplies it's size by TF
        TX = self.registers[0]
        TY = self.registers[1]
        TF = self.registers[4]

        letter = chr(int(hex(opcode).replace('0x', '')[2:], 16) + 64)

        if letter in fontset.letters:
            original_letter = fontset.letters[letter]
            scaled_letter = self.scale(original_letter, TF, TF)
            for y, row in enumerate(scaled_letter):
                for x, pixel in enumerate(row):
                    if pixel == 1:
                        if 0 <= TX + x < 640 and 0 <= TY + y < 320:
                            self.vram[TY + y][TX + x] = 1


    def op_50(self, opcode):
        # 50: Draws a number from the built-in fontset at Xpos TX and Ypos TY starting position
        #     and multiplies it's size by TF
        TX = self.registers[0]
        TY = self.registers[1]
        TF = self.registers[4]

        number = hex(opcode).replace('0x', '')[2:]

        if number in fontset.numbers:
            original_number = fontset.numbers[number]
            scaled_number = self.scale(original_number, TF, TF)
            for y, row in enumerate(scaled_number):
                for x, pixel in enumerate(row):
                    if pixel == 1:
                        if 0 <= TX + x < 640 and 0 <= TY + y < 320:
                            self.vram[TY + y][TX + x] = 1

    def op_5(self, opcode):
        # 5: Skips next instruction if last comparison is equal
        if self.memory[0] == self.memory[1]:
            self.pc += 2

    def op_10(self, opcode):
        # 10: Skips next instruction if last comparison is not equal
        if self.memory[0] != self.memory[1]:
            self.pc += 2

    def op_8(self, opcode):
        # 8: Gets the two next hexes store in memory as values and stores
        #    them in memory slots 0x1 and 0x2 for comparison
        addr = self.pc + 1  # Next memory address after the opcode
        value1 = self.memory[addr]
        value2 = self.memory[addr + 2]

        self.memory[0] = value1
        self.memory[1] = value2

        self.pc += 4


    def run(self):
        while True:
            opcode = self.fetch_opcode()
            self.execute_opcode(opcode)
            self._check_events()
            self._update_screen()

    def fetch_opcode(self):
        if self.pc >= len(self.memory):
            return 0x0
        
        if (time() - self.waitTime) >= self.registers[4]:
            if len(self.memory) >= self.pc:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.pc += 2
                return opcode
            else:
                return 0x0
        else:
            return 0x0
    
    def execute_opcode(self, opcode):
        if opcode in self.opcodes:
            self.opcodes[opcode]()
        elif int(hex(opcode).replace('0x', '')[:2], 16) in self.argcodes:
            self.argcodes[int(hex(opcode).replace('0x', '')[:2], 16)](opcode)
        elif opcode >> 8 in self.argcodes:
            self.argcodes[opcode >> 8](opcode)
        elif (opcode >> 12) & 0xFFF in self.argcodes:
            self.argcodes[(opcode >> 12) & 0xF](opcode)
        elif (opcode & 0xF0) >> 4 in self.argcodes:
            self.argcodes[(opcode & 0xF0) >> 4](opcode)
        elif opcode & 0xFF00 in self.argcodes:
            self.argcodes[opcode & 0xFF00](opcode)
        elif opcode != 0x0:
            print("Invalid instruction: " + hex(opcode))

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
            self.memory[0xFF + i] = byte

if __name__ == '__main__':
    if len(sys.argv) > 1:
        game = Chip()
        rom = "./roms/"+sys.argv[1]
        game.load_rom(rom)
        game.run()