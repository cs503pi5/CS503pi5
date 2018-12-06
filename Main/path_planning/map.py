from dijkstra import dijkstra, shortest_path
# 0 - no connection
# 1 - straight connection
# 2 - curved connection right
# 3 - curved connection left
# 4 - intersection straight
# 5 - intersection right
# 6 - intersection left

zero = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
one = [5,0,0,0,6,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
two = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
three = [4,0,5,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
four = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
five = [6,0,4,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
six = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
seven = [0,0,6,0,4,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eight = [0,0,0,0,0,0,0,0,0,0,0,6,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nine = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
ten = [0,0,0,0,0,0,0,0,0,5,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eleven = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
twelve = [0,0,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
thirteen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0]
fourteen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,4,0,0,0,0,0,0,0,0,0,0,0,0]
fifteen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0]
sixteen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0]
seventeen = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eighteen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nineteen = [0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
twenty = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,4,0,0,0,0,0,0]
twentyone = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0]
twentytwo = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,6,0,0,0,0,0,0]
twentythree = [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
twentyfour = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,0,0,0]
twentyfive = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
twentysix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,4]
twentyseven = [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
twentyeight = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,6]
twentynine = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
thirty = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,5,0,0]
thirtyone = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0]

map = [zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,twentythree,twentyfour,twentyfive,twentysix,twentyseven,twentyeight,twentynine,thirty,thirtyone]
weighted_map = []
weightless_map = []
wm = {}
stateMachine = []
sequence = []
states = 0
repeating = False

def weight_map():
    global weightless_map, weighted_map, map
    for x in range(32):
        l = []
        for y in range(32):
            if (map[x][y] == 0):
                l.append(0)
            elif (map[x][y] == 1):
                l.append(1)
            elif (map[x][y] == 2):
                l.append(1)
            elif (map[x][y] == 3):
                l.append(10000)
            elif (map[x][y] == 4):
                l.append(1)
            elif (map[x][y] == 5):
                l.append(1)
            else:
                l.append(10000)
        weighted_map.append(l)
    x = 0
    y = 0
    l = []
    for x in range(32):
        l = []
        for y in range(32):
            if (map[x][y] == 0):
                l.append(0)
            elif (map[x][y] == 1):
                l.append(1)
            elif (map[x][y] == 2):
                l.append(1)
            elif (map[x][y] == 3):
                l.append(1)
            elif (map[x][y] == 4):
                l.append(1)
            elif (map[x][y] == 5):
                l.append(1)
            else:
                l.append(1)
        weightless_map.append(l)

def weightedToDict():
    global weight_map, wm
    for x in range(32):
        row = {}
        for y in range(32):
            if (map[x][y] != 0):
                row[y] = weighted_map[x][y]
        wm[x] = row           


def printInstructions():
    global sequence, repeating
    for i in sequence:
        if (i == 0):
            print("no connection - FAILURE")
            return False
        elif (i == 1):
            print("go straight")
        elif (i == 2):
            print("follow road, right turn")
        elif (i == 3):
            print("follow road, left turn")
        elif (i == 4):
            print("intersection, go straight")
        elif (i == 5):
            print("intersection, turn right")
        else:
            print("intersection, turn left")
    if (repeating):
        print("repeat")
    else:
        print("end of instructions")


def getStateMachine(given = None):
    global stateMachine,states
    print("Enter state machine:")
    data = 0
    while (data != -1):
        data = input()
        stateMachine.append(data)
        states = states+1
    stateMachine = stateMachine[:-1]
    states = states - 1

def stateMachineToInstructions():
    global map, stateMachine
    for i in range(states-1):
        s = map[stateMachine[i]][stateMachine[i+1]]
        if (s == 0):
            return False
        else:
            sequence.append(s)
    return True

def isRepeating():
    global repeating
    print("Is the machine repeating? y/n")
    ans = raw_input()
    if (ans == "y"):
        repeating = True
        return True
    elif (ans == "n"):
        repeating = False
        return True
    else:
        return False

def find_shortest_path(start, end, path=[]):
    global map,stateMachine
    path = path + [start]
    if start == end:
        stateMachine = path
        return path
    shortest = None
    neighbors = [x for x in range(len(map[start])) if map[start][x] != 0]
    for node in neighbors:
        if node not in path:
            newpath = find_shortest_path(node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    stateMachine = shortest
    return shortest

if __name__ == "__main__":
    print("Modes: a - given state machine, b - shortest path distance, c - shortest path weighted")
    ans = raw_input("Select mode: ")
    if (ans == "a"):
        if (isRepeating() == False):
            print("INVALID -- QUITTING")
            exit(0)
        getStateMachine()
        if (not stateMachineToInstructions()):
            print("INVALID STATE MACHINE")
        else:
            printInstructions()
    elif (ans == "b"):
        a = input("Start Node: ")
        b = input("End Node: ")
        print(find_shortest_path(a,b))
        states = len(stateMachine)
        if (not stateMachineToInstructions()):
            print("INVALID STATE MACHINE")
        else:
            printInstructions()
    elif (ans == "c"):
        weight_map()
        weightedToDict()
        a = input("Start Node: ")
        b = input("End Node: ")
        print(shortest_path(wm, a, b))
        stateMachine = shortest_path(wm,a,b)
        states = len(stateMachine)
        if (not stateMachineToInstructions()):
            print("INVALID STATE MACHINE")
        else:
            printInstructions()
    else:
        print("incorrect input - failure")
        exit(0)