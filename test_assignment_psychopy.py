# -*- coding: utf-8 -*-
"""
Testing of the matching pennies game
"""
import random
#from assignment_psychopy import bias_function, allowed_bias_combis, stick_to_prev_com_choice_function

#assert com_choice or cut_off or both?
#loop x 100 or so

def allowed_bias_combis (bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator):
    if frustrator == True:
        if bias_heads or bias_tails or bias_stick_to_prev_com_choice or bias_switch_from_prev_com_choice or bias_stick_to_prev_user_choice or bias_switch_from_prev_user_choice == True:
            raise ValueError("Frustrator is not compatible with other biases as it would simply cover all other possible effects")
    return bias_heads and bias_tails and bias_stick_to_prev_com_choice and bias_switch_from_prev_com_choice and bias_stick_to_prev_user_choice and bias_switch_from_prev_user_choice and frustrator


def test_allowed_bias_combis():
    
    frustrator = random.choice(["True", "False"])
    bias_heads = random.choice(["True", "False"])
    bias_tails = random.choice(["True", "False"])
    bias_stick_to_prev_com_choice = random.choice= random.choice(["True", "False"])
    bias_switch_from_prev_com_choice = random.choice(["True", "False"])
    bias_stick_to_prev_user_choice = random.choice(["True", "False"])
    bias_switch_from_prev_user_choice = random.choice(["True", "False"])
    
    if frustrator == "True":
        if bias_heads or bias_tails or bias_stick_to_prev_com_choice or bias_switch_from_prev_com_choice or bias_stick_to_prev_user_choice or bias_switch_from_prev_user_choice == "True":
            result_bad_combi = allowed_bias_combis(bias_heads, bias_tails, bias_stick_to_prev_com_choice, bias_switch_from_prev_com_choice, bias_stick_to_prev_user_choice, bias_switch_from_prev_user_choice, frustrator)
            assert result_bad_combi == ValueError
            
test_allowed_bias_combis()
    
  #  result_good_combi = ...
    
#    assert 
 #   ...
    
    
    
#def test_stick_to_prev_com_choice_function ():
    
