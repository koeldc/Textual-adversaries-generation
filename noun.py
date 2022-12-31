#This script reads a text file, replaces frequent nouns with less frequent synonyms, and writes the modified text to a new file.
#To determine which nouns to replace, the script first extracts all nouns from the input text and counts their frequency.
#Next, it filters the nouns to keep only those that are deemed "concrete" based on a predefined list of concrete words.
#Finally, it selects synonyms for each concrete noun by comparing the Wu-Palmer Similarity (WUP) scores of all nouns in the input text with the target noun.
#A synonym is selected if it has a WUP score less than 0.8 with the target noun
import spacy
import codecs
from nltk.corpus import wordnet as wn

def match(word, substitute):
    synset_word = wn.synsets(word)
    synset_substitute = wn.synsets(substitute)
    for item_1 in synset_word:
        for item_2 in synset_substitute:
            if item_1.wup_similarity(item_2) > 0.8:
                return False
    return True

def get_noun_chunks(text):
    """
    Extract noun chunks from a text and create a list of tags indicating which words should be replaced.
    A noun chunk is a contiguous sequence of words that includes a noun and the words that modify it.
    Only English noun chunks are extracted.

    Parameters:
    text (str): The text to extract noun chunks from.

    Returns:
    tuple: A tuple containing two lists:
        words (list): A list of words in the text.
        replace_tags (list): A list of boolean values indicating which words should be replaced (True) and which should not (False).
    """
    text_info = nlp(text)
    words = [x.text for x in text_info]
    replace_tags = [False] * len(words)
    for chunk in text_info.noun_chunks:
        if chunk.text.isalpha() and chunk.text.islower():
            replace_tags[chunk.end - 1] = True
    return words, replace_tags

nlp = spacy.load('en_core_web_sm')

# Read input file
with open('input.txt', 'r') as f:
    real_captions = f.readlines()

# Extract frequent nouns
frequent_words = {}
for caption in real_captions:
    caption = nlp(caption.lower())
    for word in caption:
        if word.pos_ == 'NOUN' and word.lemma_ != '--PRON--':
            word = word.text
            if word in frequent_words:
                frequent_words[word] += 1
            else:
                frequent_words[word] = 1
frequent_words_set = set(frequent_words)

# Extract concrete nouns and their candidate substitutes
candidate_words = {}
concreteness = [line.split() for line in codecs.open('concreteness.txt').readlines()]
concrete_words = set([item[0] for item in concreteness if float(item[1]) > 0.1])
for w in frequent_words:
    if w in concrete_words:
        candidate_words[w] = [x for x in frequent_words_set if match(w, x)]

# Replace nouns with substitutes
temp_list = []
invalid_words = set()
for caption in real_captions:
    words, replace_tags = get_noun_chunks(caption)
    for i in range(len(words)):
        if not replace_tags[i] or words[i] in invalid_words:
            temp_list.append(words[i])
            continue
        substitute_selected = False
        for w in candidate_words[words[i]]:
            if w not in invalid_words:
                temp_list.append(w)
                substitute_selected = True
                break
        if not substitute_selected:
            temp_list.append(words[i])
    temp_list.append('\n')

# Write output to file
with open('output.txt', 'w') as f:
      f.writelines(temp_list)
