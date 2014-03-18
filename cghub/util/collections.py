from __future__ import absolute_import

import collections


class OrderedSet( collections.MutableSet ):
    """
    An ordered set from http://code.activestate.com/recipes/576694/

    Note: Maybe leaky, may have O(N) lookup by index

    TODO: Consider https://github.com/LuminosoInsight/ordered-set which uses a native Python list
    instead of a linked list

    >>> s = OrderedSet( 'abracadaba' )
    >>> s
    OrderedSet(['a', 'b', 'r', 'c', 'd'])
    >>> t = OrderedSet( 'simsalabim' )
    >>> t
    OrderedSet(['s', 'i', 'm', 'a', 'l', 'b'])
    >>> s | t
    OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
    >>> s & t
    OrderedSet(['a', 'b'])
    >>> s - t
    OrderedSet(['r', 'c', 'd'])
    >>> t - s
    OrderedSet(['s', 'i', 'm', 'l'])
    >>> OrderedSet( reversed( s ) )
    OrderedSet(['d', 'c', 'r', 'b', 'a'])
    >>> s.pop()
    'd'
    >>> s
    OrderedSet(['a', 'b', 'r', 'c'])
    >>> s.discard('b')
    >>> s
    OrderedSet(['a', 'r', 'c'])
    >>> s.pop( last=False )
    'a'
    >>> s
    OrderedSet(['r', 'c'])
    >>> s.union( t )
    >>> s
    OrderedSet(['r', 'c', 's', 'i', 'm', 'a', 'l', 'b'])

    >>> s = OrderedSet()
    >>> s
    OrderedSet()
    >>> s.pop()
    Traceback (most recent call last):
    ....
    KeyError: 'set is empty'
    >>> OrderedSet( "aba" ) == OrderedSet( "ab" )
    True
    >>> OrderedSet( "aba" ) == OrderedSet( "abc" )
    False
    >>> OrderedSet( "aba" ) == OrderedSet( "ba" )
    False
    >>> OrderedSet( "aba" ) == set( "ba" )
    True
    """

    def __init__( self, iterable=None ):
        self.end = end = [ ]
        end += [ None, end, end ]  # sentinel node for doubly linked list
        self.map = { }  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__( self ):
        return len( self.map )

    def __contains__( self, key ):
        return key in self.map

    def add( self, key ):
        if key not in self.map:
            end = self.end
            curr = end[ 1 ]
            curr[ 2 ] = end[ 1 ] = self.map[ key ] = [ key, curr, end ]

    def discard( self, key ):
        if key in self.map:
            key, prev, next = self.map.pop( key )
            prev[ 2 ] = next
            next[ 1 ] = prev

    def __iter__( self ):
        end = self.end
        curr = end[ 2 ]
        while curr is not end:
            yield curr[ 0 ]
            curr = curr[ 2 ]

    def __reversed__( self ):
        end = self.end
        curr = end[ 1 ]
        while curr is not end:
            yield curr[ 0 ]
            curr = curr[ 1 ]

    def pop( self, last=True ):
        if not self:
            raise KeyError( 'set is empty' )
        key = self.end[ 1 ][ 0 ] if last else self.end[ 2 ][ 0 ]
        self.discard( key )
        return key

    def __repr__( self ):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list( self ))

    def __eq__( self, other ):
        if isinstance( other, OrderedSet ):
            return len( self ) == len( other ) and list( self ) == list( other )
        return set( self ) == set( other )

    def union(self,other):
        self |= other