from data import PrintColors, readFile

import os

profileDir = 'files/profiles/'

def getAttribute(attribute, fileLines):
    results = []

    for line in fileLines:
        if line.strip().lower().startswith(attribute.strip().lower()):
            strippedLine = line.strip()[len(attribute):].strip()
            if strippedLine != '' and strippedLine[0] == ':':
                strippedLine = strippedLine[1:].strip()
            results.append(strippedLine)

    if len(results) == 0:
        return None

    elif len(results) == 1:
        return results[0]

    else:
        raise ValueError('More than one entry found for {}'.format(attribute))


def createProfile(ID, name):
    assert type(ID) is int
    assert type(name) is str

    name = name.strip()

    profileFile = '{}{}{}.txt'.format(profileDir, ID, name.lower())

    if not os.path.exists(profileFile):
        with open(profileFile, 'w') as f:
            f.write('ID: {}\n'.format(ID))
            f.write('name: {}\n'.format(name))
            f.write('file: {}\n'.format(profileFile))
            f.write('status: active\n')
            f.write('questions attempted: 0\n')
            f.write('questions correct: 0\n')
            f.write('default: false\n')

    newProfile = Profile(ID=ID,
                         name=name,
                         file_=profileFile,
                         status='active',
                         questionsAttempted=0,
                         questionsCorrect=0,
                         default=False)

    return newProfile


def getNextProfileID():
    ID = 0

    for file_ in os.listdir(profileDir):
        fileLines = readFile(profileDir + file_)

        newID = getAttribute('ID', fileLines)

        if newID is not None and newID.isdigit():
            ID = max(int(newID), ID)

    return ID + 1


def loadProfiles():
    profiles = []

    for file_ in os.listdir(profileDir):
        fileLines = readFile(profileDir + file_)

        status = getAttribute('status', fileLines)
        if status is None:
            raise ValueError('Cannot find status in {}'.format(file_))

        if status == 'active':
            ID = getAttribute('ID', fileLines)
            if ID is None:
                raise ValueError('Cannot find ID in {}'.format(file_))
            elif not ID.isdigit():
                raise ValueError('Value of {} not appropriate for ID in {}'.format(ID, file_))
            else:
                ID = int(ID)

            name = getAttribute('name', fileLines)
            if name is None:
                raise ValueError('Cannot find name in {}'.format(file_))

            questionsAttempted = getAttribute('questions attempted', fileLines)
            if questionsAttempted is None:
                raise ValueError('Cannot find questions attempted in {}'.format(file_))
            elif not questionsAttempted.isdigit():
                raise ValueError('Value of {} not appropriate for questions attempted in {}'.format(questionsAttempted, file_))
            else:
                questionsAttempted = int(questionsAttempted)

            questionsCorrect = getAttribute('questions correct', fileLines)
            if questionsCorrect is None:
                raise ValueError('Cannot find questions correct in {}'.format(file_))
            elif not questionsCorrect.isdigit():
                raise ValueError('Value of {} not appropriate for questions correct in {}'.format(questionsCorrect, file_))
            else:
                questionsCorrect = int(questionsCorrect)

            default = getAttribute('default', fileLines)
            if default is None:
                raise ValueError('Cannot find default in {}'.format(file_))
            elif default.lower() not in ['true', 'false']:
                raise ValueError('Value of {} not appropriate for default in {}'.format(default, file_))
            elif default.lower() == 'true':
                default = True
            else:
                default = False

            newProfile = Profile(ID=ID,
                                 name=name,
                                 file_=file_,
                                 status=status,
                                 questionsAttempted=questionsAttempted,
                                 questionsCorrect=questionsCorrect,
                                 default=default)

            profiles.append(newProfile)

    return profiles


class Profile:
    def __init__(self, ID=None, name=None, file_=None, status=None,
                 questionsAttempted=0, questionsCorrect=0,
                 default=False):
        assert type(ID) is int
        assert type(name) is str
        assert type(file_) is str
        assert type(status) is str
        assert type(questionsAttempted) is int
        assert type(questionsCorrect) is int
        assert type(default) is bool

        self.ID = ID
        self.name = name
        self.file = file_
        self.status = status

        self.questionsAttempted = questionsAttempted
        self.questionsCorrect = questionsCorrect

        self.default = default
