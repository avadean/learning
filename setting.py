
spellingLevel = {'exact': 1.0,
                 'strict': 0.9,
                 'moderate': 0.8,
                 'fair': 0.7,
                 'leniant': 0.6,
                 'easy': 0.5
                 }


class Settings:
    def __init__(self, spelling='moderate'):
        self.spelling = spellingLevel.get(spelling, None)

        assert self.spelling is not None,\
            'Accepted spelling settings: {}'.format(', '.join(spellingLevel))
