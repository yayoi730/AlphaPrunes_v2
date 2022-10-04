import math
import os
from os.path import exists
import time

import numpy as np
import random
import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Pnum = 4
Enum = 4
# Point Weights
win_game = 100
win_seq_board = 60
win_center = 40
win_corner = 35
win_board = 30
two_in_row = 10
corner = 5
middle = 3
other_p = 0
free_choice = -5


def main():
    startFlag = True
    while not exists("end_game"):
        time.sleep(1)
        while not exists("enemy.go"):
            pass
        time.sleep(0.1)
        if startFlag:
            last_move = readMoves('first_four_moves')
            global Pnum
            global Enum
            if last_move[0] == "enemy":
                Pnum = 2
                Enum = 1
                last_move = readMoves('first_four_moves')
            else:
                Pnum = 1
                Enum = 2
                last_move = readMoves('first_four_moves')

            if os.path.getsize("move_file") != 0:
                last_move = readMoves("move_file")
        else:
            last_move = readMoves('move_file')
        next_move = findNextMove(last_move)
        addMove(next_move, last_move)
        startFlag = False


def readMoves(file):
    # reads in txt file and populates the board with the move information
    # returns the last move made in a list ex: ['X'. '1' '2']
    f = open(file)
    lines = f.readlines()
    for line in lines:
        last_move = line.split()
        # populates matrices
        moves = line.split()
        if moves[0] == 'enemy':
            board[int(moves[1])][int(moves[2])] = Pnum
            checkBoardComplete(int(moves[1]))
        else:
            board[int(moves[1])][int(moves[2])] = Enum
            checkBoardComplete(int(moves[1]))
    f.close()
    return last_move


def findNextMove(last_move):
    # function that determines the next move the player will make
    last_move = int(last_move[2])
    availableList = []
    availableBoards = []
    for i in range(0, 9):
        if complete_boards[i] == 0:
            availableBoards.append(i)
    if complete_boards[last_move] != 0:
        last_move = random.choice(availableBoards)
        print("Changed To: " + str(last_move))
    for i in range(0, 9):
        #    if board[last_move][i] == Enum or board[last_move][i] == Pnum:
        #    takenList.append(board[last_move][i])
        if board[last_move][i] == 0:
            availableList.append(i)
    #move = [last_move, random.choice([i for i in range(0, 8) if i not in takenList])]
    move = [last_move, random.choice(availableList)]
    print("Last Move: " + str(last_move))
    print("Chosen Move: " + str(move))
    return move

def checkBoardComplete(g_board):
    # checks 3 in a row
    a = board[g_board][:]
    if np.array_equal(board[g_board][0:3], [1., 1., 1]):
        print("row 1")
        complete_boards[g_board] = 1
    elif np.array_equal(board[g_board][3:6], [1, 1, 1]):
        print("row 2")
        complete_boards[g_board] = 1
    elif np.array_equal(board[g_board][6:9], [1, 1, 1]):
        print("row 3")
        complete_boards[g_board] = 1
    elif np.array_equal([board[g_board][0], board[g_board][3], board[g_board][6]], [1, 1, 1]):
        print("column 1")
        complete_boards[g_board] = 1
    elif np.array_equal([board[g_board][1], board[g_board][4], board[g_board][7]], [1, 1, 1]):
        print('column 2')
        complete_boards[g_board] = 1
    elif np.array_equal([board[g_board][2], board[g_board][5], board[g_board][8]], [1, 1, 1]):
        print('column 3')
        complete_boards[g_board] = 1
    elif np.array_equal([board[g_board][0], board[g_board][4], board[g_board][8]], [1, 1, 1]):
        print('diagonal 1')
        complete_boards[g_board] = 1
    elif np.array_equal([board[g_board][2], board[g_board][4], board[g_board][6]], [1, 1, 1]):
        print('diagonal 2')
        complete_boards[g_board] = 1
    elif np.array_equal(board[g_board][0:3], [2, 2, 2]):
        print("row 1")
        complete_boards[g_board] = 2
    elif np.array_equal(board[g_board][3:6], [2, 2, 2]):
        print("row 2")
        complete_boards[g_board] = 2
    elif np.array_equal(board[g_board][6:9], [2, 2, 2]):
        print("row 3")
        complete_boards[g_board] = 2
    elif np.array_equal([board[g_board][0], board[g_board][3], board[g_board][6]], [2, 2, 2]):
        print("column 1")
        complete_boards[g_board] = 2
    elif np.array_equal([board[g_board][1], board[g_board][4], board[g_board][7]], [2, 2, 2]):
        print('column 2')
        complete_boards[g_board] = 2
    elif np.array_equal([board[g_board][2], board[g_board][5], board[g_board][8]], [2, 2, 2]):
        print('column 3')
        complete_boards[g_board] = 2
    elif np.array_equal([board[g_board][0], board[g_board][4], board[g_board][8]], [2, 2, 2]):
        print('diagonal 1')
        complete_boards[g_board] = 2
    elif np.array_equal([board[g_board][2], board[g_board][4], board[g_board][6]], [2, 2, 2]):
        print('diagonal 2')
        complete_boards[g_board] = 2
    elif all(a):
        # returns true if and only if every value isn't zero in the array
        complete_boards[g_board] = 3
        print('tied')


