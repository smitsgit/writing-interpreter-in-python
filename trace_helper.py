import sys
from functools import wraps


class TraceCalls(object):
    """ Use as a decorator on functions that should be traced. Several
        functions can be decorated - they will all be indented according
        to their call depth.
    """

    def __init__(self, stream=sys.stdout, indent_step=4, show_ret=False, debug=False):
        self.stream = stream
        self.indent_step = indent_step
        self.show_ret = show_ret
        self.debug = debug

        # This is a class attribute since we want to share the indentation
        # level between different traced functions, in case they call
        # each other.
        TraceCalls.cur_indent = 0

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if self.debug:
                indent = ' ' * TraceCalls.cur_indent
                argstr = ', '.join(
                    [str(a) for a in args[1:]] +
                    ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])
                self.stream.write('\n%s BEGIN %s(%s)\n' % (indent, fn.__name__, argstr))

                TraceCalls.cur_indent += self.indent_step
            ret = fn(*args, **kwargs)

            if self.debug:
                TraceCalls.cur_indent -= self.indent_step
                self.stream.write('%s END %s(%s)\n\n' % (indent, fn.__name__, argstr))

                if self.show_ret:
                    self.stream.write('%s--> %s\n' % (indent, ret))
            return ret

        return wrapper
