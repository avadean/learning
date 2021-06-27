from data import PrintColors


spellingLevel = {'exact': 1.0,
                 'strict': 0.9,
                 'moderate': 0.8,
                 'fair': 0.7,
                 'leniant': 0.6,
                 'easy': 0.5
                 }


class Settings:
    def __init__(self, spelling='moderate'):
        assert type(spelling) is str
        assert spelling.lower() in spellingLevel, 'Accepted spelling settings: {}'.format(', '.join(spellingLevel))

        self.spellingLevel = spelling.lower()
        self.spelling = spellingLevel[spelling.lower()]

    def update(self):
        print('\nWould you like to update anything?')
        print('  1: Spelling strictness')
        print('  2: Cancel')
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset),
              end='')

        response = input().strip()

        while response not in ['1', '2']:
            print('Incorrect option supplied. Try again.')
            response = input().strip()

        if response == '1':
            self.requestSpellingUpdate()

            done = False

            while not done:
                response = input().strip()
                done = self.setSpellingUpdate(response)

        elif response == '2':
            pass

    def requestSpellingUpdate(self):
        print('\nThe current spelling setting is {}{}{}'.format(PrintColors.underline,
                                                                self.spellingLevel,
                                                                PrintColors.reset))
        print('Please choose a spelling setting: {}'.format(', '.join(spellingLevel)))
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

    def setSpellingUpdate(self, newSpelling):
        assert type(newSpelling) is str

        if newSpelling.lower() in spellingLevel:
            self.spellingLevel = newSpelling.lower()
            self.spelling = spellingLevel[newSpelling.lower()]
            print('Spelling setting updated to {}{}{}'.format(PrintColors.underline,
                                                              self.spellingLevel,
                                                              PrintColors.reset))
            return True
        else:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')
            return False