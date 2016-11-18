# Copyright (c) 2015 Hannes Schmidt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Inspired by Dominic Tarr's JavaScript at https://github.com/dominictarr/d64

class D32( object ):
    """
    Base32 encoding and decoding without padding, and using an arbitrary alphabet.
    """

    def __init__( self, alphabet ):
        super( D32, self ).__init__( )
        self.alphabet = bytearray( alphabet )
        self.lookup = bytearray( 255 )
        for i in xrange( 32 ):
            self.lookup[ self.alphabet[ i ] ] = i

    def encode( self, d ):
        """
        >>> encode = standard.encode
        >>> encode('')
        ''
        >>> encode('\\0')
        '22'
        >>> encode('\\xff')
        'zw'
        >>> encode('\\0\\1\\2\\3\\4')
        '222k62s6'
        >>> encode('\\0\\1\\2\\3\\4\\5')
        '222k62s62o'
        """
        m = len( d )
        n = (m * 8 + 4) / 5
        padding = 8 - n % 8
        e = bytearray( n + padding )
        i, j = 0, 0
        a = self.alphabet

        while i < m:
            if m - i < 5:
                g = bytearray( d[ i: ] + '\0' * (5 - (m - i)) )
            else:
                g = bytearray( d[ i:i + 5 ] )
            # bit              1          2          3
            # bit   01234567 89012345 67890123 45678901 23456789
            # byte  00000000 11111111 22222222 33333333 44444444
            # group 00000111 11222223 33334444 45555566 66677777
            e[ j + 0 ] = a[ g[ 0 ] >> 3 ]
            e[ j + 1 ] = a[ g[ 0 ] << 2 & 31 | g[ 1 ] >> 6 ]
            e[ j + 2 ] = a[ g[ 1 ] >> 1 & 31 ]
            e[ j + 3 ] = a[ g[ 1 ] << 4 & 31 | g[ 2 ] >> 4 ]
            e[ j + 4 ] = a[ g[ 2 ] << 1 & 31 | g[ 3 ] >> 7 ]
            e[ j + 5 ] = a[ g[ 3 ] >> 2 & 31 ]
            e[ j + 6 ] = a[ g[ 3 ] << 3 & 31 | g[ 4 ] >> 5 ]
            e[ j + 7 ] = a[ g[ 4 ] & 31 ]
            j += 8
            i += 5
        return str( e[ :-padding ] )

    def decode( self, e ):
        """
        >>> decode = standard.decode

        # >>> decode('222k62s62o')
        # '\\x00\\x01\\x02\\x03\\x04\\x05'
        # >>> decode('222k62s6')
        # '\\x00\\x01\\x02\\x03\\x04'
        >>> decode('zw')
        '\\xff'
        """
        n = len( e )
        m = n * 5 / 8
        padding = 5 - m % 5
        d = bytearray( m + padding )
        i, j = 0, 0
        l = self.lookup
        while j < n:
            if n - j < 8:
                g = [ l[ ord( x ) ] for x in e[ j: ] ] + [ 0 ] * (8 - (n - j))
            else:
                g = [ l[ ord( x ) ] for x in e[ j:j + 8 ] ]
            # bit              1          2          3
            # bit   01234567 89012345 67890123 45678901 23456789
            # byte  00000000 11111111 22222222 33333333 44444444
            # group 00000111 11222223 33334444 45555566 66677777
            d[ i + 0 ] = g[ 0 ] << 3 & 255 | g[ 1 ] >> 2
            d[ i + 1 ] = g[ 1 ] << 6 & 255 | g[ 2 ] << 1 & 255 | g[ 3 ] >> 4
            d[ i + 2 ] = g[ 3 ] << 4 & 255 | g[ 4 ] >> 1
            d[ i + 3 ] = g[ 4 ] << 7 & 255 | g[ 5 ] << 2 & 255 | g[ 6 ] >> 3
            d[ i + 4 ] = g[ 6 ] << 5 & 255 | g[ 7 ]
            j += 8
            i += 5
        return str( d[ :-padding ] )


# A variant of Base64 that maintains the lexicographical ordering such that for any given list of
# string l, map( decode, sorted( map( standard.encode, l ) ) == sorted( l )

standard = D32( '234567abcdefghijklmnopqrstuvwxyz' )

# A reimplementation of base64.b32encode and base64.b32encode, but faster and without padding:

base32 = D32( 'abcdefghijklmnopqrstuvwxyz234567' )
