from itertools import takewhile, izip, izip_longest, dropwhile, imap


def common_prefix( xs, ys ):
    """
    >>> list( common_prefix('','') )
    []
    >>> list( common_prefix('A','') )
    []
    >>> list( common_prefix('','A') )
    []
    >>> list( common_prefix('A','A') )
    ['A']
    >>> list( common_prefix('AB','A') )
    ['A']
    >>> list( common_prefix('A','AB') )
    ['A']
    >>> list( common_prefix('A','B') )
    []
    """
    return imap( lambda (x, y): x, takewhile( lambda (a, b): a == b, izip( xs, ys ) ) )


def disparate_suffix( xs, ys ):
    """
    >>> list( disparate_suffix('','') )
    []
    >>> list( disparate_suffix('A','') )
    [('A', None)]
    >>> list( disparate_suffix('','A') )
    [(None, 'A')]
    >>> list( disparate_suffix('A','A') )
    []
    >>> list( disparate_suffix('AB','A') )
    [('B', None)]
    >>> list( disparate_suffix('A','AB') )
    [(None, 'B')]
    >>> list( disparate_suffix('A','B') )
    [('A', 'B')]
    """
    return dropwhile( lambda (a, b): a == b, izip_longest( xs, ys ) )

