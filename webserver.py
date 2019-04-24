import socket
import json
import time
# import _thread as thread
from minimax1 import givenPlayerWon, minimax, setJK

J = 0
K = 0
L = 0

# def askFirstPlayer(connection, loser):
# 	global K, J

# 	connection.send('You begin, please give the game size.'.encode('ascii'))
# 	loser.send('The other player begins, please wait'.encode('ascii'))
# 	while True:
# 		resp = connection.recv(1024).decode('ascii')
# 		resp = json.loads(resp)
# 		x = resp['p1']
# 		y = resp['p2']
# 		if resp['cmd'] == 'size' and x > 1 and y > 1:
# 			K = x
# 			connection.send('Please give the winning length.'.encode('ascii'))
# 			while True:
# 				resp = connection.recv(1024).decode('ascii')
# 				resp = json.loads(resp)
# 				l = resp['p1']
# 				if resp['cmd'] == 'length' and l > 2 and l <= min(x, y):
# 					J = l
# 					break;
# 				else:
# 					connection.send('Invalid, try again.'.encode('ascii'))
# 			break;
# 		else:
# 			connection.send('Invalid, try again.'.encode('ascii'))


# def givenPlayerWon(game, player):
# 	mainDiagonalCount = 0
# 	antiDiagonalCount = 0
# 	for i in range(K):
# 		if game[i].count(player) is J:
# 			return True
# 		if len([player for r in range(K) if game[r][i] is player]) is J:
# 			return True
# 		if game[i][i] is player:
# 			mainDiagonalCount = mainDiagonalCount + 1
# 		if game[i][2-i] is player:
# 			antiDiagonalCount = antiDiagonalCount + 1
# 	if mainDiagonalCount is J or antiDiagonalCount is J:
# 		return True
# 	return False


# def playerVsPlayer(game, first, second):
# 	currentPlayer = first
# 	nextPlayer = second
# 	symbols = ['X', 'O']
# 	i = 0

# 	while not givenPlayerWon(game, symbols[1 - i]):
# 		resp = currentPlayer.recv(1024).decode('ascii')
# 		nextPlayer.send(resp.encode('ascii'))
# 		resp = json.loads(resp)
		
# 		(x, y) = (resp['p1'], resp['p2'])
# 		game[x][y] = symbols[i]
# 		currentPlayer, nextPlayer = nextPlayer, currentPlayer
# 		i = 1 - i
# 		print(game)
	
# 	nextPlayer.send('{"cmd" : "start", "p1": "YOU WON", "p2": 0}')
# 	nextPlayer.send('{"cmd" : "start", "p1": "YOU LOST", "p2": 0}')


def handlePvC(s):
	global J, K, L
	resp = json.loads(s.recv(1024).decode('ascii')) # size
	K = resp['p1']
	L = resp['p2']
	resp = json.loads(s.recv(1024).decode('ascii')) # length
	J = resp['p1']

	setJK(J, K)
	
	game = [['-'] * L for _ in range(K)]

	resp = json.loads(s.recv(1024).decode('ascii')) # start
	while True:
		mv = json.loads(s.recv(1024).decode('ascii')) # move
		i = mv['p1']
		j = mv['p2']
		game[i][j] = 'X'

		if givenPlayerWon(game, 'X'):
			s.send('{"cmd" : "end", "p1": "YOU WON", "p2": 0}'.encode('ascii'))
			break
		else:
			s.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))
		
		(v, i, j) = minimax(game, False)
		if (i, j) == (-1, -1):
			s.send('{"cmd" : "end", "p1": "DRAW", "p2": 0}'.encode('ascii'))
			break
		game[i][j] = 'O'
		mv = json.dumps('{"cmd" : "move", "p1":' + str(i) + ', "p2": ' + str(j) + '}')
		s.send(mv.encode('ascii'))
		
		time.sleep(0.5)
		if givenPlayerWon(game, 'O'):
			s.send('{"cmd" : "end", "p1": "YOU LOST", "p2": 0}'.encode('ascii'))
			break
		else:
			s.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))


def handleCvC(s):
	global J, K, L
	resp = json.loads(s.recv(1024).decode('ascii')) # size
	K = resp['p1']
	L = resp['p2']
	resp = json.loads(s.recv(1024).decode('ascii')) # length
	J = resp['p1']
	setJK(J, K)
	game = [['-'] * L for _ in range(K)]

	while True:
		(v, i, j) = minimax(game, True)
		if (i, j) == (-1, -1):
			s.send('{"cmd" : "end", "p1": "DRAW", "p2": 0}'.encode('ascii'))
			time.sleep(0.5)
			break
		else:
			game[i][j] = 'X'
			s.send(('{"cmd" : "move", "p1":' + str(i) + ', "p2": ' + str(j) + '}').encode('ascii'))
			time.sleep(0.5)
		
		(v, i, j) = minimax(game, False)
		if (i, j) == (-1, -1):
			s.send('{"cmd" : "end", "p1": "DRAW", "p2": 0}'.encode('ascii'))
			time.sleep(0.5)
			break
		else:
			game[i][j] = 'O'
			s.send(('{"cmd" : "move", "p1":' + str(i) + ', "p2": ' + str(j) + '}').encode('ascii'))
			time.sleep(0.5)


