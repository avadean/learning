from data import Colors
from random import sample

import time

def quickPlay(questions, settings):
    numCorrect = 0
    numQuestions = 20

    quickQuestions = sample(questions, k=numQuestions)

    time.sleep(0.2)
    for sec in range(3, 0, -1):
        print('{}...'.format(sec), end=' ', flush=True)
        time.sleep(1)
    print('Go!\n')

    timeInitial = time.time()

    for question in quickQuestions:
        numCorrect += question.ask(spelling=settings.spelling)

    timeFinal = time.time()

    perCent = round(100.0 * float(numCorrect) / float(numQuestions), 1)

    totalTime = round(timeFinal - timeInitial, 1)

    print('{}*** {} correct ({} %) in {} seconds! ***{}'.format(
        Colors.blink,
        numCorrect,
        perCent,
        totalTime,
        Colors.reset))