import math
import itertools

# use itertools to find all possible combinition given the sum, block and available values
def possible_combinations(values, n, summ):
    result = []
    possible = itertools.combinations(values, n)
    for ele in possible:
        if sum(ele) == summ:
            result.append(ele)
    return result


def main():
    kakuro = [[["clue", -1, -1], ["clue", -1, -1], ["clue", -1, -1], ["clue", -1, 22], ["clue", -1, 9]],
              [["clue", -1, -1], ["clue", -1, -1], ["clue", 11, 18], ["blank", 0], ["blank", 0]],
              [["clue", -1, -1], ["clue", 23, 11], ["blank", 0], ["blank", 0], ["blank", 0]],
              [["clue", 22, -1], ["blank", 0], ["blank", 0], ["blank", 0], ["clue", -1, -1]],
               [["clue", 4, -1], ["blank", 0], ["blank", 0], ["clue", -1, -1], ["clue", -1, -1]]]
    #initialize group and subgroup table
    group = []
    subgroup = []
    for i in range(len(kakuro)):
        group.append([])
        subgroup.append([])
        for j in range(len(kakuro[0])):
            group[i].append([])
            subgroup[i].append([])

    # build a group table to keep track of all the clues and the positions affected by them
    # build a subgroup table to keep track of which clue is affecting each blank
    for i in range(len(kakuro)):
        for j in range(len(kakuro[0])):
            if kakuro[i][j][0] == "clue":
                if kakuro[i][j][1] != -1:
                    sum = kakuro[i][j][1]
                    curr = []
                    a = i
                    b = j
                    j = j+1
                    while kakuro[i][j][0] != "clue":
                        curr.append((i, j))
                        subgroup[i][j].append([a, b, 0])
                        j = j+1
                        if j >= len(kakuro[0]):
                            break
                    group[a][b].append([sum, curr])
                    i = a
                    j = b
                else:
                    group[i][j].append((-1, []))
                if kakuro[i][j][2] != -1:
                    sum = kakuro[i][j][2]
                    curr = []
                    a = i
                    b = j
                    i = i+1
                    while kakuro[i][j][0] != "clue":
                        curr.append((i, j))
                        subgroup[i][j].append([a, b, 1])
                        i = i+1
                        if i >= len(kakuro):
                            break
                    group[a][b].append([sum, curr])
                    i = a
                    j = b
                else:
                    group[i][j].append((-1, []))
            else:
                group[i][j].append((-1, []))
                group[i][j].append((-1, []))



    # initialize a candidate table to keep track of the current available numbers
    candidates = []
    for row in range(len(kakuro)):
        candidates.append([])
        for col in range(len(kakuro[0])):
            candidates[row].append([])
            if kakuro[row][col][0] == "clue":
                candidates[row][col] = [-1]
            else:
                candidates[row][col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # check the initial clues
    stack = []
    for r in group:
        for single_clue in r:
            for order in (0, 1):
                if single_clue[order] != (-1, []):
                    for pos in single_clue[order][1]:
                        avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        number = len(single_clue[order][1])
                        sum = single_clue[order][0]
                        combinations = possible_combinations(avail, number, sum)
                        lis = []
                        for comb in combinations:
                            for num in comb:
                                if num not in lis:
                                    lis.append(num)
                        new = []
                        for ele in candidates[pos[0]][pos[1]]:
                            if ele in lis:
                                new.append(ele)
                        candidates[pos[0]][pos[1]] = new
                        # whenever the candidates table get updated, check the length
                        # if equal to 1, put into stack
                        if len(candidates[pos[0]][pos[1]]) == 1:
                            stack.append(pos)

    # while the stack is not empty
    while stack:
        # take the first and implement the puzzle
        position = stack[0]
        stack.remove(position)
        i = position[0]
        j = position[1]
        kakuro[i][j] = ["blank", candidates[i][j][0]]

        # define variables for later use
        for clue in subgroup[i][j]:
            posi_1 = (subgroup[i][j][0][0], subgroup[i][j][0][1])
            order_1 = subgroup[i][j][0][2]
            posi_2 = (subgroup[i][j][1][0], subgroup[i][j][1][1])
            order_2 = subgroup[i][j][1][2]
        for affected in group[posi_1[0]][posi_1[1]][order_1][1]:
            if affected != position:
                avail_this = candidates[affected[0]][affected[1]]
                avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                if candidates[i][j][0] in avail:
                    avail.remove(candidates[i][j][0])
                number = 0
                sum = group[posi_1[0]][posi_1[1]][order_1][0]
                for blank in group[posi_1[0]][posi_1[1]][order_1][1]:
                    if kakuro[blank[0]][blank[1]][1] == 0:
                        number = number + 1
                    else:
                        sum = sum - kakuro[blank[0]][blank[1]][1]
                combinations = possible_combinations(avail, number, sum)
                lis = []
                for comb in combinations:
                    for num in comb:
                        if num not in lis:
                            lis.append(num)
                new = []
                for ele in candidates[affected[0]][affected[1]]:
                    if ele in lis:
                        new.append(ele)
                candidates[affected[0]][affected[1]] = new
                # find the intersection between current available numnbers and
                # the numbers available for sum requirement
                if len(candidates[affected[0]][affected[1]]) == 1:
                    stack.append(affected)
        # do this for the other direction
        for affected in group[posi_2[0]][posi_2[1]][order_2][1]:
            if affected != position:
                avail = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                if candidates[i][j][0] in avail:
                    avail.remove(candidates[i][j][0])
                number = 0
                sum = group[posi_2[0]][posi_2[1]][order_2][0]
                for blank in group[posi_2[0]][posi_2[1]][order_2][1]:
                    if kakuro[blank[0]][blank[1]][1] == 0:
                        number = number + 1
                    else:
                        sum = sum - kakuro[blank[0]][blank[1]][1]
                combinations = possible_combinations(avail, number, sum)
                lis = []
                for comb in combinations:
                    for num in comb:
                        if num not in lis:
                            lis.append(num)
                new = []
                for ele in candidates[affected[0]][affected[1]]:
                    if ele in lis:
                        new.append(ele)
                candidates[affected[0]][affected[1]] = new
                if len(candidates[affected[0]][affected[1]]) == 1:
                    stack.append(affected)

    # output the puzzle
    print(kakuro)
main()
