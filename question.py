from data import Colors, intToStr
from difflib import SequenceMatcher
from imghdr import what
from os import path
from PIL import Image
from random import shuffle


imagesDir = 'images/'

assert path.isdir(imagesDir),\
    '{} directory for images not found.'.format(imagesDir)


class Question:
    def __init__(self, question=None, answer=None, answers=None,
                 options=None, image=None, hint=None):
        self.question = ''
        self.answer = ''
        self.answers = []
        self.options = None
        self.image = None
        self.hint = None

        self.lastResponse = None

        assert question is not None, 'A question must be supplied'
        assert type(question) is str
        self.question = question

        assert answer is not None, 'A preferable answer must be given, even if multiple answers are acceptable'

        self.answer = str(answer)
        self.answers.append(str(answer))
        if intToStr.get(answer, None) is not None:
            self.answers.append(intToStr[answer])

        if answers is not None:
            assert type(answers) is list
            for ans in answers:
                self.answers.append(str(ans))
                if intToStr.get(ans, None) is not None:
                    self.answers.append(intToStr[ans])

        if options is not None:
            assert type(options) is list
            assert len(options) > 1

            self.options = [str(option) for option in options]
            shuffle(self.options)

        if image is not None:
            assert type(image) is str
            assert what(imagesDir + image) in ['jpeg', 'png'],\
                '{} is not an image file'.format(imagesDir + image)

            self.image = Image.open(imagesDir + image)

        if hint is not None:
            assert type(hint) is str

            self.hint = hint

    def ask(self, spelling=1.0, keepAsking=False):
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
                    prompt += '{}{}{},'.format(Colors.options,
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

        correct = False
        spellingMatch = self.takeResponse(prompt)

        while spellingMatch < spelling:
            if self.lastResponse == '':
                print(u'\u23F9  skipping.\n')
                break
            elif keepAsking:
                print(u'\u274C incorrect')
                spellingMatch = self.takeResponse('    ')
            else:
                print(u'\u274C incorrect\n')
                break
        else:
            correct = True
            print(u'\u2705 correct!{}\n'.format(
                ' Exact answer is: {}'.format(self.answer)
                if spellingMatch < 1.0 else ''))

        # if self.image is not None:
        #     self.image.close()

        return 1 if correct else 0

    def takeResponse(self, prompt):
        self.lastResponse = input(prompt).strip()

        bestMatch = max([SequenceMatcher(None, self.lastResponse, ans).ratio()
                         for ans in self.answers])

        return bestMatch


cellQuestions = [Question('How many cells is a prokaryote?',
                          answer=1,
                          options=['one', 'many']),
                 Question('How many cells is a eukaryote?',
                          answer='many',
                          options=['one', 'many']),
                 Question('The major component of the cell membrane is a lipid bilayer. What phospholipids is this lipid bilayer mainly made up of?',
                          answer='amphipathic',
                          options=['hydrophilic', 'hydrophobic', 'amphipathic']),
                 Question('Do prokaryotes have a nucleus?',
                          answer='no'),
                 Question('Do eukaryotes have a nucleus?',
                          answer='yes'),
                 Question('Is this a nice picture?',
                          answer='yes',
                          image='cell.jpg')
                 ]

questions = cellQuestions
