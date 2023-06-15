import os

from bs4 import BeautifulSoup

# Root directory where sub-directories are stored
corpus_directory = ''

# We create a dictionary for storing entities count
entity_counter = {'PER': 0,
                  'LOC': 0,
                  'TER': 0}

for subdir, dirs, files in os.walk(corpus_directory):
    for file in files:
        PER_counter = 0
        LOC_counter = 0
        TER_counter = 0
        print(f'Processing {file} in sub-directory {subdir}')
        print(entity_counter)
        with open(os.path.join(subdir, file), mode='r', encoding='utf-8') as fh:
            # we create a list for storing (token, label)
            annotations = []
            # parsing the XML-TEI file
            soup = BeautifulSoup(fh, features='xml')
            # looking for <body>
            for elem in soup.find_all("body"):
                # by default, we iterate on all <p>s, can be modified depending on the TEI tree
                for p in elem.find_all("p"):
                    # we iterate on all children of <p>
                    for child in p.children:
                        # if child is <term>, we have an entity
                        if child.name == 'term':
                            # we keep track of said entity count
                            TER_counter += 1
                            # if tokenized child has more than one token, then it's a multi-token entity
                            if len(child.text.split()) > 1:
                                counter = 0 
                                for token in child.text.split():
                                    if counter > 0:
                                        annotations.append((token, 'I-TER'))
                                    else:
                                        annotations.append((token, 'B-TER'))
                                    counter += 1
                            # otherwise, it's a single token entity
                            else:
                                label = 'B-TER'
                                for token in child.text.split():
                                    annotations.append((token, label))

                        # same logic is used for remaining entities
                        elif child.name == 'placeName':
                            LOC_counter += 1
                            if len(child.text.split()) > 1:
                                counter = 0 
                                for token in child.text.split():
                                    if counter > 0:
                                        annotations.append((token, 'I-LOC'))
                                    else:
                                        annotations.append((token, 'B-LOC'))
                                    
                                    counter += 1
                            else:
                                label = 'B-LOC'
                                for token in child.text.split():
                                    annotations.append((token, label))

                        elif child.name == 'persName':
                            PER_counter += 1
                            if len(child.text.split()) > 1:
                                counter = 0 
                                for token in child.text.split():
                                    if counter > 0:
                                        annotations.append((token, 'I-PER'))
                                    else:
                                        annotations.append((token, 'B-PER'))
                                    
                                    counter += 1
                            else:
                                label = 'B-PER'
                                for token in child.text.split():
                                    annotations.append((token, label))

                        # if child is not an annotated entity, then it's a simple token
                        else:
                            label = 'O'
                            for token in child.text.split():
                                annotations.append((token, label))        

        # updating the entities count
        entity_counter['LOC'] += LOC_counter
        entity_counter['PER'] += PER_counter
        entity_counter['TER'] += TER_counter

        # writing a new directory for storing annotations, based on subdir name
        if not os.path.exists(f'{subdir.split("/")[-1]}'):
            os.makedirs(f'{subdir.split("/")[-1]}')

        # writing the annotations in bio format
        with open(f'{subdir.split("/")[-1]}/{file}_iob.txt', mode='w+', encoding='utf-8') as bio_file:
            for annotation in annotations:
                bio_file.write('\t'.join(str(item) for item in annotation) + '\n')

# printing entities count
print(entity_counter)