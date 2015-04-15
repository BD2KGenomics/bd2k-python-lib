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


