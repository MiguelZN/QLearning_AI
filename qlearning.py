'''
Miguel Zavala
4/26/20
CISC481-Intro to AI
Homework 4: Q-learning
Dr.Rahmat
'''

from enum import Enum
import math

class TILE_TYPES(Enum):
    START = 'start'
    GOAL = 'goal'
    FORBIDDEN = 'forbidden'
    WALL = 'wall'
    ORDINARY = 'ordinary'

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
    def __init__(self, type=TILE_TYPES.ORDINARY,unique_index:int=-1):
        self.value = None
        self.type = type
        self.unique_index = unique_index

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "("+str(self.type)+"|Index "+str(self.unique_index)+")"

class Board(list):
    def __init__(self,n_Rows:int=4,n_Columns:int=4):
        self.n_Rows = n_Rows
        self.n_Columns = n_Columns
        self.size = self.n_Rows*self.n_Columns

        self.createBoard(self.n_Rows,self.n_Columns)

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

        #Readjusts the row if the row is divisible by the number of rows in the board
        if(unique_index!=0 and unique_index%boardObject.n_Rows==0):
            row +=1

        if(row<0 or row>=boardObject.n_Rows):
            return None
        if(column<0 or column>=boardObject.n_Columns):
            return None

        #print(row,column)

        return boardObject[row][column]

    def printBoard(boardObject):
        print("BOARD:")
        for i in range(boardObject.n_Rows):
            currRow = ""
            for j in range(boardObject.n_Columns):
                currRow+=str(boardObject[i][j])

            print(currRow)


def getUserInputForBoard():
    isSelecting = True
    listOfTileValues = []
    output_type = ""

    while(isSelecting):
        print("Enter your board input, EX: '15 12 8 6'\n(first two ints=goal locations, third int=forbidden location, fourth int=wall location)")
        tile_input = input()
        listOfStringTileValues = tile_input.split(' ')
        print(listOfStringTileValues)
        print(len(listOfStringTileValues))
        for i in range(len(listOfStringTileValues)):
            print("WORKING")
            if (listOfStringTileValues[i].isdigit() == False):
                print("NOT A VALID SEQUENCE OF INTEGERS")
                listOfTileValues = []
                continue
            else:
                listOfTileValues.append(listOfStringTileValues[i])

        print("Enter your output type:\n'p':print optimal policy\n'q':print optimal values")
        outputtype_input = input()
        if(outputtype_input!='q' and outputtype_input!='p'):
            print("NOT A VALID OUTPUT TYPE")
            output_type = ""
            continue
        else:
            output_type = outputtype_input

        break

    print(listOfTileValues)
    print(output_type)













print(TILE_TYPES.ORDINARY == 'ordinary')
print(TILE_TYPES.ORDINARY == TILE_TYPES.ORDINARY)

print(Board())
Board1 = Board()
print(Board.getTileUniqueIndex(Board1,16))
Board.getTileUniqueIndex(Board1,16).type=TILE_TYPES.START
print(Board.getTileUniqueIndex(Board1,16))

Board.printBoard(Board1)
getUserInputForBoard()