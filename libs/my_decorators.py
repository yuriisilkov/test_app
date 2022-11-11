import logging
from nose import SkipTest


logger = logging.getLogger("My_logs")


def description(msg):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result == 'test_skipped':
                raise SkipTest('SKIPPED')
            if not result:
                logger.error(f"FAILED: {msg}")
                assert result, msg
            logger.info(f"PASSED: {msg}")
            return result
        return wrapper
    return decorator