import os

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


def writeFile(fileLines, file_):
    assert type(fileLines) is list
    assert all(type(line) is str for line in fileLines)
    assert type(file_) is str
    assert len(file_) > 0
    assert file_[-4:] == '.txt'
    assert os.getcwd() not in ['/', '/Users']

    with open(file_, 'w') as f:
        for line in fileLines:
            f.write(line + '\n')


def readFile(file_):
    with open(file_) as f:
        lines = f.read().splitlines()

    return lines


def wrapText(text, fontWidth, width, indent=0):
    assert type(text) is str
    assert type(fontWidth) is int
    assert type(width) is int
    assert type(indent) is int

    maxChars = width // fontWidth

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


def blitText(screen, text, font, color,
             left=None, top=None,
             center=False, centerHor=False, centerVer=False,
             topLeft=False, topRight=False, bottomLeft=False, bottomRight=False,
             leftOffset=0, topOffset=0):

    textObj = font.render(text, False, color)

    if topLeft:
        screen.blit(textObj, (leftOffset,
                              topOffset))
    elif topRight:
        screen.blit(textObj, (screen.get_width() - textObj.get_width() - leftOffset,
                              topOffset))
    elif bottomLeft:
        screen.blit(textObj, (leftOffset,
                              screen.get_height() - textObj.get_height() - topOffset))
    elif bottomRight:
        screen.blit(textObj, (screen.get_width() - textObj.get_width() - leftOffset,
                              screen.get_height() - textObj.get_height() - topOffset))
    elif center:
        screen.blit(textObj, ((screen.get_width() - textObj.get_width()) // 2,
                              (screen.get_height() - textObj.get_height()) // 2))
    elif centerHor:
        assert top is not None
        screen.blit(textObj, ((screen.get_width() - textObj.get_width()) // 2,
                               top))
    elif centerVer:
        assert left is not None
        screen.blit(textObj, (left,
                              (screen.get_height() - textObj.get_height()) // 2))
    else:
        assert left is not None and top is not None
        screen.blit(textObj, (left, top))

def blitTextWrapped(screen, text, font, color, left, width, startTop, lineSpacing=2, indent=0, maxLines=None):
    fontWidth, fontHeight = font.size("W")
    wrappedText = wrapText(text, fontWidth, width, indent)

    if maxLines is not None:
        assert type(maxLines) is int
        wrappedText = wrappedText[0:maxLines]

    textHeight = startTop
    for line in wrappedText:
        lineText = font.render(line, False, color)
        screen.blit(lineText, (left, textHeight))
        textHeight += fontHeight + lineSpacing

def blitListOfText(screen, textList, font, color, left, startTop, lineSpacing=2):
    fontWidth, fontHeight = font.size("W")

    textHeight = startTop
    for text in textList:
        lineText = font.render(text, False, color)
        screen.blit(lineText, (left, textHeight))
        textHeight += fontHeight + lineSpacing


class Fonts:
    buttons = SysFont('sfnsmono', size=24, bold=False, italic=False)

    mainMenuButtons = buttons
    mainMenuButtons.set_underline(True)

    mainMenuTitle = SysFont('sfnsmono', size=24, bold=False, italic=False)

    profileButtons = SysFont('sfnsmono', size=20, bold=False, italic=False)

    profileTitle = SysFont('sfnsmono', size=24, bold=False, italic=False)

    profile = SysFont('sfnsmono', size=22, bold=False, italic=False)
    profileList = SysFont('sfnsmono', size=18, bold=False, italic=False)

    timer = SysFont('sfnsmono', size=22, bold=False, italic=False)
    correctCount = SysFont('sfnsmono', size=22, bold=False, italic=False)

    quickPlayResponse = SysFont('sfnsmono', size=18, bold=False, italic=False)
    quickPlayLastResponse = SysFont('sfnsmono', size=24, bold=False, italic=False)
    quickPlayQuestion = SysFont('sfnsmono', size=18, bold=False, italic=False)
    quickPlaySummary = SysFont('sfnsmono', size=24, bold=False, italic=False)
    quickPlayQuestionSummary = SysFont('sfnsmono', size=14, bold=False, italic=False)


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

    buttons = black

    mainMenuButtons = buttons
    mainMenuTitle = black

    profileTitle = black

    currentProfileText = black

    quickPlayBoxes = black

    question = black
    option = orange
    response = blue
    summary = black

    timer = red

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
