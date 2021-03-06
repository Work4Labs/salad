import time

from . import config


class SaladWaiter(object):

    def __init__(self, timeout, poll_frequency=config.POLL_FREQUENCY, ignored_exceptions=None):
        """Constructor
           Args:
            - timeout - Number of seconds before timing out
            - poll_frequency - sleep interval between calls
              By default, it is 0.5 second.
            - ignored_exceptions - iterable structure of exception classes ignored during calls.

           Example:
            from salad.waiter import SaladWaiter
            element = SaladWaiter(10).until(False, some_method, method_argument1, method_argument2,..)
        """
        self._timeout = (timeout or config.DEFAULT_TIMEOUT) * config.TIMEOUT_MULTIPLIER
        self._poll = poll_frequency
        # avoid the divide by zero
        if self._poll == 0:
            self._poll = config.POLL_FREQUENCY
        exceptions = []
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError: # ignored_exceptions is not iterable
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def _until(self, negate, method, *args):
        """The provided method should return either True or False.
        It is then called until proper return value appears according to negate
        OR until timeout happens"""
        end_time = time.time() + self._timeout
        while(True):
            try:
                value = method(*args)
                if not negate:
                    if value:
                        return value
                else:
                    if not value:
                        return value
            except self._ignored_exceptions:
                pass
            time.sleep(self._poll)
            if(time.time() > end_time):
                break
        raise TimeoutException("%s did not return expected return value within %s seconds." % (method.func_name, self._timeout))

    def until(self, method, *args):
        return self._until(False, method, *args)

    def until_not(self, method, *args):
        return self._until(True, method, *args)


class TimeoutException(Exception):
    pass