def getGameDetails(first, second):
	first.send('{"cmd" : "first", "p1" : 0, "p2" : 0}'.encode('ascii'))
	second.send('{"cmd" : "second", "p1" : 0, "p2" : 0}'.encode('ascii'))

	global J, K, L
	resp = json.loads(first.recv(1024).decode('ascii')) # size
	K = resp['p1']
	L = resp['p2']
	resp = json.loads(first.recv(1024).decode('ascii')) # length
	J = resp['p1']

	second.send(('{"cmd" : "size", "p1" : ' + str(K) + ', "p2" : ' + str(L) + '}').encode('ascii'))
	time.sleep(1)
	second.send(('{"cmd" : "length", "p1" : ' + str(J) + ', "p2" : 0}').encode('ascii'))


def handlePvP(s1, s2):
	resp1 = json.loads(s1.recv(1024).decode('ascii')) # start1
	resp2 = json.loads(s2.recv(1024).decode('ascii')) # start2

	print(resp1['p1'], resp2['p1'])
	if resp1['p1'] < resp2['p1']:
		s1, s2 = s2, s1
	getGameDetails(s1, s2)
	setJK(J, K)
	game = [['-'] * L for _ in range(K)]

	while True:
		msg = s1.recv(1024)
		print(msg)
		s2.send(msg) # let player2 know where player1 moved
		time.sleep(0.5)
		mv = json.loads(msg.decode('ascii')) # move
		i = mv['p1']
		j = mv['p2']
		game[i][j] = 'X'

		if givenPlayerWon(game, 'X'):
			s1.send('{"cmd" : "end", "p1": "YOU WON", "p2": 0}'.encode('ascii'))
			s2.send('{"cmd" : "end", "p1": "YOU LOST", "p2": 0}'.encode('ascii'))
			break
		else:
			s1.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))
			s2.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))
		
		time.sleep(0.5)
		msg = s2.recv(1024)
		s1.send(msg) # let player1 know where player2 moved
		time.sleep(0.5)
		mv = json.loads(msg.decode('ascii')) # move
		i = mv['p1']
		j = mv['p2']
		game[i][j] = 'O'

		if givenPlayerWon(game, 'O'):
			s1.send('{"cmd" : "end", "p1": "YOU LOST", "p2": 0}'.encode('ascii'))
			s2.send('{"cmd" : "end", "p1": "YOU WON", "p2": 0}'.encode('ascii'))
			break
		elif len([(r,c) for r in range(K) for c in range(L) if game[r][c] == '-']) == 0:
			s1.send('{"cmd" : "end", "p1": "DRAW", "p2": 0}'.encode('ascii'))
			s2.send('{"cmd" : "end", "p1": "DRAW", "p2": 0}'.encode('ascii'))
			break
		else:
			s1.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))
			s2.send('{"cmd" : "continue", "p1": 0, "p2": 0}'.encode('ascii'))
	
	time.sleep(1)
	s1.close()
	s2.close()
		

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	PORT = 3333
	s.bind(('localhost', PORT))
	s.listen(2)

	connection1, addr = s.accept()      
	print('Connected 1')
	connection1.send('connected'.encode('ascii'))
	resp1 = json.loads(connection1.recv(1024).decode('ascii'))
	print(resp1)
	
	# switch mode
	if resp1['p1'] == 0:
		handleCvC(connection1)
	elif resp1['p1'] == 1:
		handlePvC(connection1)
	else:
		connection1.send('{"cmd" : "wait", "p1" : 0, "p2" : 0}'.encode('ascii'))
		connection2, addr = s.accept()
		connection2.send('connected'.encode('ascii'))
		connection2.recv(1024)
		print('Connected 2')
		handlePvP(connection1, connection2)
	# connection1.send('{"cmd" : "first", "p1" : "0", "p2" : "0"}'.encode('ascii'))
	# connection2, addr = s.accept()
	# print('Connected 2')
	# connection2.send('connected'.encode('ascii'))

	# resp1 = connection1.recv(1024).decode('ascii')
	# resp1 = json.loads(resp1)
	# rand1 = float(resp1['p1'])
	# resp2 = connection2.recv(1024).decode('ascii')
	# resp2 = json.loads(resp2)
	# rand2 = float(resp2['p1'])

	# print(K, J)
	
	# if rand1 > rand2:
	# 	askFirstPlayer(connection1, connection2)
	# 	game = [['-'] * K for _ in range(K)]
	# 	playerVsPlayer(game, connection1, connection2)
	# else:
	# 	askFirstPlayer(connection2, connection1)
	# 	game = [['-'] * K for _ in range(K)]
	# 	playerVsPlayer(game, connection2, connection1)
	
	# connection1.close()
	# connection2.close()

	s.close()
