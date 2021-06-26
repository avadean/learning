from data import Colors, intToStr
from difflib import SequenceMatcher
from imghdr import what
from os import path
from PIL import Image
from random import shuffle


imagesDir = 'images/'

assert path.isdir(imagesDir),\
    '{} directory for images not found.'.format(imagesDir)


class Question:
    def __init__(self, question=None, answer=None, answers=None,
                 options=None, image=None, hint=None):
        self.question = ''
        self.answer = ''
        self.answers = []
        self.options = None
        self.image = None
        self.hint = None

        self.lastResponse = None

        assert question is not None, 'A question must be supplied'
        assert type(question) is str
        self.question = question

        assert answer is not None, 'A preferable answer must be given, even if multiple answers are acceptable'

        self.answer = str(answer).lower()
        self.answers.append(str(answer).lower())
        if intToStr.get(answer, None) is not None:
            self.answers.append(intToStr[answer].lower())

        if answers is not None:
            assert type(answers) is list
            for ans in answers:
                self.answers.append(str(ans).lower())
                if intToStr.get(ans, None) is not None:
                    self.answers.append(intToStr[ans].lower())

        if options is not None:
            assert type(options) is list
            assert len(options) > 1

            self.options = [str(option) for option in options]
            shuffle(self.options)

        if image is not None:
            assert type(image) is str
            assert what(imagesDir + image) in ['jpg', 'jpeg', 'png'],\
                '{} is not an image file'.format(imagesDir + image)

            self.image = Image.open(imagesDir + image)

        if hint is not None:
            assert type(hint) is str

            if len(hint) > 0:
                self.hint = hint[0].upper() + hint[1:].lower()

    def ask(self, spelling=1.0, keepAsking=False):
        if self.image is not None:
            self.image.show()

        prompt = '{}{}{}'.format(Colors.question,
                                 self.question,
                                 Colors.reset)

        if self.options is not None:
            prompt += ' {}{}{}'.format(Colors.options,
                                       self.options[0][0].upper() +
                                       self.options[0][1:].lower(),
                                       Colors.reset)

            if len(self.options) > 2:
                prompt += ', '
                for option in self.options[1:-1]:
                    prompt += '{}{}{}, '.format(Colors.options,
                                                option,
                                                Colors.reset)
                prompt = prompt[:-2] # Get rid of the last ', '
                # prompt += ', '.join(self.options[1:-1])

            prompt += ' or {}{}{}?'.format(Colors.options,
                                          self.options[-1],
                                          Colors.reset)

        if self.hint is not None:
            prompt += ' {}({}){}'.format(Colors.hint,
                                         self.hint,
                                         Colors.reset)

        prompt += '\n    {}'.format(Colors.reset)

        correct = False
        spellingMatch = self.takeResponse(prompt)

        while spellingMatch < spelling:
            if self.lastResponse == '':
                print(u'\u23F9  skipping.\n')
                break
            elif keepAsking:
                print(u'\u274C incorrect')
                spellingMatch = self.takeResponse('    ')
            else:
                print(u'\u274C incorrect\n')
                break
        else:
            correct = True
            print(u'\u2705 correct!{}\n'.format(
                ' Exact answer is: {}'.format(self.answer)
                if spellingMatch < 1.0 else ''))

        # if self.image is not None:
        #     self.image.close()

        return 1 if correct else 0

    def takeResponse(self, prompt):
        self.lastResponse = input(prompt).strip().lower()

        rating = max([SequenceMatcher(None, self.lastResponse, ans).ratio()
                      for ans in self.answers])

        return rating


cellQuestions = [Question('How many cells is a prokaryote?',
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
                          answer='no'),

                 Question('Do eukaryotes have a nucleus?',
                          answer='yes'),

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
                          answer='yes'),

                 Question('In eukaryotes, does transcription and translation occur in the same space?',
                          answer='no'),

                 Question('Is the inside of a cell a highly crowded environment?',
                          answer='yes'),

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
                          answer='yes'),

                 Question('Does mRNA processing occur in the nucleus?',
                          answer='yes'),

                 Question('Does ribosome assembly occur in the nucleus?',
                          answer='yes'),

                 Question('Is the membrane that surrounds mitochondria a single or double lipid bilayer?',
                          answer='double',
                          options=['single', 'double']),

                 Question('What is the energy source for reactions of the cell?',
                          answer='atp',
                          answers=['adenosine triphosphate']),

                 Question('Do mitochondria contain DNA?',
                          answer='yes'),

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
                          answer='yes'),

                 Question('Is the endoplasmic reticulum responsible for the synthesis of proteins?',
                          answer='yes'),

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
                          answer='no'),

                 Question('Do sugar residues get added to proteins in the Golgi apparatus?',
                          answer='yes'),

                 Question('Do sugar residues get added to proteins in the nucleus?',
                          answer='no'),

                 Question('Is the Golgi apparatus responsible for transporting the newly created proteins to the cell '
                          'membrane and/or other cell organelles?',
                          answer='yes'),

                 Question('Is the endoplasmic reticulum responsible for transporting the newly created proteins to the cell '
                          'membrane and/or other cell organelles?',
                          answer='no'),

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

                 Question('What is the general term for the process of internalisation of material from the cell surface known '
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
                          answer='no'),

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
                          answer='yes'),

                 Question('Are actin filaments dynamic structures?',
                          answer='yes'),

                 Question('Are intermediate filaments dynamic structures?',
                          answer='no'),

                 Question('What part of the cytoskeleton provides mechanical strength to the cell?',
                          answer='intermediate filaments',
                          options=['microtubules', 'actin filaments', 'intermediate filaments'])
                 ]

questions = cellQuestions