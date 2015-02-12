from __future__ import absolute_import

import codecs
import types
import logging


class Utf8SyslogFormatter( logging.Formatter ):
    """
    Works around http://bugs.python.org/issue14452
    """

    def format( self, record ):
        origGetMessage = record.getMessage

        def getMessage( _self ):
            msg = origGetMessage( )
            if isinstance( msg, unicode ):
                try:
                    # First check if we can represent the message as ASCII without loosing
                    # information. That we we can avoid writing the BOM unless absolutely necessary.
                    msg = msg.encode( 'ascii' )
                except UnicodeEncodeError:
                    msg = codecs.BOM + msg.encode( 'utf8' )
            return msg

        types.MethodType( getMessage, record, logging.LogRecord )
        record.getMessage = types.MethodType( getMessage, record, logging.LogRecord )
        return logging.Formatter.format( self, record )
