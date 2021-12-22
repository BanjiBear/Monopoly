# Monopoly
# COMP3211 Group Project
""" Member list:
        19084858d CHEN Yi pu
        19089769D Azamat Nurpeissov
        19087011d XIE Yangxiaolong
        19085726d Rakshit Jain
"""

import random
import sys
import os
import time
import pickle

# Global Variables
playerN = 0
playerName = ['', '', '', '', '', '']
playerOrder = ['', '', '', '', '', '']
current_Player = ''
playerPosition = [1, 1, 1, 1, 1, 1]
Round = 1
res = 0
doubles = False
mes = ""
option = 0
Money = [0, 0, 0, 0, 0, 0]
inJail = ["False", "False", "False", "False", "False", "False"]
squares = ["GO", "", "", "Income tax", "", "Jail", "", "", "Chance", "", "Free Parking", "",
           "Chance", "", "", "Go to Jail", "", "", "Chance", ""]
properties_possession = [[], [], [], [], [], []] # with playerOrder
jailCnt = [0, 0, 0, 0, 0, 0]                     # with playerOrder
price = [0, 800, 700, 0, 600, 0, 400, 500, 0, 400, 0, 700, 0, 400, 500, 0, 400, 400, 0, 600]
rent = [0, 90, 65, 0, 60, 0, 10, 40, 0, 15, 0, 75, 0, 20, 25, 0, 10, 25, 0, 25]



def clear():
    os.system("clear")
    for i in range(15):
        print("")

def loading():
    animation = ["[=               ]", "[==              ]", "[===             ]", "[====            ]", "[=====           ]", "[======          ]", "[=======         ]",
                "[========        ]", "[=========       ]", "[==========      ]", "[==========      ]", "[===========     ]", "[============    ]", "[=============   ]",
                "[==============  ]", "[=============== ]", "[================]",
                "[ ===============]", "[  ==============]", "[   =============]", "[    ============]", "[     ===========]", "[      ==========]", "[       =========]",
                "[        ========]", "[         =======]", "[          ======]", "[           =====]", "[            ====]"]
    notcomplete = True
    i = 0
    while notcomplete:
        print(animation[i % len(animation)], end = '\r')
        time.sleep(0.1)
        i = i + 3
        if i == 3 * 10:
            break

# Code Components:

def main():
    os.system("python3 animation.py")
    return welcome()

def welcome():
    os.system("clear")

    for i in range(15):
        print("")
    print("Hello! Dear players~\r")
    gameLoadCheck = input("Please type in \'y\' or \'Y\' if you want to load a saved game\nOr random key to continue: ")
    if(gameLoadCheck == 'Y' or gameLoadCheck == 'y'):
        return LoadGame()
    else:
        clear()
        loading()
        while True:
            playerNumCheck = input("Please type in the number of players: ")
            if(playerNumCheck <= '6' and playerNumCheck >= '2'):
                playerNumCheck = int(playerNumCheck)
                clear()
                break
            else:
                clear()
                print("CAUTION: Number of players should be between 2 to 6.")
        for i in range(playerNumCheck):
            Name = input("Hi there, what is your name? ")
            playerName[i] = Name
        for i in range(playerNumCheck):
            Money[i] = 1500
    clear()

    for i in range(playerNumCheck):
        print("Player", ": ", end = "")
        print(playerName[i])
    print("Randomizing Player order....\n")
    loading()
    for i in range(playerNumCheck):  
        while True: 
            order = random.randint(1, playerNumCheck)
            if(playerOrder[order - 1] == ''):
                playerOrder[order - 1] = playerName[i]
                break
    global playerN
    playerN = playerNumCheck
    global current_Player
    current_Player = playerOrder[0]
    while True:
        print("Player Order:")
        for i in range(playerN):
            print(playerOrder[i], end = " ")
        print("")
        Proceed = int(input("Enter 1 to continue the game or 2 to save and play later: "))
        loading()
        if(Proceed == 1):
            return StartGame()
        elif(Proceed == 2):
            clear()
            return SaveGame()
            # print("Game Saved Successfully.\nSee you next time~\r\r")
        else:
            clear()
            print("CAUTION: Please type in only 1 or 2.")

