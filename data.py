import os

from pygame import Color, draw, Rect
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
             horOffset=0, verOffset=0):

    textObj = font.render(text, False, color)

    if topLeft:
        screen.blit(textObj, (horOffset,
                              verOffset))
    elif topRight:
        screen.blit(textObj, (screen.get_width() - textObj.get_width() - horOffset,
                              verOffset))
    elif bottomLeft:
        screen.blit(textObj, (horOffset,
                              screen.get_height() - textObj.get_height() - verOffset))
    elif bottomRight:
        screen.blit(textObj, (screen.get_width() - textObj.get_width() - horOffset,
                              screen.get_height() - textObj.get_height() - verOffset))
    elif center:
        screen.blit(textObj, ((screen.get_width() - textObj.get_width()) // 2,
                              (screen.get_height() - textObj.get_height()) // 2))
    elif centerHor:
        assert type(top) is int

        screen.blit(textObj, ((screen.get_width() - textObj.get_width()) // 2,
                               top - textObj.get_height() // 2))
    elif centerVer:
        assert type(left) is int

        screen.blit(textObj, (left - textObj.get_width() // 2,
                              (screen.get_height() - textObj.get_height()) // 2))
    else:
        assert type(left) is int
        assert type(top) is int

        screen.blit(textObj, (left - textObj.get_width() // 2,
                              top - textObj.get_height() // 2))

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

def blitListOfText(screen, textList, font, color,
                   left=None, startTop=None,
                   center=False, centerHor=False, centerVer=False,
                   lineSpacing=2):
    fontWidth, fontHeight = font.size("W")

    if center:
        textHeight = startTop
        for text in textList:
            lineText = font.render(text, False, color)
            screen.blit(lineText, ((screen.get_width() - lineText.get_width()) // 2,
                                  (screen.get_height() - lineText.get_height()) // 2))
            textHeight += fontHeight + lineSpacing

    elif centerHor:
        assert type(startTop) is int

        textHeight = startTop
        for text in textList:
            lineText = font.render(text, False, color)
            screen.blit(lineText, ((screen.get_width() - lineText.get_width()) // 2,
                                   textHeight))
            textHeight += fontHeight + lineSpacing

    elif centerVer:
        assert type(left) is int

        textHeight = startTop
        for text in textList:
            lineText = font.render(text, False, color)
            screen.blit(lineText, (left,
                                   (screen.get_height() - lineText.get_height()) // 2))
            textHeight += fontHeight + lineSpacing

    else:
        assert type(left) is int
        assert type(startTop) is int

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
    profileHeader = SysFont('sfnsmono', size=18, bold=False, italic=False)
    profileHeader.set_underline(True)

    profile = SysFont('sfnsmono', size=22, bold=False, italic=False)
    profileList = SysFont('sfnsmono', size=18, bold=False, italic=False)

    settings = SysFont('sfnsmono', size=18, bold=False, italic=False)
    settingsTitle = SysFont('sfnsmono', size=24, bold=False, italic=False)

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

    profileButtons = buttons

    profileTitle = black

    settingsTitle = black

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


class Button:
    def __init__(self, text='', optionList=None,
                 width=None, height=None,
                 left=None, top=None,
                 screenWidth=None, screenHeight=None,
                 center=False, centerHor=False, centerVer=False,
                 topLeft=False, topRight=False, bottomLeft=False, bottomRight=False,
                 horOffset=0, verOffset=0,
                 color=None, highlightColor=None, borderColor=None, font=None):

        assert type(text) is str

        if optionList is not None:
            assert type(optionList) is list
            assert all(type(option) == str for option in optionList)

        assert type(width) is int
        assert type(height) is int

        assert type(center) is bool
        assert type(centerHor) is bool
        assert type(centerVer) is bool
        assert type(topLeft) is bool
        assert type(topRight) is bool
        assert type(bottomLeft) is bool
        assert type(bottomRight) is bool

        if center:
            assert type(screenWidth) is int
            assert type(screenHeight) is int

        elif centerHor:
            assert type(screenWidth) is int
            assert type(top) is int

        elif centerVer:
            assert type(left) is int
            assert type(screenHeight) is int

        elif topLeft:
            assert type(horOffset) is int
            assert type(verOffset) is int

        elif topRight:
            assert type(horOffset) is int
            assert type(verOffset) is int
            assert type(screenWidth) is int

        elif bottomLeft:
            assert type(horOffset) is int
            assert type(verOffset) is int
            assert type(screenHeight) is int

        elif bottomRight:
            assert type(horOffset) is int
            assert type(verOffset) is int
            assert type(screenWidth) is int
            assert type(screenHeight) is int

        else:
            assert type(left) is int
            assert type(top) is int

        if topLeft:
            self.left = horOffset
            self.top = verOffset

        elif topRight:
            self.left = screenWidth - width - horOffset
            self.top = verOffset

        elif bottomLeft:
            self.left = horOffset
            self.top = screenHeight - height - verOffset

        elif bottomRight:
            self.left = screenWidth - width - horOffset
            self.top = screenHeight - height - verOffset

        elif center:
            self.left = (screenWidth - width) // 2
            self.top = (screenHeight - height) // 2

        elif centerHor:
            self.left = (screenWidth - width) // 2
            self.top = top

        elif centerVer:
            self.left = left
            self.top = (screenHeight - height) // 2

        else:
            self.left = left
            self.top = top

        if color is not None:
            assert type(color) is Color

        if highlightColor is not None:
            assert type(highlightColor) is Color

        if borderColor is not None:
            assert type(borderColor) is Color

        #assert type(font) is SysFont

        self.width = width
        self.height = height

        self.rect = Rect(self.left, self.top, self.width, self.height)

        self.text = text
        self.optionList = optionList

        self.color = color if color is not None else False
        self.highlightColor = highlightColor if highlightColor is not None else False
        self.borderColor = borderColor if borderColor is not None else False
        self.font = font

        self.selected = False

    def draw(self, screen):
        if self.selected and self.highlightColor:
            draw.rect(screen, self.highlightColor, self.rect)
        elif self.color:
            draw.rect(screen, self.color, self.rect)

        if self.borderColor:
            draw.rect(screen, self.borderColor, self.rect, 2)

        text = self.font.render(self.text, False, ScreenColors.black)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def updateText(self, newText):
        assert type(newText) is str

        self.text = newText

    def clicked(self, mousePos):
        mouseX, mouseY = mousePos

        if (self.left <= mouseX <= (self.left + self.width)) and (self.top <= mouseY <= (self.top + self.height)):
            return True

        return False
