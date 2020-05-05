'''
Miguel Zavala
4/26/20
CISC481-Intro to AI
Homework 4: Q-learning
Dr.Rahmat
'''

from enum import Enum
import math,random

#The agent's possible moves:
class MOVES(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
    EXIT = 'exit' #?

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if(isinstance(other,str)):
            return self.value==str
        elif(isinstance(other,MOVES)):
            return other.value==self.value

#The different tile types/states:
class TILE_TYPES(Enum):
    START = 'start'
    GOAL = 'goal'
    FORBIDDEN = 'forbidden'
    WALL = 'wall'
    NORMAL = 'normal'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other,TILE_TYPES):
            if(other.value==self.value):
                return True
        elif(isinstance(other,str)):
            if(self.value==other):
                return True

        return False

class Tile:
    def __init__(self, type=TILE_TYPES.NORMAL,unique_index:int=-1):
        #self.qvalue = 0 #All tile q values start at 0
        self.value = 0 #maybe not using
        self.type = type
        self.unique_index = unique_index

        self.reward = 0

        if(self.type==TILE_TYPES.GOAL):
            self.qvalues = {
                "exit":QL.REACH_GOAL
            }
            self.value = QL.REACH_GOAL
            self.reward = QL.REACH_GOAL
        elif(self.type==TILE_TYPES.FORBIDDEN):
            self.qvalues = {
                'exit':QL.REACH_FORBIDDEN
            }
            self.value = QL.REACH_FORBIDDEN
            self.reward = QL.REACH_FORBIDDEN
        else:
            self.qvalues = {
                "north":0,
                "south":0,
                "west":0,
                "east":0
            }


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "("+str(self.type)+"|Index "+str(self.unique_index)+")"

#Board class made up of Tile lists:
class Board(list):
    def __init__(self,n_Rows:int=4,n_Columns:int=4, start_index = 2):
        self.n_Rows = n_Rows
        self.n_Columns = n_Columns
        self.size = self.n_Rows*self.n_Columns
        self.createBoard(self.n_Rows,self.n_Columns)
        Board.getTileUniqueIndex(self,start_index).type = TILE_TYPES.START #Setting the start tile
        self.agent = QLearningAgent(self,start_index) #Starts the agent at 'start_index'

    def createBoard(self,n_Rows:int,n_Columns:int)->None:
        self.clear() #Clears the current board

        curr_index = 1
        for r in range(n_Rows):
            current_row = []
            for c in range(n_Columns):
                current_row.append(Tile(unique_index=curr_index))
                curr_index+=1

            #Adding the row to the board
            self.insert(0,current_row)

    def getTileUniqueIndex(boardObject,unique_index:int)->Tile:
        row = (boardObject.n_Rows)-math.floor(unique_index/boardObject.n_Rows)-1
        column = (unique_index-1)%(boardObject.n_Columns)

        #Re-adjusts the row if the row is divisible by the number of rows in the board
        if(unique_index!=0 and unique_index%boardObject.n_Rows==0):
            row +=1
        if(row<0 or row>=boardObject.n_Rows):
            return None
        if(column<0 or column>=boardObject.n_Columns):
            return None

        #print(row,column)

        return boardObject[row][column]

    def getRowColumnFromUniqueIndex(boardObject,unique_index:int)->tuple:
        row = (boardObject.n_Rows)-math.floor(unique_index/boardObject.n_Rows)-1
        column = (unique_index-1)%(boardObject.n_Columns)

        #Re-adjusts the row if the row is divisible by the number of rows in the board
        if(unique_index!=0 and unique_index%boardObject.n_Rows==0):
            row +=1
        if(row<0 or row>=boardObject.n_Rows):
            return None
        if(column<0 or column>=boardObject.n_Columns):
            return None

        #print(row,column)

        return (row,column)

    def getTileFromLocationGivenMove(boardObject,rowcolumntuple,move):
        currLocation = rowcolumntuple
        currRow = currLocation[0]
        currColumn = currLocation[1]

        if(move==MOVES.NORTH.value):
            next_tile= boardObject[currRow - 1][currColumn]
            return next_tile

        elif(move==MOVES.SOUTH.value):
            next_tile= boardObject[currRow + 1][currColumn]
            return next_tile

        elif(move==MOVES.EAST.value):
            next_tile= boardObject[currRow][currColumn+1]
            return next_tile

        elif(move==MOVES.WEST.value):
            next_tile=boardObject[currRow][currColumn-1]
            return next_tile

        return None

    def isRowColumnWithinBounds(boardObject,rowcolumntuple:tuple):
        row = rowcolumntuple[0]
        column = rowcolumntuple[1]

        if (row >= 0 and row < boardObject.n_Rows and column >= 0 and column < boardObject.n_Columns):
            return True
        else:
            return False

    def printBoard(boardObject):
        print("BOARD STATES:")
        for i in range(boardObject.n_Rows):
            currRow = ""
            for j in range(boardObject.n_Columns):
                currRow+="("+str(boardObject[i][j].unique_index)+":"+str(boardObject[i][j].type)+")"

            print(currRow)

    def printTileRewardsBoard(boardObject):
        print("Rewards:")
        for i in range(boardObject.n_Rows):
            currRow = ""
            for j in range(boardObject.n_Columns):
                currRow += "("+str(boardObject[i][j].unique_index)+":"+str(boardObject[i][j].reward)+")"


            print(currRow)

    def printQActionValuesBoard(boardObject):
        print("Q-Values:")
        for i in range(boardObject.n_Rows):
            currRow = ""
            for j in range(boardObject.n_Columns):
                currRow += "("+str(boardObject[i][j].unique_index)+":"+str(boardObject[i][j].qvalues)+")"


            print(currRow)

    def getQStateMaxQActionValue(boardObject,qstate:Tile)->tuple:
        sortedQActionsValuesTuple = sorted(qstate.qvalues.items(), key=lambda x: x[1], reverse=True)
        #print(sortedQActionsValuesTuple)

        maxvalue = -float("inf")
        maxaction = None

        for i in range(len(sortedQActionsValuesTuple)):
            #print("TUPLE:"+str(sortedQActionsValuesTuple))
            currentActionValue = sortedQActionsValuesTuple[i]
            currentaction = currentActionValue[0]
            currentvalue = currentActionValue[1]

            #print(currentaction)

            if(boardObject.agent.isValidMove(currentaction)):
                maxvalue = currentvalue
                maxaction = currentaction

                #print("BEST ACTION:"+str((maxaction,maxvalue)))
                return (maxaction,maxvalue)
            else:
                ''
                #print("CANNOT DO ACTION:"+str(currentaction))

        return (maxaction,maxvalue)



