import math
import os
from os.path import exists
import time

import numpy as np
import random

import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Pnum = 0
Enum = 0
# Point Weights
lose_game = -math.inf
win_game = +math.inf
win_seq_board = 60
win_center = 40
win_corner = 35
win_board = 30
two_in_row = 10
three_in_row = 30
corner = 5
middle = 3
side = 1
other_p = 0
free_choice = -5
# List of Sets of Possible Sequences for Boards
possible_two_seq = [{0, 1}, {1, 2}, {0, 2}, {0, 3}, {3, 6}, {0, 6}, {0, 4}, {0, 8}, {4, 8},
                    {1, 4}, {4, 7}, {1, 7}, {2, 5}, {5, 8}, {2, 8}, {2, 4}, {4, 6}, {2, 6}]
# List of Sets of Possible Board Win States
possible_win_states = [{0, 1, 2}, {0, 3, 6}, {0, 4, 8}, {1, 4, 7}, {3, 4, 5}, {2, 5, 8}, {2, 4, 6}, {6, 7, 8}]


def main():
    startFlag = True
    while not exists("end_game"):
        time.sleep(1)
        while not exists("AlphaPrunes.go"):
            pass
        time.sleep(1)
        if startFlag:
            last_move = readMoves('first_four_moves')
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
        addMove(next_move)
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
                checkBoardComplete(int(moves[1]), complete_boards, board)
            else:
                board[int(moves[1])][int(moves[2])] = Enum
                checkBoardComplete(int(moves[1]), complete_boards, board)
    f.close()
    return last_move
