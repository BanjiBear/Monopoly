# Monopoly
This is a Monopoly Game made for course semester group Project. 
All rights belong to: CHEN Yi pu(Banjibear), Azamat Nurpeissov, XIE Yangxiaolong, and Rakshit Jain

The Game is Designed for Mac and Linix users written in Python. Monopoly accepts 2-6 players at a time and provides loading and storing game status. Without the need of installing pygame, the game is displayed and played through terminals

Game Objective:

Become the player with the most assets, through buying or renting properties! 
This can be seen in the Asset table! Asset of a player will be printed out with the updated information after the player makes his or her moves.

Game Conditions
Each player is given HKD $1,500 and randomly assigned a player number (p1,p2...p6)

Game Movement:
Each player rolls 2 dices and the result of that is used to calculate how far he will move on the board, clockwise.

Game Asset Management
Each time a player passes GO square, he gets 1500 HKD added to his account
Each time a player lands on an un-owned property he’s given a chance to buy it, given that one has enough money!
Each time a player lands on a non-self-owned property, he has to pay the respective rent to the owner player.
Each time a player lands on a special square, that is, CHANCE, GO TO JAIL, or INCOME TAX, there will be random addition or deduction on the amount of money or alteration on the player’s position.
All the above event will be shown by the system message, player can simply follow the instructions and options given on the board

Special Properties
Chance: Landing player gains a random amount (multiple of 10) up to HKD 200 or loses a
random amount (multiple of 10) up to HKD 300.
Income Tax: Landing Player pays 10% of their money (rounded down to a multiple of 10) as tax.
Free parking: This square has no effect.
Go to Jail: Go to Jail. If a player lands on this square, she immediately goes to the “In Jail”
square

# Installation
Pre-Requisite:
Only a few prerequisite steps to get started playing our Monopoly game!

OS Requirements:  macOS 10.4+ / Linux (Kernel 3.14+)

Software Requirements: 
Python3: Python3 comes preinstalled in both macOS and all major Linux Distributions. Confirm that python3 is installed by opening the terminal and typing python3 --version. If you see a python version, then we’re good to go! If not, click here to install: https://www.w3computing.com/python/installing-python-windows-macos-linux/

Compiling and Running:
1. Open Terminal: Simply open up the terminal on your macOS / Linux computer.
2. Locate the downloaded game folder: Assuming the game is in downloads folder, type cd Downloads/Group20Project/Monopoly
3. Now simply type python3 __init__.py
4. Game is ready!

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

# License
MIT

# To-Do
1. Improve the UI design
2. Make changes to improve the fluency of the game
