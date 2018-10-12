import sys
sys.path.append("../myutil")
from input_filtered import int_input

def bit_flag(bit, index):
    return bit >> index & 1

def next_generation(state, rule):
    if len(state) == 1:
        return [bit_flag(rule, state[0] * 2)]
    next_gen = []
    for i in range(len(state)):
        index = 0
        if i == 0:
            index = state[0] * 2 + state[1]
        elif i == len(state) - 1:
            index = state[i-1] * 4 + state[i] * 2
        else:
            index = state[i-1] * 4 + state[i] * 2 + state[i+1]
        next_gen.append(bit_flag(rule, index))
    return next_gen

def show_state(state):
    for s in state:
        if s == 0:
            print(' ', end="")
        elif s == 1:
            print('*', end="")
    print()

if __name__ == '__main__':
    rule = int_input(min_val=0, max_val=255, description="Rule:")
    epochs = int_input(min_val=0, description="Epochs:")

    print("Input seed, like ' *  *  '. This mean 0100100.")
    init_seed = input("Seed:")
    state = []
    for c in init_seed:
        if c == ' ':
            state.append(0)
        elif c == '*':
            state.append(1)
    length = len(state)

    print()
    show_state(state)
    for epoch in range(epochs):
        state = next_generation(state, rule)
        show_state(state)
