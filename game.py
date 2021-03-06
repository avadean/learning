from data import PrintColors
from question import questions
from random import sample

import time

def getQuickPlay(numQuestions):
    return sample(questions, k=numQuestions)




def quickPlayOLD(settings):
    numCorrect = 0
    numQuestions = 20

    wrong = []

    quickQuestions = sample(questions, k=numQuestions)

    time.sleep(0.2)
    for sec in range(3, 0, -1):
        print('{}...'.format(sec), end=' ', flush=True)
        time.sleep(1)
    print('Go!\n')

    timeInitial = time.time()

    for ques in quickQuestions:
        correct = ques.ask(spelling=settings.spellingValue)
        if not correct:
            wrong.append(ques)
        numCorrect += correct

    timeFinal = time.time()

    perCent = round(100.0 * float(numCorrect) / float(numQuestions), 1)

    totalTime = round(timeFinal - timeInitial, 1)

    print('{}*** {} correct ({} %) in {} seconds! ***{}'.format(
        PrintColors.blink,
        numCorrect,
        perCent,
        totalTime,
        PrintColors.reset))

    if len(wrong) > 0:
        print('\nAnswers to incorrect questions:')
        for ques in wrong:
            ques.printQuestion(withAnswer=True)