import struct
import sys
import re

codes = []

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
                print("Invalid token at position:", pos)
                break
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
            if args != None:
                self.statements[signature](args)
            else:
                self.statements[signature]()
        else:
            print(f"Error: No statement found for signature '{signature}'")

tokenizer = Tokenizer({
    'CLS': r'\bCLS\b',
    'DRW': r'\bDRW\b',
    'MV': r'\bMV\b',
    'INT': r'\b\d+\b',
    'REG': r'\bTX|TY\b',
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
def drw(args):
    value = args[1]
    value_hex = hex(value)[2:].zfill(4)
    register = args[0]

    if len(value_hex) == 4:
        code = 0xB
        if register == "TY":
            code = 0xC

        codes.append(int(hex(code) + hex(value)[2:], 16))
    else:
        raise ValueError("INT out of range. (MV REG, INT)")

def parse(code):
    code = code.split(';', 1)[0].strip()
    if not code:
        return 
    tokens = tokenizer.tokenize(code)
    current_tokens = []
    arg_tokens = []
    for token_type, token_value in tokens:
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
        elif not any(signature.startswith(str(statement)) for statement in registry.statements):
            pass

def parse_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            parse(line.strip())   

if len(sys.argv) > 1:
    parse_file(sys.argv[1])

    with open(sys.argv[1].split(".")[0]+".ch69", "wb") as f:
        for code in codes:
            f.write(struct.pack('!H', code))

    print("File compiled as "+sys.argv[1].split(".")[0]+".ch69")
else:
    print("No file provided.")