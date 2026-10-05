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

    def chk_current_token_value(self, type, value):
        return self.current_token().type == type and self.current_token().value == value

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
        while self.current_token().type not in ['EOF', 'RBRACE']:

            while self.current_token().type in ['SEMICOLON', 'NEWLINE']:
                self.advance()
            
            if self.current_token().type in ['EOF', 'RBRACE']:
                break

            statements.append(self.parse_statement())
            
        return ast.BlockNode(statements)
    
    def parse_statement(self) -> ast.StatementNode:
        if self.current_token().type == 'IDENTIFIER' and self.tokens[self.position+1].type == 'EQUAL':
            node = self.parse_identifier()
        elif self.chk_current_token_value('KEYWORD', 'if'):
            node = self.parse_if()
        elif self.chk_current_token_value('KEYWORD', 'repeat'):
            node = self.parse_repeat()
        elif self.chk_current_token_value('KEYWORD', 'break'):
            self.advance()
            node = ast.BreakNode()
        elif self.chk_current_token_value('KEYWORD', 'continue'):
            self.advance()
            node = ast.ContinueNode()
        else:
            node = self.parse_or()
            
        return ast.StatementNode(node)

    def parse_repeat(self) -> ast.ASTNode:
        self.advance()

        if self.current_token().type == 'LPAREN':
            return self.parse_for_loop()
        elif self.current_token().type == 'LBRACE':
            return self.parse_do_while_loop()
        elif self.chk_current_token_value('KEYWORD', 'until'):
            return self.parse_while_loop()
        else:
            raise fadeError.InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected '(', '{' or until after repeat _"
                )

    def parse_for_loop(self) -> ast.ForLoopNode:
        self.advance()
        count = self.parse_or()

        if self.current_token().type != 'RPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected ')' after repeat (..._"
            )
        
        self.advance()

        if self.current_token().type != 'LBRACE':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '{' after repeat (...) _"
            )
        
        body = self.parse_block()

        return ast.ForLoopNode(count, body)
    
    def parse_while_loop(self) -> ast.WhileLoopNode:
        self.advance()

        if self.current_token().type != 'LPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '(' after repeat until _"
            )
        
        self.advance()
        condition = self.parse_or()

        if self.current_token().type != 'RPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected ')' after repeat until (..._"
            )
        
        self.advance()

        if self.current_token().type != 'LBRACE':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '{' after repeat until (...) _"
            )
        
        body = self.parse_block()
        
        return ast.WhileLoopNode(condition, body)
    
    def parse_do_while_loop(self) -> ast.DoWhileLoopNode:
        body = self.parse_block()
        
        if not self.chk_current_token_value('KEYWORD', 'until'):
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected 'until' after repeat {...} _"
            )
        
        self.advance()

        if self.current_token().type != 'LPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected '(' after repeat {...} until _"
            )

        self.advance()        
        condition = self.parse_or()

        if self.current_token().type != 'RPAREN':
            raise fadeError.InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                "Expected ')' after repeat {...} until (..._"
            )

        self.advance()
        
        return ast.DoWhileLoopNode(body, condition)

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

        while self.current_token().type == 'NEWLINE':
            self.advance()

        if self.chk_current_token_value('KEYWORD', 'else'):
            self.advance()
            if self.current_token().type != 'LBRACE' and (self.current_token().type != 'KEYWORD' and self.current_token().value != 'if'):
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
