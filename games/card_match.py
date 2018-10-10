import random
from time import sleep

cards = []
player_score = 0
cpu_score = 0
turn = 0

alphabets = "abcdefghijklmnopqrstuvwxyz"

def init_cards(num):
    global player_score
    global cpu_score
    global turn
    global cards

    player_score = 0
    cpu_score = 0
    turn = 0

    cards = []
    for i in range(num):
        c = random.choice(alphabets)
        for i in range(2):
            cards.append(c)

def show_lie_cards():
    for i in range(len(cards)):
        print("{:3}".format(i), end="")
    print()
    for i in range(len(cards)):
        print("  *", end="")
    print()

def show_reverse_cards(idx1, idx2):
    for i in range(len(cards)):
        if i in [idx1, idx2]:
            print("  {}".format(cards[i]), end="")
        else:
            print("  *", end="")
    print()

def inputs_filtered():
    while True:
        inputs = input(">")
        try:
            filtered = [int(w) for w in inputs.split()]
        except ValueError:
            continue
        if len(filtered) != 2:
            continue
        if filtered[0] < 0 and len(cards) <= filtered[0]:
            continue
        if filtered[1] < 0 and len(cards) <= filtered[1]:
            continue
        return filtered

def cpu_random_choice():
    print("CPU choicing...")
    sleep(random.gauss(1, 1))
    chocies = [i for i in range(len(cards))]
    inputs = []
    while len(inputs) != 2:
        c = random.choice(chocies)
        if c not in inputs:
            inputs.append(c)
    return inputs

def check_and_remove_cards(idx1, idx2, player=True):
    global player_score
    global cpu_score
    if cards[idx1] == cards[idx2]:
        if idx1 < idx2:
            del cards[idx2]
            del cards[idx1]
        else:
            del cards[idx1]
            del cards[idx2]
        if player:
            player_score += 2
        else:
            cpu_score += 2

def print_score():
    print("Player Score :", player_score, "CPU Score:", cpu_score)

num = input("Num Cards?: ")
init_cards(num // 2)

while len(cards) != 0:
    turn += 1
    print("Turn:", turn)
    show_lie_cards()

    idx1, idx2 = inputs_filtered()
    show_reverse_cards(idx1, idx2)
    check_and_remove_cards(idx1, idx2, player=True)

    cpu1, cpu2 = cpu_random_choice()
    show_reverse_cards(cpu1, cpu2)
    check_and_remove_cards(cpu1, cpu2, player=False)

    print_score()
    print()
