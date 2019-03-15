import sudoku
# from random import shuffle
import random
# from random import choice


def pprint(values):
	for it in range(9):
		print(values[it])


if __name__ == "__main__":
	values = [[0 for r in range(9)] for c in range(9)]

	for it in range(3):
		randList = list(range(1,10))
		random.shuffle(randList)
		
		for row in range(3):
			for col in range(3):
				values[row + it * 3][col + it * 3] = randList[row * 3 + col]

	initialSudoku = ""
	for row in range(9):
		for col in range(9):
			if values[row][col] > 0:
				initialSudoku = initialSudoku + str(values[row][col])
			else:
				initialSudoku = initialSudoku + "."
	
	pprint(values)
	print(initialSudoku)
	x = sudoku.solveSudoku(initialSudoku)
	sudoku.prettyPrint(x)

	# now delete random squares and try to solve. if solvable, done, else, retry deletion

	countDeleted = 0
	while (countDeleted < 40):
		row = random.randint(0, 8)
		col = random.randint(0, 8)
		while x[(row, col)] == [0]:
			row = random.randint(0, 8)
			col = random.randint(0, 8)
		x[(row, col)] = [0]
		countDeleted = countDeleted + 1
	
	# print("\n\nAfter deleting cells:")
	# sudoku.prettyPrint(x)
	newSudoku = ""
	for row in range(9):
		for col in range(9):
			if x[(row,col)][0] > 0:
				newSudoku = newSudoku + str(x[(row,col)][0])
			else:
				newSudoku = newSudoku + "."
	print(newSudoku)

	y = sudoku.solveSudoku(newSudoku)
	if y != False:
		sudoku.prettyPrint(y)
	else:
		print("Unsolvable")
