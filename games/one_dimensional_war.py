import random
import sys
sys.path.append('../myutil')
from input_filtered import alphabets_input

alphabets = "abcdefghijklmnopqrstuvwxyz"


class Entity(object):
    def __init__(self, hp, gp_recovery_rate, name):
        self.hp = hp
        self.gp = 0
        self.gp_recovery_rate = gp_recovery_rate
        self.name = name

    def update(self):
        self.gp += self.gp_recovery_rate

    def _generate_alpha(self):
        return " "

    def generate_alpha(self):
        alpha = self._generate_alpha()
        if alpha not in alphabets:
            return alpha

        gp_consamption = alphabets.index(alpha) + 1
        if self.gp >= gp_consamption:
            self.gp -= gp_consamption
            return alpha
        elif self.gp == 0:
            return " "
        else:
            alpha_max = alphabets[self.gp - 1]
            self.gp = 0
            return alpha_max

    def receive_damage(self, alpha):
        self.hp -= alphabets.index(alpha) + 1

    def is_lose(self):
        return self.hp <= 0

    def __str__(self):
        return self.name


class Player(Entity):
    def __init__(self, hp, gp_recovery_rate, name):
        super().__init__(hp, gp_recovery_rate, name)

    def _generate_alpha(self):
        alpha = alphabets_input(min_length=1, max_length=1,
                                description="Alphabet:",
                                filter_null=False
                                )
        return alpha if len(alpha) != 0 else " "


class RandomCPU(Entity):
    def __init__(self, hp, gp_recovery_rate, name):
        super().__init__(hp, gp_recovery_rate, name)

    def _generate_alpha(self):
        idx = random.choice(range(min(self.gp, len(alphabets))))
        return alphabets[idx]


class DicCPU(Entity):
    def __init__(self, hp, gp_recovery_rate, name):
        super().__init__(hp, gp_recovery_rate, name)
        self.tactics = ['a'] * 10 + ['c'] * 5 + ['d'] * 10 + ['z'] * 100

    def _generate_alpha(self):
        alpha = self.tactics[self.gp]
        return alpha


class GameMaster(object):
    def __init__(self, player1, player2, field_length, threthold=2):
        self.player1 = player1
        self.player2 = player2
        self.field_length = field_length
        self.p1_field = [" "] * field_length
        self.p2_field = [" "] * field_length
        self.field = [0] * field_length  # 陣地 p1: +, p2: -
        self.threthold = threthold

    def update(self):
        self.player1.update()
        self.player2.update()
        p1_generate = self.player1.generate_alpha()
        p2_generate = self.player2.generate_alpha()

        # Update Field
        self._update_field()

        # Damage processing
        last_idx = self.field_length - 1
        if self.p1_field[last_idx] != " ":
            self.player2.receive_damage(self.p1_field[last_idx])
        if self.p2_field[0] != " ":
            self.player1.receive_damage(self.p2_field[0])

        # Remove old alphabet and Add new alphabet
        del self.p1_field[last_idx]
        self.p1_field.insert(0, p1_generate)
        del self.p2_field[0]
        self.p2_field.append(p2_generate)

        # Duplication processing
        for i, (alpha1, alpha2) in enumerate(zip(self.p1_field, self.p2_field)):
            if alpha1 in alphabets and alpha2 in alphabets:
                idx1 = alphabets.index(alpha1)
                idx2 = alphabets.index(alpha2)
                if idx1 > idx2:
                    idx1_next = idx1 - idx2 - 1
                    self.p1_field[i] = alphabets[idx1_next]
                    self.p2_field[i] = " "
                    self.field[i] = min(
                        self.field[i] + (idx1_next + 1), self.threthold)
                elif idx1 == idx2:
                    self.p1_field[i] = " "
                    self.p2_field[i] = " "
                else:
                    idx2_next = idx2 - idx1 - 1
                    self.p1_field[i] = " "
                    self.p2_field[i] = alphabets[idx2_next]
                    self.field[i] = max(
                        self.field[i] - (idx2_next + 1), -self.threthold)

    def _update_field(self):
        # Update p1_field
        for i, alpha in enumerate(self.p1_field):
            if alpha not in alphabets:
                continue
            if self.field[i] >= self.threthold:
                continue
            idx = alphabets.index(alpha)
            next_idx = idx - 1
            if next_idx < 0:
                self.field[i] += 1
                self.p1_field[i] = " "
            else:
                self.p1_field[i] = alphabets[next_idx]

        # Update p2_field
        for i, alpha in enumerate(self.p2_field):
            if alpha not in alphabets:
                continue
            if self.field[i] <= -self.threthold:
                continue
            idx = alphabets.index(alpha)
            next_idx = idx - 1
            if next_idx < 0:
                self.field[i] -= 1
                self.p2_field[i] = " "
            else:
                self.p2_field[i] = alphabets[next_idx]

    def show_field(self):
        p1_name = str(self.player1)
        p2_name = str(self.player2)

        # Player|ac     f  c  a|CPU
        print("{}|".format(p1_name), end="")
        for alpha1, alpha2 in zip(self.p1_field, self.p2_field):
            if alpha1 in alphabets:
                print("{}>".format(alpha1), end="")
            elif alpha2 in alphabets:
                print("<{}".format(alpha2), end="")
            else:
                print("  ", end="")
        print("|{}".format(p2_name))

        # Player|ac     f  c  a|CPU
        #        22000000200001
        print(" " * (len(p1_name) + 1), end="")
        for field_val in self.field:
            print(" {}".format(abs(field_val)), end="")
        print()

        # Player|ac     f  c  a|CPU
        #        22000000200001
        #        ++      -    -
        print(" " * (len(p1_name) + 1), end="")
        for field_val in self.field:
            if field_val <= -self.threthold:
                print(" c", end="")
            elif field_val >= self.threthold:
                print(" p", end="")
            elif field_val < 0:
                print(" -", end="")
            elif field_val > 0:
                print(" +", end="")
            else:
                print("  ", end="")
        print()

    def game_end(self):
        if self.player1.is_lose() and self.player2.is_lose():
            print('Draw')
            return True

        elif self.player1.is_lose():
            print('Winner is {}'.format(self.player2))
            return True

        elif self.player2.is_lose():
            print('Winner is {}'.format(self.player1))
            return True

        else:
            return False

    def show_players_status(self):
        print("{}| HP: {} GP: {}".format(self.player1,
                                         self.player1.hp,
                                         self.player1.gp))
        print("{}| HP: {} GP: {}".format(self.player2,
                                         self.player2.hp,
                                         self.player2.gp))


def play(master):
    master.show_players_status()
    master.show_field()
    print()

    while not master.game_end():
        master.update()
        print()
        master.show_players_status()
        master.show_field()


if __name__ == '__main__':
    hp = 30
    gp_recovery_rate = 6
    field_length = 15

    print('Stage1\n')

    player = Player(hp, gp_recovery_rate, "Player")
    cpu = RandomCPU(hp, gp_recovery_rate, "CPU")
    master = GameMaster(player, cpu, field_length, threthold=3)
    play(master)

    print('\nStage2\n')
    cpu2 = DicCPU(hp, int(gp_recovery_rate * 1.3), "CPU2")
    master2 = GameMaster(player, cpu2, field_length, threthold=3)
    play(master2)

    print('\nStage3\n')
    cpu3 = DicCPU(hp, int(gp_recovery_rate * 1.5), "CPU3")
    master3 = GameMaster(player, cpu3, field_length, threthold=3)
    play(master3)

    print('Clear!')
