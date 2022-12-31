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

def substitute_prepositions(doc, prep_substitute_dict):
    words = [token.text for token in doc]
    for i, token in enumerate(doc):
        if token.pos_ == 'ADP' and token.text in prep_substitute_dict:
            substitute = random.choice(list(prep_substitute_dict[token.text]))
            words[i] = substitute
    return ' '.join(words)

def modify_captions(captions, prep_substitute_dict):
    modified_captions = []
    for caption in captions:
        doc = nlp(caption.lower())
        noun_phrases = detection_of_noun_phrases(doc)
        modified_caption = substitute_prepositions(doc, prep_substitute_dict)
        modified_captions.append(modified_caption)
    return modified_captions

def main():
    prep_substitute_dict = {
        'in': {'at', 'on'},
        'on': {'at', 'in'},
        'at': {'in', 'on'},
    }

    real_captions_file = 'input.txt'
    real_captions = []

    # Read in the list of captions from the file
    with open(real_captions_file, 'r') as f:
        for line in f:
            real_captions.append(line.strip())

    modified_captions = modify_captions(real_captions, prep_substitute_dict)
    for p, modified_caption in enumerate(modified_captions):
        print(f"p: {p}")
        print(modified_caption)

if __name__ == '__main__':
    main()