def DisplayGameOver():
    global Money, playerName, playerN
    print("GAME OVER!")
    loading()
    loading()
    clear()
    indeX = Money.index(max(Money))
    winner = playerName[indeX]
    for i in range(playerN):
        if(Money[i] == max(Money)):
            if(indeX == i):
                continue
            else:
                winner = winner + " and " + playerName[i]
    print("GAME OVER!")
    print("The Winner is...")
    print(winner, "!!!!")
    print("")
    exit(0)

def StartGame():
    # Determine Player order
    global playerN, current_Player, playerName, playerOrder, playerPosition, Round, inJail, properties_possession, option, res, mes, Money, jailCnt, doubles
    
    counter = 0
    for i in playerName:
        if(i != ""):
            counter = counter + 1
    while(Round <= 100 and counter > 1): 
        for i in range(playerN):
            counter = 0
            for p in playerName:
                if(p != ""):
                    counter = counter + 1
            if(counter <= 1 or Round > 100):
                DisplayGameOver()
            if(current_Player == ""):
                current_Player = playerOrder[i + 1]
                continue
            os.system("clear")
            mes = ""
            option = 0
            doubles = False
            # Handle in jail and retire
            print("Current player:", current_Player)
            if(inJail[playerName.index(current_Player)] == "True"):
                if(jailCnt[playerOrder.index(current_Player)] == 3):
                    while True:
                        r = input("You must roll the dice! Enter 1: ")
                        if(r == "1"):
                            break
                    res = diceRoll()
                    time.sleep(1)
                    if(doubles == True):
                        inJail[playerName.index(current_Player)] = False
                        jailCnt[playerOrder.index(current_Player)] = 0
                        mes = current_Player + " is now FREE!"
                        MovePlayer()
                        EventHandler()
                        DisplayGameScreen()
                    else:
                        Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] - 150
                        inJail[playerName.index(current_Player)] = False
                        jailCnt[playerOrder.index(current_Player)] = 0
                        mes = current_Player + " pays $150 to get free..."
                        MovePlayer()
                        EventHandler()
                        DisplayGameScreen()
                else:
                    while True:
                        r = input("Enter 0 to pay the fine, 1 to roll a dice or 2 to save game: ")
                        if(r == "0"):
                            Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] - 150
                            mes = current_Player + " pays 150 to get out and roll a dice"
                            DisplayGameScreen()
                            time.sleep(5)
                            res = diceRoll()
                            time.sleep(1)
                            inJail[playerName.index(current_Player)] = False
                            jailCnt[playerOrder.index(current_Player)] = 0
                            MovePlayer()
                            EventHandler()
                            DisplayGameScreen()
                            break
                        elif(r == "1"):
                            res = diceRoll()
                            time.sleep(1)
                            if(doubles == True):
                                inJail[playerName.index(current_Player)] = False
                                jailCnt[playerOrder.index(current_Player)] = 0
                                MovePlayer()
                                EventHandler()
                                DisplayGameScreen()
                            else:
                                jailCnt[playerOrder.index(current_Player)] = jailCnt[playerOrder.index(current_Player)] + 1
                                mes = current_Player + " stays in prison!"
                                DisplayGameScreen()
                            break
                        elif(r == "2"):
                            return SaveGame()
            else:
                while True:
                    r = input("Enter 1 to roll a dice or 2 to save game: ")
                    if(r == "1"):
                        res = diceRoll()
                        time.sleep(1)
                        break
                    elif(r == "2"):
                        return SaveGame()
                MovePlayer()
                EventHandler()
                DisplayGameScreen()
            while True:
                Proceed = input("")
                if(option == 1 and Proceed == "1"):
                    if(Money[playerName.index(current_Player)] < 0):
                        retire()
                    break
                elif(option == 1 and Proceed == "2"):
                    properties_possession[playerOrder.index(current_Player)].append(playerPosition[playerName.index(current_Player)])
                    squares[playerPosition[playerName.index(current_Player)] - 1] = current_Player
                    Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] - price[playerPosition[playerName.index(current_Player)] - 1]
                    mes = "Successful transaction >>> LOADING...."
                    DisplayGameScreen()
                    time.sleep(5)
                    if(Money[playerName.index(current_Player)] < 0):
                        retire()
                    break
                elif(Proceed == "1"):
                    if(Money[playerName.index(current_Player)] < 0):
                        retire()
                    break
            if(i == playerN - 1):
                    current_Player = playerOrder[0]
            else:
                current_Player = playerOrder[i + 1]
            if(i == playerN - 1):
                Round = Round + 1
    if(counter <= 1 or Round > 100):
        DisplayGameOver()
    return

