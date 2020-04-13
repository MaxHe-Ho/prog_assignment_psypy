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

winner = visual.TextStim (win, text='YOU WIN!', pos = (0, 0.6), color='green')
loser = visual.TextStim (win, text='YOU LOSE!', pos = (0, 0.6), color='red')

txt_user = visual.TextStim (win, pos = (-0.5,0.42), text='Your choice:')
txt_com = visual.TextStim (win, pos = (0.5,0.42), text="Computer's choice:")
txt_continue = visual.TextStim (win, pos = (0,-0.85), text="Press any key to continue", height = 0.08)


def score_function (wins, losses):
    """
    Generates visual.text.TextStim with score of the current round and specifies its location on the screen

    Parameters
    ----------
    wins : int
        stores the amount of wins of the subject
    losses : int
        stores the amount of losses of the subject

    Returns
    -------
    score: visual.text.TextStim
            Visual stimulus of the current score ready to be displayed
    """
    txt_score = """Score:
{} - {}"""
    txt_score = txt_score.format(wins, losses)
    score = visual.TextStim (win, pos=(0, 0.86), text=txt_score)
    return score

# %% quit function and global quit key 'escape'

#No Docstring for the quit function because it's exremely short & obvious. 
#It simply takes two functions as input and returns both. It is used below for global event keys
def quit_function(func_1, func_2):
    return func_1 and func_2

#clears global keys 
event.globalKeys.clear()
#escape key can be used quit the experiment at any time also skipping the end screen, probably most useful for experimenter
#despite reoccuring AttributeError used as a faster exit option throughout the whole program
event.globalKeys.add(key='escape', func=quit_function(core.quit, win.close))
#Source for global event keys: https://www.psychopy.org/coder/globalKeys.html

# %%Intro screens

welcome.draw()
win.flip()
event.waitKeys()

instruction.draw()
txt_continue.draw()
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
frustrator = False
##As an adaptation of the program, one might collect data (as the amount of attempts and reaction times) from user reacting to frustrator in order to get e.g. some proxy of frustration tolerance or trust in the experimenter

# %% bias functions, start of loop and cut_off variable

#function to give error message for bad values of the bias and except for that only returns the bias
def bias_function (bias):
    """
    Simply returns the bias. Closes win before raising the error to prevent win from getting stuck.
    
    Parameters
    ----------
    bias : float
        the bias of the computer chosen by the experimenter.

    Raises
    ------
    ValueError
        raises an exception if the bias is smaller than -0.5 or bigger than 0.5
        as this would in the end mean that the program had to calculate probabilities
        smaller than 0 or bigger than 1.

    Returns
    -------
    bias : float
        the bias of the computer chosen by the experimenter.
    """
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


def allowed_bias_combis (bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator):
    """
    Simply returns all the bias functions. Closes win before raising the error to prevent win from getting stuck.

    Parameters
    ----------
    bias_heads : function
        a function that biases the computer towards choosing heads.
    bias_tails : function
        a function that biases the computer towards choosing tails.
    bias_stick_to_prev_com_choice : function
        a function that biases the computer towards sticking to its previous choice.
    bias_switch_from_prev_com_choice : function
        a function that biases the computer towards switching from its previous choice.
    bias_stick_to_prev_user_choice : function
        a function that biases the computer towards sticking to the user's previous choice.
    bias_switch_from_prev_user_choice : function
        a function that biases the computer towards sticking to the user's previous choice.
    frustrator : function
        a function that always chooses the opposite of the user.

    Raises
    ------
    ValueError
        raises an exception if the bias function frustrator is combined with other functions.
        This is because the frustrator doesn't work with probabilites and necessarily simply
        overwrites all other biases. 

    Returns
    -------
    all the parameters listed above with identical properties.
    """
    if frustrator == True:
        if bias_heads or bias_tails or bias_stick_to_prev_com_choice or bias_switch_from_prev_com_choice or bias_stick_to_prev_user_choice or bias_switch_from_prev_user_choice == True:
            win.close()
            raise ValueError("Frustrator is not compatible with other biases as it would simply cover all other possible effects")
    return bias_heads and bias_tails and bias_stick_to_prev_com_choice and bias_switch_from_prev_com_choice and bias_stick_to_prev_user_choice and bias_switch_from_prev_user_choice and frustrator

allowed_bias_combis (bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator)


def stick_to_prev_com_choice_function (choice_computer, cut_off, bias):
    """
    Biases the computer towards sticking to its previous choice

    Parameters
    ----------
    choice_computer : str
        stores the decision of the computer between heads and tails of the current round.
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        sticking to its previous choice.
    """
    if choice_computer == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off


