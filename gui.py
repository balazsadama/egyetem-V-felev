import socket
import random
import json
import _thread as thread
import tkinter as tk
import time
root = tk.Tk()

HEIGHT = 600
WIDTH = 800

K = 0
L = 0
J = 0
mode = -1

port = 3333
s = socket.socket()



def modeSelected(m):
	global mode
	mode = m

	gameModeFrame.pack_forget()
	s.connect(('localhost', port))
	print(s.recv(1024).decode('ascii'))
	
	msgMode = '{"cmd" : "mode", "p1" : ' + str(mode) + ', "p2" : 0}'
	s.send(msgMode.encode('ascii'))
	if mode == 0: # computer vs computer
		dimensionsFrame.pack()
	elif mode == 1: # player vs computer
		dimensionsFrame.pack()
	else: # player vs player
		msg = ('{"cmd" : "start", "p1" : ' + str(random.random()) + ', "p2" : 0}').encode('ascii')
		s.send(msg)
		msg = s.recv(1024).decode('ascii')
		msg = json.loads(msg)
		# print(msg)
		if msg['cmd'] == 'wait':
			waitJoinFrame.pack()
			thread.start_new_thread(handleWait, ())
			# msg = s.recv(1024).decode('ascii')
			# msg = json.loads(msg)
			# waitJoinFrame.pack_forget()
			# if msg['cmd'] == 'first':
			# 	dimensionsFrame.pack()
			# else: # second
			# 	waitBeginFrame.pack()
		elif msg['cmd'] == 'first':
			dimensionsFrame.pack()
		else: # second
			waitBeginFrame.pack()
			thread.start_new_thread(waitForGameDetails, ())
		

def handleWait():
	msg = s.recv(1024).decode('ascii')
	msg = json.loads(msg)
	waitJoinFrame.pack_forget()
	if msg['cmd'] == 'first':
		dimensionsFrame.pack()
	else: # second
		waitBeginFrame.pack()
		thread.start_new_thread(waitForGameDetails, ())


def waitForGameDetails():
	global J, K, L
	msg = s.recv(1024).decode('ascii')
	msg = json.loads(msg)
	K = msg['p1']
	L = msg['p2']
	msg = json.loads(s.recv(1024).decode('ascii'))
	J = msg['p1']

	for i in range(K):
		buttons.append([])
		frames.append(tk.Frame(frame))
		for j in range(L):
			buttons[i].append(tk.Button(frames[i], text='  ', command=lambda x=(i,j): buttonClicked(x, 'X')))
			buttons[i][j].pack(side='left')
		frames[i].pack()
	
	waitBeginFrame.pack_forget()
	# thread.start_new_thread(handlePvP, ())
	thread.start_new_thread(waitOpponentMove, ())


def buttonClicked(coords, text):
	(i,j) = coords
	if buttons[i][j]['text'] == '  ':
		buttons[i][j]['text'] = text
		msg = '{"cmd" : "move", "p1" : ' + str(i) + ', "p2" : ' + str(j) + '}'
		s.send(msg.encode('ascii'))
		
		# continue or end
		resp = s.recv(1024).decode('ascii')
		resp = json.loads(resp)
		if not(type(resp) is dict):
			resp = json.loads(resp) # otherwise it stays as string
		if resp['cmd'] == 'end':
			print(resp['p1'])
			gameOver(resp['p1'], s)
		else:
			waitForOpponentLabel.pack()
			thread.start_new_thread(waitOpponentMove, ())


def waitOpponentMove():
	resp = s.recv(1024).decode('ascii')
	resp = json.loads(resp)
	if not(type(resp) is dict):
		resp = json.loads(resp) # otherwise it stays as string

	if resp['cmd'] == 'end':
		print(resp['p1'])
		gameOver(resp['p1'], s)
	else:
		i = resp['p1']
		j = resp['p2']
		buttons[i][j]['text'] = 'O'

		resp = s.recv(1024).decode('ascii')
		if not(type(resp) is dict):
			resp = json.loads(resp) # otherwise it stays as string
		if resp['cmd'] == 'end':
			print(resp['p1'])
			gameOver(resp['p1'], s)
	
	waitForOpponentLabel.pack_forget()


def gameOver(msg, conn):
	for i in range(K):
		frames[i].pack_forget()
	gameOverLabel['text'] = msg
	gameOverLabel.pack()
	conn.close()


