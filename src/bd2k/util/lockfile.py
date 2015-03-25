from __future__ import absolute_import

import errno
import logging as log
import os
from lockfile.pidlockfile import PIDLockFile


class SmartPIDLockFile( PIDLockFile ):
    """
    A PID lock file that breaks the lock if the owning process doesn't exist
    """

    def process_alive(self, pid):
        try:
            os.kill( pid, 0 )
            # now we know the process exists
            return True
        except OSError as e:
            if e.errno == errno.ESRCH:
                # now we know the process doesn't exist
                return False
            else:
                # now we're not sure
                return None

    def acquire(self, timeout=None):
        owner = self.read_pid( )
        if owner is not None and owner != os.getpid( ) and self.process_alive( owner ) is False:
            log.warn( "Breaking lock '%s' since owning process %i is dead."
                      % ( self.lock_file, owner ) )
            self.break_lock( )
        PIDLockFile.acquire( self, timeout )