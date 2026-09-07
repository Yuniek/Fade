from .errors import FadeRuntimeError

# ##################################
# Abstract Syntax Tree
# ##################################

class ASTNode:
    def is_truthy(self) -> bool:
        raise FadeRuntimeError(
            f"{type(self).__name__} has no truthiness defined"
        )

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def is_truthy(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return f'{self.value}'

class BooleanNode(ASTNode):
    def __init__(self, value: bool):
        self.value = value

    def is_truthy(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f'true' if self.value else 'false'

class StringNode(ASTNode):
    def __init__(self, value):
            self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

class IdentifierNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Identifier({self.value})"

class UnaryOperation(ASTNode):
    def __init__(self, op:str, operand:ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'({self.op} {self.operand})'

class BinaryOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'

class AssignmentOperation(ASTNode):
    def __init__(self, identifier:IdentifierNode, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"{self.identifier} = {self.expression}"

class BooleanOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'