def addMove(next_move):
    # function that takes in the next move (int) and adds it to move_file
    board[int(next_move[0])][int(next_move[1])] = Pnum
    checkBoardComplete(next_move[0], complete_boards, board)
    f = open("move_file", "r+")
    f.truncate(0)
    f.write("AlphaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    f.close()
    print("Moved made: AlphaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    display()
def findNextMove(last_move):
    # function that determines the next move the player will make
    last_move = int(last_move[2])
    moves_list = nextMoves(last_move)
    move = minimax_starter(moves_list, board, complete_boards)
    #move = [last_move, random.choice(availableList)]
    print("Last Move: " + str(last_move))
    return move

def minimax_starter(moves_list, updated_board, temp_list): #takes list of potential moves, the board, and list of complete boards
    final_move = [] #move that AI will choose
    top_score = -100000 #set negative so AI will pick a move
    c_updated_board = updated_board

    for i in range(0, len(moves_list)): #every potential move
        updated_board = updateBoard(moves_list[i], updated_board, temp_list, Pnum) #gets board with next move on it and updates temp list
        score = minimax(moves_list, updated_board, temp_list, 20, 10000, -10000, False)
        if (score > top_score):
            top_score = score
            final_move = moves_list[i]
        updated_board = c_updated_board
    return final_move

def minimax(moves_list, updated_board, temp_list, depth, alpha, beta, ally):
    # miniMax function with Alpha-Beta Pruning implemented
    if depth == 0:
        won = points_won(updated_board)
        return won  # checks the number of points won
    if ally:
        max_eval = -math.inf
        for possible_move in moves_list:
            temp_list = np.copy(temp_list, 'K')
            updated_board = updateBoard(possible_move, updated_board, temp_list, Pnum)
            eval = minimax(nextMoves(possible_move[1]), updated_board, temp_list, depth - 1, alpha, beta, not ally)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for possible_move in moves_list:
            temp_list = np.copy(temp_list, 'K')
            updated_board = updateBoard(possible_move, updated_board, temp_list, Enum)
            eval = minimax(nextMoves(possible_move[1]), updated_board, temp_list, depth - 1, alpha, beta, ally)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def nextMoves(last_move):
    free_moves = []
    if complete_boards[last_move] != 0:  # check if last move was to a complete board
        for i in range(0, 9):  # generates a list of free spaces for all uncomplete boards
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
    copy_board[tempMove[0]][tempMove[1]] = num
    checkBoardComplete(tempMove[1], tempList, copy_board)
    return copy_board

def points_won(temp_board):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param temp_board: tempo
    :return: points_sum: total points won by the Pnum (Player)
    """

    point_sum = 0
    # create initial list of incomplete boards
    incomplete_boards = [x for x, n in enumerate(complete_boards) if n == 0]
    c_boards = complete_boards  # c_board: list of all complete boards
    # update number of complete boards based on temp_board config.
        # print("c_boards: " + str(c_boards))
    for g_board in incomplete_boards:
        """
        For every board in incomplete_boards, check if that board has been completed in the temp_board,
        return updated list of completed boards which is set to c_boards
        """
        c_boards = checkBoardComplete2(g_board, c_boards, temp_board).copy()  # set board to updated list
    # update incomplete_boards
    incomplete_boards = [x for x, n in enumerate(c_boards) if n == 0]
    # sum points for # of boards one, and check for seq. boards
    board_points = won_board_points(c_boards)
    point_sum += board_points
    # search and sum points for two_in_row
    twr_points = two_in_rows(incomplete_boards, temp_board)
    point_sum += twr_points
    # evaluates individual spots on a board
    point_sum += corner_center_side_eval_func(temp_board, incomplete_boards)
    return point_sum
def two_in_rows(incomplete_boards, temp_board):
    """
    Determines the number of two in a rows Pnum (Player) has made and totals points
    :param incomplete_boards (list of incomplete boards), temp_board: temporary global board config.
    :return: points_sum: total points won by the Pnum (Player)
    """
    point_sum = 0
    for i in incomplete_boards:  # change to incomplete boards
        arr = temp_board[i][:]   # retrieves a board
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
        #enemy
        if (a[0] == Enum).sum() == 2 and (a[0] == Pnum).sum() == 0:
            point_sum += -two_in_row
        if (a[1] == Enum).sum() == 2 and (a[1] == Pnum).sum() == 0:
            point_sum += -two_in_row
        if (a[2] == Enum).sum() == 2 and (a[2] == Pnum).sum() == 0:
            point_sum += -two_in_row
        # via columns:
        if (a[:, 0] == Enum).sum() == 2 and (a[:, 0] == Pnum).sum() == 0:
            point_sum += -two_in_row
        if (a[:, 1] == Enum).sum() == 2 and (a[:, 1] == Pnum).sum() == 0:
            point_sum += -two_in_row
        if (a[:, 2] == Enum).sum() == 2 and (a[:, 2] == Pnum).sum() == 0:
            point_sum += -two_in_row
        # via diagonals:
        if (a.diagonal() == Enum).sum() == 2 and (a.diagonal() == Pnum).sum() == 0:
            point_sum += -two_in_row
        if (np.fliplr(a).diagonal() == Enum).sum() == 2 and (np.fliplr(a).diagonal() == Pnum).sum() == 0:
            point_sum += -two_in_row
    return point_sum
def checkBoardComplete(g_board, c_boards, a_board):
    """
    Checks whether a board has been complete after a move and updates the global complete_boards list
    :param g_board, c_boards (list of complete boards), a_boarg (global board config).
    :return: list of complete boards where 0 = incomplete, Pnum = complete
    """
    arr = a_board[g_board][:]  # retrieves array size = 9 at location g_board in a_board
    a = np.reshape(arr, (3, 3))  # shapes it into 3x3 matrix
    # check rows
    if (a[0] == Pnum).sum() == 3 or (a[0] == Enum).sum() == 3:
        if Pnum in a[0]:
            c_boards[g_board] = Pnum
            print("Pnum Row1")
        else:
            c_boards[g_board] = Enum
            print("Enum Row1")
    elif (a[1] == Pnum).sum() == 3 or (a[1] == Enum).sum() == 3:
        if Pnum in a[1]:
            c_boards[g_board] = Pnum
            print("Pnum Row2")
        else:
            c_boards[g_board] = Enum
            print("Enum Row2")
    elif (a[2] == Pnum).sum() == 3 or (a[2] == Enum).sum() == 3:
        if Pnum in a[2]:
            c_boards[g_board] = Pnum
            print("Pnum Row3")
        else:
            c_boards[g_board] = Enum
            print("Enum Row3")
    # check columns
    elif (a[:, 0] == Pnum).sum() == 3 or (a[:, 0] == Enum).sum() == 3:
        if Pnum in a[:, 0]:
            c_boards[g_board] = Pnum
            print("Pnum Col1")
        else:
            c_boards[g_board] = Enum
            print("Enum Col1")
    elif (a[:, 1] == Pnum).sum() == 3 or (a[:, 1] == Enum).sum() == 3:
        if Pnum in a[:, 1]:
            c_boards[g_board] = Pnum
            print("Pnum Col2")
        else:
            c_boards[g_board] = Enum
            print("Enum Col2")
    elif (a[:, 2] == Pnum).sum() == 3 or (a[:, 2] == Enum).sum() == 3:
        if Pnum in a[:, 2]:
            c_boards[g_board] = Pnum
            print("Pnum Col3")
        else:
            c_boards[g_board] = Enum
            print("Enum Col3")
    # check diagonal
    elif (a.diagonal() == Pnum).sum() == 3 or (a.diagonal() == Enum).sum() == 3:
        if Pnum in a.diagonal():
            c_boards[g_board] = Pnum
            print("Pnum Diagonal1")
        else:
            c_boards[g_board] = Enum
            print("Enum Diagonal1")
    elif (np.fliplr(a).diagonal() == Pnum).sum() == 3 or (np.fliplr(a).diagonal() == Enum).sum() == 3:
        if Pnum in np.fliplr(a).diagonal():
            c_boards[g_board] = Pnum
            print("Pnum Diagonal2")
        else:
            c_boards[g_board] = Enum
            print("Enum Diagonal2")
    # check if board is tied
    elif np.all(a):
        # returns true if and only if every value isn't zero in the array
        c_boards[g_board] = 3
    return complete_boards
def won_board_points(c_boards):
    """
    Determines the number of boards won and in what seq, adds points based on the two
    :param c_boards: List of Completed Boards in form [0, Pnum, Enum]
    :return: points_sum: Total points earned
    """
    game_end = False
    points_sum = 0
    # Get indices of boards that have been won by Pnum and Enum
    Pnum_boards = [i for i, x in enumerate(c_boards) if x == Pnum]
    Enum_boards = [i for i, x in enumerate(c_boards) if x == Enum]
    # Check if Player has won game
    for a_set1 in possible_win_states:
        # Check's if Pnum has won
        if a_set1.issubset(Pnum_boards):
            game_end = True
            points_sum += win_game
            break
        # Check's if Enum has won
        if a_set1.issubset(Enum_boards):
            game_end = True
            points_sum += lose_game
            break
    # if game has not ended, continue scoring points
    if not game_end:
        # Add and Subtract points based on winning players
        points_sum += len(Pnum_boards) * win_board
        points_sum -= len(Enum_boards) * win_board
        # Check for seq. boards
        for a_set2 in possible_two_seq:
            # Checks Pnum's seq. boards
            if a_set2.issubset(Pnum_boards):
                points_sum += win_seq_board
            # Checks Enum's seq. boards
            if a_set2.issubset(Enum_boards):
                points_sum -= win_seq_board
    return points_sum
def corner_center_side_eval_func(hypo_board_config, incomplete_boards):
    eval_points = 0
    for x in range(0, len(hypo_board_config)):
        for y in range(0, len(hypo_board_config[x])):
            if hypo_board_config[x][y] == Pnum and (y == 0 or y == 2 or y == 6 or y == 8):
                eval_points += corner
            elif hypo_board_config[x][y] == Pnum and (y == 1 or y == 3 or y == 5 or y == 7):
                eval_points += side
            elif hypo_board_config[x][y] == Pnum and (y == 4):
                eval_points += middle
            #enemy
            if hypo_board_config[x][y] == Enum and (y == 0 or y == 2 or y == 6 or y == 8):
                eval_points -= corner
            elif hypo_board_config[x][y] == Enum and (y == 1 or y == 3 or y == 5 or y == 7):
                eval_points -= side
            elif hypo_board_config[x][y] == Enum and (y == 4):
                eval_points -= middle

    return eval_points

def checkBoardComplete2(g_board, c_boards, a_board):
    """
    DUPLICATE OF checkBOARDCOMPLETE without print statements, used inside points_won, here for debugging atm
    """
    arr = a_board[g_board][:]  # retrieves array size = 9 at location g_board in a_board
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
    elif (np.fliplr(a).diagonal() == Pnum).sum() == 3 or (np.fliplr(a).diagonal() == Enum).sum() == 3:
        if Pnum in np.fliplr(a).diagonal():
            c_boards[g_board] = Pnum
        else:
            c_boards[g_board] = Enum
    # check if board is tied
    elif np.all(a):
        # returns true if and only if every value isn't zero in the array
        c_boards[g_board] = 3
    return complete_boards
def display():
    """"
    function that can be called to display the current state of the board in terms of [0, Pnum, Enum]
    """
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
