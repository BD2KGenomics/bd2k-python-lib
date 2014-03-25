from functools import wraps
import pwd
import grp
import re


def uid_to_name( uid ):
    return pwd.getpwuid( uid ).pw_name


def gid_to_name( gid ):
    return grp.getgrgid( gid ).gr_name


def name_to_uid( name ):
    return pwd.getpwnam( name ).pw_uid


def name_to_gid( name ):
    return grp.getgrnam( name ).gr_gid


def memoize( f ):
    """
    A decorator that memoizes a function result based on its parameters. For example, this can be
    used in place of lazy initialization.
    """
    memory = { }

    @wraps( f )
    def new_f( *args ):
        if args not in memory:
            memory[ args ] = f( *args )
        return memory[ args ]

    return new_f


def properties( obj ):
    """
    Returns a dictionary with one entry per attribute of the given object. The key being the
    attribute name and the value being the attribute value. Attributes starting in two
    underscores will be ignored. This function is an alternative to vars() which only returns
    instance variables, not properties. Note that methods are returned as well but the value in
    the dictionary is the method, not the return value of the method.

    >>> class Foo():
    ...     def __init__(self):
    ...         self.var = 1
    ...     @property
    ...     def prop(self):
    ...         return self.var + 1
    ...     def meth(self):
    ...         return self.var + 2
    >>> foo = Foo()
    >>> properties( foo ) == { 'var':1, 'prop':2, 'meth':foo.meth }
    True

    Note how the entry for prop is not a bound method (i.e. the getter) but a the return value of
    that getter.
    """
    return dict( (attr, getattr( obj, attr ))
        for attr in dir( obj )
        if not attr.startswith( '__' ) )


def ilen( it ):
    """
    Return the number of elements in an iterable

    >>> ilen(xrange(0,100))
    100
    """
    return sum( 1 for _ in it )


def rfc3339_datetime_re( anchor=True ):
    """
    Returns a regular expression for syntactic validation of ISO date-times, RFC-3339 date-times
    to be precise.


    >>> bool( rfc3339_datetime_re().match('2013-11-06T15:56:39Z') )
    True

    >>> bool( rfc3339_datetime_re().match('2013-11-06T15:56:39.123Z') )
    True

    >>> bool( rfc3339_datetime_re().match('2013-11-06T15:56:39-08:00') )
    True

    >>> bool( rfc3339_datetime_re().match('2013-11-06T15:56:39.123+11:00') )
    True

    It anchors the matching to the beginning and end of a string by default ...

    >>> bool( rfc3339_datetime_re().search('bla 2013-11-06T15:56:39Z bla') )
    False

    ... but that can be changed:

    >>> bool( rfc3339_datetime_re( anchor=False ).search('bla 2013-11-06T15:56:39Z bla') )
    True

    >>> bool( rfc3339_datetime_re( anchor=False ).match('2013-11-06T15:56:39Z bla') )
    True

    Keep in mind that re.match() always anchors at the beginning:

    >>> bool( rfc3339_datetime_re( anchor=False ).match('bla 2013-11-06T15:56:39Z') )
    False

    It does not check whether the actual value is a semantically valid datetime:

    >>> bool( rfc3339_datetime_re().match('9999-99-99T99:99:99.9-99:99') )
    True
    """
    return re.compile(
        ( '^' if anchor else '' ) +
        '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})' +
        ( '$' if anchor else '' ) )


def strict_bool( s ):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError( 'Not a valid bool literal' )