import collections
import time
import os
import sys
import math
import heapq
#import resource
import psutil

def getCurrentMemory():
	pid = os.getpid()
	py = psutil.Process(pid)
	memoryUse = py.memory_info()[0] / 2. ** 30
	return memoryUse

class board(object):
	"Class for board states"
	def __init__(self, n, nums):
		self.size = n
		self.grid = []
		self.pos = (0, 0)
		if type(nums[0]) == int:
			for i in range(n):
				self.grid.append(nums[i * n: i * n + n])
				if 0 in self.grid[-1]:
					self.pos = (i, self.grid[-1].index(0))
		else:
			self.grid = nums
			for i in range(n):
				if 0 in self.grid[i]:
					self.pos = (i, self.grid[i].index(0))
					break

def isSolved(self):
	c = 0
	for i in range(self.size):
		for j in range(self.size):
			if self.grid[i][j] != c:
				return False
			c += 1
	return True

def canGoTo(self, dir):
	if (dir == 0 and self.pos[0] > 0 or dir == 1 and self.pos[0] < self.size - 1 or dir == 2 and self.pos[1] > 0 or dir == 3 and self.pos[1] < self.size - 1):
		return True
	return False

# Returns a board object after change, original object remains unchanged
def go(self, dir):
	tempgrid = [x[:] for x in self.grid]
	temp = board(self.size, tempgrid)
	i, j = temp.pos[0], temp.pos[1]
	if dir == 0:
		temp.grid[i][j], temp.grid[i - 1][j] = temp.grid[i - 1][j], temp.grid[i][j]
		temp.pos = (i - 1, j)
	elif dir == 1:
		temp.grid[i][j], temp.grid[i + 1][j] = temp.grid[i + 1][j], temp.grid[i][j]
		temp.pos = (i + 1, j)
	elif dir == 2:
		temp.grid[i][j], temp.grid[i][j - 1] = temp.grid[i][j - 1], temp.grid[i][j]
		temp.pos = (i, j - 1)
	elif dir == 3:
		temp.grid[i][j], temp.grid[i][j + 1] = temp.grid[i][j + 1], temp.grid[i][j]
		temp.pos = (i, j + 1)
	return temp

# Hashes a board state
def hash(grid):
	ret = ''
	for i in grid:
		ret += ',' + str(i)
	return ret

def bfs(cur_board, stats):
	frontier = collections.deque()
	frontier.append(['', cur_board])
	vis = {hash(cur_board.grid): True}
	while len(frontier) > 0:
		stats['maxFringe'] = max(stats['maxFringe'], len(frontier))
		cur = frontier.popleft()

		if isSolved(cur[1]):
			stats['frontier'] = len(frontier)
			return cur[0]

		stats['nodes'] += 1
		for i in range(len(dirs)):
			if canGoTo(cur[1], i):
				moved = go(cur[1], i)
				cur_hash = hash(moved.grid)
				if not vis.get(cur_hash):
					vis[cur_hash] = True
					new_path = cur[0] + ',' + str(i)
					frontier.append([new_path, moved])
					
					# Statistics
					stats['maxDepth'] = max(stats['maxDepth'], len(new_path) / 2)
					stats['maxRam'] = max(stats['maxRam'], getCurrentMemory())

def dfs(cur_board, stats):
	frontier = collections.deque()
	frontier.append(['', cur_board])
	vis = {hash(cur_board.grid): True}
	while len(frontier) > 0:
		stats['maxFringe'] = max(stats['maxFringe'], len(frontier))
		cur = frontier.pop()

		if isSolved(cur[1]):
			stats['frontier'] = len(frontier)
			return cur[0]

		stats['nodes'] += 1
		for i in range(len(dirs) - 1, -1, -1):
			if canGoTo(cur[1], i):
				moved = go(cur[1], i)
				cur_hash = hash(moved.grid)
				if not vis.get(cur_hash):
					vis[cur_hash] = True
					new_path = cur[0] + ',' + str(i)
					frontier.append([new_path, moved])

					# Statistics
					stats['maxDepth'] = max(stats['maxDepth'], len(new_path) / 2)
					stats['maxRam'] = max(stats['maxRam'], getCurrentMemory())

# Calculate h(n) for A-Star
def h(grid):
	n = len(grid[0])
	ret = 0
	for i in range(n):
		for j in range(n):
			if (grid[i][j] != 0):
				ret += abs(grid[i][j] % n - j % n)
				ret += abs(math.floor(grid[i][j] / n) - math.floor(i / n))
	return ret

