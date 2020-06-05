import sys
import getpass
from lexer import monkey_lexer
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from pygments.lexers import load_lexer_from_file
from parser import Parser
from evaluator.peval import eval

MONKEY = """\
            __,__
   .--.  .-"     "-.  .--. 
  / .. \/  .-. .-.  \/ ..  |
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"`` ``"-./, -' /
   `'-' /_   ^ ^   _\ '-'`
       |  \._   _./  |
       \   \ `~` /   /
       '._ '-=-' _.'
           '~---~'
       """

def main(argv):
    PROMPT = ">> "
    print(f"Hello {getpass.getuser()}, This is the Monkey programming language!\n")
    print(f"{MONKEY}")
    print(f"Feel free to type in commands")
    suggestions = WordCompleter([item for item in monkey_lexer.keywords], ignore_case=True)
    lexer = load_lexer_from_file("/Users/smital/PycharmProjects/writing-interpreter-in-python/monkey_pyg_lexer.py",
                                 "MonkeyLexer")
    while True:
        # TODO: lexer=lexer Get the custom lexer working for monkey language
        data = prompt(f"{PROMPT}",
                      history=FileHistory('history.txt'),
                      auto_suggest=AutoSuggestFromHistory(),
                      completer=suggestions,
                      multiline=False)
        lexer = monkey_lexer.Lexer(data)
        parser = Parser.new(lexer)
        program = parser.parse()
        output = eval(program)
        print(output)


if __name__ == '__main__':
    main(sys.argv)
