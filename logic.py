import time
from typing import Sequence


class Player():
    def __init__(self, name: str):
        self.name: str = name
        self.passed: bool = False
        self.elapsed_time: float = 0.0


class Game():
    def __init__(self, players: Sequence[Player]):
        self.players = list(players)
        self.time_since_last_action = time.time()

    def take_turn(self):
        self.players[0].elapsed_time += (time.time() - self.time_since_last_action)
        self.players.append(self.players.pop(0))
        while self.players[0].passed:
            self.players.append(self.players.pop(0))
        self.reset_timer()

    def update_turn_order(self, player_names: list[str]):
        new_order: list[Player|None] = [None for _ in range(len(player_names))]
        for p in self.players:
            if p.name in player_names:
                new_order[player_names.index(p.name)] = p
                p.passed = False
            else:
                p.passed = True
        self.reset_timer()


    def reset_timer(self):
        self.time_since_last_action = time.time()
        