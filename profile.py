from data import readFile, writeFile

from os import listdir
from os.path import exists

profileDir = 'files/profiles/'

def updateAttribute(attribute, newValue, file_, strict=False):
    assert type(attribute) is str
    assert type(newValue) in [str, int, bool]
    assert type(file_) is str
    assert type(strict) is bool

    fileLines = readFile(profileDir + file_)

    attribute = attribute.strip().lower()

    updated = False

    for num, line in enumerate(fileLines):
        line = line.strip().lower()

        if line.startswith(attribute):

            if type(newValue) is bool:
                newValue = 'true' if newValue else 'false'

            fileLines[num] = '{}: {}'.format(attribute, newValue)

            updated = True

    writeFile(fileLines, profileDir + file_)

    if strict and not updated:
        raise ValueError('Cannot find {} in {}'.format(attribute, file_))


def getAttribute(attribute, fileLines):
    results = []

    attribute = attribute.strip().lower()

    for line in fileLines:
        line = line.strip()
        if line.lower().startswith(attribute):
            strippedLine = line[len(attribute):].strip()
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

    profileFile = '{}{}.txt'.format(ID, name.lower())

    if not exists(profileDir + profileFile):
        with open(profileDir + profileFile, 'w') as f:
            f.write('id: {}\n'.format(ID))
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

    for file_ in listdir(profileDir):
        fileLines = readFile(profileDir + file_)

        newID = getAttribute('id', fileLines)

        if newID is not None and newID.isdigit():
            ID = max(int(newID), ID)

    return ID + 1


def loadProfiles():
    profiles = []

    for file_ in listdir(profileDir):
        fileLines = readFile(profileDir + file_)

        status = getAttribute('status', fileLines)
        if status is None:
            raise ValueError('Cannot find status in {}'.format(file_))

        if status == 'active':
            ID = getAttribute('id', fileLines)
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

    def updateID(self, newID=None, noFileUpdate=False):
        assert type(newID) is int
        assert type(noFileUpdate) is bool

        self.ID = newID

        if not noFileUpdate:
            updateAttribute('id', self.ID, self.file)

    def updateName(self, newName=None, noFileUpdate=False):
        assert type(newName) is str
        assert type(noFileUpdate) is bool

        self.name = newName

        if not noFileUpdate:
            updateAttribute('name', self.name, self.file)

    def updateStatus(self, newStatus=None, noFileUpdate=False):
        assert type(newStatus) is str
        assert type(noFileUpdate) is bool

        self.status = newStatus

        if not noFileUpdate:
            updateAttribute('status', 'inactive', self.file)

    def updateQuestionsAttempted(self, newQuestionsAttempted=None, noFileUpdate=False):
        assert type(newQuestionsAttempted) is int
        assert type(noFileUpdate) is bool

        self.questionsAttempted = newQuestionsAttempted

        if not noFileUpdate:
            updateAttribute('questions attempted', self.questionsAttempted, self.file)

    def updateQuestionsCorrect(self, newQuestionsCorrect=None, noFileUpdate=False):
        assert type(newQuestionsCorrect) is int
        assert type(noFileUpdate) is bool

        self.questionsCorrect = newQuestionsCorrect

        if not noFileUpdate:
            updateAttribute('questions correct', self.questionsCorrect, self.file)

    def updateDefault(self, newDefault=None, noFileUpdate=False):
        assert type(newDefault) is bool
        assert type(noFileUpdate) is bool

        self.default = newDefault

        if not noFileUpdate:
            updateAttribute('default', self.default, self.file)

    def setDefault(self, noFileUpdate=False):
        assert type(noFileUpdate) is bool

        self.updateDefault(True, noFileUpdate)

    def delete(self, noFileUpdate=False):
        assert type(noFileUpdate) is bool

        self.updateStatus('inactive', noFileUpdate)

    def rewriteFile(self):
        updateAttribute('id', self.ID, self.file)
        updateAttribute('name', self.name, self.file)
        updateAttribute('status', self.status, self.file)
        updateAttribute('questions attempted', self.questionsAttempted, self.file)
        updateAttribute('questions correct', self.questionsCorrect, self.file)
        updateAttribute('default', self.default, self.file)