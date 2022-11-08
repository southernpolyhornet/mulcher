
import os
import typing

os.system('')

_ESC: str = u'\x1b['
_END: str = u'\x1b[0m'


def _clamp256(_n: int) -> int:
    return max(0, min(255, _n))


def _ansi_tc(*args: int, m: str) -> str:
    if not args:
        return f'{m};5;0'
    if len(args) == 1:
        return f"{m};5;{_clamp256(args[0])}"
    if len(args) == 2:
        return f"{m};2;{_clamp256(args[0])};{_clamp256(args[1])};0"
    return f"{m};2;{_clamp256(args[0])};{_clamp256(args[1])};{_clamp256(args[2])}"


def _fg_ANSI_TrueColor(*args: int) -> str:
    return _ansi_tc(*args, m='38')


def _bg_ANSI_TrueColor(*args: int) -> str:
    return _ansi_tc(*args, m='48')


class Colors:

    BLACK: str = '30'
    RED: str = '31'
    GREEN: str = '32'
    YELLOW: str = '33'
    BLUE: str = '34'
    MAGENTA: str = '35'
    CYAN: str = '36'
    WHITE: str = '37'

    @staticmethod
    def FG_CUSTOM(c: typing.Union[int, typing.Tuple[int, int, int]]) -> str:
        if isinstance(c, int):
            return _fg_ANSI_TrueColor(c)
        return _fg_ANSI_TrueColor(*c)

    @staticmethod
    def BG_CUSTOM(c: typing.Union[int, typing.Tuple[int, int, int]]) -> str:
        if isinstance(c, int):
            return _bg_ANSI_TrueColor(c)
        return _bg_ANSI_TrueColor(*c)


class TextStyle:

    def __new__(
            cls,
            fg: typing.Optional[str] = None,
            bg: typing.Optional[str] = None,
            blink: bool = False,
            bold: bool = False,
            underline: bool = False
    ) -> typing.Callable[[str], str]:

        _esc_s: str = _ESC + ';'.join(
            filter(
                None,
                [
                    '5' if blink else '',
                    '1' if bold else '',
                    '4' if underline else '',
                    fg,
                    bg
                ]
            )
        ) + 'm'

        def _ts(text: str) -> str:
            return _esc_s + text + _END

        return _ts


TextStyle_Timestamp: typing.Callable[[str], str] = TextStyle(fg=Colors.FG_CUSTOM((128, 128, 138)))
TextStyle_FunctionName: typing.Callable[[str], str] = TextStyle(fg=Colors.FG_CUSTOM((185, 130, 0)), bold=True)
TextStyle_Complete: typing.Callable[[str], str] = TextStyle(fg=Colors.GREEN, bold=True, underline=True)
TextStyle_Error: typing.Callable[[str], str] = TextStyle(fg=Colors.RED, bold=True, underline=True)
