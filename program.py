from data import Colors
from profile import loadProfiles, Profile

class Program:
    def __init__(self):
        self.profiles = loadProfiles()

        self.currentProfile = self.profiles[0] # This is the default profile.

        for prof in self.profiles:
            if prof.default:
                self.currentProfile = prof
                break

        print('Profile {} loaded...'.format(self.currentProfile.name))

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
            Colors.underline, Colors.reset,
            Colors.underline, Colors.reset,
            Colors.underline, Colors.reset,
            Colors.underline, Colors.reset))
        print('{}->{} '.format(Colors.blink, Colors.reset), end='')

        response = input().strip().lower()

        while response not in ['create', 'select', 'delete', 'back']:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(Colors.blink, Colors.reset), end='')
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
            print('Would you like to make this the default profile? {}Yes{} or {}no{}?'.format(Colors.underline,
                                                                                               Colors.reset,
                                                                                               Colors.underline,
                                                                                               Colors.reset))
            print('{}->{} '.format(Colors.blink, Colors.reset), end='')

            response = input().strip().lower()
            while response not in ['yes', 'no']:
                print('Incorrect option supplied. Try again.')
                print('{}->{} '.format(Colors.blink, Colors.reset),
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
        print('{}->{} '.format(Colors.blink, Colors.reset), end='')

        response = input().strip().lower()
        while response not in [prof.nameNormal.lower() for prof in self.profiles]:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(Colors.blink, Colors.reset), end='')
            response = input().strip().lower()

        for num, nameNormal in enumerate([prof.nameNormal.lower() for prof in self.profiles]):
            if response == nameNormal:
                self.currentProfile = self.profiles[num]

        print('Profile {} now in use'.format(self.currentProfile.name))

    def deleteProfile(self):
        print('Please choose a profile to delete: {}'.format(', '.join([prof.name for prof in self.profiles])))
        print('{}->{} '.format(Colors.blink, Colors.reset), end='')

        response = input().strip().lower()
        while response not in [prof.nameNormal.lower() for prof in self.profiles]:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(Colors.blink, Colors.reset), end='')
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
        print('\nNo profiles loaded. Would you like to create your own? {}Yes{} or {}no{}?'.format(Colors.underline,
                                                                                                   Colors.reset,
                                                                                                   Colors.underline,
                                                                                                   Colors.reset))
        print('{}->{} '.format(Colors.blink, Colors.reset), end='')

        response = input().strip().lower()
        while response not in ['yes', 'no']:
            print('Incorrect option supplied. Try again.')
            print('{}->{} '.format(Colors.blink, Colors.reset), end='')
            response = input().strip().lower()

        if response == 'yes':
            self.createProfile()
        elif response == 'no':
            self.createGuestProfile()