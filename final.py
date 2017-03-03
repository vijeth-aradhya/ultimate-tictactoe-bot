import sys
import random
import signal
import time
import copy


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
		return (mult + (us_num-them_num)*pow(2, abs(us_num-them_num)))

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
				# print "\n\nWAIT\n\n"
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
						# print "\n\n"
						# print "FULL DEPTH not reached --> ", depth
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
						# print "\n\n"
						# print "FULL DEPTH not reached --> ", depth
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