def MovePlayer():
    global current_Player, res, playerPosition, playerName, Money, Round
    i = playerName.index(current_Player)
    playerPosition[i] = playerPosition[i] + res
    if(playerPosition[i] > 20):
        playerPosition[i] = playerPosition[i] - 20
        Money[i] = Money[i] + 1500
    # print(playerPosition)
    return

def EventHandler():
    global playerN, current_Player, playerName, playerOrder, playerPosition, Money, Round, inJail, properties_possession, mes, option
    POS = playerPosition[playerName.index(current_Player)]
    # Income Tax
    if(POS == 4):
        c = Money[playerName.index(current_Player)] // 10 // 10 * 10
        #c = int(Money[playerName.index(current_Player)] * 0.1)
        Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] - c
        mes = "TAX: " + current_Player + " pays " + str(c) + " dollars..."
        return
    # Chance
    elif(POS == 9 or POS == 13 or POS == 19):
        c = chance()
        if(c > 0):
            mes = "CHANCE: " + current_Player + " earns " + str(abs(c)) + " dollars!"
        elif(c < 0):
            mes = "CHANCE: " + current_Player + " loses " + str(abs(c)) + " dollars..."
        elif(c == 0):
            mes = "CHANCE: " + current_Player + " gets" + " nothing..."
        Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] + c
        return
    # Go to Jail
    elif(POS == 16):
        playerPosition[playerName.index(current_Player)] = 6
        mes = "YOU'RE UNDER ARREST FOR BEING A FREE RIDER"
        inJail[playerName.index(current_Player)] = "True"
        return

    # Check for Properties
    elif(POS != 1 and POS != 6 and POS != 11):
        global option
        for i in range(len(properties_possession)):
            if(playerPosition[playerName.index(current_Player)] in properties_possession[i]):
                if(i == playerOrder.index(current_Player)):
                    option = 0
                    return
                # Money deduction
                Money[playerName.index(current_Player)] = Money[playerName.index(current_Player)] - rent[POS - 1]
                # Money Addition
                Money[playerName.index(squares[POS - 1])] = Money[playerName.index(squares[POS - 1])] + rent[POS - 1]
                mes = current_Player + " pays " + str(rent[playerPosition[playerName.index(current_Player)] - 1]) + " dollars to " + squares[POS - 1]
                option = 2
                return
        option = 1
    return

