##### Miguel Zavala 5/4/20 CISC481-Intro to AI Dr.Rahmat

### README: Homework 4-Qlearning

##### To run: 
```sh
$ python3 qlearning.py
```

##### Entering Input:
You will be prompted to enter a sequence of numbers,char:
You can either:
1) Enter **4 numbers in sequence** followed by the char **'p'** to print the optimal
policy(Π*) 
EX: '15 12 8 6 p '
### OR
2) Enter **4 numbers in sequence** followed by the char **'q'** followed by **1 number** (unique index tile/state you would to know the optimal Q-values of) 
EX: '15 12 8 6 q 11'

#### Notes:
* The start state of the agent is hardcoded to the tile:unique index=2 or Board[3][1] (as wanted by the homework assignment)
* As shown in the homework assignment description, each tile has a 'unique index' that corresponds to it. When entering input to get the optimal Q-values of a tile, enter its unique index. 
**EX1: Tile at row:0, column:0 corresponds to unique index = 13 (for a 4x4 board)**
**EX2: Tile at the bottom left of a 4x4 board is at row:3,column:0 and corresponds to unique index = 1**
* The initial properties of the board are also printed in the output such as the rewards of each state, the types/states of each tile, and the initial q-values of each tile
* The end output also prints the end Q-Values of every tile in the board represented by:
EX: '13:{'north': 0, 'south': 0.36278737229360614, 'west': 0, 'east': 24.09999999997674}' for the 13th unique_index tile
