import copy
import math
import os
from os.path import exists
import time
import numpy as np

board = np.zeros((9, 9))  # stores the moves that have been played
complete_boards_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # list that stores boards that've been completed (won)
Pnum = 0
Enum = 0
move_time = 6  # time in seconds allowed per move
depth_multiplier = 1  # depth multiplier for Iterative_Deepeming
# Point Weights, Grading System
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
    startFlag = True  # startFlag is made to determine if the code is at the start, this is used to determine whether we read from move file or first four move
    while not exists("end_game"):  # checks if end game file exists if it does it ends the player
        time.sleep(1)
        while not exists("BetaPrunes.go"):  # blocks the code from running unless it sees its file name.go
            pass
        time.sleep(0.1)
        if startFlag:  # if this is the start of the game
            last_move = readMoves(
                'first_four_moves')  # read the moves and output the last move of the first four moves file
            global Pnum
            global Enum
            if last_move[
                0] == "BetaPrunes":  # if the last move from first four move file is ours set the player number to 2 signifying we go second
                Pnum = 2
                Enum = 1
                last_move = readMoves('first_four_moves')
            else:  # if the last move from first four move file is the enmey set the player number to 1 signifying we go first
                Pnum = 1
                Enum = 2
                last_move = readMoves('first_four_moves')
            if os.path.getsize("move_file") != 0:
                last_move = readMoves("move_file")
        else:
            last_move = readMoves('move_file')
        next_move = findNextMove(last_move)  # calls the findNextMove function based on the last move
        addMove(next_move)  # calls the addMove function which adds the given move to the board and move file
        startFlag = False  # sets start flag to false telling code this is no longer the first turn


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
            if moves[0] == 'BetaPrunes':
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
    """
    #takes in the previous move and then calls the minimax function to find the next move
    :param last_move: The previous move made
    :return: move: The new move to be made
    """
    # function that determines the next move the player will make
    print("Last Move: " + str(last_move))
    last_move_on_local = int(last_move[2])
    moves_available = nextMoves(last_move_on_local, complete_boards_list, board)
    move = minimax_starter(moves_available, board, complete_boards_list)
    # move = [last_move, random.choice(availableList)]
    return move


def sort_moves(unsorted_moves):
    """
    #takes in a list of unsorted moves and then uses insertion sort to sort based off the points that each move is worth
    :param unsorted_moves: The previous move made
    :return: sorted_moves: The sorted moves list
    """
    for i in range(1, len(unsorted_moves)):
        c_b_l = complete_boards_list.copy()  # copy of list of complete boards
        points_of_move = points_won(updateBoard(unsorted_moves[i], board, c_b_l, Pnum), c_b_l)
        key_point = points_of_move
        key_move = unsorted_moves[i]
        j = i - 1
        while j >= 0 and points_won(updateBoard(unsorted_moves[j], board, c_b_l, Enum), c_b_l) > key_point:
            unsorted_moves[j + 1] = unsorted_moves[j]
            j -= 1
        unsorted_moves[j + 1] = key_move
    sorted_moves = copy.deepcopy(unsorted_moves)
    return sorted_moves


def minimax_starter(moves_list, updated_board, temp_list):
    """
    Starts the minimax algorithm and iterates through a given set of moves returning the move
    with the highest score for Pnum
    :param moves_list: takes in a list of possible moves
    :param updated_board: updated global board
    :param temp_list: temporary list of completed boards
    :return: final_move: move determined to be optimal by minimax
    """
    final_move = []  # move that AI will choose
    top_score = -math.inf  # set negative so AI will pick a move
    c_updated_board = updated_board.copy()
    c_temp_list = temp_list.copy()
    curr_depth = 1  # Starting depth for Iterative-Deepening Heuristic

    # DEPTH-ITERATIVE HEURISTIC
    start_time = time.time()  # start time for Iterative-Deepening
    while curr_depth <= 500:
        for i in range(0, len(moves_list)):  # for every move in the move list
            # Creates a copy of the completed_boards_list
            temp_comp_board = np.copy(c_temp_list, 'K')
            # gets board with next move on it and updates temp list
            temp_updated_board = updateBoard(moves_list[i], c_updated_board, temp_comp_board, Pnum)

            # Sorts list of available moves
            unsorted_available_moves = copy.deepcopy(nextMoves(moves_list[i][1], temp_comp_board, temp_updated_board))
            sorted_available_moves = copy.deepcopy(sort_moves(unsorted_available_moves))
            sorted_available_moves.reverse()

            # Removes a number of lists
            if len(sorted_available_moves) > 4:  # if length of possible moves is greater than 4
                sorted_list_len = len(sorted_available_moves)
                for l in range(0, int(sorted_list_len / 5)):  # Gets rid of the worst fifth of the list
                    sorted_available_moves.pop()

            # returns score
            score = minimax(sorted_available_moves, temp_updated_board, temp_comp_board, curr_depth, math.inf,
                            -math.inf, False, start_time)  # finds score
            # break if return is None (time limit breached)
            if score == None:
                break
            move = moves_list[i]  # set move equal to move list
            # Check if score is greater than top_score
            if score >= top_score:  # Set top_score to current move score
                top_score = score
                final_move = move
            # Check if current_score wins game
            if score >= win_game:
                final_move = move
        # Check if current_score wins game
        if score >= win_game:
            final_move = move
        curr_depth += curr_depth + depth_multiplier  # add depth
    return final_move


