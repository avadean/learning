import pygame
pygame.init()

from data import PrintColors, ScreenColors, Fonts, blitText, blitTextWrapped
from profile import loadProfiles, Profile
from time import time

import game


def updateDisplay():
    pygame.display.update()


class Program:
    clock = pygame.time.Clock()

    screenWidth = 768
    screenHeight = 576
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(ScreenColors.fill)

    learnButton = None
    profilesButton = None
    quickPlayButton = None
    settingsButton = None
    exitButton = None
    backButton = None
    learnText = None
    profilesText = None
    quickPlayText = None
    settingsText = None
    exitText = None
    backText = None
    learnRect = None
    profilesRect = None
    quickPlayRect = None
    settingsRect = None
    exitRect = None
    backRect = None

    mainMenuButtonWidth = 280
    mainMenuButtonHeight = 40

    backButtonWidth = 280
    backButtonHeight = 40

    def __init__(self, settings):
        self.running = True
        self.state = 'main menu'
        self.settings = settings

        self.profiles = None
        self.currentProfile = None
        self.getProfiles()

        self.createButtons()

        self.quickPlayQuestion = None
        self.quickPlayQuestionNum = 0
        self.quickPlayQuestions = []
        self.quickPlayResponse = ''
        self.quickPlayLastResponse = ''
        self.quickPlayNumCorrect = 0
        self.quickPlayNumQuestions = 20
        self.quickPlayLastQuestion = None
        self.startTime = None
        self.finishTime = None
        self.totalTime = None

        self.playing = False
        self.completed = False

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = event.pos

                if self.state == 'main menu':
                    if self.learnButton.collidepoint(mousePos):
                        self.state = 'learn'
                    elif self.profilesButton.collidepoint(mousePos):
                        self.state = 'profiles'
                    elif self.quickPlayButton.collidepoint(mousePos):
                        self.state = 'quick play'
                        self.initialiseQuickPlay()
                    elif self.settingsButton.collidepoint(mousePos):
                        self.state = 'settings'
                    elif self.exitButton.collidepoint(mousePos):
                        self.running = False

                elif self.state == 'quick play':
                    if self.backButton.collidepoint(mousePos):
                        self.resetQuickPlay()

            if event.type == pygame.KEYDOWN:
                if self.state == 'quick play':

                    if self.playing:
                        if event.key == pygame.K_RETURN:
                            self.quickPlayProcessResponse()

                        elif event.key == pygame.K_BACKSPACE:
                            self.quickPlayResponse = self.quickPlayResponse[:-1]

                        elif event.key == pygame.K_ESCAPE:
                            self.resetQuickPlay()

                        else:
                            self.quickPlayResponse += event.unicode

    def update(self):
        if self.state == 'main menu':
            pass
        elif self.state == 'learn':
            pass
        elif self.state == 'profiles':
            pass
        elif self.state == 'quick play':
            if self.running and not self.completed:
                self.updateTimer()
        elif self.state == 'settings':
            pass

    def createButtons(self):
        self.learnButton = pygame.Rect((self.screenWidth - self.mainMenuButtonWidth) // 2,
                                       self.screenHeight // 6,
                                       self.mainMenuButtonWidth,
                                       self.mainMenuButtonHeight)

        self.profilesButton = pygame.Rect((self.screenWidth - self.mainMenuButtonWidth) // 2,
                                           self.screenHeight // 3,
                                           self.mainMenuButtonWidth,
                                           self.mainMenuButtonHeight)

        self.quickPlayButton = pygame.Rect((self.screenWidth - self.mainMenuButtonWidth) // 2,
                                           self.screenHeight // 2,
                                           self.mainMenuButtonWidth,
                                           self.mainMenuButtonHeight)

        self.settingsButton = pygame.Rect((self.screenWidth - self.mainMenuButtonWidth) // 2,
                                           2 * self.screenHeight // 3,
                                           self.mainMenuButtonWidth,
                                           self.mainMenuButtonHeight)

        self.exitButton = pygame.Rect((self.screenWidth - self.mainMenuButtonWidth) // 2,
                                       5 * self.screenHeight // 6,
                                       self.mainMenuButtonWidth,
                                       self.mainMenuButtonHeight)

        self.backButton = pygame.Rect((self.screenWidth - self.backButtonWidth) // 2,
                                      5 * self.screenHeight // 6,
                                      self.backButtonWidth,
                                      self.backButtonHeight)

        self.learnText = Fonts.mainMenuButtons.render('Learn', False, ScreenColors.black)
        self.profilesText = Fonts.mainMenuButtons.render('Profiles', False, ScreenColors.black)
        self.quickPlayText = Fonts.mainMenuButtons.render('Quick play', False, ScreenColors.black)
        self.settingsText = Fonts.mainMenuButtons.render('Settings', False, ScreenColors.black)
        self.exitText = Fonts.mainMenuButtons.render('Exit', False, ScreenColors.black)
        self.backText = Fonts.buttons.render('Back', False, ScreenColors.black)

        self.learnRect = self.learnText.get_rect(center=(self.learnButton.x + self.mainMenuButtonWidth // 2,
                                                         self.learnButton.y + self.mainMenuButtonHeight // 2))

        self.profilesRect = self.profilesText.get_rect(center=(self.profilesButton.x + self.mainMenuButtonWidth // 2,
                                                               self.profilesButton.y + self.mainMenuButtonHeight // 2))

        self.quickPlayRect = self.quickPlayText.get_rect(center=(self.quickPlayButton.x + self.mainMenuButtonWidth // 2,
                                                                 self.quickPlayButton.y + self.mainMenuButtonHeight // 2))

        self.settingsRect = self.settingsText.get_rect(center=(self.settingsButton.x + self.mainMenuButtonWidth // 2,
                                                               self.settingsButton.y + self.mainMenuButtonHeight // 2))

        self.exitRect = self.exitText.get_rect(center=(self.exitButton.x + self.mainMenuButtonWidth // 2,
                                                       self.exitButton.y + self.mainMenuButtonHeight // 2))

        self.backRect = self.backText.get_rect(center=(self.backButton.x + self.backButtonWidth // 2,
                                                       self.backButton.y + self.backButtonHeight // 2))

    def draw(self):
        self.screen.fill(ScreenColors.fill)
        if self.state == 'main menu':
            self.drawMainMenu()
        elif self.state == 'learn':
            self.drawLearn()
        elif self.state == 'profiles':
            self.drawProfiles()
        elif self.state == 'quick play':
            self.drawQuickPlay()
        elif self.state == 'settings':
            self.drawSettings()

    def drawMainMenu(self):
        pygame.draw.rect(self.screen, ScreenColors.mainMenuButtons, self.learnButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.mainMenuButtons, self.profilesButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.mainMenuButtons, self.quickPlayButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.mainMenuButtons, self.settingsButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.mainMenuButtons, self.exitButton, 2)

        self.screen.blit(self.learnText, self.learnRect)
        self.screen.blit(self.profilesText, self.profilesRect)
        self.screen.blit(self.quickPlayText, self.quickPlayRect)
        self.screen.blit(self.settingsText, self.settingsRect)
        self.screen.blit(self.exitText, self.exitRect)

        self.drawCurrentProfile()
        blitText(screen=self.screen,
                 text='What would you like to do?',
                 font=Fonts.mainMenuTitle,
                 color=ScreenColors.mainMenuTitle,
                 top=20,
                 centerHor=True)

    def drawLearn(self):
        raise NotImplementedError

    def drawProfiles(self):
        raise NotImplementedError

    def drawQuickPlay(self):
        self.drawCurrentProfile()
        self.drawBackButton()

        if self.playing:
            lineSpacing = 2

            # blit the question
            blitTextWrapped(screen=self.screen,
                            text=self.quickPlayQuestion.getQuestionBasic(),
                            font=Fonts.quickPlayQuestion,
                            color=ScreenColors.question,
                            left=self.screenWidth // 10,
                            width=4 * self.screenWidth // 5,
                            startTop=self.screenHeight // 8,
                            lineSpacing=lineSpacing,
                            indent=2)

            # blit the options
            blitTextWrapped(screen=self.screen,
                            text=self.quickPlayQuestion.getOptionsBasic(),
                            font=Fonts.quickPlayQuestion,
                            color=ScreenColors.option,
                            left=self.screenWidth // 10,
                            width=4 * self.screenWidth // 5,
                            startTop=self.screenHeight // 2,
                            lineSpacing=lineSpacing,
                            indent=2)

            # blit the response
            blitTextWrapped(screen=self.screen,
                            text=self.quickPlayResponse,
                            font=Fonts.quickPlayResponse,
                            color=ScreenColors.response,
                            left=self.screenWidth // 10,
                            width=4 * self.screenWidth // 5,
                            startTop=2 * self.screenHeight // 3,
                            lineSpacing=lineSpacing,
                            indent=2)

            # and the response box
            pygame.draw.rect(self.screen, ScreenColors.quickPlayBoxes,
                             (-5 + self.screenWidth // 10,
                              -5 + 2 * self.screenHeight // 3,
                              +5 + 4 * self.screenWidth // 5,
                              +5 + 3 * (Fonts.quickPlayResponse.get_height() + lineSpacing)),
                             2)

            # blit the response to the last question if there has been a last question
            if self.quickPlayLastQuestion is not None:
                blitText(screen=self.screen,
                         text='{}'.format(self.quickPlayLastQuestion.exactResponse if self.quickPlayLastQuestion.correct\
                                              else self.quickPlayLastResponse),
                         font=Fonts.quickPlayLastResponse,
                         color=ScreenColors.responseCorrect if self.quickPlayLastQuestion.correct\
                             else ScreenColors.responseWrong,
                         left=5,
                         top=self.screenHeight - Fonts.quickPlayLastResponse.get_height() - 5)

            # blit the timer
            blitText(screen=self.screen,
                     text='{:6.2f}'.format(self.totalTime),
                     font=Fonts.timer,
                     color=ScreenColors.timer,
                     topRight=True,
                     leftOffset=10,
                     topOffset=10)

            # blit the correct count
            blitText(screen=self.screen,
                     text='{}/{}'.format(self.quickPlayNumCorrect, self.quickPlayQuestionNum-1),
                     font=Fonts.correctCount,
                     color=ScreenColors.black,
                     topLeft=True,
                     leftOffset=10,
                     topOffset=10)

        elif self.completed:
            lineSpacing = 2

            perCent = 100.0 * float(self.quickPlayNumCorrect) / float(self.quickPlayNumQuestions)

            blitText(screen=self.screen,
                     text='*** {} correct ({:5.1f} %) in {:6.2f} seconds! ***'.format(self.quickPlayNumCorrect,
                                                                                      perCent,
                                                                                      self.totalTime),
                     font=Fonts.quickPlaySummary,
                     color=ScreenColors.summary,
                     centerHor=True,
                     top=20)

            height = 40 + Fonts.quickPlaySummary.get_height()
            fontHeight = Fonts.quickPlayQuestionSummary.get_height()
            for num, ques in enumerate(self.quickPlayQuestions, 1):
                # blit the question
                blitTextWrapped(screen=self.screen,
                                text='{:>2}. {}'.format(num, ques.getQuestionBasic()),
                                font=Fonts.quickPlayQuestionSummary,
                                color=ScreenColors.question,
                                left=self.screenWidth // 24,#self.screenWidth // 16,
                                width=self.screenWidth // 3,#self.screenWidth // 4,
                                startTop=height,
                                maxLines=1)

                # blit the response
                blitTextWrapped(screen=self.screen,
                                text='{}'.format(ques.lastResponse),
                                font=Fonts.quickPlayQuestionSummary,
                                color=ScreenColors.responseCorrect if ques.correct else ScreenColors.responseWrong,
                                left=3 * self.screenWidth // 8 + self.screenWidth // 24,
                                width=self.screenWidth // 4,
                                startTop=height,
                                maxLines=1)

                # if wrong blit the correct answer
                if not ques.correct:
                    blitTextWrapped(screen=self.screen,
                                    text='{}'.format(', '.join(ques.answers)),
                                    font=Fonts.quickPlayQuestionSummary,
                                    color=ScreenColors.blue,
                                    left=2 * self.screenWidth // 3 + self.screenWidth // 24,
                                    width=self.screenWidth // 4,
                                    startTop=height,
                                    maxLines=1)

                height += lineSpacing + fontHeight

        else:
            # Draw countdown.
            pass

    def drawSettings(self):
        raise NotImplementedError

    def drawCurrentProfile(self):
        blitText(screen=self.screen,
                 text='{}'.format(self.currentProfile.nameNormal),
                 font=Fonts.profile,
                 color=ScreenColors.black,
                 bottomRight=True,
                 leftOffset=10,
                 topOffset=10)

    def drawBackButton(self):
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.exitButton, 2)
        self.screen.blit(self.backText, self.backRect)

    def initialiseQuickPlay(self):
        self.startTime = time()
        self.playing = True
        self.completed = False
        self.quickPlayQuestions = game.getQuickPlay(self.quickPlayNumQuestions)
        self.updateQuestion()

    def finaliseQuickPlay(self):
        self.finishTime = time()
        self.totalTime = self.finishTime - self.startTime
        self.quickPlayQuestion = None
        self.quickPlayQuestionNum = 0
        self.quickPlayLastQuestion = None
        self.playing = False
        self.completed = True

    def resetQuickPlay(self):
        self.startTime = None
        self.finishTime = None
        self.totalTime = None
        self.quickPlayQuestion = None
        self.quickPlayQuestionNum = 0
        self.quickPlayQuestions = []
        self.quickPlayLastQuestion = None
        self.quickPlayResponse = ''
        self.quickPlayLastResponse = ''
        self.quickPlayNumQuestions = 20
        self.quickPlayNumCorrect = 0
        self.playing = False
        self.completed = False
        self.state = 'main menu'

    def quickPlayProcessResponse(self):
        self.quickPlayQuestion.takeResponse(self.quickPlayResponse)
        self.quickPlayQuestion.calcExactResponseWithRating()

        correct = self.quickPlayQuestion.lastReponseRating >= self.settings.spelling
        self.quickPlayNumCorrect += correct
        self.quickPlayQuestion.updateCorrect(correct)

        self.quickPlayLastResponse = self.quickPlayResponse if self.quickPlayResponse.strip() != '' else '-'
        self.quickPlayResponse = ''
        self.updateQuestion()

    def updateQuestion(self):
        if self.quickPlayQuestionNum == self.quickPlayNumQuestions:
            self.finaliseQuickPlay()
        else:
            self.quickPlayLastQuestion = self.quickPlayQuestion
            self.quickPlayQuestion = self.quickPlayQuestions[self.quickPlayQuestionNum]
            self.quickPlayQuestionNum += 1

    def updateTimer(self):
        self.totalTime = time() - self.startTime

    def getProfiles(self):
        self.profiles = loadProfiles()
        self.currentProfile = self.profiles[0] # This is the Guest profile.

        for prof in self.profiles:
            if prof.default:
                self.currentProfile = prof
                break

    def queryProfiles(self):
        if len(self.profiles) == 0:
            self.zeroProfiles()
        elif self.currentProfile is None:
            print('\nNo profile selected')
            self.selectProfile()

        print('\nCurrent profile: {}'.format(self.currentProfile.name))

        otherProfiles = [prof.name for prof in self.profiles if prof.name != self.currentProfile.name]

        if len(otherProfiles) == 0:
            print('No other profiles to select')
        else:
            print('Other profiles: {}'.format(', '.join(otherProfiles)))

        print('\nWould you like to {}create{}, {}select{} or {}delete{} a profile? Or go {}back{}?'.format(
            PrintColors.underline, PrintColors.reset,
            PrintColors.underline, PrintColors.reset,
            PrintColors.underline, PrintColors.reset,
            PrintColors.underline, PrintColors.reset))
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

        response = input().strip().lower()

        while response not in ['create', 'select', 'delete', 'back']:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')
            response = input().strip().lower()

        if response == 'create':
            self.createProfile()
        elif response == 'select':
            self.selectProfile()
        elif response == 'delete':
            self.deleteProfile()
        elif response == 'back':
            pass

    def createProfile(self):
        print('')
        name = input('Please enter a name: ').strip()

        while name.lower() in [prof.nameNormal.lower() for prof in self.profiles]:
            name = input('That name is taken, please enter a different one: ').strip()

        newProfile = Profile(name)
        self.profiles.append(newProfile)

        if sum(prof.default for prof in self.profiles) >= 1:
            print('Would you like to make this the default profile? {}Yes{} or {}no{}?'.format(PrintColors.underline,
                                                                                               PrintColors.reset,
                                                                                               PrintColors.underline,
                                                                                               PrintColors.reset))
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

            response = input().strip().lower()
            while response not in ['yes', 'no']:
                print('Incorrect option supplied. Try again.')
                print('{}->{} '.format(PrintColors.blink, PrintColors.reset),
                      end='')
                response = input().strip().lower()

            if response == 'yes':
                self.currentProfile.default = False
                newProfile.default = True

        else:
            newProfile.default = True

        self.currentProfile = newProfile
        print('Profile {} created and now in use'.format(self.currentProfile.name))

    def selectProfile(self):
        print('\nPlease choose a profile to select: {}'.format(', '.join([prof.name for prof in self.profiles])))
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

        response = input().strip().lower()
        while response not in [prof.nameNormal.lower() for prof in self.profiles]:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')
            response = input().strip().lower()

        for num, nameNormal in enumerate([prof.nameNormal.lower() for prof in self.profiles]):
            if response == nameNormal:
                self.currentProfile = self.profiles[num]

        print('Profile {} now in use'.format(self.currentProfile.name))

    def deleteProfile(self):
        print('Please choose a profile to delete: {}'.format(', '.join([prof.name for prof in self.profiles])))
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

        response = input().strip().lower()
        while response not in [prof.nameNormal.lower() for prof in self.profiles]:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')
            response = input().strip().lower()

        self.profiles = [prof for prof in self.profiles if prof.nameNormal.lower() != response]

        if len(self.profiles) == 0:
            self.zeroProfiles()
        else:
            self.selectProfile()

    def createGuestProfile(self):
        newGuestProfile = Profile('Guest')
        self.profiles.append(newGuestProfile)
        self.currentProfile = newGuestProfile

    def zeroProfiles(self):
        print('\nNo profiles loaded. Would you like to create your own? {}Yes{} or {}no{}?'.format(PrintColors.underline,
                                                                                                   PrintColors.reset,
                                                                                                   PrintColors.underline,
                                                                                                   PrintColors.reset))
        print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')

        response = input().strip().lower()
        while response not in ['yes', 'no']:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(PrintColors.blink, PrintColors.reset), end='')
            response = input().strip().lower()

        if response == 'yes':
            self.createProfile()
        elif response == 'no':
            self.createGuestProfile()