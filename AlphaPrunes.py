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
        while not exists("AlphaPrunes.go"):
            pass
        time.sleep(1)
        if startFlag:
            last_move = readMoves('first_four_moves')
            print("This is last moves " + last_move[0])
            global Pnum
            global Enum
            if last_move[0] == "AlphaPrunes":
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
        if line.isspace():
            break
        else:
            # populates matrices
            moves = line.split()
            if moves[0] == 'AlphaPrunes':
                board[int(moves[1])][int(moves[2])] = Pnum
                checkBoardComplete(int(moves[1]),complete_boards,board)
            else:
                board[int(moves[1])][int(moves[2])] = Enum
                checkBoardComplete(int(moves[1]),complete_boards,board)
    f.close()
    return last_move


def findNextMove(last_move):
    # function that determines the next move the player will make
    last_move = int(last_move[2])
    abNextMove(last_move)
    availableList = []
    availableBoards = []
    for i in range(0, 9):
        if complete_boards[i] == 0:
            availableBoards.append(i)
    if complete_boards[last_move] != 0:
        last_move = random.choice(availableBoards)
        print("Changed To: " + str(last_move))
    for i in range(0, 9):
        # if board[last_move][i] == Pnum or board[last_move][i] == Enum:
        # takenList.append(board[last_move][i])
        #    takenList.append(i)
        if board[last_move][i] == 0:
            availableList.append(i)
    # move = [last_move, random.choice([i for i in range(0, 8) if i not in takenList])]
    move = [last_move, random.choice(availableList)]
    print("Last Move: " + str(last_move))
    print("Chosen Move: " + str(move))
    return move
def minimax(moves_list, updated_board, temp_list, depth, alpha, beta, ally):
    # miniMax function with Alpha-Beta Pruning implemented
    if depth == 0:
        won = points_won(updated_board)
        print(str(won))
        return won  # checks the number of points won
    if ally:
        max_eval = -math.inf
        for possible_move in moves_list:
            temp_list = np.copy(temp_list, 'K')
            updated_board = updateBoard(possible_move, updated_board, temp_list, Pnum)
            eval = minimax(nextMoves(possible_move[1]), updated_board, temp_list, depth - 1, alpha, beta, not ally)
            max_eval = max(max_eval, eval)
            """
            alpha = max(alpha, eval)
            if beta <= alpha
                break
            """
        return max_eval
    else:
        min_eval = math.inf
        for possible_move in moves_list:
            temp_list = np.copy(temp_list, 'K')
            updated_board = updateBoard(possible_move, updated_board, temp_list, Enum)
            eval = minimax(nextMoves(possible_move[1]), updated_board, temp_list, depth - 1, alpha, beta, ally)
            min_eval = min(min_eval, eval)
            """
            beta = min(beta, eval)
            if beta <= alpha
            break
            """
        return min_eval


def abNextMove(last_move):
    moves_list = nextMoves(last_move)
    print("Moves List: ")
    print(moves_list)
    move_num = minimax(moves_list, board, complete_boards, 2, -1000000, 1000000, True)
    return move_num

def nextMoves(last_move):
    free_moves = []
    if complete_boards[last_move] != 0:  #check if last move was to a complete board
        for i in range(0, 9):  #generates a list of free spaces for all uncomplete boards
            if complete_boards[i] == 0:
                for j in range(0, 9):
                    if board[last_move][i] == 0:
                        free_moves.append([i, j])
    else:
        for i in range(0, 9):
            if board[last_move][i] == 0:
                free_moves.append([last_move, i])
    return free_moves
def updateBoard(tempMove, tempBoard, tempList, num):
    copy_board = np.copy(tempBoard, 'K')
    print("copy_board: ")
    print(str(copy_board))
    print(str(tempMove))
    copy_board[tempMove[0]][tempMove[1]] = num
    checkBoardComplete(tempMove[1], tempList, copy_board)
    return copy_board

def checkBoardComplete(g_board, c_boards, a_board):
   """
   Checks whether a board has been complete after a move and updates the global complete_boards list
   :param g_board: takes in a index that corresponds to a 3x3 cell
   :return: list of complete boards where 0 = incomplete, Pnum = complete
   """
   arr = a_board[g_board][:]
   a = np.reshape(arr, (3, 3))  # shapes it into 3x3 matrix
   # check rows
   if (a[0] == Pnum).sum() == 3 or (a[0] == Enum).sum() == 3:
       if Pnum in a[0]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   elif (a[1] == Pnum).sum() == 3 or (a[1] == Enum).sum() == 3:
       if Pnum in a[1]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   elif (a[2] == Pnum).sum() == 3 or (a[2] == Enum).sum() == 3:
       if Pnum in a[2]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   # check columns
   elif (a[:, 0] == Pnum).sum() == 3 or (a[:, 0] == Enum).sum() == 3:
       if Pnum in a[:, 0]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   elif (a[:, 1] == Pnum).sum() == 3 or (a[:, 1] == Enum).sum() == 3:
       if Pnum in a[:, 1]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   elif (a[:, 2] == Pnum).sum() == 3 or (a[:, 2] == Enum).sum() == 3:
       if Pnum in a[:, 2]:
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum
   # check diagonal
   elif (a.diagonal() == Pnum).sum() == 3 or (a.diagonal() == Enum).sum() == 3:
       if Pnum in a.diagonal():
           c_boards[g_board] = Pnum
       else:
           c_boards[g_board] = Enum



def addMove(next_move, last_move):
    # function that takes in the next move (int) and adds it to move_file
    board[int(next_move[0])][int(next_move[1])] = Pnum
    checkBoardComplete(next_move[0], complete_boards, board)
    f = open("move_file", "r+")
    f.truncate(0)
    f.write("AlphaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    f.close()
    print("moved made: AlphaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
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
