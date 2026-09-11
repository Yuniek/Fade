from .environment import Environment
from . import ast, errors as fadeError

# ##################################
# Interpreter
# ##################################

class Interpreter:
    def __init__(self, node:ast.ASTNode, env:Environment):
        self.node = node
        self.env = env
        self.output = []

    def evaluate(self)->list:
        self.evaluator(self.node)
        return self.output

    def evaluator(self, node:ast.ASTNode):
        if isinstance(node, ast.BlockNode):
            statements = node.statements
            for statement in statements:
                value = self.evaluator(statement)
                if value:
                    self.output.append(value)

        if isinstance(node, ast.StatementNode):
            return self.evaluator(node.statement)

        if isinstance(node, ast.IfNode):
            condition = self.evaluator(node.condition)
            assert isinstance(condition, ast.ASTNode)
            if condition.is_truthy():
                return self.evaluator(node.body)
            elif node.else_body is not None:
                return self.evaluator(node.else_body)

        if isinstance(node, ast.AssignmentOperation):
            identifier = node.identifier.value
            expression = self.evaluator(node.expression)
            self.env.setVariable(identifier, expression)
            return None

        if isinstance(node, ast.BooleanOperation):
            left = self.evaluator(node.left)
            right = self.evaluator(node.right)
            op = node.op

            CASES = [(ast.NumberNode, ast.BooleanNode)]

            match op:
                case 'OR':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.is_truthy() or right.is_truthy())
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'AND':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.is_truthy() and right.is_truthy())
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'NOT_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value != right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'EQUALITY':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value == right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'LESSER':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value < right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'GREATER':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value > right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'LESSER_OR_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value <= right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case 'GREATER_OR_EQUAL':
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.BooleanNode(left.value >= right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case _:
                    raise fadeError.FadeRuntimeError(f"Unexpected Boolean Operator {op}")

        if isinstance(node, ast.BinaryOperation):
            left = self.evaluator(node.left)            
            right = self.evaluator(node.right)
            op = node.op

            CASES = [(ast.NumberNode, ast.BooleanNode)]

            match op:
                case "PLUS":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.NumberNode(left.value + right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case "MINUS":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.NumberNode(left.value - right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case "MUL":
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.NumberNode(left.value * right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case "DIV":
                    if right.value == 0: raise fadeError.FadeRuntimeError(f"division by zero")
                    if isinstance(left, CASES[0]) and isinstance(right, CASES[0]):
                        return ast.NumberNode(left.value / right.value)
                    raise fadeError.FadeRuntimeError(f"Invalid operands for {op}")
                case _:
                    raise fadeError.FadeRuntimeError(f"Unexpected Binary Operator {op}")

        if isinstance(node, ast.UnaryOperation):

            CASES = [(ast.NumberNode, ast.BooleanNode)]
            op = node.op
            operand = node.operand

            match op:
                case 'PLUS':
                    if isinstance(operand, CASES[0]):
                        return ast.NumberNode(self.evaluator(operand).value)
                    raise fadeError.FadeRuntimeError(f"Invalid operand for unary {op}")
                case 'MINUS':
                    if isinstance(operand, CASES[0]):
                        return ast.NumberNode(self.evaluator(operand).value * -1)
                    raise fadeError.FadeRuntimeError(f"Invalid operand for unary {op}")
                case 'NOT':
                    if isinstance(operand, CASES[0]):
                        return ast.BooleanNode(not self.evaluator(operand).is_truthy())
                    raise fadeError.FadeRuntimeError(f"Invalid operand for unary {op}")
                case _:
                    raise fadeError.FadeRuntimeError(f"Unexpected Unary Operator {op}")

        if isinstance(node, ast.IdentifierNode):
            return self.env.getVariable(node.value)

        if isinstance(node, ast.NumberNode):
            return node

        if isinstance(node, ast.BooleanNode):
                    return node