def minimax(moves_list, updated_board, comp_boards, depth, alpha, beta, ally, start_time):
    """
    Recursive minimax implementation for traversal down a node at a given depth
    :param moves_list: a list of possible
    :param updated_board: an updated board
    :param comp_boards: a list of completed boards
    :param depth: a set depth to search at
    :param alpha: alpha for alpha-beta pruning
    :param beta: beta for alpha-beta pruning
    :param ally: bool Pnum or Enum (player or enemy making move)
    :param start_time: time iterative-depining start
    :return: won (points won for a move) or Nnne (when time elapsed exceeds move_time
    """
    # miniMax function with Alpha-Beta Pruning implemented
    if depth == 0:
        won = points_won(updated_board, comp_boards)
        return won  # checks the number of points won
    if time.time() - start_time > move_time:
        return None  # returns None when time limit has elapsed
    if ally:
        # Pnum's (Player's) Turn
        max_eval = -math.inf
        for possible_move in moves_list:
            # copy list of completed boards
            temp_comp_boards = np.copy(comp_boards, 'K')
            # update a board with a given possible move
            temp_updated_board = updateBoard(possible_move, updated_board, temp_comp_boards, Pnum)
            eval = minimax(nextMoves(possible_move[1], temp_comp_boards, temp_updated_board), temp_updated_board,
                           temp_comp_boards, depth - 1, alpha, beta, not ally, start_time)
            max_eval = max(max_eval, eval)
            # alpha-beta pruning
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # Enum's (Enemies's) Turn
        min_eval = math.inf
        for possible_move in moves_list:
            # copy list of completed boards
            temp_comp_boards = np.copy(comp_boards, 'K')
            # update a board with a given possible move
            temp_updated_board = updateBoard(possible_move, updated_board, temp_comp_boards, Enum)
            eval = minimax(nextMoves(possible_move[1], temp_comp_boards, temp_updated_board), temp_updated_board,
                           temp_comp_boards, depth - 1, alpha, beta, ally, start_time)
            min_eval = min(min_eval, eval)
            # alpha-beta pruning
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def nextMoves(last_local_move, c_board_list, updated_board):
    """

    :param last_local_move: the last local move on a board
    :param c_board_list: a list of completed boards
    :param updated_board: and updated board
    :return: free_moves: list of available moves
    """
    free_moves = []
    if c_board_list[last_local_move] != 0:  # check if last move was to a complete board
        for i in range(0, 9):  # generates a list of free spaces for all incomplete boards
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
    """
    Updates a given temporary board's with a given temporary move
    :param tempMove: a temporary move
    :param tempBoard: a temporary global board configruation
    :param tempList: a temporary list of completed boards based on the temporary glboal configuration
    :param num: Player (num) or Enemy (Enum) move
    :return: copy_board: a copy of the board
    """
    copy_board = np.copy(tempBoard, 'K').copy()  # copy board
    copy_board[tempMove[0]][tempMove[1]] = num  # update board
    checkBoardComplete(tempMove[1], tempList, copy_board)
    return copy_board


def points_won(temp_board, temp_comp_board):
    """
    # static evaluation (utility) function that returns number of points won by Pnum (Player) for any given
    global board
    :param temp_board: temporary global board configuration
    :param temp_comp_board: temporary list of completed boards based on global board configuration
    :return: points_sum: total points won by the Pnum (Player)
    """
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
    """
    Checks whether a board has been complete after a move and updates the global complete_boards list
    :param g_board, c_boards (list of complete boards), a_board (global board config).
    :return: list of complete boards where 0 = incomplete, Pnum (won by Player), Enum (won by Enemy) or 3 (tiee)
    """
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
