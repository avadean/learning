from pygame import Color
from pygame.font import SysFont


intToStr = { 0: 'zero',
             1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
             6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
             11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
             16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'
             }

boolToStr = { True: 'yes', False: 'no' }

def getStrVersion(answer):
    if type(answer) is int:
        return intToStr.get(answer, None)

    if type(answer) is bool:
        return boolToStr.get(answer, None)


def wrapText(text, maxChars, indent=0):
    assert type(text) is str
    assert type(maxChars) is int
    assert type(indent) is int

    words = text.split(' ')

    wrappedText = []
    currentLine = ''
    currentLineLength = 0

    for word in words:
        lengthOfNewWord = len(word)

        if currentLineLength + lengthOfNewWord > maxChars:
            wrappedText.append(currentLine)
            currentLine = ' ' * indent + word + ' '
            currentLineLength = lengthOfNewWord + indent + 1

        elif currentLineLength + lengthOfNewWord == maxChars:
            currentLine += word
            wrappedText.append(currentLine)
            currentLine = ' ' * indent
            currentLineLength = indent

        else:
            currentLine += word + ' '
            currentLineLength += lengthOfNewWord + 1

    if currentLine.strip() != '':
        wrappedText.append(currentLine)

    return wrappedText


class Fonts:
    mainMenuButtons = SysFont('sfnsmono', size=24, bold=False, italic=False)
    mainMenuButtons.set_underline(True)

    mainMenuProfile = SysFont('sfnsmono', size=20, bold=False, italic=False)

    mainMenuTitle = SysFont('sfnsmono', size=24, bold=False, italic=False)

    quickPlayResponse = SysFont('sfnsmono', size=18, bold=False, italic=False)
    quickPlayQuestion = SysFont('sfnsmono', size=18, bold=False, italic=False)


class ScreenColors:
    white = Color('white')
    grey = Color('grey')
    black = Color('black')

    red = Color('red')
    orange = Color('orange')
    yellow = Color('yellow')
    green = Color('green')
    brown = Color('brown')
    pink = Color('pink')
    blue = Color('blue')
    purple = Color('purple')

    lightYellow = Color('light yellow')
    lightGreen = Color('light green')
    lightPink = Color('light pink')
    lightBlue = Color('light blue')

    darkRed = Color('dark red')
    darkOrange = Color('dark orange')
    darkGreen = Color('dark green')
    darkBlue = Color('dark blue')

    veryLightGreen = Color(212, 255, 228)
    veryLightPink = Color(255, 220, 255)
    veryLightBlue = Color(215, 235, 250)

    fill = veryLightPink

    mainMenuButtons = black
    mainMenuCurrentProfileText = black

    quickPlayBoxes = black

    question = black
    option = orange
    response = blue

    responseCorrect = darkGreen
    responseWrong = red


class PrintColors:
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
