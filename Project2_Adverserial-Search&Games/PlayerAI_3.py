from random import randint
from BaseAI_3 import BaseAI

# Numbers that may spawn
possible_nums = [2,4]
 
class PlayerAI(BaseAI):
	def getMove(self, grid):
		moves = grid.getAvailableMoves()
		return self.search(grid)

	# Return the best move to be made
	def search(self, grid):
		moves = grid.getAvailableMoves()
		max_value = -1
		best_move = -1

		# Try each available move
		for move in moves:
			gridCopy = grid.clone()
			gridCopy.move(move)

			value = self.maxValue(gridCopy, 1, -1e9, 1e9)
			if (value > max_value):
				max_value = value
				best_move = move
		return best_move

	def maxValue(self, grid, depth, alpha, beta):
		moves = grid.getAvailableMoves()
		if len(moves) == 0:
			return 0;
		max_value = -1e9

		# Try each available move
		for move in moves:
			gridCopy = grid.clone()
			gridCopy.move(move)
			max_value = max(max_value, self.minValue(gridCopy, depth + 1, alpha, beta))
			if (max_value >= beta):
				return max_value
			alpha = max(alpha, max_value)
		return max_value

	def minValue(self, grid, depth, alpha, beta):
		if depth == 4:
			return self.utility(grid)
		cells = grid.getAvailableCells()
		min_value = 1e9

		for cell in cells:
			gridCopy = grid.clone()
			for num in possible_nums:
				gridCopy.setCellValue(cell, num)
				min_value = min(min_value, self.maxValue(gridCopy, depth + 1, alpha, beta))
			if (min_value <= alpha):
				return min_value
			beta = min(beta, min_value)
		return min_value

	def utility(self, grid):
		ret = 0
		max_cell = 0
		max_corner = -1
		max_corner_pos = (-1,-1)
		max_side = 0
		total = 16

		# Get average cell number
		sum = 0
		for i in range(4):
			for j in range(4):
				cell_value = grid.getCellValue((i, j))
				max_cell = max(max_cell, cell_value)

				# Treat empty cells preciously
				if cell_value == 0:
					total -= 1
				elif (i, j) in [(0,0),(0,3),(3,3),(3,3)]:
					max_corner = max(max_corner, cell_value)
					max_corner_pos = (i,j)
				elif i in [0,3] or j in [0,3]:
					max_side = max(max_side, cell_value)

				sum += cell_value

		di = [0,-1,1,0]
		dj = [1,0,0,-1]
		if max_corner == max_cell:
			ret += 10000
			for i in range(4):
				x = max_corner_pos[0] + di[i]
				y = max_corner_pos[1] + dj[i]
				if not grid.crossBound((x, y)):
					ret += grid.map[x][y] * 10
		for i in range(4):
			for j in range(4):
				ret += grid.map[i][j] * (6 - abs(i - max_corner_pos[0] + j - max_corner_pos[1]))
		ret += sum / total

		# Each 2 contiguous similar cells add their summed value to the utility
		vis = [[False for i in range(4)] for j in range(4)]
		for i in range(4):
			for j in range(4):
				if grid.map[i][j] != 0 and not vis[i][j]:
					for k in range(4):
						x = i + di[k]
						y = j + dj[k]
						if (not grid.crossBound((x, y)) and not vis[x][y] and
						grid.map[i][j] == grid.map[x][y]):
							vis[i][j] = vis[x][y] = True
							ret += grid.map[i][j] * 2

				# The cell with maximum value must stick to a side
				#if grid.map[i][j] == max_cell :
				#	if (i, j) in [(0,0),(0,3),(3,3),(3,3)]:
				#		ret += 1e5
				#	elif i in [0,3] or j in [0,3]:
				#		ret += 50000
		
		return ret
