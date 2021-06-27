from data import PrintColors
from game import quickPlay
from learn import learn
from question import questions
from program import Program, flipDisplay
from setting import Settings


if __name__ == '__main__':
    program = Program()
    settings = Settings()

    while program.running:
        #program.handleEvents()
        #program.draw()

        #print('\nWhat would you like to do{}?'.format(
        #    ', {}'.format(program.currentProfile.name) if program.currentProfile is not None else ''))
        #print('  1: Learn')
        #print('  2: Profiles')
        #print('  3: Quick play (20 random timed questions!)')
        #print('  4: Settings')
        #print('  5: Exit')
        #print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

        response = input().strip().lower()

        while response not in ['1', '2', '3', '4', '5',
                               'learn', 'profiles', 'quick', 'settings', 'exit'] and False:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset),
                  end='')
            response = input().strip().lower()

        if response in ['1', 'learn']:
            learn()

        elif response in ['2', 'profiles']:
            program.queryProfiles()

        elif response in ['3', 'quick']:
            quickPlay(questions, settings)

        elif response in ['4', 'settings']:
            settings.update()

        elif response in ['5', 'exit']:
            program.running = False

        program.clock.tick(60)

        flipDisplay()
    exit(0)
