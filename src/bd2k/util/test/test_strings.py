import unittest

from bd2k.util.strings import interpolate
from bd2k.util.strings import to_english

foo = 4
bar = 1


class TestStrings( unittest.TestCase ):
    def test_interpolate( self ):
        bar = 2  # should override the global foo
        self.assertEquals( interpolate( "{foo}{bar}" ), "42" )

    def test_to_english( self ):
        self.assertEqual("'1', and '2'", to_english([1,2], wrapper="'"))
        self.assertEqual("foo, and bar", to_english(['foo','bar']))
        self.assertEqual("foo,and bar", to_english(['foo','bar'], separator=","))
        self.assertEqual("bar", to_english(['bar']))
        self.assertEqual("*1*", to_english([1], wrapper="*"))
        self.assertEqual("empty", to_english([]))
