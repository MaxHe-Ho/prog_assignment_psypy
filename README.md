# prog_assignment_psypy

## The game: Matching pennies
Click [here](https://github.com/MaxHe-Ho/prog_assignment_psypy/blob/master/assignment_psychopy.py) to get to the main program.

This program allows the user to play a game of matching pennies against the computer. The user is the even player. This means that if both pennies match, the user (even player) wins the round and gets a point and if they don't, the computer gets a point. 
The computer can be setup with different biases. It chooses randomly by default but the code allows different biases to be implemented quite easily, comments point out the slight necessary changes.
The biases are:
- a bias for heads and one for tails
- a bias for letting the computer stick to its previous choice and one for letting it switch from its previous choice
- a bias for letting the computer stick to the user's previous choice and one for letting it switch from the user's previous choice
- a bias that turns the computer into a frustrator, i.e. a device that always chooses the opposite of the user and thus 
guarantees that the user looses

For all the biases, the strenght/ extend of the bias can be changed. Additionally, all the biases except for the frustrator-bias can be freely combined. Though of course the effects of some biases (e.g. for both heads & tails) cancel each other out.

The programme automatically prints the following information after each round:
  - The amount of wins of the user and computer
  - The current score
  - How often the subject switched their choice compared to their choice in the previous round
  - How often the subject switched their choice compared to the computer’s choice in the previous round

## How to use the program
Best download the whole zip file from this repository, unpack it and run the main program. There's an additional file for testing the functions of the main program. 
Everything the user needs to know is explained on the screen that pops up when running the program. Regarding the experimenter: Changing the biases is straightforward and explained in detail in comments within the main program. Details about how the program runs are included in the comments & docstrings in the main program. Comments that start with "##" indicate a suggestion for an adaptation of the program.

By pressing 'h', the subject chooses heads and by pressing 't', the subject chooses tails. The computer chooses 
randomly or according to the bias that is currently setup. After the subject has made their choice, both pennies are shown on the screen and subject gets the information whether they won and what the current scores are. The subject can quit at any point by pressing 'q' or 'escape'.

### Data
Click [here](https://github.com/MaxHe-Ho/prog_assignment_psypy/tree/master/data) to get to the two images of a penny that the programm uses.

### License information
If you actually want to read license information, you can find it [here](https://github.com/MaxHe-Ho/prog_assignment_psypy/blob/master/LICENSE).

#### Such wow! Much useful information about yourself you always wanted to have!!
To find out details about your greatest ability, way more reliable than online personality tests and horoscopes, click [here](https://en.wikipedia.org/wiki/Procrastination). 
