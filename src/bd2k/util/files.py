import errno
import os


def mkdir_p( path ):
    """
    The equivalent of mkdir -p
    """
    try:
        os.makedirs( path )
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir( path ):
            pass
        else:
            raise


def rm_f( path ):
    """
    Remove the file at the given path with os.remove(), ignoring errors caused by the file's absence.
    """
    try:
        os.remove( path )
    except OSError as e:
        if e.errno == errno.ENOENT:
            pass
        else:
            raise


if False:

    # These are not needed for Python 2.7 as Python's builtin file object's read() and write()
    # method are greedy. For Python 3.x these may be useful.

    def gread( readable, n ):
        """
        Greedy read. Read until readable is exhausted, and error occurs or the given number of bytes
        have been read. If it returns fewer than the requested number bytes if and only if the end of
        file has been reached.

        :type readable: io.FileIO
        """
        bufs = [ ]
        i = 0
        while i < n:
            buf = readable.read( n - i )
            m = len( buf )
            if m == 0:
                break
            bufs.append( buf )
            i += m
        return ''.join( bufs )


    def gwrite( writable, buf ):
        """
        Greedy write. Write until the entire buffer has been written to or an error occurs.

        :type writable: io.FileIO[str|bytearray]

        :type buf: str|bytearray
        """
        n = len( buf )
        i = 0
        while i < n:
            i += writable.write( buf[ i: ] )
