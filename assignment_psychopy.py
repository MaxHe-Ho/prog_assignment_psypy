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
    - Computer with a different strategy than 'random choice' --> bias in direction of heads or tails or sticking to/ switching 
      from its or users choice in the previous round. Computer can also be turned into a frustrator.
    - Printout at the end of the program showing how often the subject switched their choice from own & computers choice in previous round.

User experience really important!

Think of the testing function!
"""

import os
import random
from psychopy import data, event, core, visual

# %% Window & Text stimuli

win = visual.Window(color='black')

welcome_text = """Welcome to my experiment. You will play matching pennies against the computer.

Press any key to begin."""

instruction_text = """You are the "even" player, i.e. you win a given round when the amount of heads and tails presented by you 
and the computer together is even. Press 'h' for head and 't' for tails. 

To exit, press q."""

welcome = visual.TextStim (win, text = welcome_text)
instruction = visual.TextStim (win, text = instruction_text)

winner = visual.TextStim (win, text='YOU WIN!', color='green')
loser = visual.TextStim (win, text='YOU LOSE!', color='red')

# %% quit function and quit keys

#quit function which takes two functions as input and returns both, is used below for global event keys
def quit_function(func_1, func_2):
    return func_1 and func_2

#clear global keys to avoid problem when spacebar is used to skip intro text
event.globalKeys.clear()

#Keys to quit the experiment at any time 
#AttributeError because it still runs the loop but win is closed and then asked to flip again towards the end. Nevertehless prefered option over many exit options throughout the program
event.globalKeys.add(key='q', func=quit_function(core.quit, win.close))
event.globalKeys.add(key='escape', func=quit_function(core.quit, win.close))
#idea from https://www.psychopy.org/coder/globalKeys.html

# %%Intro screens

welcome.draw()
win.flip()

event.waitKeys()

instruction.draw()
win.flip()

event.waitKeys()

# %% necessary & self-explanatory variables

wins = 0
losses = 0
rounds = 1
choice_change_subject = 0
choice_change_computer = 0

# %% bias variables

#change value of the bias variable to determine the bias of the computer i.e. the degree to which its decision will diverge from a 50/50 chance for heads and tails 
#the value determines the degree of all the (possible) biases below (if they are activated)
#choose a bias between -0.5 and +0.5! 
bias = 0.4

##As an adaptation of this program to make it psychologically more interesting and turn it into a test somewhat like the Wisconsin Card Sorting Test, the user could be asked to find out the bias of the computer which is changed at times
#change one of the following biases to True if you want that bias to be implemented
#to make the program flexible, the biases can be freely combined amongst each other except for the frustrator, 
#which cannot be combined with another bias. Though of course the effects of some biases cancel each other out

#To bias the computer towards choosing heads more often, set the "bias_heads"-variable to True (and perhaps adjust the bias above)
bias_heads = False
#To bias the computer towards choosing tails more often, set the "bias_tails"-variable to True (and perhaps adjust the bias above)
bias_tails = False

#To bias the computer towards sticking to its own previous choice more often, set the "bias_stick_to_prev_com_choice"-variable to True (and perhaps adjust the bias above)
bias_stick_to_prev_com_choice = False
#To bias the computer towards switching from its own previous choice more often, set the "bias_switch_from_prev_com_choice"-variable to True (and perhaps adjust the bias above)
bias_switch_from_prev_com_choice = False

#To bias the computer towards sticking to the users previous choice more often, set the "bias_stick_to_prev_user_choice"-variable to True (and perhaps adjust the bias above)
bias_stick_to_prev_user_choice = False
#To bias the computer towards switching from the users previous choice more often, set the "bias_switch_from_prev_com_choice"-variable to True (and perhaps adjust the bias above)
bias_switch_from_prev_user_choice = False

#In case you want to be evil and turn the computer into a frustrator, i.e. a device that always chooses the opposite of the user and thus 
#guarantees that the user looses, set the "frustrator"-variable to True. 
##As an adaptation of the program, one might collect data (as the amount of attempts and reaction times) from user reacting to frustrator in order to get e.g. some proxy of frustration tolerance or trust in the experimenter
frustrator = False

# %% bias functions, start of loop and cut_off variable

#function to give error message for bad values of the bias and except for that only returns the bias
def bias_function (bias):
    if bias < -0.5:
        win.close()
        raise ValueError ("""You chose a value for bias that is smaller than -0.5. As the cut-off 
                         value is equal to 0.5, which is used to compute probabilities, adding a 
                         value smaller than -0.5 makes the probability negative. Probabilites however 
                         are always >= 0 (at least on standard interpretations of probabilities).
                         Try a value that is between -0.5 and 0.5 instead!""")
    if bias > 0.5:
        win.close()
        raise ValueError ("""You chose a value for bias that is bigger than 0.5. As the cut-off 
                         value is equal to 0.5, which is used to compute probabilities, adding a 
                         value bigger than 0.5 makes the probability <1. Probabilites however 
                         are always <= 1 (at least on standard interpretations of probabilities).
                         Try a value that is between -0.5 and 0.5 instead!""")
    return bias

#function for allowed combinations of biases
def allowed_bias_combis (bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator):
    if frustrator == True:
        if bias_heads or bias_tails or bias_stick_to_prev_com_choice or bias_switch_from_prev_com_choice or bias_stick_to_prev_user_choice or bias_switch_from_prev_user_choice == True:
            #win.close()
            raise ValueError("Frustrator is not compatible with other biases as it would simply cover all other possible effects")
    return bias_heads and bias_tails and bias_stick_to_prev_com_choice and bias_switch_from_prev_com_choice and bias_stick_to_prev_user_choice and bias_switch_from_prev_user_choice and frustrator

allowed_bias_combis (bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator)

#function to bias the computer towards sticking to its previous choice
def stick_to_prev_com_choice_function (choice_computer, cut_off, bias):
    if choice_computer == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off

#function to bias the computer towards switching from its previous choice
def switch_from_prev_com_choice_function (choice_computer, cut_off, bias):
    if choice_computer == 'h':
        cut_off = round (cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off

#function to bias the computer towards sticking to the user's previous choice
def bias_stick_to_prev_user_choice_function (choice_subject, cut_off, bias):
    if choice_subject == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off

#function to bias the computer towards switching from the user's previous choice
def bias_switch_from_prev_user_choice_function (choice_subject, cut_off, bias):
    if choice_subject == 'h':
        cut_off = round (cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off

#function to bias the computer towards heads
def bias_heads_function (cut_off, bias):
    cut_off = cut_off + bias_function(bias)
    return cut_off

#function to bias the computer towards tails
def bias_tails_function (cut_off, bias):
    cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off

#function to turn the computer into a frustrator
def frustrator_function (choice_subject, choice_computer):
    if choice_subject == 'h':
        choice_computer = 't'
    else: choice_computer = 'h'
    return choice_computer
    
while True:
    
    #The cut-off variable is (nearly) equal to the probability of the computer choosing heads.
    #the variable is placed within the loop to avoid biases from the previous rounds to influence the next decisions by the computer
    cut_off = 0.5
    
# %% choice user & two biases of the computer
    
    #wait for & restrict keys
    keys = event.waitKeys(keyList=(['h', 't', 'q', 'escape']))

    #count the amount of changes the subject makes in their decisions relative to their previous choice
    if rounds > 1:
        if choice_subject != keys[0]: #the variable choice_subject is undefined at this point but only gets used after it is defined, i.e. in the next round of the loop. As the same warning simply reoccurs in the following, I didn't comment it again.
            choice_change_subject += 1
            
        #biases the computer towards sticking to the user's previous choice
        if bias_stick_to_prev_user_choice == True:
            cut_off = bias_stick_to_prev_user_choice_function (choice_subject, cut_off, bias)
        
        #biases the computer towards switching from the user's previous choice
        if bias_switch_from_prev_user_choice == True:
            cut_off = bias_switch_from_prev_user_choice_function (choice_subject, cut_off, bias)
        
    #choice_subject
    choice_subject = keys[0]
    
# %% choice computer
    
    #count the amount of changes the subject makes in their decisions relative to their previous choice
    if rounds > 1:
        if choice_computer != choice_subject:
            choice_change_computer += 1   
            
        #biases the computer towards sticking to its previous choice
        if bias_stick_to_prev_com_choice == True:
            cut_off = stick_to_prev_com_choice_function (choice_computer, cut_off, bias)
        
        #biases the computer towards switching from its previous choice
        if bias_switch_from_prev_com_choice == True:
            cut_off = switch_from_prev_com_choice_function (choice_computer, cut_off, bias)
    
    #biases the computer towards heads
    if bias_heads == True:
        cut_off = bias_heads_function (cut_off, bias)
    
    #biases the computer towards tails
    if bias_tails == True:
        cut_off = bias_tails_function (cut_off, bias)
    
    #creates a random float
    ran_float = random.random()
    
    #use random float to determine the computer's choice
    if ran_float < cut_off:
        choice_computer = 'h'
    elif ran_float > cut_off:
        choice_computer = 't'
    #just to be super fair and not give either 'h' or 't' a slight (negligible) advantage, in case ran_float == cut_off, there is a new random choice
    else:
        choice_computer = random.choice(['h', 't'])
    
    #turns the computer into a frustrator
    #aware of the fact that this simply overwrites the previous value of choice_computer
    if frustrator == True:
        choice_computer = frustrator_function (choice_subject, choice_computer)
    
# %% Display choice of user & computer with images
    
    #save path of images
    f_heads = os.path.join("data", "penny_heads.png")
    f_tails = os.path.join("data", "penny_tails.png")
    
    #Create the texts "Your choice:", "Computer's choice:" and "to continue, press any key" 
    txt_user = visual.TextStim (win, pos = (-0.5,0.6), text='Your choice:')
    txt_com = visual.TextStim (win, pos = (0.5,0.6), text="Computer's choice:")
    txt_continue = visual.TextStim (win, pos = (0,-0.85), text="to continue, press any key", height = 0.08)
    
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
        txt_continue.draw()
        #prints everything on the screen and waits for key to be pressed
        win.flip()
        event.waitKeys() 
        
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
        txt_continue.draw()
        #prints everything on the screen and waits key to be pressed
        win.flip()
        event.waitKeys() 

# %% results round & game
    
    if choice_subject == choice_computer:
        #display result of round to user
        winner.draw()
        win.flip()
        #raise wins by 1  and wait shortly
        wins += 1
        core.wait(1.5) #wait a longer amount of time than for loss for well-being of user

    else:
        #display result of round to user
        loser.draw()
        win.flip()
        #raise losses by 1 and wait shortly
        losses += 1
        core.wait(1) #wait a shorter amount of time than for a win for well-being of user
    
    ##As an adaptation of the program, one might abstain from displaying the round info and instead ask the user for her estimate on the amounts of wins & losses conditional on different waiting times for wins & losses
    
    #infos for user at the end of each round. Contains the number of rounds, wins, losses, changes from user's previous choice and changes from computer's previous choice
    game_info = "This is round {}. You won {} times. You lost {} times. You changed your own choice {} times. You changed {} times from the computer's choice in the previous round."
    game_info = game_info.format(rounds, wins, losses, choice_change_subject, choice_change_computer)     
    
    #display result of the game so far to user
    _game_info = visual.TextStim(win, text= game_info)
    _game_info.draw()
    win.flip()

    #raise rounds by 1
    rounds += 1

# %% super useful close statement that cannot be reached but feels like it has to be part of an experiment in psychopy

win.close()
