# -*- coding: utf-8 -*-
"""
Example implementation of EM algorithm for IBM model 0.
"""
from collections import defaultdict # Used to avoid KeyError exceptions.
from decimal import Decimal         # Used for higher arithmetic precision.

import sys
import codecs


def print_phrase_table(phrase_table):
    """
    Helper method printing out the given phrase table.
    """
    print "\nEnglish    Foreign    Probability"
    print "-"*33
    for word_e, translations in phrase_table.items():
        print u"{0:>10}".format(word_e)
        for word_f, prob in translations.items():
            print u"          {0:>10}      {1:0.5f}".format(word_f, prob)
    print "-"*33


def initialise(english_text, foreign_text, phrase_table):
    """
    Initialises freq(word_f|word_e) with uniformly distributed seed value.
    
    Assumes three parameters:
    - `english_text` and `foreign_text` are two parallel sentences;
    - `phrase_table` is a two dimensional dictionary containing scores.
    
    """
    english_text = english_text.strip() # We strip any outer whitespace here.
    foreign_text = foreign_text.strip()

    # The uniform seed value is constant for the given foreign_text;  hence
    # we can pre-compute it here.  Using Decimal allows for higher precision.
    uniform_seed_value = Decimal(1) / Decimal(len(foreign_text.split()))
    
    for word_e in english_text.split():
        for word_f in foreign_text.split():
            # The current word_f might have already been seen, hence we have
            # to conserve any pre-existing value.
            pre_existing = phrase_table[word_e][word_f]
            phrase_table[word_e][word_f] = pre_existing + uniform_seed_value


def normalise(english_sentences, phrase_table):
    """
    Normalises the probabilities for all words in the given English sentences.
    """
    english_words = set()
    for sentence in english_sentences:
        english_text = sentence.strip() # We strip any outer whitespace here.
        for word_e in english_text.split():
            english_words.add(word_e)
    
    for word_e in english_words:
        total = sum(phrase_table[word_e].values()) # Sum up all probabilities.
        
        if total != Decimal(1): # Normalise probabilities if sum != 1.
            for word_f, probability in phrase_table[word_e].items():
                phrase_table[word_e][word_f] = probability / total


def update(english_text, foreign_text, phrase_table, target_table):
    """
    Updates the probabilities and normalises them for foreign words.
    
    Assumes four parameters:
    - `english_text` and `foreign_text` are two parallel sentences;
    - `phrase_table` is a two dimensional dictionary containing scores;
    - `target_table` is a two dimensional dictionary to write results into.
    
    """
    english_text = english_text.strip() # We strip any outer whitespace here.
    foreign_text = foreign_text.strip()
    
    for word_f in foreign_text.split():
        english_words = english_text.split()
        
        # Sum up all probabilities generating the foreign word word_f.
        total = Decimal(sum([phrase_table[word_e][word_f] \
          for word_e in english_words]))
        
        for word_e in english_words:
            probability = phrase_table[word_e][word_f]
            if total != Decimal(1): # Normalise probabilities if sum != 1.
                target_table[word_e][word_f] += probability / total
            else:
                target_table[word_e][word_f] += probability


def run_EM_algorithm(iterations, source_text, target_text):
    """
    Applies the EM algorithm to estimate a word alignment between texts.
    
    Assumes three parameters:
    - `iterations` defines how often the algorithm should be looped;
    - `source_text` and `target_text` are lists containing text.
    
    """
    # Create an empty phrase table.  This is implemented as a two-dimensional
    # dictionary with proper default settings which allow to access any of the
    # cells inside the phrase table without initialisation.
    phrase_table = defaultdict(lambda: defaultdict(int))
    
    counter = 0 # Initially, our iteration counter is set to zero.
    
    parallel_text = zip(source_text, target_text) # Creates a list of tuples.
    
    while counter < iterations: # Loop until finished...
        print '\nRunning iteration {0} of {1}\n'.format(counter+1, iterations)
        
        # Step 1: initialisation or computation of freq(word_f|word_e)
        if counter == 0: # If this is our first loop, we have to initialise...
            for (english_text, foreign_text) in parallel_text:
                initialise(english_text, foreign_text, phrase_table)
            
            print '[initialise]'
            print_phrase_table(phrase_table)
        
        else:
            # The update step needs a target dictionary to write into.
            target_dict = defaultdict(lambda: defaultdict(int))
            for (english_text, french_text) in parallel_text:
                update(english_text, french_text, phrase_table, target_dict)
            
            # Finally, target_dict replaces the original phrase_table.
            phrase_table = target_dict
            
            print '[update]'
            print_phrase_table(phrase_table)
        
        # Step 2: computation of new, normalised probabilities.
        print '[normalise]'
        normalise(source_text, phrase_table)
        print_phrase_table(phrase_table)
        
        # Increase iteration counter.
        counter += 1
    
    print '\nFinished training'


# pylint: disable-msg=E0602
def pretty_print(path):
    """Prints the final alignment model."""
    import os.path
    
    out = codecs.open(path + os.path.sep + 'model.out', 'w', 'utf-8')
    for word_e in sorted(PROB.keys()):
        for word_f in sorted(PROB[word_e].keys()):
            out.write(u'{0}\t{1}\t{2}\n'.format(word_e, word_f, PROB[word_e][word_f]))


if __name__ == '__main__':
    # Check arguments.
    if not len(sys.argv) == 4:
        print "\n\tusage: {0} <src-file> <tgt-file> <steps>\n".format(
          sys.argv[0])
        sys.exit(-1)
    
    # Load parallel texts into lists of Strings.
    _src = codecs.open(sys.argv[1], 'r', 'utf-8').read().lower().split('\n')
    _tgt = codecs.open(sys.argv[2], 'r', 'utf-8').read().lower().split('\n')
    
    # Determine number of iterations.
    _steps = int(sys.argv[3])
    
    # Remove empty lines from the parallel texts.
    _src = [x.strip() for x in _src if x]
    _tgt = [x.strip() for x in _tgt if x]
    
    # Run EM algorithm for _steps iterations, estimating a word alignment.
    run_EM_algorithm(_steps, _src, _tgt)