#Enumeration for storing QLearning variables:
class QL(Enum):
    LIVING_REWARD = 0.1
    HITTING_WALL = -0.1
    DISCOUNT_RATE = 0.2
    ALPHA = 0.1 #Learning Rate


    #EPSILON+ACT_CURRENT_POLICY = 1.0
    EPSILON = 0.1 #Probability the agent acts randomly
    ACT_CURRENT_POLICY = 1-EPSILON #Probability the agent acts based on current policy

    REACH_GOAL = 100 #+100 reward
    REACH_FORBIDDEN = -100 #-100 reward


    #Convergence:
    MAX_ITERATIONS = 10000 #after reached, set ellipson to 0

    def __lt__(self, other):
        if(isinstance(other,QL)):
            return self.value<other.value
        else:
            return self.value<other

    def __le__(self, other):
        if(isinstance(other,QL)):
            return self.value<=other.value
        else:
            return self.value<=other

    def __eq__(self, other):
        if (isinstance(other, QL)):
            return self.value == other.value
        else:
            return self.value == other

    def __gt__(self, other):
        if (isinstance(other, QL)):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if (isinstance(other, QL)):
            return self.value >= other.value
        else:
            return self.value >= other

    def __add__(self, other):
        if (isinstance(other, QL)):
            return self.value + other.value
        else:
            return self.value + other

    def __sub__(self, other):
        if (isinstance(other, QL)):
            return self.value - other.value
        else:
            return self.value - other

    def __repr__(self):
        return self.value

    def __str__(self):
        return self


#Returns a random probability between [0,1]
def getRandomProbability():
    p = random.random()
    return p

