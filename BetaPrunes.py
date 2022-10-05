import copy
import math
import os
from os.path import exists
import time

import numpy as np
import random

import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # list that stores boards that've been completed (won)
Pnum = 0
Enum = 0
max_depth = 5
move_time = 6
depth_multiplier = 1
# Point Weights
lose_game = -50000
win_game = 50000
win_seq_board = 300
win_center = 270
win_corner = 250
win_board = 200
two_in_row = 50
corner = 3
middle = 5
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
        while not exists("BetaPrunes.go"):
            pass
        time.sleep(0.1)
        if startFlag:
            last_move = readMoves('first_four_moves')
            global Pnum
            global Enum
            if last_move[0] == "BetaPrunes":
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
            if moves[0] == 'BetaPrunes':
                board[int(moves[1])][int(moves[2])] = Pnum
                checkBoardComplete(int(moves[1]), complete_boards_list, board)
            else:
                board[int(moves[1])][int(moves[2])] = Enum
                checkBoardComplete(int(moves[1]), complete_boards_list, board)
    f.close()
    return last_move


def addMove(next_move):
    # function that takes in the next move (int) and adds it to move_file
    board[int(next_move[0])][int(next_move[1])] = Pnum
    checkBoardComplete(next_move[0], complete_boards_list, board)
    file = open('move_file', 'r+')
    # read in the move from the other player here...
    file.seek(0)
    file.write("BetaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    file.truncate()
    file.close()
    display(board)
    print("---------------------")


def findNextMove(last_move):
    # function that determines the next move the player will make
    print("Last Move: " + str(last_move))
    last_move_on_local = int(last_move[2])
    moves_available = nextMoves(last_move_on_local, complete_boards_list, board)
    move = minimax_starter(moves_available, board, complete_boards_list)
    # move = [last_move, random.choice(availableList)]
    return move


def sort_moves(unsorted_moves):

    for i in range(1, len(unsorted_moves)):

        c_b_l = complete_boards_list.copy() #copy of list of complete boards
        points_of_move = points_won(updateBoard(unsorted_moves[i], board, c_b_l, Pnum), c_b_l)
        key_point = points_of_move
        key_move = unsorted_moves[i]
        j = i - 1

        while j >= 0 and points_won(updateBoard(unsorted_moves[j], board, c_b_l, Enum), c_b_l) > key_point:

            unsorted_moves[j + 1] = unsorted_moves[j]
            j -= 1

        unsorted_moves[j + 1] = key_move

    return unsorted_moves


# Works
def minimax_starter(moves_list, updated_board, temp_list):  # takes list of potential moves, the board, and list of complete boards
    final_move = []  # move that AI will choose
    top_score = -math.inf  # set negative so AI will pick a move
    c_updated_board = updated_board.copy()
    c_temp_list = temp_list.copy()
    #nonlocal curr_depth
    curr_depth = 1  # Current-Depth

    # DEPTH-ITERATIVE HEURISTIC
    start_time = time.time() # start time
    while curr_depth <= 500:
        print("Move score: ")
        for i in range(0, len(moves_list)):  # for every move in the move list
            # Creates a copy of the completed_boards_list
            temp_comp_board = np.copy(c_temp_list, 'K')
            # gets board with next move on it and updates temp list
            temp_updated_board = updateBoard(moves_list[i], c_updated_board, temp_comp_board, Pnum)

            unsorted_available_moves = copy.deepcopy(nextMoves(moves_list[i][1], temp_comp_board, temp_updated_board))
            sorted_available_moves = copy.deepcopy(sort_moves(unsorted_available_moves))
            sorted_available_moves.reverse()

            if len(sorted_available_moves) > 4:
                sorted_list_len = len(sorted_available_moves)
                for l in range(0, int(sorted_list_len / 3)):
                    sorted_available_moves.pop()

            # returns score
            score = minimax(sorted_available_moves, temp_updated_board, temp_comp_board, curr_depth, math.inf, -math.inf, False, start_time)  # finds score
            # break if return is None (time limit breached)
            if score == None:
                break
            move = moves_list[i] # set move equal to move list
            print("Move - [" + str(move) + "] - score - " + str(score))
            # Check if score is greater than top_score
            if score >= top_score: # Set top_score to current move score
                top_score = score
                final_move = move
                print("TOP SCORE: " + str(top_score))
                print("FINAL MOVE: " + str(final_move))
            # Check if current_score wins game
            if score >= win_game:
                final_move = move
        # Check if current_score wins game
        #if score >= win_game:
        #    final_move = move
        curr_depth += curr_depth + depth_multiplier  # add depth
    return final_move

def minimax(moves_list, updated_board, comp_boards, depth, alpha, beta, ally, start_time):
    # miniMax function with Alpha-Beta Pruning implemented
    if depth == 0:
        won = points_won(updated_board, comp_boards)
        return won  # checks the number of points won
    if time.time() - start_time > move_time:
        return None
    if ally:
        max_eval = -math.inf
        for possible_move in moves_list:
            temp_comp_boards = np.copy(comp_boards, 'K')
            temp_updated_board = updateBoard(possible_move, updated_board, temp_comp_boards, Pnum)
            eval = minimax(nextMoves(possible_move[1], temp_comp_boards, temp_updated_board), temp_updated_board,
                           temp_comp_boards, depth - 1, alpha, beta, not ally, start_time)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for possible_move in moves_list:
            temp_comp_boards = np.copy(comp_boards, 'K')
            temp_updated_board = updateBoard(possible_move, updated_board, temp_comp_boards, Enum)
            eval = minimax(nextMoves(possible_move[1], temp_comp_boards, temp_updated_board), temp_updated_board,
                           temp_comp_boards, depth - 1, alpha, beta, ally, start_time)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# What is the parameter last move? a list or just the board index
def nextMoves(last_local_move, c_board_list, updated_board):
    free_moves = []
    if c_board_list[last_local_move] != 0:  # check if last move was to a complete board
        for i in range(0, 9):  # generates a list of free spaces for all uncomplete boards
            if c_board_list[i] == 0:
                for j in range(0, 9):
                    if updated_board[i][j] == 0:
                        free_moves.append([i, j])
    else:
        for i in range(0, 9):
            if updated_board[last_local_move][i] == 0:
                free_moves.append([last_local_move, i])
    return free_moves


def updateBoard(tempMove, tempBoard, tempList, num):
    copy_board = np.copy(tempBoard, 'K')
    copy_board[tempMove[0]][tempMove[1]] = num
    checkBoardComplete(tempMove[1], tempList, copy_board)
    return copy_board


def points_won(temp_board, temp_comp_board):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param temp_board: tempo
    :return: points_sum: total points won by the Pnum (Player)
    """

    point_sum = 0
    """
    # create initial list of incomplete boards
    incomplete_boards = [x for x, n in enumerate(complete_boards_list) if n == 0]
    c_boards = np.copy(complete_boards_list, 'K')  # c_board: list of all complete boards
    # update number of complete boards based on temp_board config.
        # print("c_boards: " + str(c_boards))
    for g_board in incomplete_boards:

        For every board in incomplete_boards, check if that board has been completed in the temp_board,
        return updated list of completed boards which is set to c_boards
 
        c_boards = checkBoardComplete(g_board, c_boards, temp_board).copy()  # set board to updated list
    """
    # print("TEMP BOARD CONFIG:")
    # update incomplete_boards
    incomplete_boards = [x for x, n in enumerate(temp_comp_board) if n == 0]
    # print("TEMP Incomplete Boards: " + str(incomplete_boards))
    # print("TEMP Complete Boards: " + str(temp_comp_board))
    # sum points for # of boards one, and check for seq. boards
    board_points = won_board_points(temp_comp_board)
    point_sum += board_points
    # print("WON BOARD POINTS: " + str(board_points))
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
        arr = temp_board[i][:]  # retrieves a board
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
        # enemy
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
    if 0 in Pnum_boards:
        points_sum += win_corner
    if 0 in Enum_boards:
        points_sum -= win_corner
    if 2 in Pnum_boards:
        points_sum += win_corner
    if 2 in Enum_boards:
        points_sum -= win_corner
    if 6 in Pnum_boards:
        points_sum += win_corner
    if 6 in Enum_boards:
        points_sum -= win_corner
    if 8 in Pnum_boards:
        points_sum += win_corner
    if 8 in Enum_boards:
        points_sum -= win_corner
    if 4 in Pnum_boards:
        points_sum += win_center
    if 4 in Enum_boards:
        points_sum -= win_center
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
            # enemy
            if hypo_board_config[x][y] == Enum and (y == 0 or y == 2 or y == 6 or y == 8):
                eval_points -= corner
            elif hypo_board_config[x][y] == Enum and (y == 1 or y == 3 or y == 5 or y == 7):
                eval_points -= side
            elif hypo_board_config[x][y] == Enum and (y == 4):
                eval_points -= middle

    return eval_points


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
    return c_boards


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
    return c_boards


def display(a_board):
    """"
    function that can be called to display the current state of the board in terms of [0, Pnum, Enum]
    """
    print("Current Board:")
    print(str(a_board[0][0:3]) + " | " + str(a_board[1][0:3]) + " | " + str(a_board[2][0:3]))
    print(str(a_board[0][3:6]) + " | " + str(a_board[1][3:6]) + " | " + str(a_board[2][3:6]))
    print(str(a_board[0][6:9]) + " | " + str(a_board[1][6:9]) + " | " + str(a_board[2][6:9]))
    print("------------------------------------")
    print(str(a_board[3][0:3]) + " | " + str(a_board[4][0:3]) + " | " + str(a_board[5][0:3]))
    print(str(a_board[3][3:6]) + " | " + str(a_board[4][3:6]) + " | " + str(a_board[5][3:6]))
    print(str(a_board[3][6:9]) + " | " + str(a_board[4][6:9]) + " | " + str(a_board[5][6:9]))
    print("------------------------------------")
    print(str(a_board[6][0:3]) + " | " + str(a_board[7][0:3]) + " | " + str(a_board[8][0:3]))
    print(str(a_board[6][3:6]) + " | " + str(a_board[7][3:6]) + " | " + str(a_board[8][3:6]))
    print(str(a_board[6][6:9]) + " | " + str(a_board[7][6:9]) + " | " + str(a_board[8][6:9]))


if __name__ == "__main__":
    main()
