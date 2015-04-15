# coding=utf-8

import inspect


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