# Normal A-Star Search
def ast(cur_board, stats):
	frontier = []
	frontier.append([h(cur_board.grid), '', cur_board])
	vis = {hash(cur_board.grid): True}

	while len(frontier) > 0:
		stats['maxFringe'] = max(stats['maxFringe'], len(frontier))
		cur = heapq.heappop(frontier)

		if isSolved(cur[2]):
			stats['frontier'] = len(frontier)
			return cur[1]

		stats['nodes'] += 1
		for i in range(len(dirs) - 1, -1, -1):
			if canGoTo(cur[2], i):
				moved = go(cur[2], i)
				cur_hash = hash(moved.grid)
				if not vis.get(cur_hash):
					vis[cur_hash] = True
					new_path = cur[1] + ',' + str(i)
					heapq.heappush(frontier,
					[h(moved.grid) + len(new_path) / 2, new_path, moved])
					
					# Statistics
					stats['maxDepth'] = max(stats['maxDepth'], len(new_path) / 2)
					stats['maxRam'] = max(stats['maxRam'], getCurrentMemory())

def astLimited(cur_board, maxDepth, stats):
	frontier = []
	frontier.append([h(cur_board.grid), '', cur_board])
	vis = {hash(cur_board.grid): True}

	while len(frontier) > 0:
		stats['maxFringe'] = max(stats['maxFringe'], len(frontier))
		cur = heapq.heappop(frontier)

		if isSolved(cur[2]):
			stats['frontier'] = len(frontier)
			return cur[1]

		stats['nodes'] += 1
		for i in range(len(dirs) - 1, -1, -1):
			if canGoTo(cur[2], i):
				moved = go(cur[2], i)
				cur_hash = hash(moved.grid)
				if not vis.get(cur_hash):
					vis[cur_hash] = True
					new_path = cur[1] + ',' + str(i)
					heapq.heappush(frontier,
					[h(moved.grid) + len(new_path) / 2, new_path, moved])
					
					# Statistics
					stats['maxDepth'] = max(stats['maxDepth'], len(new_path) / 2)
					stats['maxRam'] = max(stats['maxRam'], getCurrentMemory())

					if stats['maxDepth'] > maxDepth:
						return None

# Iterative Deepening A-Star Search
def ida(cur_board, stats):
	x = 0
	ret = None
	while ret is None:
		# Reset stats
		for key in stats:
			key = 0
		x += 1
		ret = astLimited(cur_board, x, stats)
	return ret

method = sys.argv[1]
#method = 'bfs'
mylist = sys.argv[2].split(',')
# Convert to int
for i in range(len(mylist)):
	mylist[i] = int(mylist[i])

#b = board(int(math.sqrt(len(mylist))), mylist)
#b = board(3, [1,0,2,3,4,5,6,7,8])
#b = board(4, [6,5,8,3,1,4,7,2,9,14,10,12,13,0,11,15])
#b = board(3, [6,0,4,5,2,1,8,3,7])
#b = board(3, [2,6,7,4,1,3,8,0,5])

stats = {
	'frontier': 0,
	'maxFringe': 0,
	'maxDepth': 0,
	'maxRam': 0,
	'nodes': 0
	}
dirs = ['Up', 'Down', 'Left', 'Right']
path = []

start_time = time.time()

if method == 'bfs':
	path = bfs(b, stats)
elif method == 'dfs':
	path = dfs(b, stats)
elif method == 'ast':
	path = ast(b, stats)
elif method == 'ida':
	path = ida(b, stats)

end_time = time.time()

path = path.split(',')[1:]
for i in range(len(path)):
	path[i] = dirs[int(path[i])]

print('path_to_goal:', path)
print('cost_of_path:', len(path))
print('nodes_expanded:', stats['nodes'])
print('fringe_size:', stats['frontier'])
print('max_fringe_size:', stats['maxFringe'])
print('search_depth:', len(path))
print('max_search_depth:', int(stats['maxDepth']))
print('running_time:', end_time - start_time)
print('max_ram_usage:', stats['maxRam'])

with open('output.txt', 'w') as f:
	f.write('path_to_goal: ' + str(path) + '\n')
	f.write('cost_of_path: ' + str(len(path)) + '\n')
	f.write('nodes_expanded: ' + str(stats['nodes']) + '\n')
	f.write('fringe_size: ' + str(stats['frontier']) + '\n')
	f.write('max_fringe_size: ' + str(stats['maxFringe']) + '\n')
	f.write('search_depth: ' + str(len(path)) + '\n')
	f.write('max_search_depth: ' + str(int(stats['maxDepth'])) + '\n')
	f.write('running_time: ' + str(end_time - start_time) + '\n')
	f.write('max_ram_usage: ' + str(stats['maxRam']) + '\n')
	#f.write('max_ram_usage: ' +
	#str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) + '\n')
