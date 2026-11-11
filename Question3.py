# Question 3 

import random


# Die class
class Die:
    def roll(self):
        return random.randint(1, 6)


# Dice collection class
class DiceCollection:
    def __init__(self):
        self.dice = [Die() for i in range(5)]
        self.ship = False
        self.captain = False
        self.crew = False
        self.cargo = []

    def roll_dice(self):
        results = []

        for die in self.dice:
            results.append(die.roll())

        print("Rolled:", results)

        # Look for the ship
        if not self.ship and 6 in results:
            self.ship = True
            results.remove(6)
            print("Ship found!")

        # Look for the captain
        if self.ship and not self.captain and 5 in results:
            self.captain = True
            results.remove(5)
            print("Captain found!")

        # Look for the crew
        if self.captain and not self.crew and 4 in results:
            self.crew = True
            results.remove(4)
            print("Crew found!")

        # Keep only the dice that were not set aside
        self.dice = [Die() for i in range(len(results))]

        if self.crew:
            self.cargo = results

    def get_score(self):
        if self.ship and self.captain and self.crew:
            return sum(self.cargo)
        else:
            return 0


# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self):
        dice = DiceCollection()

        print("\n" + self.name + "'s turn")

        for roll in range(3):
            print("\nRoll", roll + 1)
            dice.roll_dice()

            if dice.crew:
                print("Current cargo score:", dice.get_score())

                if roll < 2:
                    choice = input("Roll again? (y/n): ").lower()

                    if choice == "n":
                        break

            elif roll < 2:
                input("Press Enter to roll again...")

        self.score = dice.get_score()
        print(self.name, "scored:", self.score)


# Game class
class Game:
    def __init__(self, num_players):
        self.players = []

        for i in range(num_players):
            name = input("Enter player name: ")
            self.players.append(Player(name))

    def play(self):
        remaining_players = self.players

        while True:
            for player in remaining_players:
                player.take_turn()

            highest_score = 0

            for player in remaining_players:
                if player.score > highest_score:
                    highest_score = player.score

            winners = []

            for player in remaining_players:
                if player.score == highest_score:
                    winners.append(player)

            print("\nRound Scores:")

            for player in remaining_players:
                print(player.name, ":", player.score)

            if len(winners) == 1:
                print("\nWinner:", winners[0].name)
                break

            else:
                print("\nThere is a tie!")

                for player in winners:
                    print(player.name)

                print("Tied players must play again.")

                remaining_players = winners


def main():
    num_players = int(input("Enter number of players (2 or more): "))

    while num_players < 2:
        print("You must have at least 2 players.")
        num_players = int(input("Enter number of players: "))

    game = Game(num_players)
    game.play()


main()