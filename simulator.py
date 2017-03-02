import sys
import random
import signal
import time
import copy
# from swag39 import *
# from working import *


class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Two_Dudes():
	def __init__(self):
		self.us = None
		self.them = None
		self.find_ply = False
		self.inf = 1000000000
		self.startTime = None
		self.stop = False
		self.mult_factor = [[0 for i in range(4)] for j in range(4)]
		self.whole_board_heuristic = [[0 for i in range(16)] for j in range(16)]
		self.best_move = None
		self.hash_table = {}
		self.hash_cell = [['-' for i in range(4)] for j in range(4)]
		self.choose = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
		pass

	def move(self, board, old_move, flag):
		# You have to implement the move function with the same signature as this
		# Find the list of valid cells allowed
		self.startTime = time.time()
		self.stop = False
		if self.find_ply is False:
			if old_move != (-1, -1):
				self.us = 'o'
				self.them = 'x'
			else:
				self.us = 'x'
				self.them = 'o'
			self.find_ply = True

			# Hashing
			# self.performHashing(self.hash_cell, 0, [])

			# Generating the whole board heuristic in the beginning
			for i in range(0, 16, 4):
				for j in range(0, 16, 4):
					t1 = i/4
					t2 = j/4
					if (((t1 == 0 or t1 == 3) and (t2 == 1 or t2 == 2)) or ((t2 == 0 or t2 == 3) and (t1 == 1 or t1 == 2))):
						mult = 1
					else:
						mult = 3
					for k1 in range(i, i+4):
						for k2 in range(j, j+4):
							if (((k1-i) == 0 or (k1-i) == 3) and ((k2-j) == 1 or (k2-j) == 2)) or (((k2-j) == 0 or (k2-j) == 3) and ((k1-i) == 1 or (k1-i) == 2)):
								self.whole_board_heuristic[k1][k2] = 5*mult
							else:
								self.whole_board_heuristic[k1][k2] = 10*mult

		"""
		# Printing HashTable
		for k, v in self.hash_table.iteritems():
			print k, v
			print ""
		"""

		"""
		for i in range(0, 16):
			for j in range(0, 16):
				print self.whole_board_heuristic[i][j],
			print ""
		"""

		return self.iterSearch(board, old_move)

	def performHashing(self, cell, index, hash_string_list):
		if index == 16:
			self.hash_table.update({''.join(hash_string_list) : self.getCellValue(cell)})
			"""
			print "\n\n"
			print ''.join(hash_string_list)
			for i in range(4):
				for j in range(4):
					print cell[i][j],
				print ""
			print ""
			print self.getCellValue(cell)
			print "\n\n"
			"""
			return
		temp_index = random.randint(0, 1)
		if(self.choose[temp_index][0]):
			hash_string_list.append('-')
			self.performHashing(cell, index+1, hash_string_list)
			hash_string_list.pop()
		if(self.choose[temp_index][1]):
			hash_string_list.append('x')
			cell[(index//4)][index%4] = 'x'
			self.performHashing(cell, index+1, hash_string_list)
			hash_string_list.pop()
			cell[(index//4)][index%4] = '-'
		if(self.choose[temp_index][2]):
			hash_string_list.append('o')
			cell[(index//4)][index%4] = 'o'
			self.performHashing(cell, index+1, hash_string_list)
			hash_string_list.pop()
			cell[(index//4)][index%4] = '-'


	def getWinValue(self, us_num, them_num, empty):
		mult = 0
		if empty == 0:
			if us_num == 0:
				mult = -self.inf
			elif them_num == 0:
				mult = self.inf
		elif them_num == 0:
			if empty == 1:
				mult = 10000
			elif empty == 2:
				mult = 10
			elif empty == 3:
				mult = 5
		elif us_num == 0:
			if empty == 1:
				mult = -10000
			elif empty == 2:
				mult = -10
			elif empty == 3:
				mult = -5
		return mult

	def getCellValue(self, cell):

		# heuristic 2
		heuristic_2 = 0
		for i in range(4):
			empty = 0
			us_num = 0
			them_num = 0
			for j in range(4):
				if cell[i][j] == '-':
					empty += 1
				elif cell[i][j] == self.us:
					us_num += 1
				else:
					them_num += 1
			heuristic_2 += self.getWinValue(us_num, them_num, empty)

		for j in range(4):
			empty = 0
			us_num = 0
			them_num = 0
			for i in range(4):
				if cell[i][j] == '-':
					empty += 1
				elif cell[i][j] == self.us:
					us_num += 1
				else:
					them_num += 1
			heuristic_2 += self.getWinValue(us_num, them_num, empty)

		empty = 0
		us_num = 0
		them_num = 0
		for i in range(4):
			if cell[i][i] == '-':
				empty += 1
			elif cell[i][i] == self.us:
				us_num += 1
			else:
				them_num += 1
		heuristic_2 += self.getWinValue(us_num, them_num, empty)

		empty = 0
		us_num = 0
		them_num = 0
		for i in range(4):
			if cell[i][3-i] == '-':
				empty += 1
			elif cell[i][3-i] == self.us:
				us_num += 1
			else:
				them_num += 1
		heuristic_2 += self.getWinValue(us_num, them_num, empty)

		"""
		print "\n--- CELL HEURISTICS ---\n"

		for i in range(4):
			for j in range(4):
				print cell[i][j],
			print ""

		print "Heuritstic 1 : ", heuristic_1
		print "Heuritstic 2 : ", heuristic_2*10

		print ""
		"""
		return (heuristic_2*30)
		# return (heuristic_1 + (heuristic_2*10))

	def getExpectedVal(self, board, our_move):
		# MAIN HEURISTIC FUNCTION

		# print "\n\nDEBUG\n\n"
		# board.print_board()

		total_cells_val = 0
		for k1 in range(0, 16):
			for k2 in range(0, 16):
				if board.board_status[k1][k2] == self.us:
					total_cells_val += self.whole_board_heuristic[k1][k2]
				elif board.board_status[k1][k2] == self.them:
					total_cells_val -= self.whole_board_heuristic[k1][k2]

		# h = total_cells_val
		# h2 = total_cells_val
		# print "\n\nH 1 : ", h

		for k1 in range(0, 16, 4):
			for k2 in range(0, 16, 4):

				"""
				# Make use of hashing
				temp_key = []
				for i in range(k1, k1+4):
					for j in range(k2, k2+4):
						temp_key.append(board.board_status[i][j])
				temp_val = self.hash_table.get(''.join(temp_key))
				if temp_val is not None:

					print "Gotcha!"
					for o in range(k1, k1+4):
						for p in range(k2, k2+4):
							print board.board_status[o][p],
						print ""

					print "\n\n"

					tt = ''.join(temp_key)
					t = o//4
					for o in range(16):
						if (t != (o//4)):
							print ""
							t = (o//4)
						print tt[o],

					print ""


					total_cells_val += temp_val
					continue

				"""
				# Normal Heuristic
				for i in range(k1, k1+4):
					empty = 0
					us_num = 0
					them_num = 0
					for j in range(k2, k2+4):
						if board.board_status[i][j] == '-':
							empty += 1
						elif board.board_status[i][j] == self.us:
							us_num += 1
						else:
							them_num += 1
					total_cells_val += self.getWinValue(us_num, them_num, empty)*30
				# print "H_2 a : ", (total_cells_val - h2)
				# h2 = total_cells_val

				for j in range(k2, k2+4):
					empty = 0
					us_num = 0
					them_num = 0
					for i in range(k1, k1+4):
						if board.board_status[i][j] == '-':
							empty += 1
						elif board.board_status[i][j] == self.us:
							us_num += 1
						else:
							them_num += 1
					total_cells_val += self.getWinValue(us_num, them_num, empty)*30
				# print "H_2 b : ", (total_cells_val - h2)
				# h2 = total_cells_val

				empty = 0
				us_num = 0
				them_num = 0
				for i in range(k1, k1+4):
					if board.board_status[i][k2+(i-k1)] == '-':
						empty += 1
					elif board.board_status[i][k2+(i-k1)] == self.us:
						us_num += 1
					else:
						them_num += 1
				total_cells_val += self.getWinValue(us_num, them_num, empty)*30
				# print "H_2 c : ", (total_cells_val - h2)
				# h2 = total_cells_val

				empty = 0
				us_num = 0
				them_num = 0
				for i in range(k1, k1+4):
					if board.board_status[i][(k2+3)-(i-k1)] == '-':
						empty += 1
					elif board.board_status[i][(k2+3)-(i-k1)] == self.us:
						us_num += 1
					else:
						them_num += 1
				total_cells_val += self.getWinValue(us_num, them_num, empty)*30
				# print "H_2 d : ", (total_cells_val - h2)
				# h2 = total_cells_val

		# print "H_2 : ", (total_cells_val-h)

		# print "\n\n"

		"""
		# heuristic 3
		if board.board_status[our_move[0] % 4][our_move[1] % 4] == '-':
			heuristic_3 = 10
		else:
			heuristic_3 = -10
		"""

		return (total_cells_val+self.getCellValue(board.block_status)*100*16)

	def iterSearch(self, board, old_move):
		self.total_depth = 3
		while self.stop is False:
			temp_best_move = self.nextMove(board, 0, self.us, -self.inf*1000, self.inf*1000, old_move)
			if self.stop is False:
				self.best_move = temp_best_move
			self.total_depth += 1
		return self.best_move

	def nextMove(self, board, depth, curr_player, alpha, beta, old_move):

		if depth >= self.total_depth:
			"""
			print "DEBUG\n\n"
			t = self.getExpectedVal(board, old_move)
			print "Expected value", t
			print ""
			board.print_board()
			print ""
			print "\n\n"
			return t
			"""
			return self.getExpectedVal(board, old_move)

		if depth == 0:
			total_branching = 0

		if curr_player == self.us:
			best_val = -self.inf*1000
			valid_moves = board.find_valid_move_cells(old_move)
			num_valid_moves = len(valid_moves)
			if num_valid_moves != 0:
				ret_move = valid_moves[0]
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+1, self.them, alpha, beta, curr_move)
				if depth == 0:
					total_branching += 1
				if self.stop is False:
					if (time.time() - self.startTime) >= 14.9:
						#print "\n\n"
						#print "FULL DEPTH not reached --> ", depth
						self.stop = True
						break
				else:
					break
				if value > best_val:
					best_val = value
					ret_move = curr_move
				alpha = max(alpha, best_val)
				if beta <= alpha:
					#print "Is_pruned :", (depth, self.total_depth)
					break
			if depth == 0:
				"""
				print "\n\n"
				print "Curr iter :", self.total_depth
				print "Valid moves :", valid_moves
				# print "Is_pruned :", total_prune
				print "Total number of branches :", total_branching, "out of", num_valid_moves
				print "\n\n"
				"""
				return ret_move
			else:
				return best_val
		else:
			best_val = self.inf*1000
			valid_moves = board.find_valid_move_cells(old_move)
			num_valid_moves = len(valid_moves)
			if num_valid_moves != 0:
				ret_move = valid_moves[0]
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+1, self.us, alpha, beta, curr_move)
				if self.stop is False:
					if (time.time() - self.startTime) >= 14.9:
						#print "\n\n"
						#print "FULL DEPTH not reached --> ", depth
						self.stop = True
						break
				else:
					break
				best_val = min(best_val, value)
				beta = min( beta, best_val)
				if beta <= alpha:
					#print "Is_pruned :", (depth, self.total_depth)
					break
			return best_val

class Random_Player():
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		return cells[random.randrange(len(cells))]

class Manual_Player:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.board_status = [['-' for i in range(16)] for j in range(16)]
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print 
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print

	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules

		if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(16):
					if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))
		return allowed_cells

	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0
		cntd = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1
				if bs[i][j] == 'd':
					cntd += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				return (col[0],'WON')
		#checking if diagnols have been won or not
		if(bs[0][0] == bs[1][1] == bs[2][2] ==bs[3][3]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[0][3] == bs[1][2] == bs[2][1] ==bs[3][0]) and (bs[0][3] == 'x' or bs[0][3] == 'o'):
			return (bs[0][3],'WON')

		if cntx+cnto+cntd <16:		#if all blocks have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL'
		self.board_status[new_move[0]][new_move[1]] = ply

		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		bs = self.board_status
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				self.block_status[x][y] = ply
				return 'SUCCESSFUL'

		#checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return 'SUCCESSFUL'
		self.block_status[x][y] = 'd'
		return 'SUCCESSFUL'

def gameplay(obj1, obj2):				#game simulator

	game_board = Board()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1)
	WINNER = ''
	MESSAGE = ''
	TIME = 15
	pts1 = 0
	pts2 = 0

	game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while(1):
		#player 1 turn
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)
		# startTime = time.time()

		try:									#try to get player 1's move			
			p1_move = obj1.move(game_board, old_move, fl1)
			# print "Time spent %.3f" % (time.time() - startTime)
			# print "Valid move played : " + str(p1_move)
		except TimedOutExc:					#timeout error
#			print e
			WINNER = 'P2'
			MESSAGE = 'TIME OUT'
			pts2 = 16
			break
		except Exception as e:
			# print "Time spent %.3f" % (time.time() - startTime)
			# print "Invalid move played : " + str(p1_move)
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16		
			break
		signal.alarm(0)

		#check if board is not modified and move returned is valid
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P2'
			MESSAGE = 'MODIFIED THE BOARD'
			pts2 = 16
			break
		if game_board.update(old_move, p1_move, fl1) == 'UNSUCCESSFUL':
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16
			break

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':							#if the game has ended after a player1 move, player 1 would win
			pts1 = 16
			WINNER = 'P1'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break

		old_move = p1_move
		game_board.print_board()

		#do the same thing for player 2
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)
		startTime = time.time()

		# p2_move = obj2.move(game_board, old_move, fl2)
		try:
			p2_move = obj2.move(game_board, old_move, fl2)
			print "Time spent %.3f" % (time.time() - startTime)
			print "Valid move played : " + str(p2_move)
		except TimedOutExc:
			WINNER = 'P1'
			MESSAGE = 'TIME OUT'
			pts1 = 16
			break
		except Exception as e:
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE'
			pts1 = 16			
			break
		signal.alarm(0)
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P1'
			MESSAGE = 'MODIFIED THE BOARD'
			pts1 = 16
			break
		if game_board.update(old_move, p2_move, fl2) == 'UNSUCCESSFUL':
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE'
			pts1 = 16
			break

		status = game_board.find_terminal_state()	#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':						#if the game has ended after a player move, player 2 would win
			pts2 = 16
			WINNER = 'P2'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':					
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break
		game_board.print_board()
		old_move = p2_move

	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for i in range(4):
		for j in range(4):
			if game_board.block_status[i][j] == 'x':
				x += 1
			if game_board.block_status[i][j] == 'o':
				o += 1
			if game_board.block_status[i][j] == 'd':
				d += 1
	print 'x:', x, ' o:',o,' d:',d
	if MESSAGE == 'DRAW':
		pts1 = x
		pts2 = o
	return (pts1,pts2)

class Two_Dudes_1():
	def __init__(self):
		self.us = None
		self.them = None
		self.find_ply = False
		self.inf = 1000000000
		self.startTime = None
		self.stop = False
		self.mult_factor = [[0 for i in range(4)] for j in range(4)]
		pass

	def move(self, board, old_move, flag):
		# You have to implement the move function with the same signature as this
		# Find the list of valid cells allowed
		if self.find_ply is False:
			if old_move != (-1, -1):
				self.us = 'o'
				self.them = 'x'
			else:
				self.us = 'x'
				self.them = 'o'
			self.find_ply = True
		self.startTime = time.time()
		self.stop = False
		return self.nextMove(board, 0, self.us, -self.inf*1000, self.inf*1000, old_move)

	def setBlockMultFactor(self, board):
		for i in range(4):
			for j in range(4):
				if ((i == 0 or i == 3) and (j == 1 or j == 2)) or ((j == 0 or j == 3) and (i == 2 or i == 1)):
					if board.block_status[i][j] == self.us:
						self.mult_factor[i][j] = 2
					elif board.block_status[i][j] == '-':
						self.mult_factor[i][j] = 1
					else:
						self.mult_factor[i][j] = -2
				else:
					if board.block_status[i][j] == self.us:
						self.mult_factor[i][j] = 5
					elif board.block_status[i][j] == '-':
						self.mult_factor[i][j] = 1
					else:
						self.mult_factor[i][j] = -5

	def getWinValue(self, us_num, them_num, empty):
		mult = 0
		if empty == 0:
			if us_num == 0:
				mult = -self.inf
			elif them_num == 0:
				mult = self.inf
		elif them_num == 0:
			if empty == 1:
				mult = 100
			elif empty == 2:
				mult = 2
		elif us_num == 0:
			if empty == 1:
				mult = -100
			elif empty == 2:
				mult = -2
		return mult

	def getCellValue(self, cell):

		# heuristic 1
		heuristic_1 = 0
		for i in range(4):
			for j in range(4):
				if ((i == 0 or i == 3) and (j == 1 or j == 2)) or ((j == 0 or j == 3) and (i == 1 or i == 2)):
					if cell[i][j] == self.us:
						heuristic_1 += 5
					elif cell[i][j] == self.them:
						heuristic_1 += -5
				else:
					if cell[i][j] == self.us:
						heuristic_1 += 10
					elif cell[i][j] == self.them:
						heuristic_1 += -10

		# heuristic 2
		heuristic_2 = 0
		for i in range(4):
			empty = 0
			us_num = 0
			them_num = 0
			for j in range(4):
				if cell[i][j] == '-':
					empty += 1
				elif cell[i][j] == self.us:
					us_num += 1
				else:
					them_num += 1
			heuristic_2 += self.getWinValue(us_num, them_num, empty)

		for j in range(4):
			empty = 0
			us_num = 0
			them_num = 0
			for i in range(4):
				if cell[i][j] == '-':
					empty += 1
				elif cell[i][j] == self.us:
					us_num += 1
				else:
					them_num += 1
			heuristic_2 += self.getWinValue(us_num, them_num, empty)

		empty = 0
		us_num = 0
		them_num = 0
		for i in range(4):
			if cell[i][i] == '-':
				empty += 1
			elif cell[i][i] == self.us:
				us_num += 1
			else:
				them_num += 1
		heuristic_2 += self.getWinValue(us_num, them_num, empty)

		empty = 0
		us_num = 0
		them_num = 0
		for i in range(4):
			if cell[i][3-i] == '-':
				empty += 1
			elif cell[i][3-i] == self.us:
				us_num += 1
			else:
				them_num += 1
		heuristic_2 += self.getWinValue(us_num, them_num, empty)

		"""
		print "\n--- CELL HEURISTICS ---\n"

		for i in range(4):
			for j in range(4):
				print cell[i][j],
			print ""

		print "Heuritstic 1 : ", heuristic_1
		print "Heuritstic 2 : ", heuristic_2*10

		print ""
		"""

		return (heuristic_1 + (heuristic_2*10))

	def getExpectedVal(self, board, our_move):
		# WHOLE BOARD
		# self.setBlockMultFactor(board)
		total_cells_val = 0
		temp_cell = [[0 for i in range(4)] for j in range(4)]
		for i in range(0, 16, 4):
			for j in range(0, 16, 4):
				for k1 in range(i, i+4):
					for k2 in range(j, j+4):
						temp_cell[k1-i][k2-j] = board.board_status[k1][k2]
				t1 = i % 4
				t2 = j % 4
				if ((t1 == 0 or t1 == 3) and (t2 == 1 or t2 == 2)) or ((t2 == 0 or t2 == 3) and (t1 == 1 or t1 == 2)):
					mult = 1
				else:
					mult = 3
				total_cells_val += self.getCellValue(temp_cell)*mult

		"""
		# heuristic 3
		if board.board_status[our_move[0] % 4][our_move[1] % 4] == '-':
			heuristic_3 = 10
		else:
			heuristic_3 = -10
		"""

		return (total_cells_val+self.getCellValue(board.block_status)*100)

	def nextMove(self, board, depth, curr_player, alpha, beta, old_move):

		if depth >= 5:
			"""
			print "DEBUG\n\n"
			t = self.getExpectedVal(board, old_move)
			print "Expected value", t
			print ""
			board.print_board()
			print ""
			print "\n\n"
			return t
			"""
			return self.getExpectedVal(board, old_move)

		inc_depth = 1

		if depth == 0:
			total_branching = 0

		if curr_player == self.us:
			best_val = -self.inf*1000
			valid_moves = board.find_valid_move_cells(old_move)
			num_valid_moves = len(valid_moves)
			if num_valid_moves != 0:
				ret_move = valid_moves[0]
			if num_valid_moves > 16:
				# print "Increasing depth by 1"
				inc_depth += 1
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+inc_depth, self.them, alpha, beta, curr_move)
				if depth == 0:
					total_branching += 1
				if self.stop is False:
					if (time.time() - self.startTime) >= 14.9:
						print "\n\n"
						print "OLD"
						print "FULL DEPTH not reached --> ", depth
						self.stop = True
						break
				else:
					break
				if value > best_val:
					best_val = value
					ret_move = curr_move
				alpha = max(alpha, best_val)
				if beta <= alpha:
					break
			if depth == 0:
				print "\n\n"
				print "OLD"
				print "Total number of branches : ", total_branching, "out of", num_valid_moves
				print "\n\n"
				return ret_move
			else:
				return best_val
		else:
			best_val = self.inf*1000
			valid_moves = board.find_valid_move_cells(old_move)
			num_valid_moves = len(valid_moves)
			if num_valid_moves != 0:
				ret_move = valid_moves[0]
			if num_valid_moves > 16:
				inc_depth += 1
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+inc_depth, self.us, alpha, beta, curr_move)
				if self.stop is False:	
					if (time.time() - self.startTime) >= 14.9:
						print "OLD"
						print "FULL DEPTH not reached --> ", depth
						self.stop = True
						break
				else:
					break
				best_val = min(best_val, value)
				beta = min( beta, best_val)
				if beta <= alpha:
					break
			return best_val


if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]
	if option == '1':
		obj1 = Two_Dudes_1()
		obj2 = Two_Dudes()

	elif option == '2':
		obj1 = Two_Dudes()
		obj2 = Two_Dudes()
	elif option == '3':
		obj1 = Random_Player()()
		obj2 = Two_Dudes_1()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(obj1, obj2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]
