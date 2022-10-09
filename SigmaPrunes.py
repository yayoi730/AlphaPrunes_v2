import math
import os
from os.path import exists
import time

import numpy as np
import random

import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Pnum = 0
Enum = 0
# Point Weights
Depth = 2
lose_game = -50000
win_game = 50000
win_seq_board = 200
win_center = 100
win_corner = 75
win_board = 200
two_in_row = 30
corner = 5
middle = 30
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
        while not exists("SigmaPrunes.go"):
            pass
        time.sleep(0.1)
        if startFlag:
            last_move = readMoves('first_four_moves')
            global Pnum
            global Enum
            if last_move[0] == "SigmaPrunes":
                Pnum = 2
                Enum = 1
                last_move = readMoves('first_four_moves')
            else:
                Pnum = 2
                Enum = 1
                last_move = readMoves('first_four_moves')
            if os.path.getsize("move_file") != 0:
                last_move = readMoves("move_file")
        else:
            last_move = readMoves('move_file')
        display(board)
        next_move = findNextMove(last_move)
        addMove(next_move)
        startFlag = False

def readMoves(file):
    """
    #read file function that reads the file and adds the move to the global board and returns the last move
    :param file: The text file that we read moves from
    :return: the last move of the file
    """

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
            if moves[0] == 'SigmaPrunes':
                board[int(moves[1])][int(moves[2])] = Pnum
                checkBoardComplete(int(moves[1]), complete_boards_list, board)
            else:
                board[int(moves[1])][int(moves[2])] = Enum
                checkBoardComplete(int(moves[1]), complete_boards_list, board)
    f.close()
    return last_move


