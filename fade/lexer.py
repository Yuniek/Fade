import re
from .errors import InvalidTokenError

# ##################################
# Tokens
# ##################################

TOKEN_TYPES = [
    ('KEYWORD',          r'\b(true|false)\b'),
    ('FLOAT',            r'\d+\.\d+'),
    ('INT',              r'\d+'),
    ('GREATER_OR_EQUAL', r'>='),
    ('LESSER_OR_EQUAL',  r'<='),
    ('GREATER',          r'>'),
    ('LESSER',           r'<'),
    ('EQUALITY',         r'=='),
    ('NOT_EQUAL',        r'!='),
    ('AND',              r'\band\b'),
    ('OR',               r'\bor\b'),
    ('NOT',              r'\bnot\b'),
    ('EQUAL',            r'='),
    ('PLUS',             r'\+'),
    ('MINUS',            r'-'),
    ('MUL',              r'\*'),
    ('DIV',              r'/'),
    ('LPAREN',           r'\('),
    ('RPAREN',           r'\)'),
    ('STRING',           r'\".*?\"'),
    ('IDENTIFIER',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('WHITESPACE',       r'\s+'),
]

OPERATIONS = {
    "PLUS": {},
    "MINUS": {},
    "MUL": {},
    "DIV": {},
    "GREATER": {},
    "LESSER": {},
    "EQUALITY": {},
    "NOT_EQUAL": {},
}

class Token:
    def __init__(self, token_type, value:int|float|str|None, pos:dict[str, int]):
        self.type:str = token_type
        self.value:int|float|str|None = value
        self.pos = pos

    def __repr__(self)->str:
        if self.value is not None:return f'{self.type}:{self.value}'
        return f'{self.type}'


# ##################################
# Lexer to Generate Tokens
# ##################################

class Lexer:
    def __init__(self, text:str):
        self.text:str = text

    def tokenize(self) -> list[Token]:
        tokens = []

        pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)

        position = 0

        for match in re.finditer(pattern, self.text):
            if match.start() != position:
                raise InvalidTokenError(position,match.start(),f"{self.text[position:match.start()]}")

            position = match.end()
            if match.lastgroup == 'WHITESPACE': continue
            token_type = match.lastgroup
            value = match.group()
            if token_type == 'FLOAT':
                value = float(value)
            elif token_type == 'INT':
                value = int(value)
            elif token_type == 'STRING':
                value = value[1:-1]
            elif token_type == 'IDENTIFIER':
                value = value
            elif token_type == 'KEYWORD':
                value = value
            else:
                value = None
            tokens.append(Token(token_type, value, {'start':match.start(), 'end':match.end()}))

        if position != len(self.text):
            raise InvalidTokenError(
                position,
                len(self.text),
                self.text[position:]
            )

        tokens.append(Token("EOF", None, {'start':position, 'end':position}))
        return tokens
