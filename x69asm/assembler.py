import struct
import sys
import re

compileFile = True
currentLine = 0
fileContent = ""
codes = []

def error(*msgs):
    global compileFile
    compileFile = False

    for msg in msgs:
        print(msg)

def getline(text, line):
    lines = text.split('\n')
    if 0 <= line < len(lines):
        return lines[line-1]
    else:
        return None

def starts(main_string, substring):
    return main_string.find(substring)

def ends(main_string, substring):
    start_index = main_string.find(substring)
    if start_index != -1:
        return start_index + len(substring)
    else:
        return -1

class Tokenizer:
    def __init__(self, tokens):
        self.tokens = tokens
        sorted_tokens = sorted(tokens.items(), key=lambda x: len(x[1]), reverse=True)
        self.token_regex = re.compile('|'.join(f'(?P<{token}>{pattern})' for token, pattern in sorted_tokens), re.IGNORECASE)

    def tokenize(self, code):
        pos = 0
        while pos < len(code):
            match = self.token_regex.match(code, pos)
            if match is None:
                yield 'UNKNOWN', code[pos]
                pos += 1
            else:
                pos = match.end()
                token_type = match.lastgroup
                token_value = match.group(token_type)
                if token_type != 'WS':
                    yield token_type, token_value

class StatementRegistry:
    def __init__(self):
        self.statements = {}

    def register(self, signature):
        def decorator(func):
            self.statements[signature] = func
            return func
        return decorator

    def execute(self, signature, args = None):
        if signature in self.statements:
            if args is not None:
                self.statements[signature](args)
            else:
                self.statements[signature]()
        else:
            error(
                f"Statement doesn't exist: `{signature}`",
                f"{' ' * 4}{currentLine}{' ' * (5 - len(str(currentLine)))}|{' ' * 4}{getline(fileContent, int(str(currentLine)))}",
                f"{' ' * 9}|{' ' * 4}{' ' * starts(getline(fileContent, currentLine), signature)}{'^' * (ends(getline(fileContent, currentLine), signature) - starts(getline(fileContent, currentLine), code))}"
            )

tokenizer = Tokenizer({
    'CLS': r'\bCLS\b',
    'DRW': r'\bDRW\b',
    'MV': r'\bMV\b',
    'INT': r'\b\d+\b',
    'REG': r'\b(TX|TY|EX|EY)\b',
    'SPACE': r'\s+',
    'COMMA': r','
})

registry = StatementRegistry()

@registry.register("CLS")
def cls():
    codes.append(int(0x2B6))

@registry.register("DRW")
def drw():
    codes.append(int(0x7D0))

@registry.register("MV SPACE REG COMMA SPACE INT")
def mv(args):
    value = args[1]
    register = args[0]

    if len(hex(value)[2:]) < 4:
        code = 0xB
        if register == "TY":
            code = 0xC
        if register == "EX":
            code = 0x9
        if register == "EY":
            code = 0xA

        codes.append(int(hex(code) + hex(value)[2:], 16))
    else:
        eCode = str(args[1])
        error(
            f"INT out of range: `{eCode}`",
            f"{' ' * 4}{currentLine}{' ' * (5 - len(str(currentLine)))}|{' ' * 4}{getline(fileContent, int(str(currentLine)))}",
            f"{' ' * 9}|{' ' * 4}{' ' * starts(getline(fileContent, currentLine), eCode)}{'^' * (ends(getline(fileContent, currentLine), eCode) - starts(getline(fileContent, currentLine), eCode))}"
        )

def parse(code):
    code = code.strip()
    if not code or code.startswith(';'):
        return 
    code = code.split(';', 1)[0].strip()
    tokens = tokenizer.tokenize(code)
    current_tokens = []
    arg_tokens = []
    unknown_token = ''
    for token_type, token_value in tokens:
        if token_type == 'UNKNOWN':
            unknown_token += token_value
        else:
            if unknown_token:
                error(
                    f"Token doesn't exist: `{unknown_token}`",
                    f"{' ' * 4}{currentLine}{' ' * (5 - len(str(currentLine)))}|{' ' * 4}{getline(fileContent, int(str(currentLine)))}",
                    f"{' ' * 9}|{' ' * 4}{' ' * starts(getline(fileContent, currentLine), unknown_token)}{'^' * len(unknown_token)}"
                )
                unknown_token = ''
            current_tokens.append(token_type)
            signature = ' '.join(current_tokens)

            if token_type == 'REG':
                arg_tokens.append(token_value)
            elif token_type == 'INT':
                arg_tokens.append(int(token_value))

            if signature in registry.statements:
                if len(arg_tokens) == 0:
                    registry.execute(signature)
                else:
                    registry.execute(signature, arg_tokens)
                current_tokens = []
                arg_tokens = []

    if unknown_token:
        error(
            f"Token doesn't exist: `{unknown_token}`",
            f"{' ' * 4}{currentLine}{' ' * (5 - len(str(currentLine)))}|{' ' * 4}{getline(fileContent, int(str(currentLine)))}",
            f"{' ' * 9}|{' ' * 4}{' ' * starts(getline(fileContent, currentLine), unknown_token)}{'^' * len(unknown_token)}"
        )

def parse_file(filename):
    global fileContent
    global currentLine

    with open(filename, 'r') as file:
        fileContent = file.read()
        file.seek(0)
        for line in file:
            currentLine += 1
            parse(line.strip())

if len(sys.argv) > 1:
    parse_file(sys.argv[1])

    if compileFile == True:
        with open(sys.argv[1].split(".")[0]+".ch69", "wb") as f:
            for code in codes:
                f.write(struct.pack('!H', code))

        print("File assembled as "+sys.argv[1].split(".")[0]+".ch69")
    else:
        print("Couldn't assemble file since error occurred.")
else:
    print("No file provided.")