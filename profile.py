from data import Colors


def loadProfiles():
    guestProfile = Profile('Guest')

    profiles = [guestProfile]

    # Find all the profiles...
    #
    #

    if sum(True if prof.default else False for prof in profiles) > 1:
        defaultProfile = None
        foundDefaultProfile = False

        for prof in profiles:
            if prof.default:
                if not foundDefaultProfile:
                    foundDefaultProfile = True
                    defaultProfile = prof
                else:
                    prof.default = False

        print('Warning: more than one profile set as default')
        print('Setting {}{}{} to default profile'.format(Colors.underline,
                                                         defaultProfile.name,
                                                         Colors.reset))

    return profiles


class Profile:
    def __init__(self, name=None,
                 questionsAttempted=0, questionsCorrect=0,
                 default=False):
        assert type(name) is str
        assert type(questionsAttempted) is int
        assert type(questionsCorrect) is int
        assert type(default) is bool

        self.name = '{}{}{}'.format(Colors.underline, name, Colors.reset)
        self.nameNormal = name

        self.questionsAttempted = questionsAttempted
        self.questionsCorrect = questionsCorrect

        self.default = default

    def __str__(self):
        string = '{}{}{}\n'.format(Colors.underline,
                                   self.name,
                                   Colors.reset)

        string += 'Questions attempted: {}'.format(self.questionsAttempted)
        string += 'Questions correct  : {}'.format(self.questionsCorrect)

        return string