from .lexer import Token
from .errors import InvalidSyntaxError
from .ast import (
    ASTNode,
    NumberNode,
    BooleanNode,
    IdentifierNode,
    UnaryOperation,
    BinaryOperation,
    AssignmentOperation,
    BooleanOperation,
)

# ##################################
# Parser
# ##################################

class Parser:
    def __init__(self, tokens:list[Token]):
        self.tokens:list[Token] = tokens
        self.position:int = -1
        self.advance()

    def current_token(self) -> Token:
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def parse(self):
        if len(self.tokens) < 2: return
        if self.current_token().type == 'IDENTIFIER' and self.tokens[self.position+1].type == 'EQUAL':
            node = self.parse_identifier()
        else:
            node = self.parse_or()

        if self.current_token().type != 'EOF':
            raise InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Unexpected token {self.current_token().type}"
            )

        return node

    def parse_identifier(self)->ASTNode:
        identifier = IdentifierNode(self.current_token().value)
        self.advance()
        if self.current_token().type != "EQUAL":
            raise InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Expected '=' after identifier token but got {self.current_token().type}"
            )
        self.advance()
        expression = self.parse_or()
        return AssignmentOperation(identifier, expression)

    def parse_unary(self)->ASTNode:
        op = self.current_token().type
        self.advance()
        operand = self.parse_factor()
        return UnaryOperation(op, operand)
    
    def parse_factor(self)->ASTNode:
        current = self.current_token()
        if current.type in ('INT', 'FLOAT'):
            self.advance()
            return NumberNode(current.value)
        
        if current.type == 'KEYWORD' and current.value in ('true', 'false'):
            self.advance()
            return BooleanNode(True) if current.value == 'true' else BooleanNode(False)

        elif current.type == 'LPAREN':
            self.advance()
            node = self.parse_or()
            if self.current_token().type != 'RPAREN':
                raise InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected ')'"
                )
            self.advance()
            return node

        elif current.type in ('PLUS', 'MINUS', 'NOT'):
            return self.parse_unary()

        elif current.type == 'IDENTIFIER':
            self.advance()
            return IdentifierNode(current.value)

        raise InvalidSyntaxError(
            self.current_token().pos['start'],
            self.current_token().pos['end'],
            f"Expected a number, '(', '+', or '-', got {current.type}"
        )

    def parse_term(self)->ASTNode:
        left = self.parse_factor()

        while self.current_token().type in ('MUL', 'DIV'):
            op = self.current_token().type
            self.advance()
            right = self.parse_factor()

            left = BinaryOperation(left, op, right)
        
        return left

    def parse_expression(self)->ASTNode:
        left = self.parse_term()

        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token().type
            self.advance()
            right = self.parse_term()

            left = BinaryOperation(left, op, right)
        return left

    def parse_comparison(self)->ASTNode:
        left = self.parse_expression()

        while self.current_token().type in ("GREATER_OR_EQUAL", "LESSER_OR_EQUAL", "GREATER", "LESSER", "EQUALITY", "NOT_EQUAL"):
            op = self.current_token().type
            self.advance()
            right = self.parse_expression()

            left = BooleanOperation(left, op, right)
        return left

    def parse_and(self)->ASTNode:
        left = self.parse_comparison()

        while self.current_token().type == "AND":
            op = self.current_token().type
            self.advance()
            right = self.parse_comparison()

            left = BooleanOperation(left, op, right)
        return left

    def parse_or(self)->ASTNode:
        left = self.parse_and()

        while self.current_token().type == "OR":
            op = self.current_token().type
            self.advance()
            right = self.parse_and()

            left = BooleanOperation(left, op, right)
        return left

