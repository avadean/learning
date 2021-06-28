from program import Program, updateDisplay
from setting import Settings


if __name__ == '__main__':
    settings = Settings()
    program = Program(settings)

    while program.running:
        program.handleEvents()
        program.update()
        program.draw()

        '''
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
        '''

        program.clock.tick(60)

        updateDisplay()

    exit(0)
