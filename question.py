from data import PrintColors, getStrVersion
from difflib import SequenceMatcher
from imghdr import what
from os import path
from PIL import Image
from random import shuffle

imagesDir = 'images/'

assert path.isdir(imagesDir), \
    '{} directory for images not found.'.format(imagesDir)

questionCategories = ['cells', 'biology']


class Question:
    def __init__(self, question=None, answer=None, answers=None,
                 options=None, image=None, hint=None,
                 categories=None):
        self.question = ''
        self.answers = []
        self.options = None
        self.image = None
        self.hint = None

        self.lastResponse = None
        self.lastReponseRating = None
        self.exactResponse = None
        # self.exactResponse is the 'exact' version of the response given
        # e.g. say the acceptable answers are ['black', 'dark']
        # if the lastResponse is 'blakc' then the exactResponse is 'black'
        # this is because the code will identify that 'blakc' was a spelling error of 'black'
        # and so the answer is accepted but the exact answer that was wanted was 'black'
        self.categories = []

        assert question is not None, 'A question must be supplied'
        assert type(question) is str
        self.question = question

        assert answer is not None or answers is not None, 'Either answer or answers must be given'

        if answer is not None:
            self.processAnswer(answer)

        if answers is not None:
            assert type(answers) is list
            for ans in answers:
                self.processAnswer(ans)

        if options is not None:
            assert type(options) is list
            assert len(options) > 1

            self.options = [str(option) for option in options]
            shuffle(self.options)

        if image is not None:
            assert type(image) is str
            assert what(imagesDir + image) in ['jpg', 'jpeg', 'png'], \
                '{} is not an image file'.format(imagesDir + image)

            self.image = Image.open(imagesDir + image)

        if hint is not None:
            assert type(hint) is str

            if len(hint) > 0:
                self.hint = hint[0].upper() + hint[1:].lower()

        if categories is not None:
            assert type(categories) is list
            assert all(category in questionCategories for category in categories), \
                'Question categories accepted are {}'.format(', '.join(questionCategories))

            self.categories = categories

    def processAnswer(self, answer):
        if type(answer) is str:
            self.answers.append(answer)
        else:
            strVersion = getStrVersion(answer)
            assert strVersion is not None, 'Answer {} not recognised'.format(answer)
            self.answers.append(strVersion)

    def addCategory(self, category=None):
        acceptedCategories = ['biology', 'cells']
        assert category in acceptedCategories, 'Question category must be in {}'.format(', '.join(acceptedCategories))

        if category not in self.categories:
            self.categories.append(category)

    def ask(self, spelling=1.0, keepAsking=False):
        if self.image is not None:
            self.image.show()

        self.printQuestion()
        self.takeResponse()
        self.calcExactResponseWithRating()

        correct = False

        while self.lastReponseRating < spelling:
            if self.lastResponse == '':
                print(u'\u23F9  skipping.\n')
                break
            elif keepAsking:
                print(u'\u274C incorrect')
                self.takeResponse('    ')
                self.calcExactResponseWithRating()
            else:
                print(u'\u274C incorrect\n')
                break
        else:
            correct = True
            print(u'\u2705 correct!{}\n'.format('{} Exact answer is: {}{}'.format(PrintColors.lightYellow,
                                                                                  self.exactResponse,
                                                                                  PrintColors.reset)
                                                if self.lastReponseRating < 1.0 else ''))

        # if self.image is not None:
        #     self.image.close()

        return correct

    def takeResponse(self, prompt=''):
        self.lastResponse = input(prompt).strip().lower()

    def calcExactResponseWithRating(self):
        # see init for explanation of what an exactResponse is

        ratings = [SequenceMatcher(None, self.lastResponse, ans).ratio() for ans in self.answers]

        bestRating = 0.0
        index = 0

        for num, rating in enumerate(ratings):
            if rating > bestRating:
                index = num
                bestRating = rating

        if bestRating == 0.0:
            self.exactResponse = None
            self.lastReponseRating = 0.0
        else:
            self.exactResponse = self.answers[index]
            self.lastReponseRating = bestRating

    def printQuestion(self, withAnswer=False):
        ques = self.getQuestion(withAnswer)
        print(ques)

    def getQuestion(self, withHint=True, withOptions=True, withAnswer=False):
        ques = '{}{}{}'.format(PrintColors.question,
                               self.question,
                               PrintColors.reset)

        if self.options is not None and withOptions and not withAnswer:
            ques += ' {}{}{}'.format(PrintColors.options,
                                     self.options[0][0].upper() +
                                     self.options[0][1:].lower(),
                                     PrintColors.reset)

            if len(self.options) > 2:
                ques += ', '
                for option in self.options[1:-1]:
                    ques += '{}{}{}, '.format(PrintColors.options,
                                              option,
                                              PrintColors.reset)
                ques = ques[:-2]  # Get rid of the last ', '
                # ques += ', '.join(self.options[1:-1])

            ques += ' or {}{}{}?'.format(PrintColors.options,
                                         self.options[-1],
                                         PrintColors.reset)

        if self.hint is not None and withHint and not withAnswer:
            ques += ' {}({}){}'.format(PrintColors.hint,
                                       self.hint,
                                       PrintColors.reset)

        if withAnswer:
            ques += ' {}{}{}'.format(PrintColors.answer,
                                     self.answer[0].upper() + self.answer[1:].lower(),
                                     PrintColors.reset)
        else:
            ques += '\n    {}'.format(PrintColors.reset)

        return ques


