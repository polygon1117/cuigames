import random
from time import sleep
import sys
sys.path.append("../myutil")
from text_effect import type_print

class Prisoner():
    def __init__(self, name):
        self.jail_years = 0
        self.name = name

    def initialize(self):
        pass

    def decision(self):
        """return confession(True) or silence(False)."""
        return True

    def say_decision(self, mydecision):
        if mydecision:
            print(self.name, ">yes")
        else:
            print(self.name, ">no")
        return mydecision

    def opponent_decision(self, opp_decision):
        pass

    def add_jail_year(self, addition_year):
        self.jail_years += addition_year

    def __str__(self):
        return self.name + "(懲役 {} 年)".format(self.jail_years)


class Player(Prisoner):
    def __init__(self, name):
        super().__init__(name)

    def decision(self):
        while True:
            inputs = input("{} >".format(self.name))
            if inputs == 'yes':
                return True
            elif inputs == 'no':
                return False
            else:
                print("おかしなことを言ってないで、正直に答えなさい。")
                continue

    def say_decision(self, mydecision):
        pass


class Honest(Prisoner):
    def __init__(self, name):
        super().__init__(name)

    def decision(self):
        return True


class Lier(Prisoner):
    def __init__(self, name):
        super().__init__(name)

    def decision(self):
        return False


class Parrot(Prisoner):
    def __init__(self, name):
        super().__init__(name)
        self.initialize()

    def initialize(self):
        self.pre_opp_decision = False

    def decision(self):
        return self.pre_opp_decision

    def opponent_decision(self, opp_decision):
        self.pre_opp_decision = opp_decision


class Dark_Parrot(Parrot):
    def __init__(self, name):
        super().__init__(name)
        self.initialize()

    def initialize(self):
        self.pre_opp_decision = True


class Randomer(Prisoner):
    def __init__(self, name):
        super().__init__(name)

    def decision(self):
        return random.choice([True, False])


class Patienter(Prisoner):
    def __init__(self, name):
        super().__init__(name)
        self.initialize()

    def initialize(self):
        self.pre_pre_opp_decision = False
        self.pre_opp_decision = False

    def decision(self):
        if self.pre_pre_opp_decision and self.pre_opp_decision:
            return True
        else:
            return False

    def opponent_decision(self, opp_decision):
        self.pre_pre_opp_decision = self.pre_opp_decision
        self.pre_opp_decision = opp_decision


class Friedman(Prisoner):
    def __init__(self, name):
        super().__init__(name)
        self.initialize()

    def initialize(self):
        self.is_angry = False

    def decision(self):
        return self.is_angry

    def opponent_decision(self, opp_decision):
        if opp_decision:
            self.is_angry = True


def one_game(prisoner1, prisoner2, jail_years):
    """
    Do one game.
    Args:
        prisoner1(Prisoner): Prisoner1
        prisoner2(Prisoner): Prisoner2
        jail_years(list): [(s, s), (s, c), (c, s), (c, c)]
            s = silence, c = confession
    """
    decision1 = prisoner1.decision()
    decision2 = prisoner2.decision()
    prisoner1.say_decision(decision1)
    prisoner2.say_decision(decision2)

    prisoner1.opponent_decision(decision2)
    prisoner2.opponent_decision(decision1)

    if not decision1 and not decision2:
        judge = jail_years[0]
    elif not decision1 and decision2:
        judge = jail_years[1]
    elif decision1 and not decision2:
        judge = jail_years[2]
    else:
        judge = jail_years[3]
    prisoner1.add_jail_year(judge[0])
    prisoner2.add_jail_year(judge[1])


def show_result(prisoners, interval):
    prisoners_with_jail = {prisoner: prisoner.jail_years for prisoner in prisoners}
    prisoners_with_jail = sorted(prisoners_with_jail.items(), key=lambda x: x[1])
    print("Winner: ", end="")
    for i, prisoner in enumerate(dict(prisoners_with_jail).keys()):
        sleep(interval)
        name = str(prisoner)
        type_interval = 0.3 / (i / 4 + 1)
        type_print(name, type_interval)


def init_prisoners():
    player = Player(name if not name == "" else "プレイヤー")
    honest = Honest("正直者")
    lier = Lier("嘘つき")
    parrot = Parrot("オウム")
    dark_parrot = Dark_Parrot("黒オウム")
    patienter = Patienter("我慢の人")
    randomer = Randomer("サル")
    friedman = Friedman("フリードマン")

    prisoners = []
    prisoners.append(player)
    prisoners.append(honest)
    prisoners.append(lier)
    prisoners.append(parrot)
    prisoners.append(dark_parrot)
    prisoners.append(patienter)
    prisoners.append(randomer)
    prisoners.append(friedman)

    return prisoners


if __name__ == '__main__':
    name = input("あなたの名前は?\n>")
    n_stage = int(input("何ステージ行う?\n>"))
    n_game_per_stage = int(input("1ステージで何回駆け引きを行う?\n>"))
    print()

    prisoners = init_prisoners()

    heavy = random.randint(5, 20)
    regular = random.randint(3, heavy-1)
    light = random.randint(1, regular-1)
    # [(s, s), (s, c), (c, s), (c, c)]
    jail_years = [(light, light), (heavy, 0), (0, heavy), (regular, regular)]

    # ゲーム説明
    print("本来ならお前たちは懲役{}年だが、もし2人とも黙秘すれば、証拠不十分として2人とも懲役{}年となる。".format(regular, light))
    print("もし片方だけが自白したら、そいつはその場で釈放してやろう。黙秘していた方は懲役{}年だが。".format(heavy))
    print("ただし、2人とも自白したら、判決通り2人とも懲役{}年だ。".format(regular))
    print("という、設定で2人づつの組に分け、何回かゲームを行う。")
    print("自白するならyes, 黙秘するならnoと答えてもらう。")
    print("最終的に懲役年数が少ないものの勝利とする。")
    print("それでは始めよう。")

    for stage in range(n_stage):
        print("\nステージ{}".format(stage))
        random.shuffle(prisoners)

        # [p1, p2, p3, p4] => [(p1, p2), (p3, p4)]
        prisoners_groups = zip(*[iter(prisoners)] * 2)
        for group in prisoners_groups:
            print(group[0], "and", group[1])
            group[0].initialize()
            group[1].initialize()
            for i in range(n_game_per_stage):
                print("駆け引き[{}]".format(i))
                one_game(group[0], group[1], jail_years)
            print("途中結果:", group[0], group[1])
            print()
    print()

    type_print("判決を言い渡す!", 0.4)
    sleep(0.5)
    show_result(prisoners, 1.5)
