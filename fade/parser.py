from .lexer import Token
from . import ast, errors as fadeError

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

        node = self.parse_block()

        if self.current_token().type != 'EOF':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Unexpected token {self.current_token().type}"
            )

        return node

    def parse_block(self) -> ast.BlockNode:
        if self.current_token().type == 'LBRACE':
            self.advance()
            node = self.parse_statements()
            if self.current_token().type != 'RBRACE':
                raise fadeError.InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected '}'"
                )
            self.advance()
            return node
        node = self.parse_statements()
        return node

    def parse_statements(self) -> ast.BlockNode:
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())

            if self.current_token().type == 'SEMICOLON':
                self.advance()
            else:
                break
            
        return ast.BlockNode(statements)
    
    def parse_statement(self) -> ast.StatementNode:
        if self.current_token().type == 'KEYWORD' and self.current_token().value == 'if':
            node = self.parse_if()
        elif self.current_token().type == 'IDENTIFIER' and self.tokens[self.position+1].type == 'EQUAL':
            node = self.parse_identifier()
        else:
            node = self.parse_or()
            
        return ast.StatementNode(node)

    def parse_if(self) -> ast.IfNode:
        self.advance()
        if self.current_token().type != 'LPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '(' after if"
            )

        condition = self.parse_or()
        if self.current_token().type != 'LBRACE':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '{' after if (condition)"
            )
        body=self.parse_block()
        else_body = None

        if self.current_token().type == 'KEYWORD' and self.current_token().value == 'else':
            self.advance()
            if self.current_token().type != 'LBRACE':
                raise fadeError.InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected '{' after else"
                )
            else_body = self.parse_block()

        return ast.IfNode(condition,body,else_body)

    def parse_identifier(self)->ast.ASTNode:
        identifier = ast.IdentifierNode(self.current_token().value)
        self.advance()
        if self.current_token().type != "EQUAL":
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Expected '=' after identifier token but got {self.current_token().type}"
            )
        self.advance()
        expression = self.parse_or()
        return ast.AssignmentOperation(identifier, expression)

    def parse_or(self)->ast.ASTNode:
        left = self.parse_and()

        while self.current_token().type == "OR":
            op = self.current_token().type
            self.advance()
            right = self.parse_and()

            left = ast.BooleanOperation(left, op, right)
        return left

    def parse_and(self)->ast.ASTNode:
        left = self.parse_comparison()

        while self.current_token().type == "AND":
            op = self.current_token().type
            self.advance()
            right = self.parse_comparison()

            left = ast.BooleanOperation(left, op, right)
        return left

    def parse_comparison(self)->ast.ASTNode:
        left = self.parse_expression()

        while self.current_token().type in ("GREATER_OR_EQUAL", "LESSER_OR_EQUAL", "GREATER", "LESSER", "EQUALITY", "NOT_EQUAL"):
            op = self.current_token().type
            self.advance()
            right = self.parse_expression()

            left = ast.BooleanOperation(left, op, right)
        return left

    def parse_expression(self)->ast.ASTNode:
        left = self.parse_term()

        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token().type
            self.advance()
            right = self.parse_term()

            left = ast.BinaryOperation(left, op, right)
        return left

    def parse_term(self)->ast.ASTNode:
        left = self.parse_factor()

        while self.current_token().type in ('MUL', 'DIV'):
            op = self.current_token().type
            self.advance()
            right = self.parse_factor()

            left = ast.BinaryOperation(left, op, right)
        
        return left
    
    def parse_factor(self)->ast.ASTNode:
        current = self.current_token()
        if current.type in ('INT', 'FLOAT'):
            self.advance()
            return ast.NumberNode(current.value)
        
        if current.type == 'KEYWORD' and current.value in ('true', 'false'):
            self.advance()
            return ast.BooleanNode(True) if current.value == 'true' else ast.BooleanNode(False)

        elif current.type == 'LPAREN':
            self.advance()
            node = self.parse_or()
            if self.current_token().type != 'RPAREN':
                raise fadeError.InvalidSyntaxError(
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
            return ast.IdentifierNode(current.value)

        raise fadeError.InvalidSyntaxError(
            self.current_token().pos['start'],
            self.current_token().pos['end'],
            f"Expected a number, '(', '+', or '-', got {current.type}"
        )

    def parse_unary(self)->ast.ASTNode:
        op = self.current_token().type
        self.advance()
        operand = self.parse_factor()
        return ast.UnaryOperation(op, operand)
