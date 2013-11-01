from functools import wraps
import pwd
import grp


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