# coding=utf-8

import inspect


def to_english( iterable, separator=", ", conjunction=' and ', empty='empty',
                wrapper=None, pair_conjunction=None):
    """
    Convert list to a string containing an enumeration in plain English.

    :param iterable: an iterable of strings or objects that can be cast to a string

    :param separator: the text to insert between elements

    :param conjunction: the text used to connect the final element

    :param empty: the text to be used to represent an empty iterable

    :param wrapper: the text to surround the elements

    :param pair_conjunction: the conjunction to use between elements if there are exactly two of
                             them, defaults to conjunction

    >>> to_english( [], empty='nada' )
    'nada'
    >>> to_english( [ 1 ] )
    '1'
    >>> to_english( [ 1, 2 ], conjunction=' or ' )
    '1 or 2'
    >>> to_english( [ 1, 2, 3 ], conjunction=' or ')
    '1, 2 or 3'
    >>> to_english( [ 1, 2, 3 ], separator='; ', conjunction=' or ')
    '1; 2 or 3'
    >>> to_english( [ 1, 2, 3 ], conjunction=', and ', pair_conjunction=' and ' )
    '1, 2, and 3'
    >>> to_english( [ 1, 2 ], conjunction=', and ', pair_conjunction=' and ' )
    '1 and 2'
    >>> to_english( [ 1 ], conjunction=', and ', pair_conjunction=' and ' )
    '1'
    """
    i = iter( iterable )
    try:
        x = i.next( )
    except StopIteration:
        return empty
    r = [ ]
    while True:
        x = str( x )
        if wrapper is not None:
            x = wrapper + x + wrapper
        try:
            n = i.next( )
        except StopIteration:
            if len(r) > 2:
                r.append( conjunction )
            elif len(r) > 0:
                r.append( conjunction if pair_conjunction is None else pair_conjunction )
            r.append( x )
            break
        else:
            if r: r.append( separator )
            r.append( x )
            x = n
    return ''.join( r )


def interpolate( template, skip_frames=0, **kwargs ):
    """
    Interpolate {…} placeholders in the given template string with the given values or the local
    variables in the calling scope. The syntax of the format string is the same as for the
    built-in string format function. Explicitly passed keyword arguments take precedence over
    local variables which take precedence over global variables.

    Unlike with Python scoping rules, only the variables in a single frame are examined.

    Example usage:

    >>> x = 1
    >>> interpolate( "{x}" )
    '1'
    >>> interpolate( "{x}", x=2 )
    '2'
    >>> interpolate( "{x} {y}", y=2 )
    '1 2'

    Use

    from bd2k.util.strings import interpolate as fmt

    to import this function under a shortened alias.
    """
    return __interpolate( template, skip_frames, kwargs )


def interpolate_dict( template, dictionary, skip_frames=0 ):
    """
    Equivalent to

    interpolate( template, skip_frames, **dictionary )

    Example usage:

    >>> x = 1
    >>> interpolate_dict( "{x}", {} )
    '1'
    >>> interpolate_dict( "{x}", dict(x=2) )
    '2'
    >>> interpolate_dict( "{x} {y}", dict(y=2) )
    '1 2'
    """
    return __interpolate( template, skip_frames, dictionary )


# This is a separate function such that the depth to the client stack frame is the same for
# interpolate() and interpolate_dict()

def __interpolate( template, skip_frames, dictionary ):
    frame = inspect.currentframe( )
    for i in xrange( skip_frames + 2 ):
        prev_frame = frame
        frame = frame.f_back
        del prev_frame
    try:
        env = frame.f_globals.copy( )
        env.update( frame.f_locals )
        env.update( dictionary )
    finally:
        del frame
    return template.format( **env )
