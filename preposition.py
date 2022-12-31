prepositions in the captions with randomly selected substitutes.
# The captions are processed using the Spacy library, and noun phrases in the captions are detected using a custom function.
# The preposition substitution is performed using a dictionary of substitutes.
# Input:
# - A text file containing a list of captions, one per line
#- The input file is encoded in UTF-8
# - The input file contains only valid English captions 
# Output:
# - A modified caption with prepositions replaced by substitutes

import os
import random
import spacy

nlp = spacy.load('en_core_web_sm')

def detection_of_noun_phrases(doc):
    noun_phrases = []
    current_noun_phrase = []
    for token in doc:
        if token.dep_ == 'compound':
            current_noun_phrase.append(token.text)
        elif token.dep_ == 'attr':
            current_noun_phrase.append(token.text)
        elif token.dep_ == 'dobj':
            current_noun_phrase.append(token.text)
        elif current_noun_phrase:
            noun_phrases.append(' '.join(current_noun_phrase))
            current_noun_phrase = []
    if current_noun_phrase:
        noun_phrases.append(' '.join(current_noun_phrase))
    return noun_phrases

prep_substitute_dict = {
    'in': {'at', 'on'},
    'on': {'at', 'in'},
    'at': {'in', 'on'},
}

real_captions_file = 'caption.txt'
real_captions = []

# Read in the list of captions from the 'new.en' file
with open(real_captions_file, 'r') as f:
    for line in f:
        real_captions.append(line.strip())

for p, caption in enumerate(real_captions):
    print("p:", p)
    substitution_cnt = 0
    doc = nlp(caption.lower())
    noun_phrases = detection_of_noun_phrases(doc)
    words = [token.text for token in doc]
    for i, token in enumerate(doc):
        if token.pos_ == 'ADP' and token.text in prep_substitute_dict:
            substitute = random.choice(list(prep_substitute_dict[token.text]))
            words[i] = substitute
    modified_caption = ' '.join(words)
    print(modified_caption)

