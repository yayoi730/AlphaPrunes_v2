import math
import os
from os.path import exists
import time

import numpy as np
import random

import pygame

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # list that stores indices of completed (won) boards
Pnum = 2
Enum = 1
depth = 4
# Point Weights, Grading System for Moves:
lose_game = -50000
win_game = 50000
win_board = 300
# Bonus Points Based on What and Where Board is Won:
win_seq_board = 250
win_center = 200
win_corner = 175
# Other Points
two_in_row = 100
corner = 5
middle = 15
side = 1
other_p = 0
free_choice = -5
# List of Sets of Possible Sequences for Boards
possible_two_seq = [{0, 1}, {1, 2}, {0, 2}, {0, 3}, {3, 6}, {0, 6}, {0, 4}, {0, 8}, {4, 8},
                    {1, 4}, {4, 7}, {1, 7}, {2, 5}, {5, 8}, {2, 8}, {2, 4}, {4, 6}, {2, 6}]
# List of Sets of Possible Board Win States
possible_win_states = [{0, 1, 2}, {0, 3, 6}, {0, 4, 8}, {1, 4, 7}, {3, 4, 5}, {2, 5, 8}, {2, 4, 6}, {6, 7, 8}]


def main():
    # startFlag is made to determine if the code is at the start;
    # this is used to determine whether we read from move file or first four move
    startFlag = True
    while not exists("end_game"):  # checks if end game file exists, ends game if true
        time.sleep(1)
        while not exists("SigmaPrunes.go"):  # blocks the code from running unless it sees its: name.go
            pass
        time.sleep(0.1)
        if startFlag:  # if this is the start of the game
            # read the moves and output the last move of the first four moves file
            last_move = read_moves('first_four_moves')  # Sets Pnum and Enum values based on global values
            if os.path.getsize("move_file") != 0:
                last_move = read_moves("move_file")
        else:
            last_move = read_moves('move_file')
        display(board)
        next_move = find_next_move(last_move)  # finds the next move
        add_move(next_move)  # writes next move to the move_file
        startFlag = False  # sets startFlag = false, no longer first move


def read_moves(file):
    """
    #read file function that reads the file and adds the move to the global board and returns the last move
    :param file: The text file that we read moves from
    :return: the last move of the file
    """

    # reads in txt file and populates the board with the move information
    # returns the last move made in a list ex: ['PlayerName'. 'g_board' 'l_board']
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
                check_board_complete(int(moves[1]), complete_boards_list, board)
            else:
                board[int(moves[1])][int(moves[2])] = Enum
                check_board_complete(int(moves[1]), complete_boards_list, board)
    f.close()
    return last_move


