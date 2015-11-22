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

from __future__ import absolute_import
from unittest import TestCase
from bd2k.util.d64 import standard as d64
import os


class TestD64( TestCase ):
    def test( self ):
        data = [ (os.urandom( i ), i) for i in xrange( 1000 ) ]
        encoded_data = [ (d64.encode( d ), i) for d, i in data ]
        decoded_data = [ (d64.decode( s ), i) for s, i in encoded_data ]
        self.assertEqual( data, decoded_data )
        # Ensure that lexicographical sort is consistent between data and encoded data
        self.assertEqual( zip( *sorted( data ) )[ 1 ], zip( *sorted( encoded_data ) )[ 1 ] )
