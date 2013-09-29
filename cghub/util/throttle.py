from __future__ import absolute_import

import time
import threading
from cghub.util.threading import BoundedEmptySemaphore


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

    def throttle(self):
        # I think there is a race in Thread.start(), hence the lock
        with self.thread_start_lock:
            if not self.thread_started:
                self.thread.start( )
                self.thread_started = True
        self.semaphore.acquire( )

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
        :param min_interval: The minimum interval in seconds between invocations of the throttle
        method or, if this throttle is used as a decorator, invocations of the decorated method.
        """
        self.min_interval = min_interval
        self.per_thread = threading.local( )
        self.per_thread.last_invocation = None

    def throttle(self):
        """
        Sleeps the current thread if needed such that at least the configured minimum interval
        passes since the last invocation in the current thread.
        """
        now = time.time( )
        per_thread = self.per_thread
        if per_thread.last_invocation is not None:
            interval = now - per_thread.last_invocation
            if interval < self.min_interval:
                remainder = self.min_interval - interval
                time.sleep( remainder )
        per_thread.last_invocation = now

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            self.throttle( )
            return function( *args, **kwargs )

        return wrapper