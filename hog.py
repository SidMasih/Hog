"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
   #Using flag as indicator to know if 1 has been rolled or not

    flag, sum_score, i = True, 0, 1
    while(i <= num_rolls):

        dice_roll = dice()
        sum_score += dice_roll
        if(dice_roll == 1):
            flag = False
        i += 1
            
    if(flag):
        return sum_score
    else:
        return 0
    # END Question 1


def isPrime(n):
    """returns True or False if prime number
    >>> isPrime(6)
    False
    """
    #checks for prime nos > 1
    for i in range(2,(n//2) + 1) :
        if(n % i == 0):
            return False
    return True

def nextPrime(n):
    """ returns next prime number after n
    """
    while(not isPrime(n+1)):
        n = n + 1
    return n + 1

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2

    #Applying Free Bacon rule
    if(num_rolls == 0):
        turn_total =  (1 + max(opponent_score % 10,(opponent_score//10) % 10))
    else:
        turn_total = roll_dice(num_rolls,dice)

    #Applying Hogtimus Prime rule
    if(isPrime(turn_total) and turn_total>= 2):
        return nextPrime(turn_total)
    else:
        return turn_total


    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 

    #Applying Hog Wild rule
    if((score + opponent_score) % 7 == 0):
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 

    #Applying Swine Swap
    reverse = ( (score0%10) * 10) + ( (score0//10) % 10)
    return (reverse == score1%100)
    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5

    while(score0 < goal and score1 < goal):

        #tests to see if needed to choose 4 or 6 sided dice
        the_dice = select_dice(score0,score1)

        #player 1
        if(who == 0):
            num_of_rolls = strategy0(score0,score1)
            turn_score = take_turn( num_of_rolls , score1, the_dice )
            if(turn_score == 0):
                score1 += num_of_rolls
            score0 += turn_score

        #player 2
        else:
            num_of_rolls = strategy1(score1,score0)
            turn_score = take_turn( num_of_rolls , score0, the_dice )
            if(turn_score == 0):
                score0 += num_of_rolls
            score1 += turn_score

        #tests to see if need to swap scores
        if(is_swap(score0,score1)):
            temp = score0
            score0 = score1
            score1 = temp

        who = other(who)

    return score0, score1
    # END Question 5
    


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def another(*args):
        result = 0
        for i in range(0,num_samples):
            result += fn(*args)
        return result/num_samples

    return another
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    best_roll = 1
    best_avg = 0
    avg_func = make_averaged(roll_dice,num_samples)
    for i in range(1,11):
        current_avg = avg_func(i,dice)
        if(current_avg > best_avg):
            best_avg = current_avg
            best_roll = i

    return best_roll

    # END Question 7


def initial_rolls_strategy(score, opponent_score):
    """return optimal number of die to roll depending on score(s)

    performs initial analysis to see what would be the optimum roll for
    the computer to roll

    this method must be called first for each turn to find the initial number
    of die to be rolled for each turn the computer does

    # of die rolled are primarily divided by stages of the game (based on the
    strategy users score) with in general greater risk being taken in the
    beginning but risk reduction procedures towards the end of the game

    within each stage of the game, different # of die are rolled depending on
    whether the strategy user is ahead, behind, or very behind from the
    opponent,special care is taken to avoid swaping scores if the strategy user's
    score is higher
    """
    sum_score = score + opponent_score

    #test for multiple of 7 or for a 0 - 0 score
    if (sum_score % 7 == 0):
       return 4

    elif(sum_score == 0):
        return 4

    # initial high risk stage of the game
    elif(score < 25):

        # more risk if behind
        if(score - opponent_score >= 10):
            return hog_wild_strategy(score,opponent_score,6)

        # attempt to swap if behind
        elif(opponent_score - score >= 10):
            return piggyswap_strategy(score, opponent_score, hog_wild_strategy(score,opponent_score,5) )

        else:
            return hog_wild_strategy(score,opponent_score,4)

    # risk lowered for this phase
    elif(score < 45):

        if(score - opponent_score >= 10):
            return hog_wild_strategy(score,opponent_score,4)

        elif(opponent_score - score >= 10):
            return piggyswap_strategy(score, opponent_score, hog_wild_strategy(score,opponent_score,5) )

        else:
            return hog_wild_strategy(score,opponent_score,3)

    #risk especially lowered for this phase
    elif(score < 70):

        if(score - opponent_score >= 10):
            return hog_wild_strategy(score,opponent_score,3)

        elif(opponent_score - score >= 10):
            return piggyswap_strategy(score, opponent_score, hog_wild_strategy(score,opponent_score,4) )
        else:
            return hog_wild_strategy(score,opponent_score,2)

    # either opponent or strategy user close to winning so very low risk
    else:

        if(score - opponent_score >= 10):
            return hog_wild_strategy(score,opponent_score,2)

        elif(opponent_score - score >=10):
            return piggyswap_strategy(score, opponent_score, hog_wild_strategy(score,opponent_score,3) )

        else:
            return hog_wild_strategy(score,opponent_score,1)




def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)

    if score0 > score1:
        return 0

    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test main strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies
def hog_wild_strategy (score, opponent_score, num_rolls):
    """ return # of die to roll. This method will attempt to return a 0 dice
    roll if Hog Wild will be triggered for opponent, a four sided dice increases
    the risk of rolling a 1 and causing piggyback in the strategy users favor

    attempts to use Free Bacon to cause Hog Wild
    """
    if ((score + take_turn(0, opponent_score) + opponent_score) % 7 == 0):
        return 0

    else:
        return num_rolls

def piggyswap_strategy(score, opponent_score, num_rolls):
    """returns # of die to roll, piggyswap_strategy tries to add points to the
    opponent so that a swine swap can occur in the strategy user's favor
    Otherwise, gives a huge boost to our score as it turns > 6 (with essentially no 1s)


    THIS METHOD SHOULD ONLY BE CALLED IF THE STRATEGY USER IS LOOSING!


    if a swap is not optimal the method returns num_rolls
    strategy was found to be highly effective

    """
    if(is_swap(score,opponent_score + 6)):
        return 6
    elif(is_swap(score,opponent_score + 7)):
        return 7
    elif(is_swap(score, opponent_score + 8)):
        return 8
    elif(is_swap(score, opponent_score + 9)):
        return 9
    elif(is_swap(score, opponent_score + 10)):
        return 10
    else:
        return num_rolls
    

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """return # of die rolled. This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8

    #takes psuedo-turn with 0 roll to see if Free Bacon is optimal
    if(take_turn(0,opponent_score) >= margin ):
        return 0

    else:
        return num_rolls
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy returns 0 roll when it results in a beneficial swap,
    using the Free Bacon principal or
    returns NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    turn_total = take_turn(0,opponent_score) + score

    if(( is_swap(turn_total, opponent_score) ) and opponent_score > turn_total):
        return 0

    else:
        return num_rolls
    # END Question 9


def final_strategy(my_score, opponent_score):
    """return optimal # or die to roll

    final strategy first checks initial optimum roll #, please reffer to the final_strategy
    documentation for greater detail!

    next bacon_strategy tests if free bacon will return greater points than
    the initially deterimend score based on the initial number of die rolled

    next piggyswap_strategy looks if it is benificial to roll a 0 to cause a swine swap
    if and only if strategy user is behind opponent
    """
    # BEGIN Question 10

    #minimize piggyback affect
    roll_number = initial_rolls_strategy(my_score, opponent_score)

    #check to see if we want some good free bacon!
    roll_number = bacon_strategy(my_score, opponent_score, 6, roll_number)

    #test to see if benificial to swap scores
    if(my_score < opponent_score):
        roll_number = piggyswap_strategy(my_score, opponent_score, roll_number)

    return roll_number


    # END Question 10

##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
