# -*- coding: utf-8 -*-
"""
Testing of the functions in the matching pennies game
"""

# %% Setup: Imports, functions and variables

import random

# copy paste of the functions that are to be tested as importing the functions
# unfortunately runs the whole assignment_psychopy program and opens the win
# just as in the original program.


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
            # win.close()
            raise ValueError("""Frustrator is not compatible with other biases
                             as it would simply cover all other possible
                             effects""")


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
        # win.close()
        raise ValueError("""You chose a value for bias that is smaller than
                         -0.5. As the cut-off value is equal to 0.5, which is
                         used to compute probabilities, adding a value smaller
                         than -0.5 makes the probability negative. Probabilites
                         however are always >= 0 (at least on standard
                         interpretations of probabilities). Try a value that is
                         between -0.5 and 0.5 instead!""")
    if bias > 0.5:
        # win.close()
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
        decision is
        heads, otherwise it is tails.
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
        decision is
        heads, otherwise it is tails.
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


###########################################################################################
## still missing test of score_function; however how shoud it be tested as it opens win? ##
###########################################################################################

cut_off = 0.5
bias = 0.4

# %% defines test functions

# no testing of quit_function and bias_function because they simply return
# variables or functions unless some error is triggered.
# ??? no testing of allowed bias combis because it doesn't have a return value


# test of function to bias the computer towards sticking to its previous choice
def test_stick_to_prev_com_choice_function():
    prev_com_choice = random.choice(['h', 't'])
    if prev_com_choice == "h":
        case_heads = stick_to_prev_com_choice_function(prev_com_choice,
                                                       cut_off, bias)
        assert case_heads == 0.9
    else:
        case_tails = stick_to_prev_com_choice_function(prev_com_choice,
                                                       cut_off, bias)
        assert case_tails == 0.1


# test of function to bias the computer towards switching from its
# previous choice
def test_switch_from_prev_com_choice_function():
    prev_com_choice = random.choice(['h', 't'])
    if prev_com_choice == "h":
        case_heads = switch_from_prev_com_choice_function(prev_com_choice,
                                                          cut_off, bias)
        assert case_heads == 0.1
    else:
        case_tails = switch_from_prev_com_choice_function(prev_com_choice,
                                                          cut_off, bias)
        assert case_tails == 0.9


# test of function to bias the computer towards sticking to the user's
# previous choice
def test_bias_stick_to_prev_user_choice_function():
    prev_subj_choice = random.choice(['h', 't'])
    if prev_subj_choice == "h":
        case_heads = bias_stick_to_prev_user_choice_function(prev_subj_choice,
                                                             cut_off, bias)
        assert case_heads == 0.9
    else:
        case_tails = bias_stick_to_prev_user_choice_function(prev_subj_choice,
                                                             cut_off, bias)
        assert case_tails == 0.1


# test of function to bias the computer towards switching from the user's
# previous choice
def test_bias_switch_from_prev_user_choice_function():
    prev_subj_choice = random.choice(['h', 't'])
    if prev_subj_choice == "h":
        case_heads = bias_switch_from_prev_user_choice_function(prev_subj_choice,
                                                                cut_off, bias)
        assert case_heads == 0.1
    else:
        case_tails = bias_switch_from_prev_user_choice_function(prev_subj_choice,
                                                                cut_off, bias)
        assert case_tails == 0.9


# test of the function to bias the computer towards heads
def test_bias_heads_function():
    assert bias_heads_function(cut_off, bias) == 0.9


# test of the function to bias the computer towards tails
def test_bias_tails_function():
    assert bias_tails_function(cut_off, bias) == 0.1


# test of the frustrator function
def test_frustrator_function():
    choice_subject = random.choice(['h', 't'])
    if choice_subject == 'h':
        choice_computer = 't'
    else:
        choice_computer = 'h'

    if choice_subject == 'h':
        assert frustrator_function(choice_subject, choice_computer) == 't'
    else:
        assert frustrator_function(choice_subject, choice_computer) == 'h'


# %% actual tests

test_bias_heads_function()
test_bias_tails_function()

# To be sure they work, tests with random values are tested several times below
for repeats in range(50):
    test_stick_to_prev_com_choice_function()
    test_switch_from_prev_com_choice_function()
    test_bias_stick_to_prev_user_choice_function()
    test_bias_switch_from_prev_user_choice_function()
    test_frustrator_function()
