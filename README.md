TinyMT
======

Sample code showing how SMT systems function...

0. Checking out the repository

You can clone this GitHub repository using the following command:

    $ git clone git@github.com:cfedermann/TinyMT.git TinyMT

This creates a local folder named `TinyMT` and adds all repository contents.


1. Exercise: Word Alignment
---------------------------

Implement IBM Model 0.  For starters, try to get your code running with our toy example discussed in class on June 18, 2013.

The following output shows what your code should generate for two iterations of the algorithm...

    cfedermann$ python estimate_word_alignment.py ./toy-story.en toy-story.fr 2
    
    Running iteration 1 or 2
    
    [initialise]
    
    English    Foreign    Probability
    ---------------------------------
         small
                   petit      0.50000
                   chien      0.50000
     dangerous
                 méchant      0.50000
                   chien      0.50000
           dog
                 méchant      0.50000
                   chien      1.00000
                   petit      0.50000
    ---------------------------------
    [normalise]
    
    English    Foreign    Probability
    ---------------------------------
         small
                   petit      0.50000
                   chien      0.50000
     dangerous
                 méchant      0.50000
                   chien      0.50000
           dog
                 méchant      0.25000
                   chien      0.50000
                   petit      0.25000
    ---------------------------------
    
    Running iteration 2 or 2
    
    [update]
    
    English    Foreign    Probability
    ---------------------------------
         small
                   petit      0.66667
                   chien      0.50000
     dangerous
                 méchant      0.66667
                   chien      0.50000
           dog
                 méchant      0.33333
                   chien      1.00000
                   petit      0.33333
    ---------------------------------
    [normalise]
    
    English    Foreign    Probability
    ---------------------------------
         small
                   petit      0.57143
                   chien      0.42857
     dangerous
                 méchant      0.57143
                   chien      0.42857
           dog
                 méchant      0.20000
                   chien      0.60000
                   petit      0.20000
    ---------------------------------
    
    Finished training

