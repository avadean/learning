import pygame
pygame.init()
pygame.mixer.init()

from data import Button, Fonts, ScreenColors, blitText, blitTextWrapped, blitListOfText
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
                    if self.learnButton.clicked(mousePos):
                        self.state = 'learn'
                    elif self.profilesButton.clicked(mousePos):
                        self.state = 'profiles'
                    elif self.quickPlayButton.clicked(mousePos):
                        self.state = 'quick play'
                        self.initialiseQuickPlay()
                    elif self.settingsButton.clicked(mousePos):
                        self.state = 'settings'
                    elif self.exitButton.clicked(mousePos):
                        self.running = False

                elif self.state == 'profiles':
                    if self.addProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.addProfileButton.updateText(self.profileResponse)
                        self.state = 'add profile'
                    elif self.selectProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.selectProfileButton.updateText(self.profileResponse)
                        self.state = 'select profile'
                    elif self.deleteProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.deleteProfileButton.updateText(self.profileResponse)
                        self.state = 'delete profile'
                    elif self.backButton.clicked(mousePos):
                        self.state = 'main menu'

                elif self.state == 'add profile':
                    if not self.addProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'select profile':
                    if not self.selectProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'delete profile':
                    if not self.deleteProfileButton.clicked(mousePos):
                        self.profileResponse = ''
                        self.state = 'profiles'

                elif self.state == 'quick play':
                    if self.backButton.clicked(mousePos):
                        self.resetQuickPlay()
                        self.state = 'main menu'

                elif self.state == 'settings':
                    if self.backButton.clicked(mousePos):
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
                        self.addProfileButton.updateText('Add')
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.addProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.addProfileButton.updateText('Add')
                        self.state = 'profiles'
                    elif event.key == pygame.K_BACKSPACE:
                        self.profileResponse = self.profileResponse[:-1]
                    else:
                        self.profileResponse += event.unicode

                elif self.state == 'select profile':
                    if event.key == pygame.K_ESCAPE:
                        self.profileResponse = ''
                        self.selectProfileButton.updateText('Select')
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.selectProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.selectProfileButton.updateText('Select')
                        self.state = 'profiles'
                    elif event.key == pygame.K_BACKSPACE:
                        self.profileResponse = self.profileResponse[:-1]
                    else:
                        self.profileResponse += event.unicode

                elif self.state == 'delete profile':
                    if event.key == pygame.K_ESCAPE:
                        self.profileResponse = ''
                        self.deleteProfileButton.updateText('Delete')
                        self.state = 'profiles'
                    elif event.key == pygame.K_RETURN:
                        self.deleteProfile(self.profileResponse)
                        self.profileResponse = ''
                        self.deleteProfileButton.updateText('Delete')
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

                elif self.state == 'settings':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'main menu'

    def update(self):
        self.checkMusic()

        if self.state == 'main menu':
            pass
        elif self.state == 'learn':
            pass
        elif self.state == 'profiles':
            pass
        elif self.state == 'add profile':
            self.addProfileButton.updateText(self.profileResponse)
        elif self.state == 'select profile':
            self.selectProfileButton.updateText(self.profileResponse)
        elif self.state == 'delete profile':
            self.deleteProfileButton.updateText(self.profileResponse)
        elif self.state == 'quick play':
            if self.running and not self.completed:
                self.updateTimer()
        elif self.state == 'settings':
            pass

    def createButtons(self):
        self.learnButton = Button(text='Learn',
                                  centerHor=True,
                                  width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                  top=self.screenHeight // 6, height=self.mainMenuButtonHeight,
                                  borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        self.profilesButton = Button(text='Profiles',
                                     centerHor=True,
                                     width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                     top=self.screenHeight // 3, height=self.mainMenuButtonHeight,
                                     borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        self.quickPlayButton = Button(text='Quick play',
                                      centerHor=True,
                                      width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                      top=self.screenHeight // 2, height=self.mainMenuButtonHeight,
                                      borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        self.settingsButton = Button(text='Settings',
                                     centerHor=True,
                                     width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                     top=2 * self.screenHeight // 3, height=self.mainMenuButtonHeight,
                                     borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        self.exitButton = Button(text='Exit',
                                 centerHor=True,
                                 width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                 top=5 * self.screenHeight // 6, height=self.mainMenuButtonHeight,
                                 borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        self.backButton = Button(text='Back',
                                 centerHor=True,
                                 width=self.mainMenuButtonWidth, screenWidth=self.screenWidth,
                                 top=5 * self.screenHeight // 6, height=self.mainMenuButtonHeight,
                                 borderColor=ScreenColors.mainMenuButtons, font=Fonts.mainMenuButtons)

        w = (self.screenWidth - 3 * self.profileMenuButtonWidth) // 4

        self.addProfileButton = Button(text='Add',
                                       topLeft=True,
                                       width=self.profileMenuButtonWidth,
                                       height=self.profileMenuButtonHeight,
                                       horOffset=w,
                                       verOffset=7 * self.screenHeight // 10,
                                       borderColor=ScreenColors.profileButtons, font=Fonts.profileButtons)

        self.selectProfileButton = Button(text='Select',
                                          centerHor=True,
                                          width=self.profileMenuButtonWidth,
                                          height=self.profileMenuButtonHeight,
                                          top=7 * self.screenHeight // 10,
                                          screenWidth=self.screenWidth,
                                          borderColor=ScreenColors.profileButtons, font=Fonts.profileButtons)

        self.deleteProfileButton = Button(text='Delete',
                                          topRight=True,
                                          width=self.profileMenuButtonWidth,
                                          height=self.profileMenuButtonHeight,
                                          horOffset=w,
                                          verOffset=7 * self.screenHeight // 10,
                                          screenWidth=self.screenWidth,
                                          borderColor=ScreenColors.profileButtons, font=Fonts.profileButtons)

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
        self.drawCurrentProfile()

        self.learnButton.draw(self.screen)
        self.profilesButton.draw(self.screen)
        self.quickPlayButton.draw(self.screen)
        self.settingsButton.draw(self.screen)
        self.exitButton.draw(self.screen)

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
        self.backButton.draw(self.screen)

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

        self.addProfileButton.draw(self.screen)
        self.selectProfileButton.draw(self.screen)
        self.deleteProfileButton.draw(self.screen)

    def drawQuickPlay(self):
        self.drawCurrentProfile()
        self.backButton.draw(self.screen)

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
                         bottomLeft=True,
                         horOffset=10,
                         verOffset=10)

            # blit the timer
            blitText(screen=self.screen,
                     text='{:6.2f}'.format(self.totalTime),
                     font=Fonts.timer,
                     color=ScreenColors.timer,
                     topRight=True,
                     horOffset=10,
                     verOffset=10)

            # blit the correct count
            blitText(screen=self.screen,
                     text='{}/{}'.format(self.quickPlayNumCorrect, self.quickPlayQuestionNum-1),
                     font=Fonts.correctCount,
                     color=ScreenColors.black,
                     topLeft=True,
                     horOffset=10,
                     verOffset=10)

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
        self.drawCurrentProfile()
        self.backButton.draw(self.screen)

        blitText(screen=self.screen,
                 text='Settings',
                 font=Fonts.settingsTitle,
                 color=ScreenColors.settingsTitle,
                 top=self.screenHeight // 20,
                 centerHor=True)

        blitListOfText(screen=self.screen,
                       textList=self.settings.getSettings(),
                       font=Fonts.settings,
                       color=ScreenColors.black,
                       startTop=self.screenHeight // 8,
                       centerHor=True)

    def drawCurrentProfile(self):
        if self.currentProfile is not None:
            blitText(screen=self.screen,
                     text='{}'.format(self.currentProfile.name),
                     font=Fonts.profile,
                     color=ScreenColors.black,
                     bottomRight=True,
                     horOffset=10,
                     verOffset=10)

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

        correct = self.quickPlayQuestion.lastReponseRating >= self.settings.spellingValue
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

        if profileName.strip() == '':
            return

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

        if not pygame.mixer.music.get_busy() and self.settings.musicOn:
            self.playNextSong()
        elif pygame.mixer.music.get_busy():
            self.stopSong()

    def playNextSong(self):
        nextSong = self.songs[0]

        pygame.mixer.music.load(nextSong)
        pygame.mixer.music.play()

        self.songs = self.songs[1:] + [nextSong]

    def stopSong(self):
        pygame.mixer.stop()

        self.songs = self.songs[1:] + [self.songs[0]]
