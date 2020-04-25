# -*- coding: utf-8 -*-
"""
Subject plays a matching pennies game:

One player = 'even', other player = 'odd', each has a penny.
Player and computer present their penny heads-up or tails-up. If the two
pennies match, the 'even' player wins a point and if they don't, the 'odd'
player wins.

By pressing 'h', the subject chooses heads and by pressing 't', the subject
chooses tails. The computer chooses randomly. After the subject has made their
choice, both pennies are shown on the screen and subject gets the information
whether they won and what the current scores are. The subject can quit at any
point by pressing 'q'.

Additional features:
- Computer with a different strategy than 'random choice' --> bias in direction
    of heads or tails or sticking to/ switching from its or users choice in the
    previous round. Computer can also be turned into a frustrator.
- Printout at the end of the program showing how often the subject switched
    their choice from own & computers choice in previous round.

The code has been checked to stick to the PEP 8 conventions using pycodestyle.
"""
# %% imports

import os
import random
from psychopy import event, core, visual

# %% Window, text stimuli, paths to images and score_function

win = visual.Window(color='black')

welcome_text = """
Welcome to my experiment. You will play matching pennies against the computer.

Press any key to begin."""

instruction_text = """You are the "even" player, i.e. you win a given round
when the amount of heads and tails presented by you and the computer together
is even. Press 'h' for head and 't' for tails.

To exit, press q."""

welcome = visual.TextStim(win, text=welcome_text)
instruction = visual.TextStim(win, text=instruction_text)

winner = visual.TextStim(win, text='YOU WIN!', pos=(0, 0.6), color='green')
loser = visual.TextStim(win, text='YOU LOSE!', pos=(0, 0.6), color='red')

txt_user = visual.TextStim(win, pos=(-0.5, 0.42), text='Your choice:')
txt_com = visual.TextStim(win, pos=(0.5, 0.42), text="Computer's choice:")
txt_continue = visual.TextStim(win, pos=(0, -0.85),
                               text="Press any key to continue", height=0.08)

# save path of images used later on
f_heads = os.path.join("data", "penny_heads.png")
f_tails = os.path.join("data", "penny_tails.png")


