from imghdr import what
from os import path
from PIL import Image


imagesDir = 'images/'

assert path.isdir(imagesDir),\
    '{} directory for images not found.'.format(imagesDir)


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


class Question:
    def __init__(self, question, answers, options=None, image=None, hint=None):
        self.question = None
        self.answers = None
        self.options = None
        self.image = None
        self.hint = None

        assert type(question) is str
        self.question = question

        assert type(answers) is list
        self.answers = [str(answer) for answer in answers]
        self.answers += [intToStr[answer] for answer in answers
                         if intToStr.get(answer, None) is not None]

        if options is not None:
            assert type(options) is list
            assert len(options) > 1

            self.options = [str(option) for option in options]

        if image is not None:
            assert type(image) is str
            assert what(imagesDir + image) in ['jpeg', 'png'],\
                '{} is not an image file'.format(imagesDir + image)

            self.image = Image(image)

        if hint is not None:
            assert type(hint) is str

            self.hint = hint

    def ask(self):
        if self.image is not None:
            self.image.show()

        prompt = '{}{}{}'.format(Colors.question,
                                 self.question,
                                 Colors.reset)

        if self.options is not None:
            prompt += ' {}{}{}'.format(Colors.options,
                                       self.options[0][0].upper() +
                                       self.options[0][1:].lower(),
                                       Colors.reset)

            if len(self.options) > 2:
                prompt += ', '
                for option in self.options[1:-1]:
                    prompt += '{}{}{}, '.format(Colors.options,
                                                option,
                                                Colors.reset)
                # prompt += ', '.join(self.options[1:-1])

            prompt += ' or {}{}{}?'.format(Colors.options,
                                           self.options[-1],
                                           Colors.reset)

        if self.hint is not None:
            prompt += ' {}({}){}'.format(Colors.hint,
                                         self.hint,
                                         Colors.reset)

        prompt += '\n    {}'.format(Colors.reset)

        response = input(prompt).strip()

        while response not in self.answers:
            if response == '':
                print(u'\u23F9  stopping.\n')
                return
            else:
                print(u'\u274C incorrect')
                response = input('    ').strip()

        # print(u'\u2713')
        print(u'\u2705 correct!\n')
