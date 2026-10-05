from .lexer         import Lexer
from .              import ast
from .parser        import Parser
from .environment   import Environment
from .interpreter   import Interpreter
from .errors        import FadeError
import json

# ##################################
# Run function to execute the code
# ##################################

def run(text:str, env, show_tokens:bool=False, show_ast:bool=False):
    """
    text should be a fade code.
    """
    

    lexer = Lexer(text)
    tokens = lexer.tokenize()
    if show_tokens is True:
        print(tokens)
    
    parser = Parser(tokens)
    tree = parser.parse()

    if tree is None:
        return
    
    if show_ast is True:
        print(json.dumps(
            tree.to_dict(),
            indent=4
        ))
    
    if not (show_tokens or show_ast) and isinstance(tree, ast.ASTNode):
        interpreter = Interpreter(tree, env)
        interpreter.evaluate()
    