#Agent class to navigate board with states: goal,forbidden,wall,normal,start
class QLearningAgent:
    def __init__(self, board:Board,startLocation:int):
        self.startLocationUniqueIndex = startLocation #UniqueIndex
        self.startLocationRowColumn = Board.getRowColumnFromUniqueIndex(board,self.startLocationUniqueIndex)

        self.board = board
        self.currentLocationRowColumn = self.startLocationRowColumn


        self.totalrewards = 0

    def getLocation(self):
        return self.currentLocationRowColumn

    def getTileLocation(self):
        return self.board[self.currentLocationRowColumn[0]][self.currentLocationRowColumn[1]]

    #4 possibilities
    #Q*(s,a) tells us the best action at this current state
    def generatePolicyMoveCurrentState(self):
        p = getRandomProbability()
        currLocation = self.getLocation()
        currentState = self.board[currLocation[0]][currLocation[1]]
        maxaction = None
        maxvalue = -float("inf")
        pickedMove = None

        #For a random move, keeps randomly picking until it gets a move that results in a valid tile
        #EX: if starting at the bottom row of board, you cannot pick move 'SOUTH' because it will not work
        if(p<=QL.EPSILON):
            while(True):
                pickedMove = random.choice([MOVES.NORTH.value,MOVES.EAST.value,MOVES.WEST.value,MOVES.SOUTH.value])

                if(self.board.agent.isValidMove(pickedMove)):
                    break


            maxvalue = currentState.qvalues[pickedMove]
        elif(p<=QL.EPSILON+QL.ACT_CURRENT_POLICY):
            qstateargmaxtuple = Board.getQStateMaxQActionValue(self.board,currentState)
            pickedMove =qstateargmaxtuple[0]
            maxvalue = qstateargmaxtuple[1]

        #print("FSDJFLSDF")
        #print(pickedMove,maxvalue)
        return (pickedMove,maxvalue)

    def resetToStartLocation(self):
        self.currentLocationRowColumn = self.startLocationRowColumn

    def isValidMove(self,move:MOVES):
        movetorow = self.getLocation()[0]
        movetocolumn = self.getLocation()[1]

        #print("BEFORE:"+str((movetorow,movetocolumn)))

        if(move==MOVES.NORTH.value):
            movetorow-=1

        elif(move==MOVES.SOUTH.value):
            movetorow+=1

        elif(move==MOVES.EAST.value):
            movetocolumn+=1

        elif(move==MOVES.WEST.value):
            movetocolumn-=1

        #print("IS THIS VALID?:"+str((movetorow,movetocolumn)))

        return Board.isRowColumnWithinBounds(self.board,(movetorow,movetocolumn))



    def move(self,move:MOVES):
        nextLocationRowColumn = None

        currentrow = self.currentLocationRowColumn[0]
        currentcolumn = self.currentLocationRowColumn[1]

        if (move == MOVES.NORTH.value):
            nextLocationRowColumn = (currentrow - 1, currentcolumn)
        elif (move == MOVES.SOUTH.value):
            nextLocationRowColumn = (currentrow + 1, currentcolumn)
        elif (move == MOVES.EAST.value):
            nextLocationRowColumn = (currentrow, currentcolumn + 1)
        elif (move == MOVES.WEST.value):
            nextLocationRowColumn = (currentrow, currentcolumn - 1)

        nextrow = nextLocationRowColumn[0]
        nextcolumn = nextLocationRowColumn[1]

        if(Board.isRowColumnWithinBounds(self.board,nextLocationRowColumn)):
            #print("MOVING AGENT FROM:"+str(self.currentLocationRowColumn))
            self.currentLocationRowColumn = nextLocationRowColumn
            #print("MOVED AGENT TO:"+str(self.currentLocationRowColumn))
        else:
            print("DID NOT MOVE AGENT, OUT OF BOUNDS")






