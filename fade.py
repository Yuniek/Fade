import argparse
import fade

parser = argparse.ArgumentParser(
    prog="fade",
    description="The Fade programming language"
)

parser.add_argument(
    'file',
    nargs='?',
    help='program read from script file'
)

parser.add_argument(
    '--tokens',
    action='store_true',
    help='display generated tokens'
)

parser.add_argument(
    '--ast',
    action='store_true',
    help='display generated AST'
)

args = parser.parse_args()

env = fade.Environment()

def run(code):
    try:
        results = fade.run(code, env, args.tokens, args.ast)
        return True
            
    except fade.FadeError as error:
        print(error)
        return False

if args.file is None:
    while True:
        text = input('fade > ')

        if text == 'bye()': exit()

        run(text)
else:
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        parser.error(f"file not found: {args.file}")
    
    if not run(file_content): exit(1)