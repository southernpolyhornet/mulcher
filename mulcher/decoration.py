
import time
import functools
import datetime
import sys

from style import *


def mulch(_func: typing.Callable) -> typing.Callable:

    f_name: str = _func.__name__

    @functools.wraps(_func)
    def _fw(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        _t1: float = time.time()
        sys.stdout.write(
            f"{TextStyle_Timestamp(datetime.datetime.fromtimestamp(_t1).isoformat())} "
            f"[ '{TextStyle_FunctionName(f_name)}' ] :: "
        )
        sys.stdout.flush()
        try:
            _r: typing.Any = _func(*args, **kwargs)
            _t2: float = time.time()
            sys.stdout.write(TextStyle_Complete('Complete!') + f" (dT={(_t2-_t1) * 1000:0.3f}ms)\n")
            sys.stdout.flush()
        except Exception as E:
            sys.stdout.write(TextStyle_Error('FAILED!\n'))
            sys.stdout.flush()
            raise E
        return _r

    return _fw
