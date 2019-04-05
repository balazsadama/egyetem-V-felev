
def minimax(game, maximizingPlayer):
	emptySquares = [(r,c) for r in range(3) for c in range(3) if game[r][c] == '-']
	if givenPlayerWon(game, 'O' if maximizingPlayer else 'X'):
		return evaluateNode(game, maximizingPlayer)
	if len(emptySquares) is 0:	# draw
		return 0
	if maximizingPlayer:
		val = -50000;
		for (r,c) in emptySquares:
			newGame = [row[:] for row in game]
			newGame[r][c] = 'X'
			val = max(val, minimax(newGame, False))
		return val
	else:		# minimizing player
		val = 50000;
		for (r,c) in emptySquares:
			newGame = [row[:] for row in game]
			newGame[r][c] = 'O'
			val = min(val, minimax(newGame, True))
		return val


def givenPlayerWon(game, player):
	mainDiagonalCount = 0
	antiDiagonalCount = 0
	for i in range(3):
		if game[i].count(player) is 3:
			return True
		if len([player for r in range(3) if game[r][i] is player]) is 3:
			return True
		if game[i][i] is player:
			mainDiagonalCount = mainDiagonalCount + 1
		if game[i][2-i] is player:
			antiDiagonalCount = antiDiagonalCount + 1
	if mainDiagonalCount is 3 or antiDiagonalCount is 3:
		return True
	return False


def evaluateNode(game, maximizingPlayer):
	valRow = [0] * 3
	valCol = [0] * 3
	sign = {'X' : 1, 'O' : -1}

	for i in range(3):
		# evaluate row
		if not ('X' in game[i] and 'O' in game[i]):
			valRow[i] = 10 ** (max(game[i].count('X'), game[i].count('O')) - 1) * sign['X' if 'X' in game[i] else 'O']
		
		# evaluate col
		col = [game[j][i] for j in range(3)]
		if not ('X' in col and 'O' in col):
			valCol[i] = 10 ** (max(col[i].count('X'), col[i].count('O')) - 1) * sign['X' if 'X' in col[i] else 'O']
		
	# evaluate diagonal
	diagonal = [game[i][i] for i in range(3)]
	valDiagonal = 0
	if not ('X' in diagonal and 'O' in diagonal):
		valDiagonal = 10 ** (max(diagonal.count('X'), diagonal.count('O')) - 1) * sign['X' if 'X' in diagonal else 'O']
	
	# evaluate antidiagonal
	antidiagonal = [game[i][2-i] for i in range(3)]
	valAntidiagonal = 0
	if not ('X' in antidiagonal and 'O' in antidiagonal):
		valAntidiagonal = 10 ** (max(antidiagonal.count('X'), antidiagonal.count('O')) - 1) * sign['X' if 'X' in antidiagonal else 'O']
	
	toSum = [valDiagonal, valAntidiagonal]
	toSum.extend(valRow)
	toSum.extend(valCol)
	if maximizingPlayer:
		totalSum = sum([10*x if x < 0 else x for x in toSum])
	else:
		totalSum = sum([10*x if x > 0 else x for x in toSum])
	
	return totalSum
		


if __name__ == "__main__":
	J = 3
	K = 3
	game = [['-'] * K for _ in range(K)]
	minimax(game, True)
	
	print(x)
	
