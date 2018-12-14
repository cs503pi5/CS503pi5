# 0 - no connection
# 1 - straight connection
# 2 - straight curved connection right
# 3 - straight curved connection left
# 4 - intersection straight
# 5 - intersection right
# 6 - intersection left
# 7 - straight speed track inside
# 8 - straight speed track outside
# 9 - intersection speed track inside
# 10 - intersection speed track outside
# 11 - intersection curved connection right
# 12 - intersection curved connection left

# contains the neighbors each state can go to. The index of value in the list == the actual state number 
one = [0,0,0,6,0,0,0,0,0,0,0,4]
two = [0,0,0,0,5,0,0,0,4,0,0,0]   
three = [0,0,0,0,0,0,0,5,0,0,0,6]
four = [0,0,0,0,0,0,12,0,0,0,11,0]
five = [0,0,6,0,0,0,3,0,0,0,0,0]
six = [0,0,5,0,0,0,0,0,0,0,2,0]
seven = [6,0,0,0,0,0,0,0,0,8,0,0]
eight = [0,0,0,0,0,11,0,0,0,10,0,0]
nine = [5,0,0,0,0,2,0,0,0,0,0,0]
ten = [0,6,0,0,3,0,0,0,0,0,0,0]
eleven = [0,5,0,0,0,0,0,0,7,0,0,0]
twelve = [0,0,0,0,12,0,0,0,9,0,0,0]

map = [one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve]
weighted_map = []
weightless_map = []
wm = {}
stateMachine = []
#sequence = []
#states = 0

# returns shortest list of states/numberss to get from state to end state
def find_shortest_path(start, end, path=[]):
    global map,stateMachine # map is a list of state's neighbors list, 
    path = path + [start] # add start state's number to the path
    if start == end: # return if start == end
        stateMachine = path
        return path
    shortest = None
    neighbors = [x for x in range(len(map[start])) if map[start][x] != 0] # for each element in the start states neighbor list, add its index if != 0
    for node in neighbors:
        if node not in path:
            newpath = find_shortest_path(node, end, path) # recurse down on each neighbor
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    stateMachine = shortest # statemachine == shortest at the end of it
    return shortest


def statesToInstructions(path):
    global map
    seq = []
    for i in range(len(path)-1):
        s = map[stateMachine[i]][stateMachine[i+1]]
        if (s == 0):
            return False
        else:
            seq.append(s)
    return seq

def printInstructions(seq):
    for i in seq:
        if (i == 0):
            print("no connection - FAILURE")
            return False
        elif (i == 1):
            print("straight connection")
        elif (i == 2):
            print("straight curved connection right")
        elif (i == 3):
            print("straight curved connection left")
        elif (i == 4):
            print("intersection straight")
        elif (i == 5):
            print("intersection right")
        elif (i == 6):
            print("intersection left")
        elif (i == 7):
            print("straight speed track inside")
        elif (i == 8):
            print("straight speed track outside")
        elif (i == 9):
            print("intersection speed track inside")
        elif (i == 10):
            print("intersection speed track outside")
        elif (i == 11):
            print("intersection curved connection right")            
        else:
            print("intersection curved connection left")

def getPath():
    a = input("Start Node: ")
    a = a-1
    b = input("End Node: ")
    b = b-1
    path = find_shortest_path(a,b)
    print([x+1 for x in path])
    sequence = statesToInstructions(path)
    printInstructions(sequence)
    return(sequence)