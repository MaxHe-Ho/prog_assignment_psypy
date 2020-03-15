# -*- coding: utf-8 -*-
"""
Subject plays a matching pennies game:
    One player = 'even', other player = 'odd', each has a penny.
    Player and computer present their penny heads-up or tails-up. If the two pennies match, the 'even' player wins 
    a point and if they don't, the 'odd' player wins.

By pressing 'h', the subject chooses heads and by pressing 't', the subject chooses tails. The computer chooses 
randomly. After the subject has made their choice, both pennies are shown on the screen and subject gets the 
information whether they won and what the current scores are. The subject can quit at any point by pressing 'q'.
Additional features:
    - Computer with a different strategy than 'random choice' --> bias in direction of heads or tails or sticking to/ switching from previous round (or different response
      than player beforehands, frustrator).
    - printout at the end of the program showing how often the subject switched their choice from own & computers choice in previous round.

User experience really important!

Think of some errors/ exceptions & useful messages for that
Think of the testing function!
"""

import os
import random
from psychopy import data, event, core, visual

# %% Window & Text stimuli

win = visual.Window()#size=[1024,768]

welcome_text = """Welcome to my experiment.
You will play matching pennies against the computer.
Press any key to begin.
"""

instruction_text = """You are the "even" player, i.e. you win a given round when the amount of heads and tails by you and the computer is even.
Press 'h' for head and 't' for tails.
To exit, press q.
"""

welcome = visual.TextStim (win, text = welcome_text)
instruction = visual.TextStim (win, text = instruction_text)

winner = visual.TextStim (win, text='YOU WIN!', color='green')
loser = visual.TextStim (win, text='YOU LOSE!', color='red')

# %% quit function and quit keys

#define quit function
def quit_function(func_1, func_2):
    return func_1 and func_2

#clear global keys to avoid problem when spacebar is used to skip intro text
event.globalKeys.clear()

#Keys to quit the experiment at any time ##what's the error sign? Why does it show the attribute error but work fine?
event.globalKeys.add(key='q', func=win.close)
event.globalKeys.add(key='escape', func=quit_function(core.quit, win.close))

# %%Intro screens

welcome.draw()
win.flip()

event.waitKeys()

instruction.draw()
win.flip()

core.wait(2)

# %% necessary & self-explanatory variables, start of loop

wins = 0
losses = 0
rounds = 1
choice_change_subject = 0
choice_change_computer = 0

#The cut-off variable is (nearly) equal to the probability of the computer choosing heads.
#So to bias the computer towards choosing heads more often, increase it. 
# And to bias it towards choosing tails, decrease it.
cut_off = 0.5

while True:
    
# %% choice user
    
    #wait for & restrict keys
    keys = event.waitKeys(keyList=(['h', 't']))

    #count the amount of changes the subject makes in their decisions relative to their previous choice
    if rounds > 1:
        if choice_subject != keys[0]: #the variable choice_subject is undefined at this point but only gets used after it is defined, i.e. in the next round of the loop
            choice_change_subject += 1
        
    #choice_subject
    choice_subject = keys[0]
    print("Your choice: ", choice_subject)
    
# %% choice computer
    
    #count the amount of changes the subject makes in their decisions relative to their previous choice
    if rounds > 1:
        if choice_computer != choice_subject  : #the variable choice_computer is undefined at this point but only gets used after it is defined, i.e. in the next round of the loop
            choice_change_computer += 1   
 
    ran_float = random.random()
    print(ran_float)
    #use random float for choice of computer
    if ran_float < cut_off:
        choice_computer = 'h'
    elif ran_float > cut_off:
        choice_computer = 't'

        #just to be super fair and not give either 'h' or 't' a slight advantage, in case ran_float == 0.5, there is a new random choice
    else:
        choice_computer = random.choice(['h', 't'])

    #Just in case you want to be evil: To turn the computer to a frustrator, i.e. a device that always chooses the opposite of the user & thus 
    #guarantees that the user looses, delete the '#' in lines 120-122 and put a '#' in front of the other lines in the "choice computer" section
#    if choice_subject == 'h':
#        choice_computer = 't'
#    else: choice_computer = 'h'
            
    print("Computer's choice: ", choice_computer)

# %% Display choice of user & computer with images
    
    #save path of images
    f_heads = os.path.join("data", "penny_heads.png")
    f_tails = os.path.join("data", "penny_tails.png")
    
    #Create the texts "Your choice:" and "Computer's choice" 
    txt_user = visual.TextStim (win, pos = (-0.5,0.6), text='Your choice:')
    txt_com = visual.TextStim (win, pos = (0.5,0.6), text="Computer's choice")
    
    #gets image of head of penny ready to be displayed if user chooses head
    if choice_subject == 'h':
        heads = visual.ImageStim(win,size = (0.7,0.94), pos = (-0.5,-0.2), image=f_heads)
        heads.draw()
        #gets image of head of penny ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win,size = (0.7,0.94), pos = (0.5,-0.2), image=f_heads)
            heads.draw()
        #gets image of tail of penny ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win,size = (0.7,0.94), pos = (0.5,-0.2), image=f_tails)
            tails.draw()
        #get text for user and computer ready to be displayed
        txt_user.draw()
        txt_com.draw()
        #prints everything on the screen and waits 2 seconds
        win.flip()
        core.wait(2) 
        
    #gets image of tail of penny ready to be displayed if user chooses tail    
    else:
        tails = visual.ImageStim(win,size = (0.7,0.94), pos = (-0.5,-0.2), image=f_tails)
        tails.draw()
        #gets image of head of penny ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win,size = (0.7,0.94), pos = (0.5,-0.2), image=f_heads)
            heads.draw()
        #gets image of tail of penny ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win,size = (0.7,0.94), pos = (0.5,-0.2), image=f_tails)
            tails.draw()
        #get text for user and computer ready to be displayed
        txt_user.draw()
        txt_com.draw()
        #prints everything on the screen and waits 2 seconds
        win.flip()
        core.wait(2)


# %% results round & game
    
    #info for user
    game_info = "This is round ", rounds, ". You won ", wins, "times. You lost", losses, " times.", " You changed your own choice ", choice_change_subject, " times. You changed ", choice_change_computer, " times from the computers choice in the previous round."
    #game_info = "This is round {}. You won {} times. You lost {} times." ## --> unfortunately does not work, why?
    #game_info.format("rounds", "wins", "losses")
    
    if choice_subject == choice_computer:
        
        #display result of round to user
        winner.draw()
        win.flip()
        
        #raise wins by 1
        wins += 1

        core.wait(1.5) #wait a longer amount of time for well-being of user

    else:
        #display result of round to user
        loser.draw()
        win.flip()
        
        #raise losses by 1
        losses += 1

        core.wait(1) #wait a shorter amount of time for well-being of user
               
    #display result of the game so far to user
    _game_info = visual.TextStim(win, text= game_info)
    _game_info.draw()
    win.flip()

    #raise rounds by 1
    rounds += 1

# %% super useful close statement that cannot be reached but feels like it has to be part of an experiment in psychopy

win.close()