biologyQuestions = [Question('There are four types of biological molecules that are the \'ingredients for life\'. '
                             'Carbohydrates, lipids, proteins and what other?',
                             answer='nucleic acids',
                             answers=['nucleic']),

                    Question('There are four types of biological molecules that are the \'ingredients for life\'. '
                             'Carbohydrates, lipids, nucleic acids and what other?',
                             answer='proteins'),

                    Question('There are four types of biological molecules that are the \'ingredients for life\'. '
                             'Carbohydrates, nucleic acids, proteins and what other?',
                             answer='lipids'),

                    Question('There are four types of biological molecules that are the \'ingredients for life\'. '
                             'Nucleic acids, lipids, proteins and what other?',
                             answer='carbohydrates'),

                    Question('What polysaccharide is the main short-term energy storage in animals, fungi and bacteria?',
                             answer='glycogen'),

                    Question('What macromolecules are the main long-term energy storage in animals?',
                             answer='lipids'),

                    Question('Glycerol plus three fatty acids gives what?',
                             answer='triglyceride')
                    ]

cellsQuestions = [Question('How many cells is a prokaryote?',
                           answer=1,
                           options=['one', 'many']),

                  Question('How many cells is a eukaryote?',
                           answer='many',
                           options=['one', 'many']),

                  Question('The major component of the cell membrane is a lipid bilayer. What phospholipids is this lipid '
                           'bilayer mainly made up of?',
                           answer='amphipathic',
                           options=['hydrophilic', 'hydrophobic', 'amphipathic']),

                  Question('Do prokaryotes have a nucleus?',
                           answer=False),

                  Question('Do eukaryotes have a nucleus?',
                           answer=True),

                  Question('Where does the DNA reside inside prokaryotes?',
                           answer='cell',
                           options=['cell', 'nucleus']),

                  Question('Where does the DNA reside inside eukaryotes?',
                           answer='nucleus',
                           options=['cell', 'nucleus']),

                  Question('Is the membrane that surrounds the nucleus a single or double lipid bilayer?',
                           answer='double',
                           options=['single', 'double']),

                  Question('Is the membrane that surrounds the cell a single or double lipid bilayer?',
                           answer='single',
                           options=['single', 'double']),

                  Question('Are the organelle structures large or small?',
                           answer='large',
                           options=['large', 'small']),

                  Question('Are the vesicles and tubules large or small?',
                           answer='small',
                           options=['large', 'small']),

                  Question('What are the contents of the eukaryotic cell referred to?',
                           answer='cytoplasm',
                           options=['cytoplasm', 'cytosol', 'organelle', 'vesicle', 'tubule', 'lumen']),

                  Question('What is the aqueous part of the cytoplasm called?',
                           answer='cytosol',
                           options=['cytosol', 'organelle', 'vesicle', 'tubule', 'lumen']),

                  Question('What is the inside of an organelle, vesicle or tubule called?',
                           answer='lumen'),

                  Question('What is the process of DNA turning into mRNA called?',
                           answer='transcription',
                           options=['transcription', 'translation']),

                  Question('What is the process of mRNA turning into protein called?',
                           answer='translation',
                           options=['transcription', 'translation']),

                  Question('What turns DNA into mRNA?',
                           answer='polymerase',
                           options=['polymerase', 'ribosomes']),

                  Question('What turns mRNA into protein?',
                           answer='ribosomes',
                           options=['polymerase', 'ribosomes']),

                  Question('In prokaryotes, does transcription and translation occur in the same space?',
                           answer=True),

                  Question('In eukaryotes, does transcription and translation occur in the same space?',
                           answer=False),

                  Question('Is the inside of a cell a highly crowded environment?',
                           answer=True),

                  Question('The proteins that aid interaction with exterior environments of cells have been '
                           'post-translationally modified by the addition of what residues?',
                           answer='sugar'),

                  Question('Which organelle harbours the majority of the DNA within a cell?',
                           answer='nucleus',
                           options=['nucleus', 'endoplasmic reticulum', 'Golgi apparatus', 'mitochondria', 'lysosomes',
                                    'endosomes', 'peroxisomes', 'chloroplasts']),

                  Question('Endosymbiosis is where one organism lives inside or alongside another organism?',
                           answer='inside',
                           options=['inside', 'alongside']),

                  Question('Does gene transcription occur in the nucleus?',
                           answer=True),

                  Question('Does mRNA processing occur in the nucleus?',
                           answer=True),

                  Question('Does ribosome assembly occur in the nucleus?',
                           answer=True),

                  Question('Is the membrane that surrounds mitochondria a single or double lipid bilayer?',
                           answer='double',
                           options=['single', 'double']),

                  Question('What is the energy source for reactions of the cell?',
                           answer='atp',
                           answers=['adenosine triphosphate']),

                  Question('Do mitochondria contain DNA?',
                           answer=True),

                  Question('Does the inner or outer membrane of mitochondria contain mitochondrial ATP synthase?',
                           answer='inner',
                           options=['inner', 'outer']),

                  Question('Peroxisomes contain high concentrations of what type of enzymes?',
                           answer='oxidative',
                           options=['oxidative', 'reductive']),

                  Question('Is the job of peroxisomes to create or eliminate substances?',
                           answer='eliminate'),

                  Question('Is the membrane that surrounds endoplasmic reticulum a single or double lipid bilayer?',
                           answer='single',
                           options=['single', 'double']),

                  Question('What does the endoplasmic reticulum store?',
                           answer='calcium',
                           answers=['ca']),

                  Question('Regulated release of what, in response to extracellular signals, leads to change in activity of '
                           'cell processes?',
                           answer='calcium',
                           answers=['ca']),

                  Question('Is the endoplasmic reticulum responsible for lipid biosynthesis?',
                           answer=True),

                  Question('Is the endoplasmic reticulum responsible for the synthesis of proteins?',
                           answer=True),

                  Question('The space between the two lipid bilayers of the nucleus is known as the what?',
                           answer='lumen'),

                  Question('Membrane proteins are proteins that reside inside the membranes of organelles and allow for the '
                           'transport in and out of the organelle. Roughly how many proteins are membrane proteins?',
                           answer='third',
                           options=['all', 'half', 'third', 'quarter', 'eighth', 'none']),

                  Question('Where is DNA transcribed (turned into mRNA)?',
                           answer='nucleus'),

                  Question('Where is mRNA translated (turned into protein)?',
                           answer='cytosol'),

                  Question('Where do newly created proteins (from mRNA) attach to?',
                           answer='endoplasmic reticulum',
                           answers=['er']),

                  Question('Unless it is destined to be a membrane protein, where does a newly created protein end up after it '
                           'passes through the protein-lined channel in the endoplasmic reticulum membrane?',
                           answer='lumen',
                           options=['lumen', 'cytosol', 'cytoplasm', 'nucleus', 'Golgi apparatus']),

                  Question('After a protein is newly created, where does it end up first on its pathway out of the eukaryotic '
                           'cell?',
                           answer='endoplasmic reticulum',
                           answers=['er'],
                           options=['endoplasmic reticulum', 'Golgi apparatus', 'cytosol', 'nucleus']),

                  Question('In the secretory pathway, what comes first? The endoplasmic reticulum or the Golgi apparatus?',
                           answer='endoplasmic reticulum',
                           answers=['er']),

                  Question('What transports proteins from the endoplasmic reticulum to the Golgi apparatus?',
                           answer='vesicles'),

                  Question('What face of the Golgi apparatus do vesicles deliver proteins to?',
                           answer='cis',
                           options=['cis', 'trans', 'medial']),

                  Question('Where are newly created proteins folded?',
                           answer='endoplasmic reticulum',
                           answers=['er'],
                           options=['endoplasmic reticulum', 'Golgi apparatus']),

                  Question('What directions can protein traffic move in the Golgi apparatus?',
                           answer='both',
                           options=['forward', 'backward', 'both']),

                  Question('What is the forward movement of protein traffic in the Golgi apparatus called?',
                           answer='anterograde',
                           options=['anterograde', 'retrograde']),

                  Question('What is the backward movement of protein traffic in the Golgi apparatus called?',
                           answer='retrograde',
                           options=['anterograde', 'retrograde']),

                  Question('Do sugar residues get added to proteins in the endoplasmic reticulum?',
                           answer=False),

                  Question('Do sugar residues get added to proteins in the Golgi apparatus?',
                           answer=True),

                  Question('Do sugar residues get added to proteins in the nucleus?',
                           answer=False),

                  Question('Is the Golgi apparatus responsible for transporting the newly created proteins to the cell '
                           'membrane and/or other cell organelles?',
                           answer=True),

                  Question('Is the endoplasmic reticulum responsible for transporting the newly created proteins to the cell '
                           'membrane and/or other cell organelles?',
                           answer=False),

                  Question('What is the main function of lysosomes?',
                           answer='recycling',
                           options=['recycling', 'protein creation', 'mRNA creation', 'ATP production']),

                  Question('From where can a transcription factor move from to the nucleus to reduce the level of mRNA '
                           'processing and in turn reduce the activity of the cell if it is being starved?',
                           answer='lysosome'),

                  Question('Where are macromolecules delivered to to be broken down into their building blocks (e.g proteins '
                           'to amino acids and polysaccharides to monosaccharides)?',
                           answer='lysosome'),

                  Question('The enzymes that hydrolyse macromolecules in the lysosome are acid hydrolases or alkali '
                           'hydrolases?',
                           answer='acid'),

                  Question('What is the pH type of the lumen of the lysosome?',
                           answer='acidic',
                           options=['acidic', 'alkaic', 'neutral']),

                  Question('What is the pH type of the Golgi and trans-Golgi network?',
                           answer='acidic',
                           options=['acidic', 'alkaic', 'neutral']),

                  Question('What is the pH type of the cytosol?',
                           answer='alkaic',
                           options=['acidic', 'alkaic', 'neutral']),

                  Question('From the trans Golgi network, what intermediate compartment are lysosomal enzymes delivered to?',
                           answer='late endosome',
                           options=['late endosome', 'nucleus', 'Golgi apparatus', 'mitochondria', 'endoplasmic reticulum']),

                  Question(
                      'What is the general term for the process of internalisation of material from the cell surface known '
                      'as?',
                      answer='endocytosis'),

                  Question('Are the vesicles that are formed from the internalisation of material from the cell surface known '
                           'as early or late endosomes?',
                           answer='early'),

                  Question('What is the pH type of early endosomes?',
                           answer='acidic',
                           options=['acidic', 'alkaic', 'neutral']),

                  Question('What are the endosomes that return material to the cell surface called?',
                           answer='recycling',
                           options=['recycling', 'early', 'late']),

                  Question('The transferrin receptor releases iron that is bound to transferrin in the early endosome or '
                           'recycling endosome. Once this process is completed, the receptor returns to the surface via an '
                           'endosome. What type of endosome would this be?',
                           answer='recycling',
                           options=['recycling', 'early', 'late']),

                  Question('The epidermal growth factor receptor transmits signals which trigger cell growth and cell '
                           'division. These signals need to be regulated by the cell and thus these receptors need to be '
                           'degraded in the lysosome. What type of endosome would transport these receptors to the lysosome?',
                           answer='late',
                           options=['recycing', 'early', 'late']),

                  Question('What is the framework that gives a cell its structure and spatial organisation?',
                           answer='cytoskeleton'),

                  Question('Does the movement of vesicles and tubules between compartments occur at random?',
                           answer=False),

                  Question('What are the proteins called that vesicles and tubules depend on for their movement?',
                           answer='motor',
                           answers=['motor proteins']),

                  Question('The cytoskeleton is made up of microtubules, actin filaments and what other type of filament?',
                           answer='intermediate',
                           answers=['intermediate filament']),

                  Question('The cytoskeleton is made up of microtubules, intermediate filaments and what other type of '
                           'filament?',
                           answer='actin',
                           answers=['actin filament']),

                  Question('The cytoskeleton is made up of actin filaments, intermediate filaments and what other type of '
                           'tubule?',
                           answer='micro',
                           answers=['microtubule']),

                  Question('What part of the cytoskeleton is best described by \'long hollow tubes\'?',
                           answer='microtubules',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton is best described by \'double-stranded helical polymer\'?',
                           answer='actin filaments',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton is best described by \'elongated and fibrous subunits\'?',
                           answer='intermediate filaments',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton localises organelles within the cell?',
                           answer='microtubules',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton provides tracks along which many vesicles and tubules move?',
                           answer='microtubules',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton is pivotal in the physical separation of chromosomes during mitosis?',
                           answer='microtubules',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton provides the shape of the cell\'s surface?',
                           answer='actin filaments',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('What part of the cytoskeleton plays a major roles in the protrusion of material from the cell '
                           'surface?',
                           answer='actin filaments',
                           options=['microtubules', 'actin filaments', 'intermediate filaments']),

                  Question('Are microtubules dynamic structures?',
                           answer=True),

                  Question('Are actin filaments dynamic structures?',
                           answer=True),

                  Question('Are intermediate filaments dynamic structures?',
                           answer=False),

                  Question('What part of the cytoskeleton provides mechanical strength to the cell?',
                           answer='intermediate filaments',
                           options=['microtubules', 'actin filaments', 'intermediate filaments'])
                  ]

biologyCellsQuestions = [Question('What group is the hydrophilic head of the constituents of a cell membrane made from?',
                                  answer='phosphate',
                                  answers=['phosphate group']),

                         Question('What acids are the hydrophobic tail of the constituents of a cell membrane made from?',
                                  answer='fatty',
                                  answers=['fatty acids'])
                         ]

for q in biologyQuestions:
    q.addCategory('biology')

for q in cellsQuestions:
    q.addCategory('cells')

questions = cellsQuestions + biologyQuestions