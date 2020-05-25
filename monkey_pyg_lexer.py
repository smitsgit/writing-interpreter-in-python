from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import *

__all__ = ['MonkeyLexer']


class MonkeyLexer(RegexLexer):
    name = 'Monkey'
    aliases = ['monkey']
    filenames = ['*.mk']

    tokens = {
        'root': [
            (r' .*\n', Text),
            (words(('else', 'if', 'let', 'return', 'fn'), suffix=r'\b'), Keyword),
            (r'(true|false)\b', Keyword.Constant),
        ]
    }
