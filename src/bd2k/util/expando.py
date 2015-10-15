class Expando(dict):
    """
    Pass inital attributes to the constructor:

    >>> o = Expando(foo=42)
    >>> o.foo
    42

    Dynamically create new attributes:

    >>> o.bar = 'hi'
    >>> o.bar
    'hi'

    Expando is a dictionary:

    >>> isinstance(o,dict)
    True
    >>> o['foo']
    42

    Works great with JSON:

    >>> import json
    >>> s='{"foo":42}'
    >>> o = json.loads(s,object_hook=Expando)
    >>> o
    {u'foo': 42}
    >>> o.foo
    42
    >>> o.bar = 'hi'
    >>> o
    {u'foo': 42, 'bar': 'hi'}

    And since Expando is a dict, it serializes back to JSON just fine:

    >>> json.dumps(o)
    '{"foo": 42, "bar": "hi"}'
    """

    def __init__( self, *args, **kwargs ):
        super( Expando, self ).__init__( *args, **kwargs )
        self.__slots__ = None
        self.__dict__ = self

class MagicExpando(Expando):
    """
    Use MagicExpando for chained attribute access. The first time a missing attribute is
    accessed, it will be set to a new child MagicExpando.

    >>> o=MagicExpando()
    >>> o.foo = 42
    >>> o
    {'foo': 42}
    >>> o.bar.hello = 'hi'
    >>> o
    {'foo': 42, 'bar': {'hello': 'hi'}}
    """
    def __getattribute__( self, name ):
        try:
            return super( Expando, self ).__getattribute__( name )
        except AttributeError:
            child = self.__class__( )
            self[name] = child
            return child

