from data import Colors
from question import questions
from setting import Settings
from random import choices

import time


if __name__ == '__main__':
    settings = Settings()

    print('Hello! What would you like to do?')
    print('  1: Learn')
    print('  2: Profiles')
    print('  3: Quick play (20 random timed questions!)')
    print('  4: Settings')
    print('  5: Exit')
    print('{}->{} '.format(Colors.blink, Colors.reset),
          end='')

    response = input().strip()

    if response not in ['1', '2', '3', '4', '5']:
        exit(1)

    if response == '1':
        raise NotImplementedError

    elif response == '2':
        raise NotImplementedError

    elif response == '3':
        numCorrect = 0
        numQuestions = 20

        quickQuestions = choices(questions, k=numQuestions)

        print('')
        time.sleep(0.2)
        for sec in range(3, 0, -1):
            print('{}...'.format(sec), end=' ', flush=True)
            time.sleep(1)
        print('Go!\n')

        timeInitial = time.time()

        for question in quickQuestions:
            numCorrect += question.ask(spelling=settings.spelling)

        timeFinal = time.time()

        perCent = 100.0 * float(numCorrect) / float(numQuestions)

        totalTime = round(timeFinal - timeInitial, 1)

        print('{}*** {} correct ({} %) in {} seconds! ***{}'.format(
            Colors.blink,
            numCorrect,
            perCent,
            totalTime,
            Colors.reset))

    elif response == '4':
        raise NotImplementedError

    elif response == '5':
        exit(0)
