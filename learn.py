from data import Colors


def learn():
    print('\nWhat would you like to learn about?')
    print('  1: Cell biology')
    print('{}->{} '.format(Colors.blink, Colors.reset), end='')

    response = input().strip().lower()

    while response not in ['1',
                           'cells']:
        print('Incorrect option supplied. Try again.')
        print('{}->{} '.format(Colors.blink, Colors.reset), end='')
        response = input().strip().lower()

    if response in ['1', 'cells']:
        cells()


def cells():
    raise NotImplementedError





class Knowledge:
    def __init__(self, knowledge=None, category='general'):
        assert type(knowledge) is str
        assert type(category) is str

        self.knowledge = knowledge
        self.category = category


cellsFacts = [Knowledge('Prokaryotes are single-celled organisms', 'cells'),
              Knowledge('Eukaryotes are multi-cellular organisms', 'cells')
              ]

