# import sys
# sys.path.append(r"C:\Users\varun kumar\Downloads\latex\Sudoku_Generator_Code\puzzle_maker.py")
import numpy as np
from random import sample, randint
import copy
# import puzzle_maker

TEMP = {'2':0.5, '3':0.5, '4':0.5} #Default temperatures to use for every dimension

#Swap in blocks and score rows,columns
def solveSudokubyBlocks(puzzle_input,maxIterations=5000000,T=TEMP['3'],coolingRate=1.0 - 1e-5,verbose=False):

    if(verbose):
        print("Puzzle")
        puzzle_maker.Print(puzzle_input)
    
    reheat_rate = T/0.3
    
    puzzle = copy.deepcopy(puzzle_input)
    side = len(puzzle)
    sq_size = int(np.sqrt(side))
    
    empty_cells = Initialize(puzzle)
    
    if(verbose):
        print("Initialized puzzle")
        puzzle_maker.Print(puzzle)
    
    #Start annealing
    score = CalcScore(puzzle)
    target_score = -2*side*side
    best_score = score
    stuck_count=0

    for i in range(maxIterations):
        if(i%10000 ==0 and verbose):
            print("Iteration "+str(i)+", current score:"+str(score)+"  Best score: "+str(best_score))
            
        # Adjust temperature
        if(score == target_score or T==0):
            break
            
        #If stuck then reheat the annealer
        if(stuck_count>5000 or T < 1e-4):
            print("Annealer is stuck at T={} and stuck_count={}, so re-initializing...".format(T,stuck_count))
            T=T*reheat_rate
            puzzle=copy.deepcopy(puzzle_input)
            empty_cells = Initialize(puzzle)
            stuck_count=0
        
        
        neighbor_puzzle = FindNeighbor(puzzle,empty_cells) # Find neighbouring state
        s2 = CalcScore(neighbor_puzzle) # Energy of neighbouring state
        delta_s = float(score-s2) # Energy difference
        probability = np.exp(delta_s/T) #Acceptance probability
            
        random_probability = np.random.uniform(low=0,high=1,size=1)
        
        if(probability > random_probability): #Acceptance condition, ref: accept-reject sampling
            puzzle = copy.deepcopy(neighbor_puzzle)
            score = s2
            if(score<best_score):
                best_score=score
            stuck_count=0
            
        stuck_count+=1
            
        T=coolingRate*T
    
    if(verbose):
        print("Total number of iterations done: ",i+1," to get score:", score)    
        #Print solution
        print("Solution:")
        puzzle_maker.Print(puzzle)
        
    return puzzle  


def mapEmptyCell(empty_cells,dim,sqcount):
    
    empty_puzzle_cells = []
    
    for row in range(dim):
        for col in empty_cells[row]:
            r= row + dim*(sqcount//dim)
            c= col + dim*(sqcount%dim)
            empty_puzzle_cells.append((r,c))
    return empty_puzzle_cells


def Initialize(puzzle):

    side = len(puzzle)
    sq_size = int(np.sqrt(side))
    
    i=0
    j=0
    empty_cells=[]
    square=[]
    square_count=0
    while(i<side and j<side):

        square.append(puzzle[i][j:j+sq_size])
        
        if ((i+1)%sq_size == 0 and (j+sq_size)%sq_size == 0):
            
            fixed_cells=[]
            empty=[]
            
            values=list(range(1,side+1))
            #Find empty cells and fixed cells in the block
            for row in range(sq_size):
                empty.append(np.where(np.array(square)[row]==0)[0].tolist())
                fixed_cells.append(np.where(np.array(square)[row]!=0)[0].tolist())
            
                #Find fixed values in the block
                for f in fixed_cells[row]:
                    values.remove(square[row][f])

            #Map empty cell to puzzle indices
            index_map = mapEmptyCell(empty,sq_size,square_count)
            empty_cells.append(index_map)

            #Fill empty cells in the block uniquely
            for cell in index_map:        

                random_val=sample(values,1)[0]

                puzzle[cell[0]][cell[1]] = random_val
                
                values.remove(random_val)
                    
            square_count+=1
            j+=sq_size
            i-=sq_size
            square=[]
            if(j%side==0):
                i=i+sq_size
                j=0
        
        i+=1
        
    return empty_cells
        


def CalcScore(puzzle):
    '''
    Calculate the score for a puzzle. Puzzle is scored by number of unique elements in every row and column.
    '''
    
    side = len(puzzle)    
    score = 0
    
    #Count in the columns
    puzzle_transpose =  list(zip(*puzzle))
    for i in range(side):
        
        #Score by unique elements
        score -= len(list(set(puzzle[i])))
        score -= len(list(set(puzzle_transpose[i])))
        
    return score


            
def FindNeighbor(puzzle,empty_cells):
    
    side = len(puzzle)
    sq_size = int(np.sqrt(side))
    new_puzzle = copy.deepcopy(puzzle)
    
    empty_block_size=0
    while(empty_block_size<2 ):
        #Pick a random block
        block = randint(0,side-1)
        empty_block_size = len(empty_cells[block])
        
    #Randomly find 2 cells in the block to swap
    a, b = sample(range(len(empty_cells[block])),2)
    cell1, cell2 = empty_cells[block][a], empty_cells[block][b]
    
    #Swap entries
    new_puzzle[cell1[0]][cell1[1]], new_puzzle[cell2[0]][cell2[1]] = new_puzzle[cell2[0]][cell2[1]], new_puzzle[cell1[0]][cell1[1]]

    return new_puzzle