from data import Colors, intToStr
from imghdr import what
from os import path
from PIL import Image


imagesDir = 'images/'

assert path.isdir(imagesDir),\
    '{} directory for images not found.'.format(imagesDir)


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

    def ask(self, keepAsking=False):
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
                return 0
            elif keepAsking:
                print(u'\u274C incorrect')
                response = input('    ').strip()
            else:
                print(u'\u274C incorrect\n')
                return 0

        # print(u'\u2713')
        print(u'\u2705 correct!\n')

        return 1


cellQuestions = [Question('How many cells is a prokaryote?',
                          [1]),
                 Question('How many cells is a eukaryote?',
                          ['many'],
                          ['one', 'many'])
                 ]

questions = cellQuestions
