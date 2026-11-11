# Question 1

import random

class Die:
    def roll(self):
        sides = ["L", "C", "R", ".", ".", "."]
        return random.choice(sides)

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 3

class Pot:
    def __init__ (self):
        self.chips = 0

    def add_chip(self):
        self.chips += 1

class Game:
    def __init__(self, num_players):
        self.players = []

        for i in range(num_players):
            name = input("Enter player name: ")
            self.players.append(Player(name))

        self.die = Die()
        self.pot = Pot()

    def play(self):
        current_player = 0 

        while True:
            player = self.players[current_player]

            print("\n" + player.name + "'s turn")
            print("Chips:", player.chips)

            if player.chips > 0:
                num_rolls = min(player.chips, 3)

                for i in range(num_rolls):
                    result = self.die.roll()
                    print("Rolled:", result)

                    if result == "L":
                        player.chips -= 1
                        left = (current_player + 1) % len(self.players)
                        self.players[left].chips += 1

                    elif result == "R":
                        player.chips -= 1
                        right = (current_player - 1) % len(self.players)
                        self.players[right].chips += 1

                    elif result == "C":
                        player.chips -= 1
                        self.pot.add_chip()

            else:
                print("No chips. Skipping turn.")

            print("\nCurrent chip counts:")
            for p in self.players:
                print(p.name, ":", p.chips)

            print("Center pot:", self.pot.chips)

            active_players = 0 
            winner = None

            for p in self.players:
                if p.chips > 0:
                    active_players += 1
                    winner = p 

            if active_players == 1:
                print("\nWinner:", winner.name)
                winner.chips += self.pot.chips
                print("Final chips:", winner.chips)
                break

            current_player = (current_player + 1) % len(self.players)

def main():
    num_players = int(input("Enter number of players (3 or more): "))

    while num_players < 3:
        print("You must have at least 3 players.")
        num_players = int(input("Enter number of players: "))

    game = Game(num_players)
    game.play()

main()
