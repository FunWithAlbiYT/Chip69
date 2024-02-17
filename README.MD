# Chip69
An emulator for a device that... doesn't exist?

### Emulating
Before being able to emulate, you must have
these requirements:
- Python 3.8+

After those are installed then you can
emulate doing this:         <br />
`$ python main.py rom.ch69` <br />
replace \`rom.ch69\` with the filename of your
rom that must be located in the /roms/ folder

### Assembling
I'm not going to teach you how to code x69 assembly
but I am going to show you how to assemble your code
if you have written it.

If you want to learn look at the \`code.asm\` file in the which uses all functions implemented
into Chip69

Alright, lets start.
Make sure you have the requirements, they're listed in the [Emulating](#Emulating) section before starting.

This is the code on assembling:  <br />
`$ python assembler.py code.asm` <br />
replace \`code.asm\` with the filename of your assembly
code.

### Opcodes
| Hex Code      | PY Equivelant  | Explanation   |
|-------------- |----------------|---------------|
| 0x2B6         | screen.clear()         | Clears the screen        |
| 0x7D0         | screen.draw(TX, TY, EX, EY)         | Draws pixels from point (TX, YX) to point (EX, YX) with white        |
| 0x45         | screen.drawLetter(TX, TY, ?)         | Draws the ?th letter of the alphabet at point (TX, TY)        |
| 0x50         | screen.drawNumber(TX, TY, ?)         | Draws the number ? at point (TX, TY)        |
| 0xB           | TX = ?         | Sets TX to value to last two bytes of opcode         |
| 0xC           | TY = ?         | Sets TY to value to last two bytes of opcode         |
| 0x1           | TF = ?         | Sets TF to value to last two bytes of opcode         |
| 0x9           | EX = ?         | Sets EX to value to last two bytes of opcode         |
| 0xA           | EY = ?         | Sets EY to value to last two bytes of opcode         |
| 0x1A4         | registers.clear()         | Sets value of all registers to 0        |
| 0x3E7          | RAM.clear()         |   Exits the current ROM       |
| 0x1EC          | time.sleep(TF)         | Sleeps for a TF amount of seconds         |

