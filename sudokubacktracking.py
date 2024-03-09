def is_valid_move(grid, row, col, number):
    for x in range(9):
        if grid[row][x] == number:
            return False
        
    for x in range(9):
        if grid[x][col] == number:
            return False     

    corner_row = row - row % 3
    corner_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False
            
    return True

def is_valid_input(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0
                if not is_valid_move(grid, i, j, num):
                    return False
                grid[i][j] = num
    return True

def solve(grid, row, col):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve(grid, row, col + 1)

    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve(grid, row, col + 1):
                return True 
        grid[row][col] = 0

    return False

def get_input():
    # Prompt the user to input the Sudoku puzzle
    print("Enter the Sudoku puzzle (use 0 for empty cells):")
    grid = []
    for _ in range(9):
        row = list(map(int, input().split()))
        grid.append(row)
    return grid

grid = get_input()  # Get Sudoku puzzle from user
if is_valid_input(grid):
    print("Input Sudoku puzzle is valid.")
    if solve(grid, 0, 0):
        print("Sudoku solved:")
        for i in range(9):
            for j in range(9):
                print(grid[i][j], end=" ") 
            print()
    else:
        print("No solution exists")
else:
    print("Input Sudoku puzzle is not valid.")