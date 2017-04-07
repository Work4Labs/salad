from django.conf import settings


# this controls the polling frequency when trying to see if elements
# exist in the DOM, default to 0.5 seconds.
POLL_FREQUENCY = getattr(settings, "SALAD_POLL_FREQUENCY", 0.5)

# this controls the default timeout if not timeout is passed to
# steps that try to find elements, default to 0 seconds.
DEFAULT_TIMEOUT = getattr(settings, "SALAD_DEFAULT_TIMEOUT", 0)

# this controls a multiplier that makes it possible to adjust the timeouts
# for steps trying to find elements, defaults to 1.
TIMEOUT_MULTIPLIER = getattr(settings, "SALAD_TIMEOUT_MULTIPLIER", 1)
