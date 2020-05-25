import sys
import getpass
import monkey_lexer
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from pygments.lexers import load_lexer_from_file


def main(argv):
    PROMPT = ">> "
    print(f"Hello {getpass.getuser()} This is the Monkey programming language!\n")
    print(f"Feel free to type in commands")
    suggestions = WordCompleter([item for item in monkey_lexer.keywords], ignore_case=True)
    lexer = load_lexer_from_file("/Users/smital/PycharmProjects/writing-interpreter-in-python/monkey_pyg_lexer.py", "MonkeyLexer")
    while True:
        # Todo: lexer=lexer Get the custom lexer working for monkey language
        data = prompt(f"{PROMPT}",
                      history=FileHistory('history.txt'),
                      auto_suggest=AutoSuggestFromHistory(),
                      completer=suggestions,
                      multiline=True


                      )
        lexer = monkey_lexer.Lexer(data)
        for item in lexer:
            print(item)


if __name__ == '__main__':
    main(sys.argv)