def addMove(next_move):
    """
    #adds the move to the board and writes the move to the move text file
    :param next_move: the move to make

    """
    # function that takes in the next move (int) and adds it to move_file
    print("SigmaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    board[next_move[0]][next_move[1]] = Pnum
    checkBoardComplete(next_move[0], complete_boards_list, board)
    file = open('move_file', 'r+')
    # read in the move from the other player here...
    file.seek(0)
    file.write("SigmaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    file.truncate()
    file.close()
    print("---------------------")


def findNextMove(last_move):
    """
    #takes in the previous move and then calls the minimax function to find the next move
    :param last_move: The previous move made
    :return: move: The new move to be made
    """
    # function that determines the next move the player will make
    print("Last Move: " + str(last_move))
    last_move = [int(last_move[1]), int(last_move[2])]
    best_move = minimax_starter(last_move, 2)
    return best_move


def minimax_starter(last_move, depth):
    """
    Calls minimax function to determine best_move
    :param last_move: last_move made by Enum in form of g_board, l_board tuple
    :param depth: depth to traverse
    :return: best_move: move to print to move_file in form of g_board, l_board tuple
    """
    copy_board = np.copy(board, 'K').copy()
    copy_curr_list_c_boards = complete_boards_list.copy()
    best_move, score = minimax(copy_board, copy_curr_list_c_boards, last_move, 2, math.inf, -math.inf, True)
    return best_move


def minimax(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally):
    """

    :param curr_board:
    :param curr_list_c_boards:
    :param last_move:
    :param depth:
    :param alpha:
    :param beta:
    :param ally:
    :return:
    """
    if depth == 0:
        total_points_won = points_won(curr_board, curr_list_c_boards)
        return [last_move, total_points_won]
    # TODO: implement time_constraint
    if ally:
        best_move, max_score = max_value(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, not ally)
        return [best_move, max_score]
    else:
        best_move, min_score = min_value(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally)
        return [best_move, min_score]
    return [best_move, score]


def max_value(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally):
    best_move = None
    list_of_possible_moves, g_board = generate_list_of_moves(curr_board, curr_list_c_boards, last_move)
    print("MAX List of Moves on " + str(g_board) + " : " + str(list_of_possible_moves))
    # EVALUATION OF MOVES
    max_score = -math.inf
    for move in list_of_possible_moves:
        chosen_move = [g_board, move]
        # Update Board with Chosen Move
        u_curr_board, u_curr_list_c_boards = update_board(np.copy(curr_board, 'K').copy(), curr_list_c_boards.copy(),
                                                          chosen_move,
                                                          not ally)
        # Calculate Min Score Amoung Those Moves
        min_move, score = minimax(u_curr_board, u_curr_list_c_boards, chosen_move, depth - 1, alpha, beta, ally)
        if score > max_score:
            max_score = score
            best_move = chosen_move
        print("Move - [" + str(chosen_move) + "] - score - " + str(score))
        """
        # alpha-beta pruning
        alpha = max(alpha, score)
        if beta <= alpha:
            break
        """
    print("Best Move - [" + str(best_move) + "] - score - " + str(score))
    print("---------------------------------")
    return [best_move, max_score]


def min_value(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally):
    best_move = None
    list_of_possible_moves, g_board = generate_list_of_moves(curr_board, curr_list_c_boards.copy(), last_move)
    print("MIN List of Moves on " + str(g_board) + " : " + str(list_of_possible_moves))
    # EVALUATION OF MOVES
    min_score = math.inf
    for move in list_of_possible_moves:
        chosen_move = [g_board, move]
        #
        u_curr_board, u_curr_list_c_boards = update_board(np.copy(curr_board, 'K').copy(), curr_list_c_boards.copy(),
                                                          chosen_move,
                                                          ally)
        max_move, score = minimax(u_curr_board, u_curr_list_c_boards, chosen_move, depth - 1, alpha, beta, not ally)
        print("Move - [" + str(chosen_move) + "] - score - " + str(score))
        if score < min_score:
            min_score = score
            best_move = chosen_move
        """
        # alpha-beta pruning
        beta = min(beta, score)
        if beta <= alpha:
            break
        """
    print("Chosen Move - [" + str(best_move) + "] - score - " + str(score))
    print("---------------------------------")
    return [best_move, min_score]


# Helper Functions for minimax:
def update_board(curr_board, curr_list_of_c_boards, last_move, ally):
    """
    Returns an updated board and list of completed boards given:
    :param curr_board: current global board config.
    :param curr_list_of_c_boards: list of boards already completed
    :param last_move: g_board and l_board tuple
    :param ally: bool determines whose move (Pnum or Enum)
    :return: updated_board, updated_list_c_boards tuple
    """
    g_board = last_move[0]  # global board
    l_board = last_move[1]  # local board (move)
    updated_board = np.copy(curr_board, 'K').copy()
    updated_list_c_boards = curr_list_of_c_boards.copy()
    if ally:
        updated_board[g_board][l_board] = Pnum
        updated_list_c_boards = checkBoardComplete(g_board, updated_list_c_boards, updated_board)
    else:
        updated_board[g_board][l_board] = Enum
        updated_list_c_boards = checkBoardComplete(g_board, updated_list_c_boards, updated_board)
    return [updated_board, updated_list_c_boards]


def generate_list_of_moves(curr_board, curr_list_of_c_boards, last_move):
    # Check if last move completed a board <-- is this necessary if we check after reading in moves
    l_board = last_move[1]
    if curr_list_of_c_boards[l_board] == 0:
        # Generate list of available moves for l_board
        all_local_moves = curr_board[l_board][:]
        possible_moves_list = [x for x, n in enumerate(all_local_moves) if
                               n == 0]  # returns indices of all unpopulated grids within a g_board
        g_board = l_board
    else:
        # TODO: FREE-CHOICE HEURISTIC FUNCTION
        # pick random from available boards in mean time
        unpopulated_boards = [x for x, n in enumerate(curr_list_of_c_boards) if
                              n == 0]  # returns indices of all unpopulated boards
        g_board = random.choice(unpopulated_boards)
        all_local_moves = curr_board[g_board][:]
        possible_moves_list = [x for x, n in enumerate(all_local_moves) if
                               n == 0]  # returns indices of all unpopulated grids within chosen_board
    return [possible_moves_list, g_board]


# TODO: sort list of moves based on non-terminal utility function
# TODO: remove undesirable moves from sorted list
def points_won(temp_board, temp_comp_board):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param temp_board: temporary global board configuration
    :param temp_comp_board: temporary list of completed boards based on global board configuration
    :return: points_sum: total points won by the Pnum (Player)
    """
    print(temp_board)
    point_sum = 0
    # update incomplete_boards
    incomplete_boards = [x for x, n in enumerate(temp_comp_board) if n == 0]
    # sum points for # of boards one, and check for seq. boards
    board_points = won_board_points(temp_comp_board)
    point_sum += board_points
    # search and sum points for two_in_row
    twr_points = two_in_rows(incomplete_boards, temp_board)
    point_sum += twr_points
    # evaluates individual spots on a board
    ccse_points = corner_center_side_eval_func(temp_board)
    point_sum += ccse_points
    return point_sum


def two_in_rows(incomplete_boards, temp_board):
    # TODO: verify works as planned with random agent
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
    # TODO: verify works as planned with random agent
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
    # Sum Bonus Points based on the location of the board won
    # Check if a corner board is won by Pnum or Enum
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
    # Check if a center board is won by Pnum or Enum
    if 4 in Pnum_boards:
        points_sum += win_center
    if 4 in Enum_boards:
        points_sum -= win_center
    return points_sum
def corner_center_side_eval_func(hypo_board_config):
    # TODO: verify works as planned with random agent
    """
    Function that returns points based on local board configuration. Considers corner, sides, and middles.
    Adds (Pnum) and Subtracts (Enum) based on who is on the board
    :param hypo_board_config: temporary board configuration
    :return: eval_points:  sum of points won
    """
    eval_points = 0
    for x in range(0, len(hypo_board_config)):
        for y in range(0, len(hypo_board_config[x])):
            # Check for Pnum moves
            if hypo_board_config[x][y] == Pnum and (y == 0 or y == 2 or y == 6 or y == 8):
                eval_points += corner
            elif hypo_board_config[x][y] == Pnum and (y == 1 or y == 3 or y == 5 or y == 7):
                eval_points += side
            elif hypo_board_config[x][y] == Pnum and (y == 4):
                eval_points += middle
            # Check for E
            if hypo_board_config[x][y] == Enum and (y == 0 or y == 2 or y == 6 or y == 8):
                eval_points -= corner
            elif hypo_board_config[x][y] == Enum and (y == 1 or y == 3 or y == 5 or y == 7):
                eval_points -= side
            elif hypo_board_config[x][y] == Enum and (y == 4):
                eval_points -= middle
    return eval_points


def checkBoardComplete(g_board, c_boards, a_board):
    # TODO: verify works as planned with random agent, check edge cases
    """
    Checks whether a board has been complete after a move and updates the global complete_boards list
    :param g_board, c_boards (list of complete boards), a_board (global board config).
    :return: list of complete boards where 0 = incomplete, Pnum (won by Player), Enum (won by Enemy) or 3 (tiee)
    """
    # print("G board: " + str(g_board) + "Completed boards: " + str(c_boards))
    arr = a_board[g_board][:]  # retrieves array size = 9 at location g_board in a_board
    a = np.reshape(arr, (3, 3))  # shapes it into 3x3 matrix
    # Checks that the sum of Pnum is equal to 3 or that the sum of Enum is equal to 3 in a row, column, or diagonal layout
    # Sets corresponding index in complete_boards_list equal to Pnum, Enum, or 3 (tie)
    # check rows:
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
    # check columns:
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
    # check diagonals:
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
    # check if board is tied:
    elif np.all(a):
        # returns true if and only if every value isn't zero in the array
        c_boards[g_board] = 3
    return c_boards  # return list of completed boards


def display(a_board):
    """
    function that can be called to display the current state of the board in terms of [0, Pnum, Enum] in a 3x3 matrix (global board)
    layout with each index being a 3x3 matrix (local board)
    :param a_board: a global board configurations
    :return:
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
