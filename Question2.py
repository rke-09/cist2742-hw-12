# Question 2 

import random
import tkinter as tk
from tkinter import simpledialog, messagebox

    
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


class TextInterface:
    def get_input(self, prompt):
        return input(prompt)
    
    def show_message(self, message):
        print(message)

    def wait_for_turn(self):
        input("\nPress Enter to roll the dice...")

    def close(self):
        pass


class GraphicalInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LCR Dice Game")
        self.root.geometry("450x450")

        self.message = tk.StringVar()
        self.ready = False

        self.label = tk.Label(
            self.root,
            textvariable=self.message,
            font = ("Arial", 12),
            justify="left",
            wraplength=400
        )
        self.label.pack(pady=20)

        self.button = tk.Button(
            self.root,
            text="Roll Dice",
            font = ("Arial", 14),
            command=self.roll_clicked
        )
        self.button.pack(pady = 10)

        self.button.config(state="disabled")


    def get_input(self, prompt):
        return simpledialog.askstring(
            "LCR Game", prompt, parent=self.root
        )

    def show_message(self, message):
        self.message.set(message)
        self.root.update()

    def roll_clicked(self):
        self.ready = True

    def wait_for_turn(self):
        self.ready = False
        self.button.config(state="normal")

        while not self.ready:
            self.root.update()

        self.button.config(state="disabled")

    def close(self):
        messagebox.showinfo(
            "Game Over", "Thanks for playing!",
            parent=self.root
        )
        self.root.destroy()
    

class Game:
    def __init__(self, num_players, interface):
        self.interface = interface
        self.players = []

        for i in range(num_players):
            name = self.interface.get_input("Enter player " + str(i + 1) + " name: ")
            self.players.append(Player(name))

        self.die = Die()
        self.pot = Pot()

    def play(self):
        current_player = 0 

        while True:
            player = self.players[current_player]

            message = (player.name + "'s turn\n" + "Chips: " + str(player.chips))

            self.interface.show_message(message)

            if player.chips > 0:
                self.interface.wait_for_turn()

                num_rolls = min(player.chips, 3)
                results = []

                for i in range(num_rolls):
                    result = self.die.roll()
                    results.append(result)

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

                message = (player.name + " rolled: " + " ".join(results) + "\n\n")

            else:
                message = (player.name + " has no chips. Turn skipped.\n\n")

            message += "Current chip counts:\n"

            for p in self.players:
                message += (p.name + ": " + str(p.chips) + "\n")

            message += ("\nCenter pot: " + str(self.pot.chips))

            self.interface.show_message(message)

            active_players = []

            for p in self.players:
                if p.chips > 0:
                    active_players.append(p)

            if len(active_players) == 1:
                winner = active_players[0]
                winner.chips += self.pot.chips
                self.pot.chips = 0

                self.interface.show_message("Winner: " + winner.name + "\nFinal chips: " + str(winner.chips))
                break

            current_player = (current_player + 1) % len(self.players)

            self.interface.wait_for_turn()

        self.interface.close()


def main():
    choice = input("Enter T for text or G for graphical: ").upper()

    if choice == "G":
        interface = GraphicalInterface()
    else:
        interface = TextInterface()

    num_players = int(interface.get_input("Enter number of players (3 or more): "))

    while num_players < 3:
        interface.show_message("You must have at least 3 players.")

        num_players = int(interface.get_input("Enter number of players: "))

    game = Game(num_players, interface)
    game.play()

main()