def getUserInputForBoard():
    isSelecting = True
    listOfTileValues = set([])
    output_type = ""
    optionalNum = -1

    redoValues = False

    numbersRequired = 4
    charRequired = 1
    optionalNumber = 1

    while(isSelecting):
        print("Enter your board input, EX: '15 12 8 6 p' or '15 12 8 6 q 11'")
        #(first two ints=goal locations, third int=forbidden location, fourth int=wall location)
        tile_input = input()
        listOfStringTileValues = tile_input.split(' ')



        #print(listOfStringTileValues)
        #print(len(listOfStringTileValues))


        for i in range(numbersRequired):
            #print("WORKING")
            if (listOfStringTileValues[i].isdigit() == False):
                #print("NOT A VALID SEQUENCE OF INTEGERS")
                listOfTileValues = set([])
                redoValues = True
                break
            elif(listOfStringTileValues[i] in listOfTileValues):
                #print("CANNOT HAVE SAME LOCATIONS FOR A TILE")
                listOfTileValues = set([])
                redoValues = True
                break
            else:
                listOfTileValues.add(listOfStringTileValues[i])

        if(listOfStringTileValues[numbersRequired]=='p'):
            output_type = 'p'


        elif(listOfStringTileValues[numbersRequired]=='q' and len(listOfStringTileValues)>numbersRequired):
            output_type = 'q'

            if(listOfStringTileValues[numbersRequired+charRequired].isdigit()):
                optionalNum = listOfStringTileValues[numbersRequired+charRequired]
            else:
                redoValues = True
        else:
            redoValues = True


        #If the user entered an invalid sequence of numbers, this causes the loop to redo
        #and have the user reenter input
        if(redoValues):
            redoValues = False
            continue


        break

    listOfTileValues = list(listOfTileValues)

    tiles = {
        'goal':[int(listOfStringTileValues[0]),int(listOfStringTileValues[1])],
        'forbidden':int(listOfStringTileValues[2]),
        'wall':int(listOfStringTileValues[3])
    }
    #print(listOfTileValues)
    #print(output_type)
    #print(tiles)

    print(tiles)

    #print(listOfStringTileValues)
    return {"tiles":tiles,"optional_number":optionalNum,"output_type":output_type}

def addTilesToBoard(board:Board,tiles:dict):
    statetypes = tiles.keys()

    for state in statetypes:
        values = tiles[state]

        #print("STATE:"+str(state))
        #print("VALUES:"+str(values))

        if(isinstance(values,list)):
            for ui in values:
                tile = Board.getTileUniqueIndex(board,int(ui))
                tile.type = state

        elif (isinstance(values, str)):
            #print("ENTERED2")
            value = int(values)
            #print("VALUE:"+str(value))
            tile = Board.getTileUniqueIndex(board, value)
            tile.type = state
        elif(isinstance(values,int)):
            tile = Board.getTileUniqueIndex(board, values)
            tile.type = state

def addRewardsValuesToTiles(board:Board):
    for r in range(board.n_Rows):
        for c in range(board.n_Columns):
            tile = board[r][c]

            if(tile.type==TILE_TYPES.GOAL):
                tile.reward = QL.REACH_GOAL.value
                tile.qvalues = {
                    'exit': QL.REACH_GOAL.value
                }
            elif(tile.type==TILE_TYPES.FORBIDDEN):
                tile.reward = QL.REACH_FORBIDDEN.value
                tile.qvalues = {
                    'exit': QL.REACH_FORBIDDEN.value
                }
            elif(tile.type==TILE_TYPES.WALL):
                tile.reward = QL.HITTING_WALL.value
            else:
                tile.reward = QL.LIVING_REWARD.value


def getPathSequenceFromUpdatedQStates(board:Board):
    currentState = board[board.agent.startLocationRowColumn[0]][board.agent.startLocationRowColumn[1]]
    board.agent.currentLocationRowColumn = board.agent.startLocationRowColumn

    #Stores the steps from the start state to a goal state:
    stepsToGoal = []
    #stepsToGoal.append(currentState)
    #print("STARTED PATH SEQUENCE:")

    i = 0
    safeBreak = 50
    while(True and i<safeBreak):
        #print(currentState)
        maxqstateactionvalueBoard_tuple=Board.getQStateMaxQActionValue(board,currentState)
        maxaction = maxqstateactionvalueBoard_tuple[0]
        #print("MAX ACTION:"+str(maxaction))

        #Appending steps to list of steps:
        if(maxaction==MOVES.NORTH.value):
            stepsToGoal.append("   "+str(currentState.unique_index)+"↑")
        elif(maxaction==MOVES.SOUTH.value):
            stepsToGoal.append("   "+str(currentState.unique_index) + "↓")
        elif(maxaction==MOVES.EAST.value):
            stepsToGoal.append("   "+str(currentState.unique_index) + "→")
        elif(maxaction==MOVES.WEST.value):
            stepsToGoal.append("   "+str(currentState.unique_index) + "←")

        #Moves agent based on optimal policy action:
        board.agent.move(maxaction)
        currentState = board[board.agent.currentLocationRowColumn[0]][board.agent.currentLocationRowColumn[1]]

        #Exits loop once the agent reached the goal state:
        if (currentState.type == TILE_TYPES.GOAL.value):
            #print("BROKE")
            #stepsToGoal.append(currentState)
            break

        i+=1
    #print(stepsToGoal)
    return stepsToGoal