def submitDimensions():
	global J, K, L
	K = int(entryX.get())
	L = int(entryY.get())
	J = int(entryJ.get())

	msg = '{"cmd" : "size", "p1" : ' + str(K) + ', "p2" : ' + str(L) + '}'
	s.send(msg.encode('ascii'))
	msg = '{"cmd" : "length", "p1" : ' + str(J) + ', "p2" : 0}'
	time.sleep(0.5)
	s.send(msg.encode('ascii'))

	for i in range(K):
		buttons.append([])
		frames.append(tk.Frame(frame))
		for j in range(L):
			buttons[i].append(tk.Button(frames[i], text='  ', command=lambda x=(i,j): buttonClicked(x, 'X')))
			buttons[i][j].pack(side='left')
		frames[i].pack()

	dimensionsFrame.pack_forget()

	# switch mode
	if mode == 0:
		# handleCvC()
		thread.start_new_thread(handleCvC, ())
	elif mode == 1:
		handlePvC()
	else:
		None
		# thread.start_new_thread(handlePvP, ())


def handlePvC():
	msg = '{"cmd" : "start", "p1" : "' + str(random.random()) + '", "p2" : "0"}'
	s.send(msg.encode('ascii'))

def handleCvC():
	player = ['X', 'O']
	p = 0
	while True:
		resp = s.recv(1024).decode('ascii')
		resp = json.loads(resp)
		if not(type(resp) is dict):
			resp = json.loads(resp) # otherwise it stays as string
		if resp['cmd'] == 'end':
			print(resp['p1'])
			gameOver(resp['p1'], s)
			break
		else:
			i = resp['p1']
			j = resp['p2']
			buttons[i][j]['text'] = player[p]
			p = 1 - p


def handlePvP():
	resp = json.loads(s.recv(1024).decode('ascii'))
	i = resp['p1']
	j = resp['p2']
	buttons[i][j]['text'] = 'O'
	# None
	# while True:
	# 	resp = json.loads(s.recv(1024).decode('ascii'))
	# 	if not(type(resp) is dict):
	# 		resp = json.loads(resp) # otherwise it stays as string
	# 	if resp['cmd'] == 'end':
	# 		print(resp['p1'])
	# 		gameOver(resp['p1'], s)
	# 		break
	# 	else:
	# 		i = resp['p1']
	# 		j = resp['p2']
	# 		buttons[i][j]['text'] = 'O'


# root
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root)
frame.place(relx=0.05, rely=0.05, relwidth=0.95, relheight=0.95)


# select game mode
gameModeFrame = tk.Frame(frame)
gameModeFrame.pack()

labelMode = tk.Label(gameModeFrame, text='Select game mode')
buttonComputerComputer = tk.Button(gameModeFrame, text='Computer vs Computer', command=lambda: modeSelected(0))
buttonPlayerComputer = tk.Button(gameModeFrame, text='Player vs Computer', command=lambda: modeSelected(1))
buttonPlayerPlayer = tk.Button(gameModeFrame, text='Player vs Player', command=lambda: modeSelected(2))
buttonComputerComputer.pack()
buttonPlayerComputer.pack()
buttonPlayerPlayer.pack()


# get dimensions
dimensionsFrame = tk.Frame(frame)

dimensionsLabel = tk.Label(dimensionsFrame, text='Game dimensions:')
dimensionsLabel.pack()

xFrame = tk.Frame(dimensionsFrame)
yFrame = tk.Frame(dimensionsFrame)
jFrame = tk.Frame(dimensionsFrame)
xFrame.pack()
yFrame.pack()
jFrame.pack()

labelX = tk.Label(xFrame, text='Rows')
labelY = tk.Label(yFrame, text='Columns')
labelJ = tk.Label(jFrame, text='Winning length')
labelX.pack(side='left')
labelY.pack(side='left')
labelJ.pack(side='left')

entryX = tk.Entry(xFrame)
entryY = tk.Entry(yFrame)
entryJ = tk.Entry(jFrame)
entryX.pack(side='left')
entryY.pack(side='left')
entryJ.pack(side='left')

buttons = []
frames = []

dimensionsButton = tk.Button(dimensionsFrame, text='Submit dimensions', command=lambda: submitDimensions())
dimensionsButton.pack(side='bottom')


# wait for other player to join
waitJoinFrame = tk.Frame(frame)
waitJoinLabel = tk.Label(waitJoinFrame, text='Waiting for another player to join...')
waitJoinLabel.pack()


# wait for other player to select game size
waitBeginFrame = tk.Frame(frame)
waitBeginLabel = tk.Label(waitBeginFrame, text='Waiting for the other player to set game settings...')
waitBeginLabel.pack()

waitForOpponentLabel = tk.Label(frame, text='Wait for your opponent to make a move...')

gameOverLabel = tk.Label(frame)

# buttons = []
# for i in range(5):
# 	# label = tk.Label(frame, text='X')
# 	# label.pack()
# 	buttons.append(tk.Button(frame, text='X'))
# 	buttons[i].pack()

# buttons[2]['state'] = 'disabled'

# button = tk.Button(frame, text='test button')
# button.pack()


root.mainloop()
# s.close()