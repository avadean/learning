import pygame

from data import PrintColors, ScreenColors
from profile import loadProfiles, Profile


def flipDisplay():
    pygame.display.flip()


class Program:
    pygame.init()

    clock = pygame.time.Clock()

    screenWidth = 1024
    screenHeight = 768
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(ScreenColors.fill)

    def __init__(self):
        self.running = True
        self.state = 'main menu'

        self.profiles = None
        self.currentProfile = None
        self.getProfiles()

        self.quickPlayButton = None
        self.learnButton = None
        self.profilesButton = None
        self.settingsButton = None
        self.exitButton = None
        self.createButtons()

    def getProfiles(self):
        self.profiles = loadProfiles()
        self.currentProfile = self.profiles[0] # This is the Guest profile.

        for prof in self.profiles:
            if prof.default:
                self.currentProfile = prof
                break

        print('Profile {} loaded...'.format(self.currentProfile.name))

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos

                if self.state == 'main menu':
                    if self.quickPlayButton.collidepoint(mousePos):
                        print('button was pressed at {}'.format(mousePos))

    def createButtons(self):
        mainMenuButtonWidth = 280
        mainMenuButtonHeight = 40

        self.learnButton = pygame.Rect((self.screenWidth - mainMenuButtonWidth) // 2,
                                       1 * self.screenHeight // 6,
                                       mainMenuButtonWidth,
                                       mainMenuButtonHeight)

        self.profilesButton = pygame.Rect((self.screenWidth - mainMenuButtonWidth) // 2,
                                           2 * self.screenHeight // 6,
                                           mainMenuButtonWidth,
                                           mainMenuButtonHeight)

        self.quickPlayButton = pygame.Rect((self.screenWidth - mainMenuButtonWidth) // 2,
                                           3 * self.screenHeight // 6,
                                           mainMenuButtonWidth,
                                           mainMenuButtonHeight)

        self.settingsButton = pygame.Rect((self.screenWidth - mainMenuButtonWidth) // 2,
                                           4 * self.screenHeight // 6,
                                           mainMenuButtonWidth,
                                           mainMenuButtonHeight)

        self.exitButton = pygame.Rect((self.screenWidth - mainMenuButtonWidth) // 2,
                                       5 * self.screenHeight // 6,
                                       mainMenuButtonWidth,
                                       mainMenuButtonHeight)

    def draw(self):
        if self.state == 'main menu':
            self.drawMainMenu()

    def drawMainMenu(self):
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.learnButton)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.profilesButton)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.quickPlayButton)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.settingsButton)
        pygame.draw.rect(self.screen, ScreenColors.buttons, self.exitButton)

        #text = font.render('Button text', 1, (136, 255, 0))

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