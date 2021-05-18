import math
import itertools

# reference: https://gist.github.com/adrian17/3a6def9f9ba22076233c
# reference: https://docs.python.org/3/library/itertools.html

# The scope of help I get from the websites:
# for finding the possible combinition and finding the available candidates,
# I read the codes on the first website and then viewed the other websites listed
# to learn about the functions that I did not know
# Then I rewrite the codes

# use itertools to find all possible combinition given the sum, block and available values
def possible_combinations(values, n, summ):
    result = []
    possible = itertools.combinations(values, n)
    for ele in possible:
        if sum(ele) == summ:
            result.append(ele)
    return result


# Given the puzzle and clues, and a specific value for a position
def make_aval(kakuro, clues, pos):
    parent = []
    avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for group in clues:
        #interpret the clue
        summ = group[0]
        subgroups = group[1]
        # find all available numbers
        for subgroup in subgroups:
            avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if subgroup == pos:
                prohib = []
                count = 0
                nonempty = []
                for subgroup in subgroups:
                    if subgroup != pos:
                        # keep track of the number of blocks that are still empty
                        count = count+1
                        if kakuro[subgroup[0]][subgroup[1]][1] != 0:
                            # keep track of other numbers entered before
                            nonempty.append(kakuro[subgroup[0]][subgroup[1]][1])
                            prohib.append(kakuro[subgroup[0]][subgroup[1]][1])
                for ele in prohib:
                    if ele in avail:
                        avail.remove(ele)
                n_empty = count + 1 - len(nonempty)
        		# a summ you have to get, minus the numbers already written
                for elem in nonempty:
                    summ = summ - elem
                combinations = possible_combinations(avail, n_empty, summ)
                # have a list of non-repeat available numbers
                lis = []
                for comb in combinations:
                    for num in comb:
                        if num not in lis:
                            lis.append(num)
                # append it as one of the parents of this position
                parent.append(lis)

    avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = []
    # if a block is only affected by a clue, present that parent
    for candidate in avail:
        if len(parent) == 1:
            return parent[0]
        else:
            # if it's affected by two, find the intersection
            if candidate in parent[0] and candidate in parent[1]:
                result.append(candidate)
    return result


def solve(kakuro, clues):
    status = 0
    remain = []

    # have a list of remaining blocks
    for i in range(len(kakuro)):
        for j in range(len(kakuro[0])):
            if kakuro[i][j][0] != "clue" and kakuro[i][j][1] == 0:
                status = 1
                remain.append((i, j))

    # if all blockes are full, print the puzzle and exit
    if status == 0:
        print(kakuro)
        print("exit")
        exit()

    # if not full, start from the beginning
    position = remain[0]
    candidates = make_aval(kakuro, clues, position)
    # if not candidates available, go back to last step
    if candidates == []:
        return
    # try each possible value, also clear the blocks entered in previous failed tries
    for value in candidates:
        for i in range(len(kakuro)):
            for j in range(len(kakuro[0])):
                if kakuro[i][j][0] != "clue":
                    if i > position[0]:
                        kakuro[i][j][1] = 0
                    elif i == position[0] and j > position[1]:
                        kakuro[i][j][1] = 0
        kakuro[position[0]][position[1]] = ["blank", value]
        solve(kakuro, clues)


def main():
    kakuro = [[["clue", -1, -1], ["clue", -1, -1], ["clue", -1, 21], ["clue", -1, 14], ["clue", -1, -1]],
              [["clue", -1, -1], ["clue", 11, 16], ["blank", 0], ["blank", 0], ["clue", -1, 14]],
              [["clue", 21, -1], ["blank", 0], ["blank", 0], ["blank", 0], ["blank", 0]],
              [["clue", 16, -1], ["blank", 0], ["blank", 0], ["blank", 0], ["blank", 0]],
               [["clue", -1, -1], ["clue", 17, -1], ["blank", 0], ["blank", 0], ["clue", -1, -1]]]

    clues = []
    # build a clue table for the puzzle
    for i in range(len(kakuro)):
        for j in range(len(kakuro[0])):
            if kakuro[i][j][0] == "clue":
                if kakuro[i][j][1] != -1:
                    summ = kakuro[i][j][1]
                    curr = []
                    # to keep track of original index
                    a = i
                    b = j
                    j = j+1
                    while kakuro[i][j][0] != "clue":
                        curr.append((i, j))
                        j = j+1
                        if j >= len(kakuro[0]):
                            break
                    clues.append((summ, curr))
                    i = a
                    j = b
                if kakuro[i][j][2] != -1:
                    summ = kakuro[i][j][2]
                    curr = []
                    a = i
                    b = j
                    i = i+1
                    while kakuro[i][j][0] != "clue":
                        curr.append((i, j))
                        i = i+1
                        if i >= len(kakuro):
                            break
                    clues.append((summ, curr))
                    i = a
                    j = b

    solve(kakuro, clues)

main()
