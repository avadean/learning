intToStr = {1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            10: 'ten'
            }


class Colors:
    default = '\033[39m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    gray = '\033[37m'
    orange = '\033[38;5;166m'

    lightRed = '\033[91m'
    lightGreen = '\033[92m'
    lightYellow = '\033[93m'
    lightBlue = '\033[94m'
    lightMagenta = '\033[95m'
    lightCyan = '\033[96m'

    reset = '\033[0m'
    bold = '\033[1m'
    italicized = '\033[3m'
    underline = '\033[4m'
    blink = '\033[5m'

    question = bold + green
    options = underline + yellow
    hint = italicized + red
    answer = blue