def add_move(next_move):
    """
    #adds the move to the board and writes the move to the move text file
    :param next_move: the move to make
    """
    # function that takes in the next move (int) and adds it to move_file
    print("SigmaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    board[next_move[0]][next_move[1]] = Pnum
    check_board_complete(next_move[0], complete_boards_list, board)
    file = open('move_file', 'r+')
    # read in the move from the other player here...
    file.seek(0)
    file.write("SigmaPrunes " + str(next_move[0]) + " " + str(next_move[1]))
    file.truncate()
    file.close()
    print("---------------------")


def find_next_move(last_move):
    """
    Takes in the previous move and then calls the minimax function to find the next move
    :param last_move: last move in string list: ['Player Name', 'g_board', 'l_board']
    :return: best_move: the next move based on minimax
    """
    # function that determines the next move the player will make
    print("Last Move: " + str(last_move))
    last_move = [int(last_move[1]), int(last_move[2])]  # Change into tuple of ints: [g_board, l_board]
    best_move = minimax_starter(last_move)
    return best_move


# Minimax Starter
def minimax_starter(last_move):
    """
    Calls minimax function to determine best_move; sets up and initiates minimax
    :param last_move: last_move  by Enum in form of [g_board, l_board] tuple
    :return: best_move: final chosen move in form of [g_board, l_board] tuple
    """
    # Copy global variable 'board' and 'complete_boards_list' before passing into function
    copy_board = np.copy(board, 'K').copy()
    copy_curr_list_c_boards = complete_boards_list.copy()
    # Calls minimax
    # TODO: Implement Iterative Deepening over this w/ time_constraint
    best_move, score = minimax(copy_board, copy_curr_list_c_boards, last_move, depth, -math.inf, math.inf, True)
    return best_move


# Minimax + Helper Functions
def minimax(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally):
    """
    Minimax
    :param curr_board: current global board configuration
    :param curr_list_c_boards: current list of completed boards
    :param last_move: last_move by Enum in form of [g_board, l_board] tuple
    :param depth: depth to traverse
    :param alpha: -inf. for pruning
    :param beta:  +inf. for pruning
    :param ally: Pnum's move (true)
    :return: best_move, score: best move and associated score in tuple
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
    """
    Returns a valid move with the highest point sum calculated by points_won() given a last move
    :param curr_board: current global board configuration
    :param curr_list_c_boards: current list of completed boards
    :param last_move:last_move  by Enum in form of [g_board, l_board] tuple
    :param depth: depth to traverse
    :param alpha: -inf. for pruning
    :param beta: +inf. for pruning
    :param ally: Pnum's move (false)
    :return: best_move, score: best move (max) and associated score in tuple
    """
    best_move = None
    # Generate list of possible moves + on what g_board
    list_of_possible_moves, g_board = generate_list_of_moves(curr_board, curr_list_c_boards,
                                                             last_move)
    print("MAX List of Moves on " + str(g_board) + " : " + str(list_of_possible_moves))
    # EVALUATION OF MOVES
    max_score = -math.inf
    for move in list_of_possible_moves:
        chosen_move = [g_board, move]
        # Update Board with Chosen Move
        u_curr_board, u_curr_list_c_boards = update_board(np.copy(curr_board, 'K').copy(), curr_list_c_boards.copy(),
                                                          chosen_move,
                                                          not ally)  # currently ally = false, false(false(ally)) = True = Pnum
        # Calculate Min Scores Among Those Moves
        min_move, score = minimax(u_curr_board, u_curr_list_c_boards, chosen_move, depth - 1, alpha, beta, ally)
        # Find The Highest Score
        if score > max_score:
            max_score = score
            best_move = chosen_move
        print("Move - [" + str(chosen_move) + "] - score - " + str(score))
        # alpha-beta pruning
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    print("Best Move - [" + str(best_move) + "] - score - " + str(score))
    print("---------------------------------")
    return [best_move, max_score]


def min_value(curr_board, curr_list_c_boards, last_move, depth, alpha, beta, ally):
    """
    Returns a valid move with the lowest point sum calculated by points_won() given a last move
    :param curr_board: current global board configuration
    :param curr_list_c_boards: current list of completed boards
    :param last_move:last_move by Pnum in form of [g_board, l_board] tuple
    :param depth: depth to traverse
    :param alpha: -inf. for pruning
    :param beta: +inf. for pruning
    :param ally: Pnum's move (false)
    :return: best_move, score: best move (min) and associated score in tuple
    """
    best_move = None
    # Generate list of possible moves + on what g_board
    list_of_possible_moves, g_board = generate_list_of_moves(curr_board, curr_list_c_boards.copy(), last_move)
    print("MIN List of Moves on " + str(g_board) + " : " + str(list_of_possible_moves))
    # EVALUATION OF MOVES
    min_score = math.inf
    for move in list_of_possible_moves:
        chosen_move = [g_board, move]
        # Update Board with Chosen Move
        u_curr_board, u_curr_list_c_boards = update_board(np.copy(curr_board, 'K').copy(), curr_list_c_boards.copy(),
                                                          chosen_move,
                                                          ally)
        # Calculate Max Score Among Those Moves
        max_move, score = minimax(u_curr_board, u_curr_list_c_boards, chosen_move, depth - 1, alpha, beta,
                                  not ally)  # currently ally = true, false(ally)) = False = Enum
        print("Move - [" + str(chosen_move) + "] - score - " + str(score))
        # Find The Lowest Score
        if score < min_score:
            min_score = score
            best_move = chosen_move
        # alpha-beta pruning
        beta = min(beta, score)
        if beta <= alpha:
            break
    print("Chosen Move - [" + str(best_move) + "] - score - " + str(score))
    print("---------------------------------")
    return [best_move, min_score]


# Helper Functions for Minimax:
# TODO: sort list of moves based on non-terminal utility function (use faster sort method, like Greedy(?))
# TODO: remove undesirable moves from sorted list (how to determine this?
def update_board(curr_board, curr_list_of_c_boards, last_move, ally):
    """
    Returns an updated board and list of completed boards given a move and bool representing who made it:
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
        updated_board[g_board][l_board] = Pnum  # set move in board = Pnum
        updated_list_c_boards = check_board_complete(g_board, updated_list_c_boards,
                                                     updated_board)  # check for completed boards
    else:
        updated_board[g_board][l_board] = Enum  # set move in board = Enum
        updated_list_c_boards = check_board_complete(g_board, updated_list_c_boards,
                                                     updated_board)  # check for completed boards
    return [updated_board, updated_list_c_boards]


def generate_list_of_moves(curr_board, curr_list_of_c_boards, last_move):
    """
    Generates a list of all available moves in a given local board based on the last move
    :param curr_board: current global board configuration
    :param curr_list_of_c_boards: current list of all completedboards
    :param last_move: last global and local move tuple
    :return:
    """
    l_board = last_move[1]
    if curr_list_of_c_boards[l_board] == 0:
        # Generate list of available moves for l_board
        all_local_moves = curr_board[l_board][:]
        possible_moves_list = [x for x, n in enumerate(all_local_moves) if
                               n == 0]  # returns indices of all unpopulated grids within a g_board
        g_board = l_board
    else:
        # TODO: FREE-CHOICE HEURISTIC FUNCTION
        # currently picks random from available boards
        unpopulated_boards = [x for x, n in enumerate(curr_list_of_c_boards) if
                              n == 0]  # returns indices of all unpopulated boards
        print("UNPOPULATED BOARDS: " + str(unpopulated_boards))
        # TODO: FIND OUT WHY UNPOPULATED BOARDS [ ] and fix
        g_board = random.choice(unpopulated_boards)
        all_local_moves = curr_board[g_board][:]
        possible_moves_list = [x for x, n in enumerate(all_local_moves) if
                                   n == 0]  # returns indices of all unpopulated grids within chosen_board
    return [possible_moves_list, g_board]


# Utility Functions:
def points_won(temp_board, temp_list_of_comp_boards):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param temp_board: temporary global board configuration
    :param temp_list_of_comp_boards: temporary list of completed boards based on global board configuration
    :return: points_sum: total points won by the Pnum (Player)
    """
    point_sum = 0
    # update incomplete_boards
    incomplete_boards = [x for x, n in enumerate(temp_list_of_comp_boards) if n == 0]
    # sum points for # of boards one, and check for seq. boards + returns state of game
    board_points, game_end = won_board_points(temp_list_of_comp_boards)
    point_sum += board_points
    # If game hasn't ended, continue calculating # of points won
    if not game_end:
        point_sum += board_points
        # search and sum points for two_in_row
        twr_points = two_in_rows(incomplete_boards, temp_board)
        point_sum += twr_points
        # evaluates individual spots on a board
        ccse_points = corner_center_side_eval_func(temp_board)
        point_sum += ccse_points
    return point_sum


# Utility Helper Functions:
def won_board_points(temp_list_of_comp_boards):
    # TODO: verify works as planned
    """
    Determines and adds points based on the number of boards won, in what sequence and in what location;.
    Function ends early if Loss or Win is detected.
    :param temp_list_of_comp_boards: List of Completed Boards in form [0, Pnum, Enum]
    :return: points_sum, game_end: Total points earned and state of game typle
    """
    game_end = False  # set inital game condition to false
    points_sum = 0
    # Get indices of boards that have been won by Pnum and Enum
    Pnum_boards = [i for i, x in enumerate(temp_list_of_comp_boards) if x == Pnum]
    Enum_boards = [i for i, x in enumerate(temp_list_of_comp_boards) if x == Enum]
    # Check if Player has won game
    for a_set1 in possible_win_states:
        # Check's if Pnum has won
        if a_set1.issubset(Pnum_boards):
            game_end = True
            points_sum += win_game
            print("GAME WON DETECTED")
            break
        # Check's if Enum has won
        if a_set1.issubset(Enum_boards):
            game_end = True
            points_sum += lose_game
            print("GAME LOST DETECTED")
            break
    # if game has not ended, continue scoring points
    if not game_end:
        # Add and Subtract points based on winning players
        points_sum += (len(Pnum_boards) * win_board)
        points_sum -= (len(Enum_boards) * win_board)
        # Check for seq. boards
        for a_set2 in possible_two_seq:
            # Checks Pnum's seq. boards
            if a_set2.issubset(Pnum_boards):
                points_sum += win_seq_board
            # Checks Enum's seq. boards
            if a_set2.issubset(Enum_boards):
                points_sum -= win_seq_board
        # Bonus Points for winning corner and center boards
        for i in Pnum_boards:
            if i in (0, 2, 6, 8):
                points_sum += win_corner
            if i == 4:
                points_sum += win_center
        for i in Enum_boards:
            if i in (0, 2, 6, 8):
                points_sum -= win_corner
            if i == 4:
                points_sum -= win_center
    return [points_sum, game_end]


def two_in_rows(incomplete_boards, temp_board):
    # TODO: verify works as planned
    """
    Determines the number of two in a rows Pnum (Player) has made (+ points) and Enum has made (- points)
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


def corner_center_side_eval_func(temp_board):
    # TODO: verify works as planned
    """
    Function that returns points based on local board configuration. Considers corner, sides, and middles.
    Adds (Pnum) and Subtracts (Enum) based on who is on the board
    :param temp_board: temporary board configuration
    :return: eval_points:  sum of points won
    """
    points_sum = 0
    for x in range(0, len(temp_board)):
        for y in range(0, len(temp_board[x])):
            # Check for Pnum moves
            if temp_board[x][y] == Pnum and (y == 0 or y == 2 or y == 6 or y == 8):
                points_sum += corner
            elif temp_board[x][y] == Pnum and (y == 1 or y == 3 or y == 5 or y == 7):
                points_sum += side
            elif temp_board[x][y] == Pnum and (y == 4):
                points_sum += middle
            # Check for Enum moves
            if temp_board[x][y] == Enum and (y == 0 or y == 2 or y == 6 or y == 8):
                points_sum -= corner
            elif temp_board[x][y] == Enum and (y == 1 or y == 3 or y == 5 or y == 7):
                points_sum -= side
            elif temp_board[x][y] == Enum and (y == 4):
                points_sum -= middle
    return points_sum


# Other Helper Functions
def check_board_complete(g_board, list_of_complete_boards, a_board):
    # TODO: verify works as planned
    """
    Checks whether a board has been complete after a move and updates the global complete_boards list
    :param g_board, list of complete boards, a_board (global board config).
    :return: list_oF_complete_boards where 0 = incomplete, Pnum (won by Player), Enum (won by Enemy) or 3 (tiee)
    """
    # print("G board: " + str(g_board) + "Completed boards: " + str(c_boards))
    arr = a_board[g_board][:]  # retrieves array size = 9 at location g_board in a_board
    a = np.reshape(arr, (3, 3))  # shapes it into 3x3 matrix

    # Checks that the sum of Pnum is equal to 3 or that the sum of Enum is equal to 3 in:
    # a row, column, or diagonal layout
    # sets corresponding index in complete_boards_list equal to Pnum, Enum, or 3 (tie)\

    # check rows:
    if (a[0] == Pnum).sum() == 3 or (a[0] == Enum).sum() == 3:
        if Pnum in a[0]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    elif (a[1] == Pnum).sum() == 3 or (a[1] == Enum).sum() == 3:
        if Pnum in a[1]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    elif (a[2] == Pnum).sum() == 3 or (a[2] == Enum).sum() == 3:
        if Pnum in a[2]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    # check columns:
    elif (a[:, 0] == Pnum).sum() == 3 or (a[:, 0] == Enum).sum() == 3:
        if Pnum in a[:, 0]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    elif (a[:, 1] == Pnum).sum() == 3 or (a[:, 1] == Enum).sum() == 3:
        if Pnum in a[:, 1]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    elif (a[:, 2] == Pnum).sum() == 3 or (a[:, 2] == Enum).sum() == 3:
        if Pnum in a[:, 2]:
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    # check diagonals:
    elif (a.diagonal() == Pnum).sum() == 3 or (a.diagonal() == Enum).sum() == 3:
        if Pnum in a.diagonal():
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    elif (np.fliplr(a).diagonal() == Pnum).sum() == 3 or (np.fliplr(a).diagonal() == Enum).sum() == 3:
        if Pnum in np.fliplr(a).diagonal():
            list_of_complete_boards[g_board] = Pnum
        else:
            list_of_complete_boards[g_board] = Enum
    # check if board is tied:
    elif np.all(a):
        # returns true if and only if every value isn't zero in the array
        list_of_complete_boards[g_board] = 3
    return list_of_complete_boards  # return list of completed boards


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