def score_function(wins, losses):
    """
    Generates visual.text.TextStim with score of the current round and
    specifies its location on the screen

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
    score = visual.TextStim(win, pos=(0, 0.86), text=txt_score)
    return score

# %% quit function and global quit key 'escape'


# No Docstring for the quit function because it's exremely short & obvious.
# It simply takes two functions as input and returns both. It is used below for
# global event keys
def quit_function(func_1, func_2):
    return func_1 and func_2


# clears global keys
event.globalKeys.clear()
# escape key can be used quit the experiment at any time also skipping the end
# screen, probably most useful for experimenter despite reoccuring
# AttributeError used as a faster exit option throughout the whole program
event.globalKeys.add(key='escape', func=quit_function(core.quit, win.close))
# Source for global event keys: https://www.psychopy.org/coder/globalKeys.html

# %%Intro screens

welcome.draw()
win.flip()
event.waitKeys()

instruction.draw()
txt_continue.draw()
win.flip()
event.waitKeys()

# %% some self-explanatory variables

wins = 0
losses = 0
rounds = 1
choice_change_subject = 0
choice_change_computer = 0
prev_com_choice = 0
prev_subj_choice = 0

# %% bias variables

# change value of the bias variable to determine the bias of the computer i.e.
# the degree to which its decision will diverge from a 50/50 chance for heads
# and tails. E.g. if you set the bias at 0.4, it will add 0.4 to the default
# value 0.5 (i.e. the cut-off defined below) yielding a 90% probability for the
# outcome specified in the biases below, say a 90% probability for heads. This
# shows that the bias determines the degree of all the (possible) biases below
# (if they are activated).
# Choose a bias between -0.5 and 0.5. Because the bias is added to the default
# value of 0.5, values bigger than 0.5 or smaller than -0.5 won't make sense.
bias = 0.4

## As an adaptation of this program to make it psychologically more interesting
# and turn it into a test somewhat like the Wisconsin Card Sorting Test, the
# user could be asked to find out the bias of the computer which is changed at
# times

# change one of the following biases to True if you want that bias to be
# implemented. To make the program flexible, the biases can be freely combined
# amongst each other except for the frustrator, which cannot be combined with
# another bias. Note that the effects of some biases cancel each other out or
# might cause the computer to stick to heads or tails indefinetely (depending
# also on the value of bias). So choose wisely!

# To bias the computer towards choosing heads more often, set the
# "bias_heads"-variable to True (and perhaps adjust the bias above)
bias_heads = False
# To bias the computer towards choosing tails more often, set the
# "bias_tails"-variable to True (and perhaps adjust the bias above)
bias_tails = False

# To bias the computer towards sticking to its own previous choice more often,
# set the "bias_stick_to_prev_com_choice"-variable to True (and perhaps adjust
# the bias above)
bias_stick_to_prev_com_choice = False
# To bias the computer towards switching from its own previous choice more
# often, set the "bias_switch_from_prev_com_choice"-variable to True (and
# perhaps adjust the bias above)
bias_switch_from_prev_com_choice = False

# To bias the computer towards sticking to the user's previous choice more
# often, set the "bias_stick_to_prev_user_choice"-variable to True (and perhaps
# adjust the bias above)
bias_stick_to_prev_user_choice = False
# To bias the computer towards switching from the user's previous choice more
# often, set the "bias_switch_from_prev_com_choice"-variable to True (and
# perhaps adjust the bias above)
bias_switch_from_prev_user_choice = False

# In case you want to be evil and turn the computer into a frustrator, i.e. a
# device that always chooses the opposite of the user and thus guarantees that
# the user looses, set the "frustrator"-variable to True.
frustrator = False

## As an adaptation of the program, one might collect data (as the amount of
# attempts and reaction times) from user reacting to frustrator in order to get
# e.g. some proxy of frustration tolerance or trust in the experimenter

# %% several functions, start of loop and cut_off variable


def allowed_bias_combis(bias_heads, bias_tails, bias_stick_to_prev_com_choice,
                        bias_switch_from_prev_com_choice,
                        bias_stick_to_prev_user_choice,
                        bias_switch_from_prev_user_choice, frustrator):
    """
    Checks if the combination of biases is valid, raises an error if not.
    Closes win before raising the error to prevent win from getting stuck.

    Parameters
    ----------
    bias_heads : bool
        stores whether the computer should be biased towards choosing heads.
    bias_tails : bool
        stores whether the computer should be biased towards choosing tails.
    bias_stick_to_prev_com_choice : bool
        stores whether the computer should be biased towards sticking to its
        previous choice.
    bias_switch_from_prev_com_choice : bool
        stores whether the computer should be biased towards switching from its
        previous choice.
    bias_stick_to_prev_user_choice : bool
        stores whether the computer should be biased towards sticking to the
        user's previous choice.
    bias_switch_from_prev_user_choice : bool
        stores whether the computer should be biased towards sticking to the
        user's previous choice.
    frustrator : bool
        stores whether the computer should always choose the opposite of the
        user.

    Raises
    ------
    ValueError
        raises an exception if the bias function frustrator is combined with
        other functions. This is because the frustrator doesn't work with
        probabilites and necessarily simply overwrites all other biases.
    """
    if frustrator is True:
        if (bias_heads or bias_tails or bias_stick_to_prev_com_choice or
            bias_switch_from_prev_com_choice or bias_stick_to_prev_user_choice
                or bias_switch_from_prev_user_choice) is True:
            win.close()
            raise ValueError("""Frustrator is not compatible with other biases
                             as it would simply cover all other possible
                             effects""")


# run the function right away to test for bad bias combis
allowed_bias_combis(bias_heads, bias_tails, bias_stick_to_prev_com_choice,
                    bias_switch_from_prev_com_choice,
                    bias_stick_to_prev_user_choice,
                    bias_switch_from_prev_user_choice, frustrator)


# function to give error message for bad values of the bias and except for
# that only returns the bias
def bias_function(bias):
    """
    Simply returns the bias. Closes win before raising the error to prevent win
    from getting stuck.

    Parameters
    ----------
    bias : float
        the bias of the computer chosen by the experimenter.

    Raises
    ------
    ValueError
        raises an exception if the bias is smaller than -0.5 or bigger than 0.5
        as this would in the end mean that the program had to calculate
        probabilities smaller than 0 or bigger than 1.

    Returns
    -------
    bias : float
        the bias of the computer chosen by the experimenter.
    """
    if bias < -0.5:
        win.close()
        raise ValueError("""You chose a value for bias that is smaller than
                         -0.5. As the cut-off value is equal to 0.5, which is
                         used to compute probabilities, adding a value smaller
                         than -0.5 makes the probability negative. Probabilites
                         however are always >= 0 (at least on standard
                         interpretations of probabilities). Try a value that is
                         between -0.5 and 0.5 instead!""")
    if bias > 0.5:
        win.close()
        raise ValueError("""You chose a value for bias that is bigger than
                         0.5. As the cut-off value is equal to 0.5, which is
                         used to compute probabilities, adding a value bigger
                         than 0.5 makes the probability > 1. Probabilites
                         however are always <= 1 (at least on standard
                         interpretations of probabilities). Try a value that is
                         between -0.5 and 0.5 instead!""")
    return bias


def stick_to_prev_com_choice_function(prev_com_choice, cut_off, bias):
    """
    Biases the computer towards sticking to its previous choice

    Parameters
    ----------
    prev_com_choice : str
        stores the decision of the computer between heads and tails of the
        previous round.
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards sticking to its previous choice.
    """
    if prev_com_choice == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round(cut_off - bias_function(bias), 2)
    return cut_off


def switch_from_prev_com_choice_function(prev_com_choice, cut_off, bias):
    """
    Biases the computer towards switching from its previous choice

    Parameters
    ----------
    prev_com_choice : str
        stores the decision of the computer between heads and tails of the
        previous round.
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards switching from its previous choice.
    """
    if prev_com_choice == 'h':
        cut_off = round(cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_stick_to_prev_user_choice_function(prev_subj_choice, cut_off, bias):
    """
    Biases the computer towards sticking to the user's previous choice

    Parameters
    ----------
    prev_subj_choice : str
        stores the decision of the subject between heads and tails of the
        previous round.
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards sticking to the user's previous choice.
    """
    if prev_subj_choice == 'h':
        cut_off = cut_off + bias_function(bias)
    else:
        cut_off = round(cut_off - bias_function(bias), 2)
    return cut_off


def bias_switch_from_prev_user_choice_function(prev_subj_choice,
                                               cut_off, bias):
    """
   Biases the computer towards switching from the user's previous choice

    Parameters
    ----------
    prev_subj_choice : str
        stores the decision of the subject between heads and tails of the
        previous round.
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards switching from the user's previous choice.
    """
    if prev_subj_choice == 'h':
        cut_off = round(cut_off - bias_function(bias), 2)
    else:
        cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_heads_function(cut_off, bias):
    """
    Biases the computer towards choosing heads

    Parameters
    ----------
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards choosing heads.
    """
    cut_off = cut_off + bias_function(bias)
    return cut_off


def bias_tails_function(cut_off, bias):
    """
    Biases the computer towards choosing tails

    Parameters
    ----------
    cut_off : float
        stores a value which is used to compute the choice of the computer.
        If a random generated float is smaller than the cut_off, the computer's
        decision is heads, otherwise it is tails.
    bias : float
        stores a value to bias the computer to the extend of the value.

    Returns
    -------
    cut_off : float
        updated version of the cut_off variable described above to bias the
        computer towards choosing tails.
    """
    cut_off = round(cut_off - bias_function(bias), 2)
    return cut_off


def frustrator_function(choice_subject, choice_computer):
    """
    Lets the computer always choose the opposite of the user

    Parameters
    ----------
    choice_subject : str
        stores the decision of the subject between heads and tails of the
        current round.
    choice_computer : str
        stores the decision of the computer between heads and tails of the
        current round.

    Returns
    -------
    choice_computer : str
        updated version of the choice_computer variable described above. Now
        always the opposite of choice_subject.
    """
    if choice_subject == 'h':
        choice_computer = 't'
    else:
        choice_computer = 'h'
    return choice_computer


while True:

    # The cut-off variable is (nearly) equal to the probability of the computer
    # choosing heads. The variable is placed within the loop to avoid biases
    # from the previous rounds to influence the next decisions by the computer
    cut_off = 0.5

# %% displays round info before the start of each round
    round_txt = """This is round {}