def switch_from_prev_com_choice_function (choice_computer, cut_off, bias):
    """
    Biases the computer towards switching from its previous choice

    Parameters
    ----------
    choice_computer : str
        stores the decision of the computer between heads and tails of the current round.
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        switching from its previous choice.
    """
    if choice_computer == 'h':
        cut_off = round (cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_stick_to_prev_user_choice_function (choice_subject, cut_off, bias):
    """
    Biases the computer towards sticking to the user's previous choice

    Parameters
    ----------
    choice_subject : str
        stores the decision of the subject between heads and tails of the current round.
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        sticking to the user's previous choice.
    """
    if choice_subject == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off


def bias_switch_from_prev_user_choice_function (choice_subject, cut_off, bias):
    """
   Biases the computer towards switching from the user's previous choice

    Parameters
    ----------
    choice_subject : str
        stores the decision of the subject between heads and tails of the current round.
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        switching from the user's previous choice.
    """
    if choice_subject == 'h':
        cut_off = round (cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_heads_function (cut_off, bias):
    """
    Biases the computer towards choosing heads

    Parameters
    ----------
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        choosing heads.
    """
    cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_tails_function (cut_off, bias):
    """
    Biases the computer towards choosing tails

    Parameters
    ----------
    cut_off : float
        stores a value which is used to compute the choice of the computer. 
        If a random generated float is smaller than the cut_off, the computer's decision is
        heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the computer towards
        choosing tails.
    """
    cut_off = round (cut_off - bias_function(bias), 2)
    return cut_off


def frustrator_function (choice_subject, choice_computer):
    """
    Lets the computer always choose the opposite of the user

    Parameters
    ----------
    choice_subject : str
        stores the decision of the subject between heads and tails of the current round.
    choice_computer : str
        stores the decision of the computer between heads and tails of the current round.

    Returns
    -------
    choice_computer : str
        updated version of the choice_computer variable described above. Now always the opposite
        of choice_subject.
    """
    if choice_subject == 'h':
        choice_computer = 't'
    else: choice_computer = 'h'
    return choice_computer
    
while True:
    
    #The cut-off variable is (nearly) equal to the probability of the computer choosing heads.
    #the variable is placed within the loop to avoid biases from the previous rounds to influence the next decisions by the computer
    cut_off = 0.5
    
# %%
    round_txt = """This is round {}


To choose heads, press 'h'.
To choose tails, press 't'."""
    round_txt = round_txt.format(rounds)
    stim_round = visual.TextStim (win, text = round_txt)
    stim_round.draw()
    win.flip()
    
# %% choice user & two biases of the computer
    
    #wait for & restrict keys
    keys = event.waitKeys(keyList=(['h', 't', 'q', 'escape']))
    
    #quit option
    if keys[0] == 'q':
        break
    
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
    
    
# %% Displays choice of the user and computer with images as well as results with text
    
    #save path of images
    f_heads = os.path.join("data", "penny_heads.png")
    f_tails = os.path.join("data", "penny_tails.png")
    
    #get texts ready to be displayed
    txt_user.draw()
    txt_com.draw()
    txt_continue.draw()
    
    #gets image of head of penny ready to be displayed if user chooses head
    if choice_subject == 'h':
        heads = visual.ImageStim(win,size = (0.68,0.92), pos = (-0.5,-0.2), image=f_heads)
        heads.draw()
        #gets image of head of penny ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win,size = (0.68,0.92), pos = (0.5,-0.2), image=f_heads)
            heads.draw()
            # raise wins by 1 and get info that the user won ready to be displayed
            wins += 1
            winner.draw()
        #gets image of tail of penny ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win,size = (0.68,0.92), pos = (0.5,-0.2), image=f_tails)
            tails.draw()
            # raise losses by 1 and get info that the user lost ready to be displayed
            losses += 1
            loser.draw()
        #update the current score and get it ready to be displayed
        score = score_function(wins, losses)
        score.draw()
        #prints everything on the screen and waits for key to be pressed
        win.flip()
        
    #gets image of tail of penny ready to be displayed if user chooses tail    
    else:
        tails = visual.ImageStim(win,size = (0.68,0.92), pos = (-0.5,-0.2), image=f_tails)
        tails.draw()
        #gets image of head of penny ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win,size = (0.68,0.92), pos = (0.5,-0.2), image=f_heads)
            heads.draw()
            # raise losses by 1 and get info that the user lost ready to be displayed
            losses += 1
            loser.draw()
        #gets image of tail of penny ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win,size = (0.68,0.92), pos = (0.5,-0.2), image=f_tails)
            tails.draw()
            # raise wins by 1 and get info that the user won ready to be displayed
            wins += 1
            winner.draw()
        #update the current score and get it ready to be displayed
        score = score_function(wins, losses)
        score.draw()
        #prints everything on the screen and waits key to be pressed
        win.flip()

    #wait a longer amount of time for a win than for a loss for well-being of user
    if choice_subject == choice_computer:
        core.wait(1.5)
    else:
        core.wait(1)
    response_key = event.waitKeys() 

    #quit option
    if response_key[0] == 'q':
        break

# %% displays the infos of the game so far at the end of the round
    
    #infos for user at the end of each round. Contains the number of rounds, wins, losses, changes from user's previous choice and changes from computer's previous choice
    txt_game_info = "Up until round {}. You won {} times. You lost {} times. You changed your own choice {} times. You changed {} times from the computer's choice in the previous round."
    txt_game_info = txt_game_info.format(rounds, wins, losses, choice_change_subject, choice_change_computer)     
    
    #display result of the game so far to user
    game_info = visual.TextStim(win, text= txt_game_info)
    game_info.draw()
    score.draw()
    txt_continue.draw()
    win.flip()
    response_key = event.waitKeys()

    ##As an adaptation of the program, one might abstain from displaying the score and game_info and instead ask the user for her estimate on the amounts of wins & losses conditional on different waiting times for wins & losses (as determined above)

    #raise rounds by 1
    rounds += 1
    
# %% displays the final score & some other information, finally closes the window
    
    #quit option
    if response_key[0] == 'q':
        break

amount_rounds = wins + losses

txt_end = """

You played {} rounds.

The final score is:

   You: {}
        
   Computer: {}
        

Thanks a lot for your participation!""".format(amount_rounds, wins, losses)

stim_end = visual.TextStim(win, text= txt_end)
stim_end.draw()
win.flip()
core.wait(6)

win.close()