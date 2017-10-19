from __future__ import division
# Copyright (c) 2014 Dominic Tarr
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

# Ported from JS found at https://github.com/dominictarr/d64



from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
class D64( object ):
    def __init__( self, special_chars ):
        super( D64, self ).__init__( )
        alphabet = 'PYFGCRLAOEUIDHTNSQJKXBMWVZpyfgcrlaoeuidhtnsqjkxbmwvz1234567890'
        self.alphabet = bytearray( sorted( alphabet + special_chars ) )
        self.lookup = bytearray( 255 )
        for i in range( 64 ):
            code = self.alphabet[ i ]
            self.lookup[ code ] = i

    def encode( self, data ):
        """
        >>> encode = standard.encode
        >>> encode('')
        ''
        >>> encode('\\x00')
        '..'
        >>> encode('\\x00\\x01')
        '..3'
        >>> encode('\\x00\\x01\\x02')
        '..31'
        >>> encode('\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07')
        '..31.kF40VR'
        """
        l = len( data )
        s = bytearray( old_div((l * 4 + 2), 3) )
        hang = 0
        j = 0
        a = self.alphabet
        for i in range( l ):
            v = ord( data[ i ] )
            r = i % 3
            if r == 0:
                s[ j ] = a[ v >> 2 ]
                j += 1
                hang = (v & 3) << 4
            elif r == 1:
                s[ j ] = a[ hang | v >> 4 ]
                j += 1
                hang = (v & 0xf) << 2
            elif r == 2:
                s[ j ] = a[ hang | v >> 6 ]
                j += 1
                s[ j ] = a[ v & 0x3f ]
                j += 1
                hang = 0
            else:
                assert False
        if l % 3:
            s[ j ] = a[ hang ]

        return str( s )

    def decode( self, e ):
        """
        >>> decode = standard.decode
        >>> decode('')
        ''
        >>> decode('..')
        '\\x00'
        >>> decode('..3')
        '\\x00\\x01'
        >>> decode('..31')
        '\\x00\\x01\\x02'
        >>> decode('..31.kF40VR')
        '\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07'
        """
        n = len( e )
        j = 0
        b = bytearray( old_div(n * 3, 4) )
        hang = 0
        l = self.lookup

        for i in range( n ):
            v = l[ ord( e[ i ] ) ]
            r = i % 4
            if r == 0:
                hang = v << 2
            elif r == 1:
                b[ j ] = hang | v >> 4
                j += 1
                hang = (v << 4) & 0xFF
            elif r == 2:
                b[ j ] = hang | v >> 2
                j += 1
                hang = (v << 6) & 0xFF
            elif r == 3:
                b[ j ] = hang | v
                j += 1
            else:
                assert False
        return bytes( b )


standard = D64( '._' )
