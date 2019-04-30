J = 0
K = 0

def setJK(j, k):
	global J, K
	J = j
	K = k
	print('called 2')

def minimax(game, maximizingPlayer, alpha, beta, depth):
	# print(game, maximizingPlayer, alpha, beta, depth)
	emptySquares = [(r,c) for r in range(K) for c in range(K) if game[r][c] == '-']
	if givenPlayerWon(game, 'O' if maximizingPlayer else 'X'):
		return (evaluateNode(game, maximizingPlayer), -1, -1)
	if len(emptySquares) is 0:	# draw
		return (0, -1, -1)
	if depth is 0:
		return (evaluateNode(game, maximizingPlayer), -1, -1)
	if maximizingPlayer:
		bestVal = float('-inf')
		for (r,c) in emptySquares:
			newGame = [row[:] for row in game]
			newGame[r][c] = 'X'
			# val = max(val, minimax(newGame, False, alpha, beta, depth - 1))
			# alpha = max(alpha, val)
			# if alpha >= beta:
			# 	break;
			val = minimax(newGame, False, alpha, beta, depth - 1)[0]
			if val > bestVal:
				bestVal = val
				bestRow = r
				bestCol = c
				alpha = max(alpha, bestVal)
			if alpha >= beta:
				break
		return (alpha, bestRow, bestCol)
	else:		# minimizing player
		bestVal = float('inf')
		for (r,c) in emptySquares:
			newGame = [row[:] for row in game]
			newGame[r][c] = 'O'
		# 	val = min(val, minimax(newGame, True, alpha, beta, depth - 1))
		# 	beta = min(beta, val)
		# 	if alpha >= beta:
		# 		break;
		# return val
			val = minimax(newGame, True, alpha, beta, depth - 1)[0]
			if val < bestVal:
				bestVal = val
				bestRow = r
				bestCol = c
				beta = min(beta, bestVal)
			if alpha >= beta:
				break
		return (beta, bestRow, bestCol)


def givenPlayerWon(game, player):
	mainDiagonalCount = 0
	antiDiagonalCount = 0
	for i in range(K):
		if game[i].count(player) is J:
			return True
		if len([player for r in range(K) if game[r][i] is player]) is J:
			return True
		if game[i][i] is player:
			mainDiagonalCount = mainDiagonalCount + 1
		if game[i][2-i] is player:
			antiDiagonalCount = antiDiagonalCount + 1
	if mainDiagonalCount is J or antiDiagonalCount is J:
		return True
	return False


def evaluateNode(game, maximizingPlayer):
	valRow = [0] * K
	valCol = [0] * K
	sign = {'X' : 1, 'O' : -1}

	for i in range(K):
		# evaluate row
		if ('X' in game[i]) != ('O' in game[i]):
			valRow[i] = (10 ** (max(game[i].count('X'), game[i].count('O')) - 1)) * sign['X' if 'X' in game[i] else 'O']
		
		# evaluate col
		col = [game[j][i] for j in range(K)]
		if ('X' in col) != ('O' in col):
			valCol[i] = (10 ** (max(col.count('X'), col.count('O')) - 1)) * sign['X' if 'X' in col else 'O']
		
	# evaluate diagonal
	diagonal = [game[i][i] for i in range(K)]
	valDiagonal = 0
	if ('X' in diagonal) != ('O' in diagonal):
		valDiagonal = (10 ** (max(diagonal.count('X'), diagonal.count('O')) - 1)) * sign['X' if 'X' in diagonal else 'O']
	
	# evaluate antidiagonal
	antidiagonal = [game[i][K-1-i] for i in range(K)]
	valAntidiagonal = 0
	if ('X' in antidiagonal) != ('O' in antidiagonal):
		valAntidiagonal = (10 ** (max(antidiagonal.count('X'), antidiagonal.count('O')) - 1)) * sign['X' if 'X' in antidiagonal else 'O']
	
	toSum = [valDiagonal, valAntidiagonal]
	toSum.extend(valRow)
	toSum.extend(valCol)
	if maximizingPlayer:
		totalSum = sum([10*x if x < 0 else x for x in toSum])
	else:
		totalSum = sum([10*x if x > 0 else x for x in toSum])
	
	return totalSum


def getBestMove(game, maximizingPlayer):
	res = minimax(game, maximizingPlayer, float('-inf'), float('inf'), 5)
	return (0, res[1], res[2])


if __name__ == "__main__":
	# J = 5
	# K = 5
	# game = [['-'] * K for _ in range(K)]
	# minimax(game, False, float('-inf'), float('inf'), 5)
	
	# print(x)
	

	J = 4
	K = 4
	game = [['X', 'O', 'X', '-'], ['O', 'X', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]
	print(minimax(game, False, -197, -107, 1))