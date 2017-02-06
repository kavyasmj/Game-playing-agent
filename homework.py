# ----------------------------------------------- Header files ---------------------------------------------------------
import string
import numpy as np
import copy
# ----------------------------------------------- Data Declarations ---------------------------------------------------
# global variables
alphabets = list(string.ascii_uppercase)
mode = ""
youPlay = ""
oppPlay = ""
depth_limit = 0
n = 0
score_matrix = None
pos_matrix = None
n_pos_matrix = None

# ---------------------------------------------- Method Declarations ---------------------------------------------------
# ----------------------------------------------------Fetch input-------------------------------------------------------
# Fetch input from the file
def fetch_input():

    global n, mode, youPlay, depth_limit, score_matrix, pos_matrix, oppPlay, n_pos_matrix
    gv_fh_input = open("input.txt", "r")

    # read the file and set the global vars
    n = int(gv_fh_input.readline().rstrip())
    mode = gv_fh_input.readline().rstrip()
    youPlay = gv_fh_input.readline().rstrip()
    if youPlay == "X":
        oppPlay = "O"
    elif youPlay == "O":
        oppPlay = "X"
    depth_limit = int(gv_fh_input.readline().rstrip())

    score_matrix = [[0 for x in range(0, n)] for y in range(0, n)]
    for i in xrange(0, n):
        score_row_list = gv_fh_input.readline().rstrip().split(" ")
        s_i_list = score_matrix[i]
        for j in xrange(0, n):
            s_i_list[j] = int(score_row_list[j])


    pos_matrix = [[0 for x in range(0, n)] for y in range(0, n)]
    for i in xrange(0, n):
        pos_row_list = list(gv_fh_input.readline().rstrip())
        pos_i_list = pos_matrix[i]
        for j in xrange(0, n):
            pos_i_list[j] = pos_row_list[j]

    # n_pos_matrix = np.array([list(word) for word in pos_matrix])
    # n_pos_matrix = np.empty((len(pos_matrix), n))
    # for i, x in enumerate(pos_matrix):
    #     n_pos_matrix[i] = pos_matrix[i]


# -------------------------------------------MINI-MAX--------------------------------------------------------------------

def term_test(p_matrix, depth_traversed):
    global youPlay, oppPlay, score_matrix
    gs = 0

    if depth_traversed == depth_limit:
        for i in xrange(0, n):
            p_i_list = p_matrix[i]
            for j in xrange(0, n):
                if p_i_list[j] == youPlay:
                    gs += score_matrix[i][j]
                elif p_i_list[j] == oppPlay:
                    gs -= score_matrix[i][j]
        return gs

    for i in xrange(0, n):
        p_i_list = p_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                return False
            elif p_i_list[j] == youPlay:
                gs += score_matrix[i][j]
            elif p_i_list[j] == oppPlay:
                gs -= score_matrix[i][j]
    return gs


def get_move(p_matrix, i, j, caller, moves_list_raid):
    # Search all stake actions before raid actions,
    # search the board in order (top left to bottom right, row by row) for each action type
    raid_row = []

    if caller == "min":
        local_you_play = oppPlay
        local_opp_play = youPlay
    else:
        local_you_play = youPlay
        local_opp_play = oppPlay

    new_stake_matrix = copy.deepcopy(p_matrix)
    new_stake_matrix[i][j] = local_you_play
    new_move_matrix = copy.deepcopy(new_stake_matrix)

    raid_possible = False
    raid_useful = False

    blank_left = j - 1
    blank_right = j + 1
    blank_up = i - 1
    blank_down = i + 1

    if blank_left >= 0:
        if p_matrix[i][blank_left] == local_you_play:
            raid_possible = True
        elif p_matrix[i][blank_left] == local_opp_play:
            raid_useful = True
            new_move_matrix[i][blank_left] = local_you_play

    if blank_right < n:
        if p_matrix[i][blank_right] == local_you_play:
            raid_possible = True
        elif p_matrix[i][blank_right] == local_opp_play:
            raid_useful = True
            new_move_matrix[i][blank_right] = local_you_play

    if blank_up >= 0:
        if p_matrix[blank_up][j] == local_you_play:
            raid_possible = True
        elif p_matrix[blank_up][j] == local_opp_play:
            raid_useful = True
            new_move_matrix[blank_up][j] = local_you_play

    if blank_down < n:
        if p_matrix[blank_down][j] == local_you_play:
            raid_possible = True
        elif p_matrix[blank_down][j] == local_opp_play:
            raid_useful = True
            new_move_matrix[blank_down][j] = local_you_play

    if (raid_possible is True) and (raid_useful is True):
        raid_row.append(new_move_matrix)
        raid_row.append(j)
        raid_row.append(i)
        moves_list_raid.append(raid_row)

    return new_stake_matrix


def min_val(p_matrix, depth_traversed):

    depth_traversed += 1

    # check if you've reached the utility func
    ret_val = term_test(p_matrix, depth_traversed)
    if type(ret_val) is int:
        return ret_val

    v = float('inf')
    moves_list_raid = []

    for i in xrange(0, n):
        p_i_list = p_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(p_matrix, i, j, "min", moves_list_raid))
                temp_v = max_val(temp_p_matrix, depth_traversed)
                if temp_v < v:
                    v = temp_v

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_v = max_val(temp_p_matrix, depth_traversed)
        if temp_v < v:
            v = temp_v

    return v


