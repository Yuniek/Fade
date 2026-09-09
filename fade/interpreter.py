from .environment import Environment
from .errors import FadeRuntimeError
from .ast import (
    ASTNode,
    NumberNode,
    BooleanNode,
    IdentifierNode,
    BlockNode,
    StatementNode,
    UnaryOperation,
    BinaryOperation,
    AssignmentOperation,
    BooleanOperation,
)

# ##################################
# Interpreter
# ##################################

class Interpreter:
    def __init__(self, ast:ASTNode, env:Environment):
        self.ast = ast
        self.env = env

    def evaluate(self)->list:
        result = self.evaluator(self.ast)
        if isinstance(result, list):
            return result
        else:
            raise FadeRuntimeError("Incorrect Format of Statements in Interpreter")

    def evaluator(self, ast:ASTNode):
        if isinstance(ast, BlockNode):
            statements = ast.statements
            returnList = []
            for statement in statements:
                returnList.append(self.evaluator(statement))
            return returnList
        if isinstance(ast, NumberNode):
            return ast
        if isinstance(ast, BooleanNode):
                    return ast
        if isinstance(ast, IdentifierNode):
            return self.env.getVariable(ast.value)
        if isinstance(ast, StatementNode):
            return self.evaluator(ast.statement)
        if isinstance(ast, AssignmentOperation):
            identifier = ast.identifier.value
            expression = self.evaluator(ast.expression)
            self.env.setVariable(identifier, expression)
            return None
        if isinstance(ast, UnaryOperation):

            CASES = [(NumberNode, BooleanNode)]
            op = ast.op
            operand = ast.operand

            match op:
                case 'PLUS':
                    if isinstance(operand, CASES[0]):
                        return NumberNode(self.evaluator(operand).value)
                    raise FadeRuntimeError(f"Invalid operand for unary {op}")
                case 'MINUS':
                    if isinstance(operand, CASES[0]):
                        return NumberNode(self.evaluator(operand).value * -1)
                    raise FadeRuntimeError(f"Invalid operand for unary {op}")
                case 'NOT':
                    if isinstance(operand, CASES[0]):
                        return BooleanNode(not self.evaluator(operand).is_truthy())
                    raise FadeRuntimeError(f"Invalid operand for unary {op}")
                case _:
                    raise FadeRuntimeError(f"Unexpected Unary Operator {op}")
        if isinstance(ast, BinaryOperation):
            left = self.evaluator(ast.left)            
            right = self.evaluator(ast.right)
            op = ast.op

            CASES = [(NumberNode, BooleanNode)]

            match op:
                case "PLUS":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return NumberNode(left.value + right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case "MINUS":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return NumberNode(left.value - right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case "MUL":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return NumberNode(left.value * right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case "DIV":
                    if right.value == 0: raise FadeRuntimeError(f"division by zero")
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return NumberNode(left.value / right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case _:
                    raise FadeRuntimeError(f"Unexpected Binary Operator {op}")
        if isinstance(ast, BooleanOperation):
            left = self.evaluator(ast.left)
            right = self.evaluator(ast.right)
            op = ast.op

            CASES = [(NumberNode, BooleanNode)]

            match op:
                case 'OR':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.is_truthy() or right.is_truthy())
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'AND':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.is_truthy() and right.is_truthy())
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'NOT_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value != right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'EQUALITY':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value == right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'LESSER':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value < right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'GREATER':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value > right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'LESSER_OR_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value <= right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case 'GREATER_OR_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return BooleanNode(left.value >= right.value)
                    raise FadeRuntimeError(f"Invalid operands for {op}")
                case _:
                    raise FadeRuntimeError(f"Unexpected Boolean Operator {op}")
