# Question 4

import random
import tkinter as tk
from tkinter import simpledialog, messagebox


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

        message = "Rolled: " + str(results) + "\n"

        if not self.ship and 6 in results:
            self.ship = True
            results.remove(6)
            message += "Ship found!\n"

        if self.ship and not self.captain and 5 in results:
            self.captain = True
            results.remove(5)
            message += "Captain found!\n"

        if self.captain and not self.crew and 4 in results:
            self.crew = True
            results.remove(4)
            message += "Crew found!\n"

        self.dice = [Die() for i in range(len(results))]

        if self.crew:
            self.cargo = results
            message += "Cargo score: " + str(self.get_score())

        return message

    def get_score(self):
        if self.ship and self.captain and self.crew:
            return sum(self.cargo)
        return 0


# Text interface class
class TextInterface:
    def get_input(self, prompt):
        return input(prompt)

    def show_message(self, message):
        print(message)

    def wait_for_turn(self):
        input("Press Enter to roll the dice...")

    def ask_roll_again(self):
        choice = input("Roll again? (y/n): ").lower()
        return choice != "n"

    def close(self):
        pass


# Graphical interface class
class GraphicalInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ship, Captain, and Crew")
        self.root.geometry("500x450")

        self.message = tk.StringVar()
        self.ready = tk.BooleanVar(value=False)

        self.label = tk.Label(
            self.root,
            textvariable=self.message,
            font=("Arial", 12),
            justify="left",
            wraplength=450
        )
        self.label.pack(pady=20)

        self.button = tk.Button(
            self.root,
            text="Roll Dice",
            font=("Arial", 14),
            command=self.roll_clicked
        )
        self.button.pack(pady=10)
        self.button.config(state="disabled")

    def get_input(self, prompt):
        return simpledialog.askstring(
            "Ship, Captain, and Crew",
            prompt,
            parent=self.root
        )

    def show_message(self, message):
        self.message.set(message)
        self.root.update_idletasks()

    def roll_clicked(self):
        self.ready.set(True)

    def wait_for_turn(self):
        self.ready.set(False)
        self.button.config(state="normal")
        self.root.wait_variable(self.ready)
        self.button.config(state="disabled")

    def ask_roll_again(self):
        return messagebox.askyesno(
            "Roll Again?",
            "Would you like to reroll your cargo dice?",
            parent=self.root
        )

    def close(self):
        messagebox.showinfo(
            "Game Over",
            "Thanks for playing!",
            parent=self.root
        )
        self.root.destroy()


# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self, interface):
        dice = DiceCollection()

        interface.show_message(self.name + "'s turn")

        for roll in range(3):
            interface.wait_for_turn()

            message = "\nRoll " + str(roll + 1) + "\n"
            message += dice.roll_dice()

            interface.show_message(message)

            if dice.crew and roll < 2:
                if not interface.ask_roll_again():
                    break

        self.score = dice.get_score()

        interface.show_message(
            self.name + " scored: " + str(self.score)
        )


# Game class
class Game:
    def __init__(self, num_players, interface):
        self.interface = interface
        self.players = []

        for i in range(num_players):
            name = self.interface.get_input(
                "Enter player " + str(i + 1) + " name: "
            )
            self.players.append(Player(name))

    def play(self):
        remaining_players = self.players

        while True:
            for player in remaining_players:
                player.take_turn(self.interface)

            highest_score = 0

            for player in remaining_players:
                if player.score > highest_score:
                    highest_score = player.score

            winners = []

            for player in remaining_players:
                if player.score == highest_score:
                    winners.append(player)

            message = "\nRound Scores:\n"

            for player in remaining_players:
                message += (
                    player.name + ": "
                    + str(player.score) + "\n"
                )

            self.interface.show_message(message)

            if len(winners) == 1:
                self.interface.show_message(
                    message + "\nWinner: " + winners[0].name
                )
                break

            else:
                message += "\nThere is a tie!\n"
                message += "Tied players play again:\n"

                for player in winners:
                    message += player.name + "\n"

                self.interface.show_message(message)
                remaining_players = winners

        self.interface.close()


# Main function
def main():
    choice = input(
        "Enter T for text or G for graphical: "
    ).upper()

    if choice == "G":
        interface = GraphicalInterface()
    else:
        interface = TextInterface()

    num_players = int(
        interface.get_input(
            "Enter number of players (2 or more): "
        )
    )

    while num_players < 2:
        interface.show_message(
            "You must have at least 2 players."
        )
        num_players = int(
            interface.get_input(
                "Enter number of players: "
            )
        )

    game = Game(num_players, interface)
    game.play()


main()