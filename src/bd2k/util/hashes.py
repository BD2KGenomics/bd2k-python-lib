from builtins import str
from past.builtins import basestring
def hash_json( hash_obj, value ):
    """
    Compute the hash of a parsed JSON value using the given hash object. This function does not
    hash the JSON value, it hashes the object tree that is the result of parsing a string in JSON
    format. Hashables (JSON objects) are hashed entry by entry in order of the lexicographical
    ordering on the keys. Iterables are hashed in their inherent order.

    If value or any of its children is an iterable with non-deterministic ordering of its
    elements, e.g. a set, this method will yield non-deterministic results.

    :param hash_obj: one of the Hash objects in hashlib, or any other object that has an update(s)
           method accepting a single string.

    :type value: int|str|float|Iterable[type(obj)]|Hashable[str,type(obj)]
    :param value: The value to be hashed

    >>> import hashlib
    >>> from builtins import str
    >>> def actual(x): h = hashlib.md5(); hash_json(h,x); return h.hexdigest()
    >>> def expect(s): h = hashlib.md5(); h.update(s.encode('utf-8')); return h.hexdigest()

    >>> actual(0) == expect('0')
    True
    >>> actual(0.0) == expect('0.0')
    True
    >>> actual(0.1) == expect('0.1')
    True
    >>> actual(True) == expect('true')
    True
    >>> actual(False) == expect('false')
    True
    >>> actual(u"") == expect(u'""')
    True
    >>> actual([]) == expect('[]')
    True
    >>> actual([0]) == expect('[0]')
    True
    >>> actual([0,1]) == expect('[0,1]')
    True
    >>> actual({}) == expect('{}')
    True
    >>> actual({'':0}) == expect('{:0}')
    True
    >>> actual({'0':0}) == expect('{0:0}')
    True
    >>> actual({'0':0,'1':1}) == expect('{0:0,1:1}')
    True
    >>> actual({'':[]}) == expect('{:[]}')
    True
    >>> actual([{}]) == expect('[{}]')
    True
    >>> actual({0:0})
    Traceback (most recent call last):
    ...
    ValueError: Dictionary keys must be strings, not type "int".
    >>> actual(object())
    Traceback (most recent call last):
    ...
    ValueError: Type "object" is not supported.
    """
    try:
        items = iter(value.items( ))
    except AttributeError:
        # Must check for string before testing iterability since strings are iterable
        if isinstance( value, str ):
            _hash_string( hash_obj, value )
        else:
            try:
                iterator = iter( value )
            except TypeError:
                # We must check for bool first since it is subclass of int (wrongly, IMHO)
                if isinstance( value, bool ):
                    _hash_bool( hash_obj, value )
                elif isinstance( value, (int, float) ):
                    _hash_number( hash_obj, value )
                else:
                    raise ValueError( 'Type "%s" is not supported.' % type( value ).__name__ )
            else:
                _hash_iterable( hash_obj, iterator )
    else:
        _hash_hashable( hash_obj, items )


def _hash_number( hash_obj, n ):
    hash_obj.update( str( n ).encode('utf-8') )


def _hash_bool( hash_obj, b ):
    hash_obj.update( str('true' if b else 'false' ).encode('utf-8'))


def _hash_string( hash_obj, s ):
    hash_obj.update( '"'.encode('utf-8') )
    hash_obj.update( s.encode('utf-8') )
    hash_obj.update( '"'.encode('utf-8') )


def _hash_iterable( hash_obj, items ):
    hash_obj.update( '['.encode('utf-8') )
    try:
        item = next( items )
        hash_json( hash_obj, item )
        while True:
            item = next( items )
            hash_obj.update( ','.encode('utf-8') )
            hash_json( hash_obj, item )
    except StopIteration:
        pass
    hash_obj.update( ']'.encode('utf-8') )


def _hash_hashable( hash_obj, items ):
    items = iter( sorted( items ) )
    hash_obj.update( '{'.encode('utf-8') )
    try:
        item = next( items )
        _hash_hashable_item( hash_obj, item )
        while True:
            item = next( items )
            hash_obj.update( ','.encode('utf-8') )
            _hash_hashable_item( hash_obj, item )
    except StopIteration:
        pass
    hash_obj.update( '}'.encode('utf-8') )


def _hash_hashable_item( hash_obj, k_v ):
    (k, v) = k_v
    if isinstance( k, basestring ):
        hash_obj.update( k.encode('utf-8') )
        hash_obj.update( ':'.encode('utf-8') )
        hash_json( hash_obj, v )
    else:
        raise ValueError( 'Dictionary keys must be strings, not type "%s".' % type( k ).__name__ )