def max_val(p_matrix, depth_traversed):

    depth_traversed += 1

    # check if you've reached the utility func
    ret_val = term_test(p_matrix, depth_traversed)
    if type(ret_val) is int:
        return ret_val

    v = float('-inf')
    moves_list_raid = []

    for i in xrange(0, n):
        p_i_list = p_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(p_matrix, i, j, "max", moves_list_raid))
                temp_v = min_val(temp_p_matrix, depth_traversed)
                if temp_v > v:
                    v = temp_v

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_v = min_val(temp_p_matrix, depth_traversed)
        if temp_v > v:
            v = temp_v

    return v


def mini_max():
    global pos_matrix

    move = ""
    move_type = ""
    p_matrix = None
    v = float('-inf')
    moves_list_raid = []

    for i in xrange(0, n):
        pos_i_list = pos_matrix[i]
        for j in xrange(0, n):
            if pos_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(pos_matrix, i, j, "max", moves_list_raid))
                temp_v = min_val(temp_p_matrix, 0)
                if temp_v > v:
                    v = temp_v
                    pos_i = i + 1
                    move_type = "S"
                    move = alphabets[j] + str(pos_i)
                    p_matrix = copy.deepcopy(temp_p_matrix)

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_v = min_val(temp_p_matrix, 0)
        if temp_v > v:
            v = temp_v
            move_type = "R"
            move = alphabets[raid_row.pop(0)] + str(raid_row.pop(0)+1)
            p_matrix = copy.deepcopy(temp_p_matrix)

    if p_matrix:
        print_to_output(move, move_type, p_matrix)


def alpha_beta_min_val(p_matrix, depth_traversed, alpha, beta):

    depth_traversed += 1

    # check if you've reached the utility func
    ret_val = term_test(p_matrix, depth_traversed)
    if type(ret_val) is int:
        return ret_val

    moves_list_raid = []

    for i in xrange(0, n):
        p_i_list = p_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(p_matrix, i, j, "min", moves_list_raid))
                temp_beta = alpha_beta_max_val(temp_p_matrix, depth_traversed, alpha, beta)
                if temp_beta < beta:
                    beta = temp_beta
                if beta <= alpha:  # prune and return alpha
                    return alpha

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_beta = alpha_beta_max_val(temp_p_matrix, depth_traversed, alpha, beta)
        if temp_beta < beta:
            beta = temp_beta
        if beta <= alpha:  # prune and return alpha
            return alpha

    return beta


def alpha_beta_max_val(p_matrix, depth_traversed, alpha, beta):

    depth_traversed += 1

    # check if you've reached the utility func
    ret_val = term_test(p_matrix, depth_traversed)
    if type(ret_val) is int:
        return ret_val

    moves_list_raid = []

    for i in xrange(0, n):
        p_i_list = p_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(p_matrix, i, j, "max", moves_list_raid))
                temp_alpha = alpha_beta_min_val(temp_p_matrix, depth_traversed, alpha, beta)
                if temp_alpha > alpha:
                    alpha = temp_alpha
                if alpha >= beta:  # prune and return beta
                    return beta

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_alpha = alpha_beta_min_val(temp_p_matrix, depth_traversed, alpha, beta)
        if temp_alpha > alpha:
            alpha = temp_alpha
        if alpha >= beta:  # prune and return beta
            return beta

    return alpha


def alpha_beta():

    global pos_matrix

    move = ""
    move_type = ""
    p_matrix = None

    alpha = float('-inf')
    beta = float('inf')
    moves_list_raid = []

    for i in xrange(0, n):
        p_i_list = pos_matrix[i]
        for j in xrange(0, n):
            if p_i_list[j] == ".":
                temp_p_matrix = copy.deepcopy(get_move(pos_matrix, i, j, "max", moves_list_raid))
                temp_alpha = alpha_beta_min_val(temp_p_matrix, 0, alpha, beta)
                if temp_alpha > alpha:
                    alpha = temp_alpha
                    pos_i = i + 1
                    move_type = "S"
                    move = alphabets[j] + str(pos_i)
                    p_matrix = copy.deepcopy(temp_p_matrix)

    for raid_row in moves_list_raid:
        temp_p_matrix = copy.deepcopy(raid_row.pop(0))
        temp_alpha = alpha_beta_min_val(temp_p_matrix, 0, alpha, beta)
        if temp_alpha > alpha:
            alpha = temp_alpha
            move_type = "R"
            move = alphabets[raid_row.pop(0)] + str(raid_row.pop(0) + 1)
            p_matrix = copy.deepcopy(temp_p_matrix)

    if p_matrix:
        print_to_output(move, move_type, p_matrix)


# ---------------------------------------------Output logic-------------------------------------------------------------
# use position specifically as value can be same at 2 positions
def print_to_output(move, move_type, final_matrix):

    # create the output file
    gv_fh_output = open("output.txt", "w")

    if move_type == "S":
        op_str = move + " " + "Stake" + "\n"
        gv_fh_output.write(op_str)
    elif move_type == "R":
        op_str = move + " " + "Raid" + "\n"
        gv_fh_output.write(op_str)

    for i in xrange(0, n):
        for j in xrange(0, n):
            gv_fh_output.write(final_matrix[i][j])
        gv_fh_output.write("\n")

    gv_fh_output.close()


# ---------------------------------------------Execution Starts Here----------------------------------------------------
fetch_input()

if mode == "MINIMAX":
    mini_max()
elif mode == "ALPHABETA":
    alpha_beta()

