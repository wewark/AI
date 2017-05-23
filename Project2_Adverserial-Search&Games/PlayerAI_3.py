from random import randint
from BaseAI_3 import BaseAI
import math

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

			value = self.minValue(gridCopy, 1, -1e9, 1e9)
			if (value > max_value):
				max_value = value
				best_move = move
		#print(max_value)
		return best_move

	def maxValue(self, grid, depth, alpha, beta):
		moves = grid.getAvailableMoves()
		if len(moves) == 0:
			return 0
		if depth == 2:
			return self.utility(grid)
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
		cells = []
		total = 16

		sum = 0
		for i in range(4):
			for j in range(4):
				cell_value = grid.getCellValue((i, j))

				if cell_value == 0:
					total -= 1
				else:
					cells.append(cell_value)

				sum += cell_value


		# Average
		ret += sum / total

		# Median
		cells.sort()
		if total % 2 == 0:
			ret += (cells[int(total / 2)] + cells[int(total / 2) - 1]) / 2
		else:
			ret += cells[math.floor(total / 2)]

		# Each 2 contiguous similar cells add their value to the utility
		di = [0,-1,1,0]
		dj = [1,0,0,-1]
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
							ret += grid.map[i][j] * 1.5
		
		# Most important one
		monotonicity = max(
			self.mono(grid, (0,0), (1,1)),
			self.mono(grid, (0,3), (1,-1)),
			self.mono(grid, (3,3), (-1,-1)),
			self.mono(grid, (3,0), (-1,1)))
		ret += monotonicity

		return ret

	def mono(self, grid, pos, dir):
		if grid.map[pos[0]][pos[1]] == 0: return 0;
		ret = grid.map[pos[0]][pos[1]] ** 2
		if not grid.crossBound((pos[0] + dir[0], pos[1])) and grid.map[pos[0] + dir[0]][pos[1]] <= grid.map[pos[0]][pos[1]]:
			ret += self.mono(grid, (pos[0] + dir[0], pos[1]), dir)
		if not grid.crossBound((pos[0], pos[1] + dir[1])) and grid.map[pos[0]][pos[1] + dir[1]] <= grid.map[pos[0]][pos[1]]:
			ret += self.mono(grid, (pos[0], pos[1] + dir[1]), dir)
		return ret;
