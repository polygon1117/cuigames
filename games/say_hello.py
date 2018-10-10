import random
from time import sleep

alphabets = list("abcdefghijklmnopqrstuvwxyz")
to_alphabets = list("abcdefghijklmnopqrstuvwxyz")
random.shuffle(to_alphabets)

def inputs_filtered(count):
    inputs = input("[{}] type 5 words: ".format(count))
    tmp = []
    for c in inputs:
        if c in alphabets:
            tmp.append(c)
    if len(tmp) > 5:
        tmp = tmp[:5]
    return "".join(tmp)


def cpu_replay(inputs):
    replay = []
    for c in inputs:
        index = alphabets.index(c)
        replay.append(to_alphabets[index])
    replay = "".join(replay)

    sleep(0.5)
    print("<", replay)

    return replay

if __name__ == "__main__":
    count = 0
    while True:
        count += 1
        inputs = inputs_filtered(count)
        replay = cpu_replay(inputs)

        if replay == "hello":
            sleep(0.3)
            print("< good job!!")
            break
