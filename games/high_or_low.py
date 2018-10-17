import random
import sys
sys.path.append('../myutil')
from savedata import save, load
from input_filtered import int_input, true_or_false_input
from text_effect import type_print

save_file = 'high_low_score'


def card_name(card):
    num_to_name = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    soot = card[0]
    num = int(card[1:])
    if num in num_to_name:
        return "{}{}".format(soot, num_to_name[num])
    else:
        return "{}{}".format(soot, num)


def card_num(card):
    return int(card[1:])


def pick_two_cards(cards):
    random.shuffle(cards)
    return cards[:2]


cards = ['{}{}'.format(soot, num + 1)
         for num in range(13)
         for soot in ['H', 'S', 'C', 'D']]

# set money_in_hand
default_money = 100
money_in_hand = load(save_file, default=default_money)
if money_in_hand <= 0:
    money_in_hand = default_money
    print('Initialize amount of money.')

# game loop
while True:
    print('You have {}$'.format(money_in_hand))

    bet = int_input(1, money_in_hand, description='How much will you bet?')
    print('Money:{}$ -{}$)'.format(money_in_hand, bet))
    money_in_hand -= bet

    card1, card2 = pick_two_cards(cards)
    num1, num2 = card_num(card1), card_num(card2)
    print('Cards: {} ***'.format(card_name(card1)))

    # high or low?
    high = true_or_false_input('high', 'low',
                               description='High or Low? ')

    # open cards
    print('Open Cards')
    type_print('Cards: {} {}'.format(card_name(card1), card_name(card2)), 0.3)

    if (high and num1 < num2) or (not high and num1 > num2):  # Victory
        print('Congratulatins!')
        print('Money{}$ +{}$'.format(money_in_hand, bet * 2))
        money_in_hand += bet * 2
    else:  # Lose
        print('Lose')

    save(save_file, money_in_hand)
    if money_in_hand <= 0:
        print('Game Over\nMoney is none.')
        break

    if not true_or_false_input('y', 'n', description='Continue? y/n:'):
        break
