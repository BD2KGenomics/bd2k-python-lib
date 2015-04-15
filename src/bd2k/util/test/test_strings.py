import unittest

from bd2k.util.strings import interpolate

foo = 4
bar = 1


class TestStrings( unittest.TestCase ):
    def test_interpolate( self ):
        bar = 2  # should override the global foo
        self.assertEquals( interpolate( "{foo}{bar}" ), "42" )
