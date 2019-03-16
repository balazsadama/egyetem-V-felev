import time
import copy
import sys
# sys.stdout = open("/home/baam0146/egyetem/mestint/sudoku/output.txt", "w")

positions = [(r,c) for r in range(9) for c in range(9)]

def getPeers():
	peers = {}
	for row in range(9):
		for col in range(9):
			cols = [c for c in range(9) if c != col]
			rows = [r for r in range(9) if r != row]

			a = [(row, c) for c in cols]
			b = [(r, col) for r in rows]
			c = getUnit(row, col)
			peers[(row,col)] = a + b + c
	
	return peers


def getUnit(row, col):
		switch = {
				0: (0, 1, 2),
				1: (3, 4, 5),
				2: (6, 7, 8)
		}
		rows = switch[row // 3]
		cols = switch[col // 3]

		return [(r, c) for r in rows if r != row for c in cols if c != col]


def assign(values, peers, pos, char):
	(row, col) = pos
	values[(row,col)] = [char]
	for p in peers[(row, col)]:
		if char in values[p]:
			values[p].remove(char)
			if len(values[p]) is 1:
				assign(values, peers, p, values[p][0])
	

def nextPos(values):
	n,p = min((len(values[p]), p) for p in positions if len(values[p]) > 1)
	return p


def solve(values, peers, pos):
	for val in values[pos]:
		newValues = copy.deepcopy(values)
		assign(newValues, peers, pos, val)
		if all([len(newValues[p]) == 1 for p in positions]):
			return newValues
		if any([len(newValues[p]) == 0 for p in positions]):
			continue
		p = nextPos(newValues)
		tmp = solve(newValues, peers, p)
		if tmp:
			return tmp
	return False


def prettyPrint(values):
	for r in range(9):
		for c in range(9):
			if c % 3 == 2 and c != 8:
				print(values[(r,c)][0], end=" | ")
			else:
				print(values[(r,c)][0], end=" ")
		if r % 3 == 2 and r != 8:
			print("\n" + "-"*22)
		else:
			print()


def testResult(values):
	for r in range(9):
		digits = [False] * 9
		for c in range(9):
			digits[values[(r,c)][0] - 1] = True
		if not all(digits):
			return False
	return True


def solveSudoku(text):
	peers = getPeers()
	values = dict(((r,c), [1, 2, 3, 4, 5 , 6, 7, 8, 9]) for r in range(9) for c in range(9))
	for row in range(9):
			for col in range(9):
				char = text[9 * row + col]
				if text[9 * row + col] in "123456789":
					assign(values, peers, (row, col), int(char))
	if not all([len(values[p]) == 1 for p in positions]):
		x = solve(values, peers, nextPos(values))
	else:
		x = values

	return x


# if __name__ == "__main__":
# 	# inputFile = open("top95.txt", "r")
# 	inputFile = open("easy50.txt", "r")
# 	peers = getPeers()

# 	totalTime = time.perf_counter()
# 	for line in inputFile:
# 		individualTime = time.perf_counter()
# 		values = dict(((r,c), [1, 2, 3, 4, 5 , 6, 7, 8, 9]) for r in range(9) for c in range(9))
# 		for row in range(9):
# 				for col in range(9):
# 					char = line[9 * row + col]
# 					if line[9 * row + col] in "123456789":
# 						assign(values, peers, (row, col), int(char))

# 		if not all([len(values[p]) == 1 for p in positions]):
# 			x = solve(values, peers, nextPos(values))
# 		else:
# 			x = values
# 		print(testResult(x))
# 		prettyPrint(x)
# 		print("Time elapsed: ", (time.perf_counter() - individualTime))
# 		print("\n")
	
# 	print("Total time elapsed: ", (time.perf_counter() - totalTime))