def QLearningAgentBoardExample(iterations:int):
    board = Board()
    userinput = getUserInputForBoard()

    print("Intial:")
    output_type = userinput["output_type"]
    optional_number = int(userinput["optional_number"])
    tiles = userinput["tiles"]
    #tiles = {'goal': ['15', '12'], 'forbidden': '8', 'wall': '6'}
    addTilesToBoard(board, tiles)
    addRewardsValuesToTiles(board)
    Board.printBoard(board)
    Board.printTileRewardsBoard(board)
    Board.printQActionValuesBoard(board)

    print("--")

    numeroftimesresetted = 0 #Keeps track of the number of times the agent went resetted to the start location

    #t is our time variable
    for t in range(0,iterations,1):
        #Current State: Q(s,a) and where agent is currently at
        qstate = board[board.agent.getLocation()[0]][board.agent.getLocation()[1]]
        #print("QSTATE:"+str(qstate))

        #Picks the action with the highest Q-Value
        policy_tuple = board.agent.generatePolicyMoveCurrentState()
        policy_action = policy_tuple[0] #argmax a Q*(s,a) action
        policy_value = policy_tuple[1]#max Q*(s,a) value

        #S prime state
        sprimestate = Board.getTileFromLocationGivenMove(board,board.agent.getLocation(),policy_action)

        #Reward: R(s,a,s')
        reward = sprimestate.reward

        #argmax Q*(s',a')
        maxqsprimetuple = Board.getQStateMaxQActionValue(board,sprimestate)
        maxqsprimevalue = maxqsprimetuple[1]

        #Setting new Q(s,a) value:
        qstateoldvalue= qstate.qvalues[str(policy_action)]

        #Updates the policies of states only if they are not the GOAL and not FORBIDDEN
        if(qstate.type!=TILE_TYPES.GOAL and qstate.type!=TILE_TYPES.FORBIDDEN):
            qstate.qvalues[str(policy_action)] = (1-QL.ALPHA.value)*qstateoldvalue+QL.ALPHA.value*(reward+QL.DISCOUNT_RATE.value*maxqsprimevalue)

            #Below is a different Q(s,a) function:
            #qstate.qvalues[str(policy_action)] = reward+0.8*maxqsprimevalue


        #Uncomment to print out the board and board Q-Values:
        #Board.printBoard(board)
        #Board.printQActionValuesBoard(board)

        #Stops agent from moving to a wall s' state
        if(sprimestate.type!=TILE_TYPES.WALL):
            #Moving agent
            board.agent.move(policy_action)


        #After getting rewards (positive,negative) reset the location of the agent to start
        if(board.agent.getTileLocation().type==TILE_TYPES.GOAL or board.agent.getTileLocation().type==TILE_TYPES.FORBIDDEN):
            board.agent.resetToStartLocation()
            numeroftimesresetted+=1

    #Uncomment to print the number of times the agent has resetted:
    #print("RESETTED:"+str(numeroftimesresetted))

    print("Output:")
    Board.printQActionValuesBoard(board)
    print("\nAgent Steps:")
    if(output_type=='p'):
        stepsToGoalFromStart = getPathSequenceFromUpdatedQStates(board)
        for step in stepsToGoalFromStart:
            print(step)
    elif(output_type=='q'):
        qvalues = board.getTileUniqueIndex(optional_number).qvalues
        print("   ↑" + str(qvalues[str(MOVES.NORTH)]))
        print("   →" + str(qvalues[str(MOVES.EAST)]))
        print("   ←" + str(qvalues[str(MOVES.WEST)]))
        print("   ↓" + str(qvalues[str(MOVES.SOUTH)]))


#Main----------------
QLearningAgentBoardExample(QL.MAX_ITERATIONS.value)