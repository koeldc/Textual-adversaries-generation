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
    text_info = nlp(text)
    words = [x.text for x in text_info]
    replace_tags = [False] * len(words)
    for chunk in text_info.noun_chunks:
        if chunk.text.isalpha() and chunk.text.islower():
            replace_tags[chunk.end - 1] = True
    return words, replace_tags

def extract_frequent_nouns(captions):
    frequent_nouns = {}
    for caption in captions:
        caption = nlp(caption.lower())
        for word in caption:
            if word.pos_ == 'NOUN' and word.lemma_ != '--PRON--':
                word = word.text
                if word in frequent_nouns:
                    frequent_nouns[word] += 1
                else:
                    frequent_nouns[word] = 1
    return frequent_nouns

def extract_concrete_nouns(frequent_nouns, concreteness_file):
    concreteness = [line.split() for line in codecs.open(concreteness_file).readlines()]
    concrete_nouns = set([item[0] for item in concreteness if float(item[1]) > 0.1])
    return {w: frequent_nouns[w] for w in frequent_nouns if w in concrete_nouns}

def get_candidate_substitutes(concrete_nouns):
    frequent_nouns_set = set(concrete_nouns)
    return {w: [x for x in frequent_nouns_set if match(w, x)] for w in concrete_nouns}

def replace_nouns(captions, concrete_nouns, candidate_substitutes):
    temp_list = []
    invalid_words = set()
    for caption in captions:
        words, replace_tags = get_noun_chunks(caption)
        for i in range(len(words)):
            if not replace_tags[i] or words[i] in invalid_words:
                temp_list.append(words[i])
                continue
            substitute_selected = False
            for w in candidate_substitutes[words[i]]:
                if w not in invalid_words:
                    temp_list.append(w)
                    substitute_selected = True
                    break
            if not substitute_selected:
                temp_list.append(words[i])
        temp_list.append('\n')
    return temp_list

def write_output_file(output_file, modified_captions):
    with open(output_file, 'w') as f:
        f.writelines(modified_captions)

def main():
    with open('input.txt', 'r') as f:
        captions = f.readlines()

    frequent_nouns = extract_frequent_nouns(captions)
    concrete_nouns = extract_concrete_nouns(frequent_nouns, 'concreteness.txt')
    candidate_substitutes = get_candidate_substitutes(concrete_nouns)
    modified_captions = replace_nouns(captions, concrete_nouns, candidate_substitutes)
    write_output_file('output.txt', modified_captions)

if __name__ == '__main__':
    main()

