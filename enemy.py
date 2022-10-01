import math
import os
from os.path import exists
import time

import numpy as np
import random

import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards = []
# lol

def main():
    startFlag = True
    while not exists("end_game"):
        time.sleep(1)
        while not exists("enemy.go"):
            pass
        if startFlag:
            last_move = readMoves('first_four_moves')
            if os.path.getsize("move_file") != 0:
                last_move = readMoves("move_file")
        else:
            last_move = readMoves('move_file')
        next_move = findNextMove(last_move)
        addMove(next_move, last_move)
        startFlag = False
    os.remove("enemy.go")
    os.remove("end_game")


def readMoves(file):
    # reads in txt file and populates the board with the move information
    # returns the last move made in a list ex: ['X'. '1' '2']
    f = open(file)
    lines = f.readlines()
    for line in lines:
        last_move = line.split()
        if line.isspace():
            break
        else:
            # populates matrices
            moves = line.split()
            if moves[0] == 'enemy':
                board[int(moves[1])][int(moves[2])] = 1
            else:
                board[int(moves[1])][int(moves[2])] = 2
    f.close()
    return last_move


def findNextMove(last_move):
    # function that determines the next move the player will make
    last_move = int(last_move[2])
    takenList = []
    if last_move in complete_boards:
        last_move = random.choice([i for i in range(0, 8) if i not in complete_boards])
    for i in range(0, 8):
        if board[last_move][i] == 1 or board[last_move][i] == 2:
            takenList.append(board[last_move][i])
    move = [last_move, random.choice([i for i in range(0, 8) if i not in takenList])]
    print("Chosen Move: " + str(move))
    print("Taken List: " + str(takenList))
    return move


def checkBoardComplete(g_board):
    # checks 3 in a row
    if board[g_board][0:3] == [1, 1, 1] or [2, 2, 2]:
        print("row 1")
    elif board[g_board][3:6] == [1, 1, 1] or [2, 2, 2]:
        print("row 2")
    elif board[g_board][6:9] == [1, 1, 1] or [2, 2, 2]:
        print("row 3")
    elif board[g_board][0, 3, 6] == [1, 1, 1] or [2, 2, 2]:
        print("column 1")
        print(board[g_board][:, 1])
    elif board[g_board][:, 2] == [1, 1, 1] or [2, 2, 2]:
        print('column 2')
    elif board[g_board][:, 3] == [1, 1, 1] or [2, 2, 2]:
        print('column 3')
    # checks all filled
    # add to list of complete boards


def addMove(next_move, last_move):
    # function that takes in the next move (int) and adds it to move_file
    f = open("move_file", "r+")
    f.truncate(0)
    board[int(next_move[0])][int(next_move[1])] = 1
    f.write("enemy " + str(next_move[0]) + " " + str(next_move[1]))

    f.close()
    display()


def minimax(g_board, depth, alpha, beta, ally):
    # miniMax function with Alpha-Beta Pruning implemented
    if depth == 0:
        return pointswon(g_board)  # checks the number of points won
    if ally:
        max_eval = -math.inf
        for possible_move in g_board:
            eval = minimax(possible_move, depth - 1, alpha, beta, not ally)
            max_eval = max(max_eval, eval)
            """
            alpha = max(alpha, eval)
            if beta <= alpha
                break
            """
        return max_eval
    else:
        min_eval = math.inf
        for possible_move in g_board:
            eval = minimax(possible_move, depth - 1, alpha, beta, ally)
            min_eval = min(min_eval, eval)
            """
            beta = min(beta, eval)
            if beta <= alpha
            break
            """
        return min_eval


def pointswon(g_board):
    # static evaluation (utility) function that returns number of points won by Player

    # check
    return 1


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