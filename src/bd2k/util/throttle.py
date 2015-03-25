from __future__ import absolute_import

import time
import threading
from bd2k.util.threading import BoundedEmptySemaphore


class GlobalThrottle:
    """
    A thread-safe rate limiter that throttles all threads globally. This should be used to
    regulate access to a global resource. It can be used as a function/method decorator or as a
    simple object, using the throttle() method. The token generation starts with the first call
    to throttle() or the decorated function. Each subsequent call to throttle() will then acquire
    a token, possibly having to wait until one becomes available. The number of unused tokens
    will not exceed a limit given at construction time. This is a very basic mechanism to
    prevent the resource from becoming swamped after longer pauses.
    """

    def __init__(self, min_interval, max_unused):
        self.min_interval = min_interval
        self.semaphore = BoundedEmptySemaphore( max_unused )
        self.thread_start_lock = threading.Lock( )
        self.thread_started = False
        self.thread = threading.Thread( target=self.generator )
        self.thread.daemon = True

    def generator(self):
        while True:
            try:
                self.semaphore.release( )
            except ValueError:
                pass
            time.sleep( self.min_interval )

    def throttle(self, wait=True):
        """
        If the wait parameter is True, this method returns True after suspending the current
        thread as necessary to ensure that no less than the configured minimum interval passed
        since the most recent time an invocation of this method returned True in any thread.

        If the wait parameter is False, this method immediatly returns True if at least the
        configured minimum interval has passed since the most recent time this method returned
        True in any thread, or False otherwise.
        """
        # I think there is a race in Thread.start(), hence the lock
        with self.thread_start_lock:
            if not self.thread_started:
                self.thread.start( )
                self.thread_started = True
        return self.semaphore.acquire( blocking=wait )

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            self.throttle( )
            return function( *args, **kwargs )

        return wrapper


class LocalThrottle:
    """
    A thread-safe rate limiter that throttles each thread independently. Can be used as a
    function or method decorator or as a simple object, using the throttle().
    """

    def __init__(self, min_interval):
        """
        Initialize this local throttle.

        :param min_interval: The minimum interval in seconds between invocations of the throttle
        method or, if this throttle is used as a decorator, invocations of the decorated method.
        """
        self.min_interval = min_interval
        self.per_thread = threading.local( )
        self.per_thread.last_invocation = None

    def throttle(self, wait=True):
        """
        If the wait parameter is True, this method returns True after suspending the current
        thread as necessary to ensure that no less than the configured minimum interval has
        passed since the last invocation of this method in the current thread returned True.

        If the wait parameter is False, this method immediatly returns True (if at least the
        configured minimum interval has passed since the last time this method returned True in
        the current thread) or False otherwise.
        """
        now = time.time( )
        last_invocation = self.per_thread.last_invocation
        if last_invocation is not None:
            interval = now - last_invocation
            if interval < self.min_interval:
                if wait:
                    remainder = self.min_interval - interval
                    time.sleep( remainder )
                else:
                    return False
        self.per_thread.last_invocation = now
        return True


    def __call__(self, function):
        def wrapper(*args, **kwargs):
            self.throttle( )
            return function( *args, **kwargs )

        return wrapper