To choose heads, press 'h'.
To choose tails, press 't'."""
    round_txt = round_txt.format(rounds)
    stim_round = visual.TextStim(win, text=round_txt)
    stim_round.draw()
    win.flip()

# %% choice user & two biases of the computer

    # wait for & restrict keys
    keys = event.waitKeys(keyList=(['h', 't', 'q', 'escape']))

    # quit option
    if keys[0] == 'q':
        break

    # count the amount of changes the subject makes in their decisions relative
    # to their previous choice
    if rounds > 1:
        if prev_subj_choice != keys[0]:
            choice_change_subject += 1

        # biases the computer towards sticking to the user's previous choice
        if bias_stick_to_prev_user_choice is True:
            cut_off = bias_stick_to_prev_user_choice_function(prev_subj_choice,
                                                              cut_off, bias)

        # biases the computer towards switching from the user's previous choice
        if bias_switch_from_prev_user_choice is True:
            cut_off = bias_switch_from_prev_user_choice_function(prev_subj_choice,
                                                                 cut_off, bias)

    # choice_subject
    choice_subject = keys[0]

# %% choice computer

    # count the amount of changes the subject makes in their decisions relative
    # to the computer's previous choice
    if rounds > 1:
        if prev_com_choice != choice_subject:
            choice_change_computer += 1

        # biases the computer towards sticking to its previous choice
        if bias_stick_to_prev_com_choice is True:
            cut_off = stick_to_prev_com_choice_function(prev_com_choice,
                                                        cut_off, bias)

        # biases the computer towards switching from its previous choice
        if bias_switch_from_prev_com_choice is True:
            cut_off = switch_from_prev_com_choice_function(prev_com_choice,
                                                           cut_off, bias)

    # biases the computer towards heads
    if bias_heads is True:
        cut_off = bias_heads_function(cut_off, bias)

    # biases the computer towards tails
    if bias_tails is True:
        cut_off = bias_tails_function(cut_off, bias)

    # creates a random float
    ran_float = random.random()

    # use random float to determine the computer's choice
    if ran_float < cut_off:
        choice_computer = 'h'
    elif ran_float > cut_off:
        choice_computer = 't'
    # just to be super fair and not give either 'h' or 't' a slight
    # (negligible) advantage, in case ran_float == cut_off, there is a new
    # random choice
    else:
        choice_computer = random.choice(['h', 't'])

    # turns the computer into a frustrator
    # aware of the fact that this simply overwrites the previous value of
    # choice_computer
    if frustrator is True:
        choice_computer = frustrator_function(choice_subject, choice_computer)

# %% Displays choice of user and computer as well as results

    # get texts ready to be displayed
    txt_user.draw()
    txt_com.draw()
    txt_continue.draw()

    # gets image of heads ready to be displayed if user chooses head
    if choice_subject == 'h':
        heads = visual.ImageStim(win, size=(0.68, 0.92), pos=(-0.5, -0.2),
                                 image=f_heads)
        heads.draw()
        # gets image of heads ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win, size=(0.68, 0.92), pos=(0.5, -0.2),
                                     image=f_heads)
            heads.draw()
            # raise wins by 1 and get "winner" text ready to be displayed
            wins += 1
            winner.draw()
        # gets image of tails ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win, size=(0.68, 0.92), pos=(0.5, -0.2),
                                     image=f_tails)
            tails.draw()
            # raise losses by 1 and get "loser" text ready to be displayed
            losses += 1
            loser.draw()
        # update the current score and get it ready to be displayed
        score = score_function(wins, losses)
        score.draw()
        # prints everything on the screen and waits for key to be pressed
        win.flip()

    # gets image of tails of penny ready to be displayed if user chooses tails
    else:
        tails = visual.ImageStim(win, size=(0.68, 0.92), pos=(-0.5, -0.2),
                                 image=f_tails)
        tails.draw()
        # gets image of penny ready to be displayed if computer chooses head
        if choice_computer == 'h':
            heads = visual.ImageStim(win, size=(0.68, 0.92), pos=(0.5, -0.2),
                                     image=f_heads)
            heads.draw()
            # raise losses by 1 and get "loser" text ready to be displayed
            losses += 1
            loser.draw()
        # gets image of tails ready to be displayed if computer chooses tail
        else:
            tails = visual.ImageStim(win, size=(0.68, 0.92), pos=(0.5, -0.2),
                                     image=f_tails)
            tails.draw()
            # raise wins by 1 and get "winner" text ready to be displayed
            wins += 1
            winner.draw()
        # update the current score and get it ready to be displayed
        score = score_function(wins, losses)
        score.draw()
        # prints everything on the screen and waits key to be pressed
        win.flip()

    # longer waiting time for win than for loss for well-being of user
    if choice_subject == choice_computer:
        core.wait(1.5)
    else:
        core.wait(1)
    response_key = event.waitKeys()

    # quit option
    if response_key[0] == 'q':
        break

# %% displays the infos of the game so far at the end of the round

    # infos for user at the end of each round. Contains the number of rounds,
    # wins, losses, changes from user's previous choice and changes from
    # computer's previous choice
    txt_game_info = """Up until round {}, you won {} times and lost {} times.
You changed your own choice {} times. You changed {} times from the computer's
choice in the previous round."""
    txt_game_info = txt_game_info.format(rounds, wins, losses,
                                         choice_change_subject,
                                         choice_change_computer)

    # display result of the game so far to user
    game_info = visual.TextStim(win, text=txt_game_info)
    game_info.draw()
    score.draw()
    txt_continue.draw()
    win.flip()
    response_key = event.waitKeys()

    ## As an adaptation of the program, one might abstain from displaying the
    # score and game_info and instead ask the user for her estimate on the
    # amounts of wins & losses conditional on different waiting times for wins
    # and losses (as determined above)

    # raise rounds by 1, update previous com and subj response
    rounds += 1
    prev_com_choice = choice_computer
    prev_subj_choice = choice_subject

# %% displays the final score & some other information, finally closes win

    # quit option
    if response_key[0] == 'q':
        break

amount_rounds = wins + losses

txt_end = """

You played {} rounds.

The final score is:

   You: {}

   Computer: {}


Thanks a lot for your participation!""".format(amount_rounds, wins, losses)

stim_end = visual.TextStim(win, text=txt_end)
stim_end.draw()
win.flip()
core.wait(6)

win.close()
