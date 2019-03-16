import sudoku
import random


def diagonalSudoku():
	values = dict(((r,c), [0]) for r in range(9) for c in range(9))

	for it in range(3):
		randList = list(range(1,10))
		random.shuffle(randList)
		
		for row in range(3):
			for col in range(3):
				# values[row + it * 3][col + it * 3] = randList[row * 3 + col]
				values[(row + it * 3, col + it * 3)][0] = randList[row * 3 + col]
	
	return values


def sudokuToText(sudoku):
	text = ""
	for row in range(9):
		for col in range(9):
			if sudoku[(row, col)][0] > 0:
				text = text + str(sudoku[(row, col)][0])
			else:
				text = text + "."
	
	return text


def deleteRandomCells(sudoku, nrToDelete):
	countDeleted = 0
	while (countDeleted < nrToDelete):
		row = random.randint(0, 8)
		col = random.randint(0, 8)
		while sudoku[(row, col)] == [0]:
			row = random.randint(0, 8)
			col = random.randint(0, 8)
		sudoku[(row, col)] = [0]
		countDeleted = countDeleted + 1


def generateSudoku(nrCellsToDelete):
	diagonal = diagonalSudoku()
	diagonalText = sudokuToText(diagonal)
	initialSudoku = sudoku.solveSudoku(diagonalText)
	
	while True:
		deleteRandomCells(initialSudoku, nrCellsToDelete)
		newSudoku = sudokuToText(initialSudoku)

		y = sudoku.solveSudoku(newSudoku)
		if y != False:
			return newSudoku
		else:
			print("Unsolvable, trying again")


if __name__ == "__main__":
	print(generateSudoku(40))