def SaveGame():
    global playerN, current_Player, playerName, playerOrder, playerPosition, Money, Round, inJail, properties_possession, jailCnt, res, mes, option, squares, price, rent

    with open('SavedGameSettings.txt', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([playerN, playerName, playerOrder, current_Player, playerPosition, Round, res, jailCnt,
                     mes,option, Money, inJail, squares, properties_possession, price, rent], f)

    loading()
    print("Game Saved Successfully.\nSee you next time~\r\r")
    return

def LoadGame():
    global playerN, current_Player, playerName, playerOrder, playerPosition, Money, Round, inJail, properties_possession, jailCnt, res, mes, option, squares,price, rent
    if(os.path.isfile('./SavedGameSettings.txt') == False):
        print("ERROR: No file found!!")
        print("LOADING...")
        time.sleep(3)
        return welcome()
    with open('SavedGameSettings.txt', 'rb') as f:
        playerN, playerName, playerOrder, current_Player, playerPosition, Round, res, jailCnt, mes, option, Money, inJail, squares, properties_possession, price, rent = pickle.load(f)

    print("Load Successful!")
    time.sleep(3)
    return StartGame()
 
def diceRoll():
    cubes = [
    """
       * * * * *      * * * * *
       *       *      *       *
       *   X   *      *   X   *
       *       *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      *       *
       *   X   *      * X   X *
       *       *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      *     X *
       *   X   *      *   X   *
       *       *      * X     *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      * X   X *
       *   X   *      *       *
       *       *      * X   X *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      *       *
       * X   X *      *   X   *
       *       *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      *       *
       * X   X *      * X   X *
       *       *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      *     X *
       * X   X *      *   X   *
       *       *      * X     *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *       *      * X   X *
       * X   X *      *       *
       *       *      * X   X *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *     X *      *       *
       *   X   *      *   X   *
       * X     *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *     X *      *       *
       *   X   *      * X   X *
       * X     *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *     X *      *     X *
       *   X   *      *   X   *
       * X     *      * X     *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       *     X *      * X   X *
       *   X   *      *       *
       * X     *      * X   X *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       * X   X *      *       *
       *       *      *   X   *
       * X   X *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       * X   X *      *       *
       *       *      * X   X *
       * X   X *      *       *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       * X   X *      *     X *
       *       *      *   X   *
       * X   X *      * X     *
       * * * * *      * * * * *
    """,
    """
       * * * * *      * * * * *
       * X   X *      * X   X *
       *       *      *       *
       * X   X *      * X   X *
       * * * * *      * * * * *
    """
    ]
    running = True
    t = 0
    global doubles
    orig_cube = cubes[:]
    os.system('cls' if os.name == 'nt' else 'clear')
    while running:
       t += 0.01
       os.system('cls' if os.name == 'nt' else 'clear')
       random.shuffle(cubes)
       print(cubes[0])
       if(orig_cube.index(cubes[0]) == 0):
          res  = 2
       elif(orig_cube.index(cubes[0]) == 1):
          res  = 3
       elif(orig_cube.index(cubes[0]) == 2):
          res  = 4
       elif(orig_cube.index(cubes[0]) == 3):
          res  = 5
       elif(orig_cube.index(cubes[0]) == 4):
          res  = 3
       elif(orig_cube.index(cubes[0]) == 5):
          res  = 4
       elif(orig_cube.index(cubes[0]) == 6):
          res  = 5
       elif(orig_cube.index(cubes[0]) == 7):
          res  = 6
       elif(orig_cube.index(cubes[0]) == 8):
          res  = 4
       elif(orig_cube.index(cubes[0]) == 9):
          res  = 5
       elif(orig_cube.index(cubes[0]) == 10):
          res  = 6
       elif(orig_cube.index(cubes[0]) == 11):
          res  = 7
       elif(orig_cube.index(cubes[0]) == 12):
          res  = 5
       elif(orig_cube.index(cubes[0]) == 13):
          res  = 6
       elif(orig_cube.index(cubes[0]) == 14):
          res  = 7
       elif(orig_cube.index(cubes[0]) == 15):
          res  = 8
       time.sleep(t)
       if t >= 0.1:
          running = False
    if(orig_cube.index(cubes[0]) == 0 or orig_cube.index(cubes[0]) == 5 or orig_cube.index(cubes[0]) == 10 or orig_cube.index(cubes[0]) == 15):
        doubles = True
    return res

def chance():
    print("CHANCE!")
    loading()
    return random.randint(-30, 20) * 10

def retire():
    global playerN, current_Player, playerName, playerOrder, playerPosition, Money, Round, inJail, properties_possession, jailCnt, res, mes, option, squares, price, rent

    #playerN = playerN - 1
    indexx = playerName.index(current_Player)

    playerName[indexx] = ''
    properties_possession[playerOrder.index(current_Player)] = []
    for i in squares:
        if(i == current_Player):
            squares[squares.index(i)] = ''
    jailCnt[playerOrder.index(current_Player)] = 0
    playerOrder[playerOrder.index(current_Player)] = ''
    playerPosition[indexx] = 0
    Money[indexx] = 0
    inJail[indexx] = "False"

    return

def DisplayGameScreen():
    global playerN, playerName, playerOrder, playerPosition, current_Player, res, Round, Money, mes, option
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows = 100, cols = 200))
    os.system("clear")
    if(inJail[playerName.index(current_Player)] != "True"):
        print(current_Player, "moves", res, "stpes")

    for i in range(playerN, 6):
        playerPosition[i] = 0
    #print(playerPosition)

    pl1Pos = playerPosition[playerName.index(playerOrder[0])]
    pl2Pos = playerPosition[playerName.index(playerOrder[1])]
    pl3Pos = playerPosition[playerName.index(playerOrder[2])]
    pl4Pos = playerPosition[playerName.index(playerOrder[3])]
    pl5Pos = playerPosition[playerName.index(playerOrder[4])]
    pl6Pos = playerPosition[playerName.index(playerOrder[5])]
    #playerPosition[playerName.index(current_Player)]

    print("")

    print(" ", end = '')
    for i in range(60):
        print("--", end = '')
    for i in range(15):
        print(" ", end = "")
    print("PLAYER INFORMATION: ", end = "")
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[0] != ''):
        print("p1: ", playerOrder[0], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[1] != ''):
        print("p2: ", playerOrder[1], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("FREE", end = '')
    for i in range(8):
        print(" ", end ='')
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("Shatin", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Tuen Mun", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("Tai Po", end = '')
    for i in range(7):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[2] != ''):
        print("p3: ", playerOrder[2], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("PARKING", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[3] != ''):
        print("p4: ", playerOrder[3], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 11):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 11):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 11):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 12):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 12):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 12):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 13):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 13):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 13):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 14):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 14):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 14):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 15):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 15):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 15):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 16):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 16):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 16):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[4] != ''):
        print("p5: ", playerOrder[4], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 11):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 11):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 11):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 12):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 12):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 12):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 13):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 13):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 13):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 14):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 14):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 14):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 15):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 15):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 15):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 16):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 16):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 16):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[5] != ''):
        print("p6: ", playerOrder[5], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(2):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("CHANCE", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(2):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Go To Jail", end = '')
    for i in range(4):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------


    print(" ", end = '')
    for i in range(60):
        print("--", end = '')
    for i in range(15):
        print(" ", end = "")
    print("Current Player: ", current_Player, end = "")
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("Round: ", Round, end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Tsing Yi", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end ='')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Sai Kung", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("PLAYER MONEY: ", end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 10):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 10):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 10):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 17):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 17):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 17):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[0] != ''):
        print("p1 money: ", Money[playerName.index(playerOrder[0])], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 10):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 10):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 10):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 17):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 17):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 17):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[1] != ''):
        print("p2 money: ", Money[playerName.index(playerOrder[1])], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[2] != ''):
        print("p3 money: ", Money[playerName.index(playerOrder[2])], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[3] != ''):
        print("p4 money: ", Money[playerName.index(playerOrder[3])], end = "")
    print("\r")
    #---------------------------------------------------------


    print(" ", end = '')
    for i in range(10):
        print("--", end = '')
    for i in range(40):
        print("  ", end = '')
    for i in range(10):
        print("--", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[4] != ''):
        print("p5 money: ", Money[playerName.index(playerOrder[4])], end = "")
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    if(option == 1):
        print("This square does not belong to anyone!   ", end = '')
    elif(option == 2):
        print("This place is owned by other player!     ", end = '')
    else:
        print("                                         ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(20):
        print(" ", end = "")
    if(playerOrder[5] != ''):
        print("p6 money: ", Money[playerName.index(playerOrder[5])], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    if(option == 1):
        print("      Do you want to buy the square?     ", end = '')
    elif(option == 2):
        print("           Please pay the rent!          ", end = '')
    else:
        print("            Enter 1 to continue          ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    if(option == 1):
        print("  Enter 1 to skip or 2 to buy the square ", end = '')
    elif(option == 2):
        print("           Enter 1 to continue           ", end = '')
    else:
        print("                                         ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Yuen Long", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 9):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 9):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 9):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 18):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 18):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 18):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 9):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 9):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 9):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 18):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 18):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 18):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("POS  Name          PRICE   RENT     OWNED BY", end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("2    Central       800     90      ", squares[1], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("CHANCE", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("3    Wan Chai      700     65      ", squares[2], end = "")
    print("\r")
    #---------------------------------------------------------


    print(" ", end = '')
    for i in range(10):
        print("--", end = '')
    for i in range(40):
        print("  ", end = '')
    for i in range(10):
        print("--", end = '')
    for i in range(15):
        print(" ", end = "")
    print("5    Stanley       600     60      ", squares[4], end = "")
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("7    Shek O        400     10      ", squares[6], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("8    Mong Kok      500     40      ", squares[7], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("Mong Kok", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("10   Tsing Yi      400     15      ", squares[9], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 8):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 8):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 8):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 19):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 19):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 19):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("12   Shatin        700     75      ", squares[11], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 8):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 8):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 8):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 19):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 19):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 19):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("14   Tuen Mun      400     20      ", squares[13], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("15   Tai Po        500     25      ", squares[14], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("CHANCE", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("17   Sai Kung      400     10      ", squares[16], end = "")
    print("\r")
    #---------------------------------------------------------


    print(" ", end = '')
    for i in range(10):
        print("--", end = '')
    if(mes != ""):
        for i in range(19):
            print(" ", end = '')
        print("System >>>", mes, end = '')
        t = 60 - len("System >>>" + mes)
        for i in range(t):
            print(" ", end = '')
    else:
        for i in range(40):
            print("  ", end = '')
    for i in range(10):
        print("--", end = '')
    for i in range(15):
        print(" ", end = "")
    print("18   Yuen long     400     25      ", squares[17], end = "")
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(15):
        print(" ", end = "")
    print("20   Tai O         600     25      ", squares[19], end = "")
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("Shek O", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(7):
        print(" ", end ='')
    print("Tai O", end = '')
    for i in range(7):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 7):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 7):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 7):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 20):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 20):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 20):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 7):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 7):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 7):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 20):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 20):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 20):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(3):
        for i in range(19):
            print(" ", end ='')
        print(" ", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------


    print(" ", end = '')
    for i in range(60):
        print("--", end = '')
    print('\r')
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("Stanley", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    print("Wan Chai", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("Central", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 6):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 6):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 6):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 5):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 5):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 5):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 4):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 4):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 4):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 3):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 3):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 3):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 2):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 2):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 2):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl1Pos == 1):
        print("p1", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl2Pos == 1):
        print("p2", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl3Pos == 1):
        print("p3", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 6):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 6):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 6):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 5):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 5):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 5):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 4):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 4):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 4):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 3):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 3):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 3):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 2):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 2):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 2):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(5):
        print(" ", end ='')
    if(pl4Pos == 1):
        print("p4", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl5Pos == 1):
        print("p5", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    if(pl6Pos == 1):
        print("p6", end = '')
    else:
        print("  ", end = '')
    print(" ", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("IN JAIL", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    for i in range(19):
        print(" ", end ='')
    print("|", end = '')
    for i in range(4):
        print(" ", end ='')
    print("INCOME TAX", end = '')
    for i in range(5):
        print(" ", end ='')
    print("|", end = '')
    for i in range(2):
        for i in range(19):
            print(" ", end ='')
        print("|", end = '')
    for i in range(6):
        print(" ", end ='')
    print("<--- GO", end = '')
    for i in range(6):
        print(" ", end ='')
    print("|", end = '')
    print("\r")
    #---------------------------------------------------------
    print(" ", end = '')
    for i in range(60):
        print("--", end = '')
    print('\r')
    return

main()

