# -*- coding: utf-8 -*-
"""
Subject plays a matching pennies game: 
    One player = 'even', other player = 'odd', each has a penny.
    Player and computer present their penny heads-up or tails-up. If the two pennies match, the 'even' player wins a point and if they don't, the 'odd' player wins.
    
By pressing 'h', the subject chooses heads and by pressing 't', the subject chooses tails. The computer chooses randomly. After the subject has made their choice, both pennies
are shown on the screen and subject gets the information whether they won and what the current scores are. The subject can quit at any point by pressing a quit key.
Additional features: 
    - Computer with a different strategy than 'random choice' --> bias in direction of heads or tails or switching from previous round (or different response
      than player beforehands, frustrator). 
    - printout at the end of the program showing how often the subject switched their choice from own & computers choice in previous round.
    
User experience really important!
"""

import os
import statistics

from psychopy import data, event, core, visual

# %% Window & Text stimuli

win = visual.Window()

welcome_text = """Welcome to my experiment.
You will play matching pennies against the computer.
Press any key to begin.
"""

instruction_text = """You are the "even" player, i.e. you win a given round when the amount of heads (and tails) 
is even.
Press 'h' for head and 't' for tails.
To exit, press q.

...
"""

welcome = visual.TextStim (win, text = welcome_text)
instruction = visual.TextStim (win, text = instruction_text)

#winner = visual.TextStim (win, text='YOU WIN!', color='green')
#looser = visual.TextStim (win, text='YOU LOOSE!', color='red')


# %% Keyboard

# We can use a dictionary to map key names to their meanings.
key_meanings = {'h': 'head', 't': 'tails', 'q': core.quit}

# The keys of the dictionary give the list of allowable keys.
allowed_keys = key_meanings.keys()


# %%Intro screens

welcome.draw()
win.flip()

# Then wait for a key press.
event.waitKeys()

instruction.draw()
win.flip()

core.wait(4)


# %% actual program

# randomize choice of robot

#choice_subject
# if choice_subject == choice of robot: 
    # Visual.TextStim (win, text = "you win")

# %% 


"""
#input_in_round = input("Next round. Press 'q' to quit, press any other key to continue")

#while input_in_round !== "q":


event.globalKeys.add(key='q', func=core.quit)

while True:
    instruction.draw()
    win.flip()


"""
win.close() 


