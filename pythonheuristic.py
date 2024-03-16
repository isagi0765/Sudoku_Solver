def find_empty_cell(board):
    min_possible_moves = float('inf')
    min_row, min_col = None, None
    
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                num_possible_moves = count_possible_moves(board, row, col)
                if num_possible_moves < min_possible_moves:
                    min_possible_moves = num_possible_moves
                    min_row, min_col = row, col
                    
    return min_row, min_col

def is_valid_move(board, row, col, num):
    if num in board[row]:
        return False
    
    if num in [board[i][col] for i in range(9)]:
        return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def count_possible_moves(board, row, col):
    count = 0
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            count += 1
    return count

def solve_sudoku(board):
    row, col = find_empty_cell(board)
    if row is None:
        return True  
    
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  
    return False  

def get_input():
    print("Enter the Sudoku puzzle (use 0 for empty cells):")
    board = []
    for _ in range(9):
        row = list(map(int, input().split()))
        board.append(row)
    return board

# Example usage:
input_puzzle = get_input()

if solve_sudoku(input_puzzle):
    print("Sudoku solved:")
    for row in input_puzzle:
        print(row)
else:
    print("No solution exists.")