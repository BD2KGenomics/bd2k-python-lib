from unittest import TestCase

from mock import MagicMock, call


class TestFiles( TestCase ):
    if False:
        from bd2k.util.files import gread, gwrite
        # See comment in module under test
        def test_gread( self ):
            for n in range( 0, 4 ):
                f = MagicMock( )
                # The mock file contains "12". Each read() invocation shall return one byte from that,
                # followed by the empty string for EOF.
                f.read.side_effect = [ '1', '2', '' ]
                # Read n bytes greedily
                # noinspection PyTypeChecker
                self.assertEqual( self.gread( f, n ), "12"[ :n ] )
                # First call to read() should request n bytes and then one less on each subsequent call.
                self.assertEqual( f.mock_calls, [ call.read( i ) for i in range( n, 0, -1 ) ] )

        def test_gwrite( self ):
            for n in range( 0, 3 ):
                f = MagicMock( )
                # Each write invocation shall write a single byte.
                f.write.side_effect = [ 1 ] * n
                s = "12"[ :n ]
                # noinspection PyTypeChecker
                self.gwrite( f, s )
                # The first call to write() should be passed the entire string, minus one byte off
                # the front for each subsequent call.
                self.assertEqual( f.mock_calls, [ call.write( s[ i: ] ) for i in range( 0, n ) ] )
