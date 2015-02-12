import re


def quote(s, level=1):
    for i in xrange( 0, level ):
        s = _quote( s )
    return s


_find_unsafe = re.compile( r'[^\w@%+=:,./-]' ).search


def _quote(s):
    """
    Return a shell-escaped version of the string *s*.

    Stolen from Python 3's shlex module
    """
    if not s:
        return "''"
    if _find_unsafe( s ) is None:
        return s

    # use single quotes, and put single quotes into double quotes
    # the string $'b is then quoted as '$'"'"'b'
    return "'" + s.replace( "'", "'\"'\"'" ) + "'"


