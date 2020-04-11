# -*- coding: utf-8 -*-
"""
Testing of the functions in the matching pennies game
"""

# %% Setup: Imports, functions and variables

import random
#from assignment_psychopy import bias_function, allowed_bias_combis, stick_to_prev_com_choice_function

#copy paste of the functions that are to be tested as importing the functions unfortunately runs the whole assignment_psychopy program and opens the win just as in the original program.

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

#function to give error message for bad values of the bias and except for that only returns the bias
def bias_function (bias):
    if bias < -0.5:
        #win.close()
        raise ValueError ("""You chose a value for bias that is smaller than -0.5. As the cut-off 
                         value is equal to 0.5, which is used to compute probabilities, adding a 
                         value smaller than -0.5 makes the probability negative. Probabilites however 
                         are always >= 0 (at least on standard interpretations of probabilities).
                         Try a value that is between -0.5 and 0.5 instead!""")
    if bias > 0.5:
        #win.close()
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



cut_off = 0.5
bias = 0.4

# %% test functions

# no testing of quit_function, bias_function and allowed_bias_combis because they simply return variables or functions unless some error is triggered.
        
#test of the function to bias the computer towards sticking to its previous choice
def test_stick_to_prev_com_choice_function ():
    choice_computer = random.choice(['h', 't'])
    if choice_computer == "h":
        case_heads = stick_to_prev_com_choice_function (choice_computer, cut_off, bias)
        assert case_heads == 0.9
    else:
        case_tails = stick_to_prev_com_choice_function (choice_computer, cut_off, bias)
        assert case_tails == 0.1

#test of the function to bias the computer towards switching from its previous choice
def test_switch_from_prev_com_choice_function ():
    choice_computer = random.choice(['h', 't'])
    if choice_computer == "h":
        case_heads = switch_from_prev_com_choice_function(choice_computer, cut_off, bias)
        assert case_heads == 0.1
    else:
        case_tails = switch_from_prev_com_choice_function(choice_computer, cut_off, bias)
        assert case_tails == 0.9

#test of the function to bias the computer towards sticking to the user's previous choice
def test_bias_stick_to_prev_user_choice_function ():
    choice_subject = random.choice(['h', 't'])
    if choice_subject == "h":
        case_heads = bias_stick_to_prev_user_choice_function(choice_subject, cut_off, bias)
        assert case_heads == 0.9
    else:
        case_tails = bias_stick_to_prev_user_choice_function(choice_subject, cut_off, bias)
        assert case_tails == 0.1

#test of the function to bias the computer towards switching from the user's previous choice
def test_bias_switch_from_prev_user_choice_function ():
    choice_subject = random.choice(['h', 't'])
    if choice_subject == "h":
        case_heads = bias_switch_from_prev_user_choice_function(choice_subject, cut_off, bias)
        assert case_heads == 0.1
    else:
        case_tails = bias_switch_from_prev_user_choice_function(choice_subject, cut_off, bias)
        assert case_tails == 0.9

#test of the function to bias the computer towards heads
def test_bias_heads_function ():
    assert bias_heads_function(cut_off, bias) == 0.9

#test of the function to bias the computer towards tails
def test_bias_tails_function ():
    assert bias_tails_function(cut_off, bias) == 0.1

#test of the frustrator function
def test_frustrator_function ():
    choice_subject = random.choice(['h', 't'])
    if choice_subject == 'h':
        choice_computer = 't'
    else: choice_computer = 'h'
    
    if choice_subject == 'h':
        assert frustrator_function(choice_subject, choice_computer) == 't'
    else: 
        assert frustrator_function(choice_subject, choice_computer) == 'h'

# %% actual tests

test_bias_heads_function()
test_bias_tails_function()

#To be sure they work, tests with random values are tested several times below
for repeats in range (50):
    test_stick_to_prev_com_choice_function()      
    test_switch_from_prev_com_choice_function()
    test_bias_stick_to_prev_user_choice_function()
    test_bias_switch_from_prev_user_choice_function()
    test_frustrator_function()
    
    
    






    
