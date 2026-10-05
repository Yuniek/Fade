from .errors import FadeRuntimeError

# ##################################
# Abstract Syntax Tree
# ##################################

class ASTNode:
    def is_truthy(self) -> bool:
        raise FadeRuntimeError(
            f"{type(self).__name__} has no truthiness defined"
        )

    def to_dict(self):
        raise NotImplementedError

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def is_truthy(self) -> bool:
        return self.value != 0

    def to_dict(self):
        return {
            "type":"Number",
            "value": self.value
        }

    def __repr__(self) -> str:
        return f'{self.value}'

class BooleanNode(ASTNode):
    def __init__(self, value: bool):
        self.value = value

    def is_truthy(self) -> bool:
        return self.value

    def to_dict(self):
        return {
            "type":"Boolean",
            "value": self.value
        }

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

    def to_dict(self):
        return {
            "type":"Identifier",
            "value": self.value
        }

    def __repr__(self) -> str:
        return f"Identifier({self.value})"

class StatementNode(ASTNode):
    def __init__(self, statement: ASTNode):
        self.statement = statement

    def to_dict(self):
        return {
            "type":"Statement",
            "value": self.statement.to_dict()
        }

    def __repr__(self) -> str:
        return f'Statement({self.statement})'
    
class BlockNode(ASTNode):
    def __init__(self, statements: list[StatementNode]):
        self.statements = statements

    def to_dict(self):
        return {
            "type":"Block",
            "value": [i.to_dict() for i in self.statements]
        }

    def __repr__(self) -> str:
        return f'Block({self.statements})'

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: BlockNode, else_body: BlockNode | None = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    
    def to_dict(self):
        return {
            "type": "If",
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict()
        }

    def __repr__(self) -> str:
        return (
            f'If({self.condition}, '
            f'{self.body}, '
            f'{self.else_body})'
        )

class ForLoopNode(ASTNode):
    def __init__(self, count:ASTNode, body:BlockNode):
        self.count = count
        self.body = body
    
    def to_dict(self):
        return {
            "type":"ForLoop",
            "count": self.count.to_dict(),
            "body": self.body.to_dict()
        }

    def __repr__(self)->str:
        return f"(repeat {self.count} times {self.body})"

class WhileLoopNode(ASTNode):
    def __init__(self, condition:ASTNode, body:BlockNode):
        self.condition = condition
        self.body = body
    
    def to_dict(self):
        return {
            "type":"WhileLoop",
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict()
        }

    def __repr__(self)->str:
        return f"(repeat until {self.condition} {self.body})"
    
class DoWhileLoopNode(ASTNode):
    def __init__(self, body:BlockNode, condition:ASTNode):
        self.body = body
        self.condition = condition
    
    def to_dict(self):
        return {
            "type":"DoWhileLoop",
            "body": self.body.to_dict(),
            "condition": self.condition.to_dict()
        }

    def __repr__(self)->str:
        return f"(repeat {self.body} until {self.condition})"

class BreakNode(ASTNode):
    def to_dict(self):
        return {
            "type": "Break"
        }

    def __repr__(self):
        return "break"

class ContinueNode(ASTNode):
    def to_dict(self):
        return {
            "type": "Continue"
        }

    def __repr__(self):
        return "continue"

class UnaryOperation(ASTNode):
    def __init__(self, op:str, operand:ASTNode):
        self.op = op
        self.operand = operand

    def to_dict(self):
        return {
            "type":"UnaryOperation",
            "operation": self.op,
            "operand": self.operand.to_dict()
        }

    def __repr__(self):
        return f'({self.op} {self.operand})'

class BinaryOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def to_dict(self):
        return {
            "type":"BinaryOperation",
            "left": self.left.to_dict(),
            "operation": self.op,
            "right": self.right.to_dict()
        }

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'

class AssignmentOperation(ASTNode):
    def __init__(self, identifier:IdentifierNode, expression:ASTNode):
        self.identifier = identifier
        self.expression = expression

    def to_dict(self):
        return {
            "type":"Assignment",
            "identifier": self.identifier.to_dict(),
            "expression": self.expression.to_dict()
        }

    def __repr__(self):
        return f"{self.identifier} = {self.expression}"

class BooleanOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right
  
    def to_dict(self):
        return {
            "type":"BooleanOperation",
            "left": self.left.to_dict(),
            "operation": self.op,
            "right": self.right.to_dict(),
        }
      
    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'
