# coding=utf-8

import inspect


def interpolate( template, skip_frames=0, **kwargs ):
    """
    Interpolate {…} placeholders in the given template string with the given values or the local
    variables in the calling scope. The syntax of the format string is the same as for
    the built-in string format function.

    Example usage:

    >>> x = 1
    >>> interpolate( "{x}" )
    '1'
    >>> interpolate( "{x}", x=2 )
    '2'

    Use

    from bd2k.util.strings import interpolate as fmt

    to import this function under a shortened alias.
    """
    return __interpolate( template, skip_frames, kwargs )


def interpolate_dict( template, skip_frames, dictionary ):
    """
    Equivalent to

    interpolate( template, **dictionary )
    """
    return __interpolate( template, dictionary )


# This is a separate function such that the depth to the client stack frame is the same for
# interpolate() and interpolate_dict()

def __interpolate( template, skip_frames, dictionary ):
    if not dictionary:
        frame = inspect.currentframe( )
        for i in xrange( skip_frames + 2 ):
            prev_frame = frame
            frame = frame.f_back
            del prev_frame
        try:
            dictionary = frame.f_globals.copy( )
            dictionary.update( frame.f_locals )
        finally:
            del frame
    return template.format( **dictionary )
