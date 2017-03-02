import sys
import random
import signal
import time
import copy


class Two_Dudes_With_IterSearch():
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
		for i in range(0, 16):
			for j in range(0, 16):
				print self.whole_board_heuristic[i][j],
			print ""
		"""

		return self.iterSearch(board, old_move)

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
				# print (k1/4, k2/4)
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
					total_cells_val += self.getWinValue(us_num, them_num, empty)
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
					total_cells_val += self.getWinValue(us_num, them_num, empty)
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
				total_cells_val += self.getWinValue(us_num, them_num, empty)
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
				total_cells_val += self.getWinValue(us_num, them_num, empty)
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

		return (total_cells_val+self.getCellValue(board.block_status)*100)

	def iterSearch(self, board, old_move):
		self.total_depth = 3
		while self.stop is False:
			self.best_move = self.nextMove(board, 0, self.us, -self.inf*1000, self.inf*1000, old_move)
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

		inc_depth = 1

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
				value = self.nextMove(new_board, depth+inc_depth, self.them, alpha, beta, curr_move)
				if depth == 0:
					total_branching += 1
				if self.stop is False:
					if (time.time() - self.startTime) >= 14.9:
						print "\n\n"
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
				print "Curr iter", self.total_depth
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
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+inc_depth, self.us, alpha, beta, curr_move)
				if self.stop is False:	
					if (time.time() - self.startTime) >= 14.9:
						print "\n\n"
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

class Two_Dudes():
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
				inc_depth += 2
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+inc_depth, self.them, alpha, beta, curr_move)
				if depth == 0:
					total_branching += 1
				if self.stop is False:
					if (time.time() - self.startTime) >= 14.9:
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
				inc_depth += 2
			for curr_move in valid_moves:
				new_board = copy.deepcopy(board)
				new_board.update(old_move, curr_move, curr_player)
				value = self.nextMove(new_board, depth+inc_depth, self.us, alpha, beta, curr_move)
				if self.stop is False:	
					if (time.time() - self.startTime) >= 14.9:
						self.stop = True
						break
				else:
					break
				best_val = min(best_val, value)
				beta = min( beta, best_val)
				if beta <= alpha:
					break
			return best_val