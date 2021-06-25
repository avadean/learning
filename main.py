from data import Colors
from question import questions
from random import choices
from time import time


if __name__ == '__main__':
    print('Hello! What would you like to do?')
    print('  1: New profile')
    print('  2: Load profile')
    print('  3: Quick play (20 random questions)')
    print('  4: Options')
    print('  5: Exit')
    print('{}-> {}'.format(Colors.blink, Colors.reset),
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

        timeInitial = time()

        for question in quickQuestions:
            numCorrect += question.ask()

        timeFinal = time()

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