def addMove(next_move, last_move):
    # function that takes in the next move (int) and adds it to move_file
    board[int(next_move[0])][int(next_move[1])] = Pnum
    checkBoardComplete(next_move[0])
    f = open("move_file", "r+")
    f.truncate(0)
    f.write("enemy " + str(next_move[0]) + " " + str(next_move[1]))
    f.close()
    print("moved made: enemy " + str(next_move[0]) + " " + str(next_move[1]))
    points = points_won(board)
    print("Points Won: " + str(points))
    display()

def points_won(g_board):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param g_board: global board
    :return: points_sum: total points won by the Pnum (Player)
    """
    point_sum = 0
    # sum points of won boards

    # determine which boards are won and sum points

    # determine sequential boards won
    incomplete_boards = []
    # search and sum points of incomplete boards
    for i in range(0, 9):  # change to incomplete boards
        arr = g_board[i][:]  # retrieves a board
        a = np.reshape(arr, (3, 3))  # shapes it into 3x3 matrix
        # check for 2 in a rows
        # via rows:
        if (a[0] == Pnum).sum() == 2 and (a[0] == Enum).sum() == 0:
            point_sum += two_in_row
        if (a[1] == Pnum).sum() == 2 and (a[1] == Enum).sum() == 0:
            point_sum += two_in_row
        if (a[2] == Pnum).sum() == 2 and (a[2] == Enum).sum() == 0:
            point_sum += two_in_row
        # via columns:
        if (a[:, 0] == Pnum).sum() == 2 and (a[:, 0] == Enum).sum() == 0:
            point_sum += two_in_row
        if (a[:, 1] == Pnum).sum() == 2 and (a[:, 1] == Enum).sum() == 0:
            point_sum += two_in_row
        if (a[:, 2] == Pnum).sum() == 2 and (a[:, 2] == Enum).sum() == 0:
            point_sum += two_in_row
        # via diagonals:
        if (a.diagonal() == Pnum).sum() == 2 and (a.diagonal() == Enum).sum() == 0:
            point_sum += two_in_row
        if (np.fliplr(a).diagonal() == Pnum).sum() == 2 and (np.fliplr(a).diagonal() == Enum).sum() == 0:
            point_sum += two_in_row
        # points from middle

        # points from corner
    return point_sum


def display():
    # function that can be called to display the current state of the board
    # arranged in ultimate tic-tac-toe style (X = 1 and O = 2)
    print("Current Board:")
    print(str(board[0][0:3]) + " | " + str(board[1][0:3]) + " | " + str(board[2][0:3]))
    print(str(board[0][3:6]) + " | " + str(board[1][3:6]) + " | " + str(board[2][3:6]))
    print(str(board[0][6:9]) + " | " + str(board[1][6:9]) + " | " + str(board[2][6:9]))
    print("------------------------------------")
    print(str(board[3][0:3]) + " | " + str(board[4][0:3]) + " | " + str(board[5][0:3]))
    print(str(board[3][3:6]) + " | " + str(board[4][3:6]) + " | " + str(board[5][3:6]))
    print(str(board[3][6:9]) + " | " + str(board[4][6:9]) + " | " + str(board[5][6:9]))
    print("------------------------------------")
    print(str(board[6][0:3]) + " | " + str(board[7][0:3]) + " | " + str(board[8][0:3]))
    print(str(board[6][3:6]) + " | " + str(board[7][3:6]) + " | " + str(board[8][3:6]))
    print(str(board[6][6:9]) + " | " + str(board[7][6:9]) + " | " + str(board[8][6:9]))


if __name__ == "__main__":
    main()
