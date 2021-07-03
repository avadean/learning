import pygame
pygame.init()
pygame.mixer.init()

from data import ScreenColors, Fonts, blitText, blitTextWrapped, blitListOfText
from os import listdir
from profile import loadProfiles, getNextProfileID, createProfile
from time import time

import game

musicDir = 'music/'


def updateDisplay():
    pygame.display.update()

def loadSongs():
    return [musicDir + song for song in listdir(musicDir)]


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
    addProfileButton = None
    selectProfileButton = None
    deleteProfileButton = None

    learnText = None
    profilesText = None
    quickPlayText = None
    settingsText = None
    exitText = None
    backText = None
    addProfileText = None
    selectProfileText = None
    deleteProfileText = None

    learnRect = None
    profilesRect = None
    quickPlayRect = None
    settingsRect = None
    exitRect = None
    backRect = None
    addProfileRect = None
    selectProfileRect = None
    deleteProfileRect = None

    mainMenuButtonWidth = 280
    mainMenuButtonHeight = 40

    backButtonWidth = 280
    backButtonHeight = 40

    profileMenuButtonWidth = 180
    profileMenuButtonHeight = 40

    state = None
    settings = None

    profiles = None
    currentProfile = None
    nextProfileID = None
    profileResponse = ''

    quickPlayQuestion = None
    quickPlayQuestionNum = 0
    quickPlayQuestions = []
    quickPlayResponse = ''
    quickPlayLastResponse = ''
    quickPlayNumCorrect = 0
    quickPlayNumQuestions = 20
    quickPlayLastQuestion = None

    startTime = None
    finishTime = None
    totalTime = None

    running = False
    playing = False
    completed = False

    def __init__(self, settings):
        self.state = 'main menu'
        self.settings = settings
        self.songs = loadSongs()

        self.getProfiles()

        self.createButtons()

        self.running = True
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

                elif self.state == 'profiles':
                    if self.addProfileButton.collidepoint(mousePos):
                        self.state = 'add profile'
                    elif self.selectProfileButton.collidepoint(mousePos):
                        self.state = 'select profile'
                    elif self.deleteProfileButton.collidepoint(mousePos):
                        self.state = 'delete profile'
                    elif self.backButton.collidepoint(mousePos):
                        self.state = 'main menu'

                elif self.state == 'add profile':
                    if not self.addProfileButton.collidepoint(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'select profile':
                    if not self.selectProfileButton.collidepoint(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'delete profile':
                    if not self.deleteProfileButton.collidepoint(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'quick play':
                    if self.backButton.collidepoint(mousePos):
                        self.resetQuickPlay()
                        self.state = 'main menu'

            if event.type == pygame.KEYDOWN:
                if self.state == 'main menu':
                    if event.key == pygame.K_1:
                        self.state = 'learn'
                    elif event.key == pygame.K_2:
                        self.state = 'profiles'
                    elif event.key == pygame.K_3:
                        self.state = 'quick play'
                        self.initialiseQuickPlay()
                    elif event.key == pygame.K_4:
                        self.state = 'settings'
                    elif event.key == pygame.K_5:
                        self.running = False

                elif self.state == 'profiles':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'main menu'

                elif self.state == 'add profile':
                    if event.key == pygame.K_ESCAPE:
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.addProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_BACKSPACE:
                        self.profileResponse = self.profileResponse[:-1]
                    else:
                        self.profileResponse += event.unicode

                elif self.state == 'select profile':
                    if event.key == pygame.K_ESCAPE:
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.selectProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_BACKSPACE:
                        self.profileResponse = self.profileResponse[:-1]
                    else:
                        self.profileResponse += event.unicode

                elif self.state == 'delete profile':
                    if event.key == pygame.K_ESCAPE:
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.deleteProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.state = 'profiles'
                    elif event.key == pygame.K_BACKSPACE:
                        self.profileResponse = self.profileResponse[:-1]
                    else:
                        self.profileResponse += event.unicode

                elif self.state == 'quick play':

                    if event.key == pygame.K_ESCAPE:
                        self.resetQuickPlay()
                        self.state = 'main menu'

                    if self.playing:
                        if event.key == pygame.K_RETURN:
                            self.quickPlayProcessResponse()
                            self.quickPlayResponse = ''

                        elif event.key == pygame.K_BACKSPACE:
                            self.quickPlayResponse = self.quickPlayResponse[:-1]

                        else:
                            self.quickPlayResponse += event.unicode

    def update(self):
        self.checkMusic()

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

        w = (self.screenWidth - 3 * self.profileMenuButtonWidth) // 4

        self.addProfileButton = pygame.Rect(w,
                                            7 * self.screenHeight // 10,
                                            self.profileMenuButtonWidth,
                                            self.profileMenuButtonHeight)

        self.selectProfileButton = pygame.Rect((self.screenWidth - self.profileMenuButtonWidth) // 2,
                                               7 * self.screenHeight // 10,
                                               self.profileMenuButtonWidth,
                                               self.profileMenuButtonHeight)

        self.deleteProfileButton = pygame.Rect(self.screenWidth - w - self.profileMenuButtonWidth,
                                               7 * self.screenHeight // 10,
                                               self.profileMenuButtonWidth,
                                               self.profileMenuButtonHeight)

        self.learnText = Fonts.mainMenuButtons.render('Learn', False, ScreenColors.black)
        self.profilesText = Fonts.mainMenuButtons.render('Profiles', False, ScreenColors.black)
        self.quickPlayText = Fonts.mainMenuButtons.render('Quick play', False, ScreenColors.black)
        self.settingsText = Fonts.mainMenuButtons.render('Settings', False, ScreenColors.black)
        self.exitText = Fonts.mainMenuButtons.render('Exit', False, ScreenColors.black)
        self.backText = Fonts.buttons.render('Back', False, ScreenColors.black)
        self.addProfileText = Fonts.profileButtons.render('Add', False, ScreenColors.black)
        self.selectProfileText = Fonts.profileButtons.render('Select', False, ScreenColors.black)
        self.deleteProfileText = Fonts.profileButtons.render('Delete', False, ScreenColors.black)

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

        self.addProfileRect = self.addProfileText.get_rect(center=(self.addProfileButton.x + self.profileMenuButtonWidth // 2,
                                                                   self.addProfileButton.y + self.profileMenuButtonHeight // 2))

        self.selectProfileRect = self.selectProfileText.get_rect(
            center=(self.selectProfileButton.x + self.profileMenuButtonWidth // 2,
                    self.selectProfileButton.y + self.profileMenuButtonHeight // 2))

        self.deleteProfileRect = self.deleteProfileText.get_rect(
            center=(self.deleteProfileButton.x + self.profileMenuButtonWidth // 2,
                    self.deleteProfileButton.y + self.profileMenuButtonHeight // 2))

    def draw(self):
        self.screen.fill(ScreenColors.fill)
        if self.state == 'main menu':
            self.drawMainMenu()
        elif self.state == 'learn':
            self.drawLearn()
        elif self.state in ['profiles', 'add profile', 'select profile', 'delete profile']:
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
                 top=self.screenHeight // 20,
                 centerHor=True)

    def drawLearn(self):
        raise NotImplementedError

    def drawProfiles(self):
        self.drawCurrentProfile()
        self.drawBackButton()

        blitText(screen=self.screen,
                 text='Profiles',
                 font=Fonts.profileTitle,
                 color=ScreenColors.profileTitle,
                 top=self.screenHeight // 20,
                 centerHor=True)

        columnWidth = self.screenWidth // 5
        w = (self.screenWidth - 3 * columnWidth) // 4

        blitText(screen=self.screen,
                 text='Name',
                 font=Fonts.profileHeader,
                 color=ScreenColors.black,
                 left=w + columnWidth // 2,
                 top=self.screenHeight // 9)

        blitText(screen=self.screen,
                 text='Qs correct',
                 font=Fonts.profileHeader,
                 color=ScreenColors.black,
                 left=2 * w + columnWidth,
                 top=self.screenHeight // 9)

        blitText(screen=self.screen,
                 text='Qs attempted',
                 font=Fonts.profileHeader,
                 color=ScreenColors.black,
                 left=3 * w + 2 * columnWidth,
                 top=self.screenHeight // 9)

        profilesSorted = sorted(self.profiles, key=lambda x: x.name)

        blitListOfText(screen=self.screen,
                       textList=['{}. {}'.format(num, prof.name) for num, prof in enumerate(profilesSorted, 1)],
                       font=Fonts.profileList,
                       color=ScreenColors.black,
                       left=w,
                       startTop=self.screenHeight // 6)

        blitListOfText(screen=self.screen,
                       textList=['{}'.format(prof.questionsCorrect) for prof in profilesSorted],
                       font=Fonts.profileList,
                       color=ScreenColors.black,
                       left=2 * w + columnWidth,
                       startTop=self.screenHeight // 6)

        blitListOfText(screen=self.screen,
                       textList=['{}'.format(prof.questionsAttempted) for prof in profilesSorted],
                       font=Fonts.profileList,
                       color=ScreenColors.black,
                       left=3 * w + 2 * columnWidth,
                       startTop=self.screenHeight // 6)

        pygame.draw.rect(self.screen, ScreenColors.buttons, self.addProfileButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.selectProfileButton, 2)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.deleteProfileButton, 2)

        if self.state == 'add profile':
            blitText(screen=self.screen,
                     text=self.profileResponse,
                     font=Fonts.profileTitle,
                     color=ScreenColors.profileTitle,
                     left=10+self.addProfileButton.left,
                     top=self.addProfileButton.top + self.profileMenuButtonHeight // 2 - Fonts.profileTitle.get_height() // 2)
        else:
            self.screen.blit(self.addProfileText, self.addProfileRect)

        if self.state == 'select profile':
            blitText(screen=self.screen,
                     text=self.profileResponse,
                     font=Fonts.profileTitle,
                     color=ScreenColors.profileTitle,
                     left=10 + self.selectProfileButton.left,
                     top=self.selectProfileButton.top + self.profileMenuButtonHeight // 2 - Fonts.profileTitle.get_height() // 2)
        else:
            self.screen.blit(self.selectProfileText, self.selectProfileRect)

        if self.state == 'delete profile':
            blitText(screen=self.screen,
                     text=self.profileResponse,
                     font=Fonts.profileTitle,
                     color=ScreenColors.profileTitle,
                     left=10 + self.deleteProfileButton.left,
                     top=self.deleteProfileButton.top + self.profileMenuButtonHeight // 2 - Fonts.profileTitle.get_height() // 2)
        else:
            self.screen.blit(self.deleteProfileText, self.deleteProfileRect)

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
        if self.currentProfile is not None:
            blitText(screen=self.screen,
                     text='{}'.format(self.currentProfile.name),
                     font=Fonts.profile,
                     color=ScreenColors.black,
                     bottomRight=True,
                     leftOffset=10,
                     topOffset=10)

    def drawBackButton(self):
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.exitButton, 2)
        self.screen.blit(self.backText, self.backRect)

    def initialiseQuickPlay(self):
        self.playing = True
        self.completed = False

        self.quickPlayQuestions = game.getQuickPlay(self.quickPlayNumQuestions)

        self.updateQuestion()
        self.startTime = time()

    def finaliseQuickPlay(self):
        self.finishTime = time()
        self.totalTime = self.finishTime - self.startTime

        self.quickPlayQuestion = None
        self.quickPlayQuestionNum = 0
        self.quickPlayLastQuestion = None

        self.playing = False
        self.completed = True

    def resetQuickPlay(self):
        if self.currentProfile is not None:
            self.currentProfile.rewriteFile()

        for ques in self.quickPlayQuestions:
            ques.updateCorrect(False)

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

    def quickPlayProcessResponse(self):
        self.quickPlayQuestion.takeResponse(self.quickPlayResponse)
        self.quickPlayQuestion.calcExactResponseWithRating()

        correct = self.quickPlayQuestion.lastReponseRating >= self.settings.spelling
        self.quickPlayNumCorrect += correct
        self.quickPlayQuestion.updateCorrect(correct)

        if self.currentProfile is not None:
            self.currentProfile.questionsAttempted += 1
            self.currentProfile.questionsCorrect += correct

        self.quickPlayLastResponse = self.quickPlayResponse if self.quickPlayResponse.strip() != '' else '-'
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
        self.nextProfileID = getNextProfileID()
        self.currentProfile = None

        for prof in self.profiles:
            if prof.default:
                self.currentProfile = prof
                break

    def addProfile(self, profileName):
        assert type(profileName) is str

        if profileName.strip().lower() in [prof.name.strip().lower() for prof in self.profiles]:
            return

        newProfile = createProfile(self.nextProfileID, profileName)

        if newProfile is None:
            return

        self.nextProfileID += 1

        self.profiles.append(newProfile)

        self.selectProfile(profileName)

    def selectProfile(self, profileName=None):
        if profileName is None:
            self.currentProfile = None
        else:
            assert type(profileName) is str

            for prof in self.profiles:
                if profileName.strip().lower() == prof.name.strip().lower():
                    self.currentProfile = prof

    def deleteProfile(self, profileName):
        assert type(profileName) is str

        profileToDelete = None
        profiles = []

        for prof in self.profiles:
            if profileName.strip().lower() == prof.name.strip().lower():
                profileToDelete = prof
            else:
                profiles.append(prof)

        if profileToDelete is None:
            return

        self.profiles = profiles

        profileToDelete.delete()

        self.getProfiles()

    def checkMusic(self):
        if len(self.songs) == 0:
            return

        if not pygame.mixer.music.get_busy():
            self.playNextSong()

    def playNextSong(self):
        nextSong = self.songs[0]

        pygame.mixer.music.load(nextSong)
        pygame.mixer.music.play()

        self.songs = self.songs[1:] + [nextSong]
