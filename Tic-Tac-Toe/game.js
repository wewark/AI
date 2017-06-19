var grid = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0]
];
var gameOn = true;

function play(x, y) {
	if (gameOn && grid[x][y] == 0) {
		grid[x][y] = 1;
		$('#' + String(3 * x + y)).html(curSym);
		if (!gameEnded()) {
			opPlay();
			gameEnded();
		}
	}
}

function opPlay() {
	var g = grid;
	var choices = [];
	var tn;

	for (var i = 0; i < 3; i++)
		for (var j = 0; j < 3; j++)
			if (g[i][j] == 0) {
				g[i][j] = 2;
				choices.push([dfs(g, 1, 1), i, j]);
				g[i][j] = 0;
			}

	// Get choice with max score (with its i and j)
	var choice = choices.reduce(function(mx, a){
		if (a[0] > mx[0])
			mx = a;
		return mx;
	}, [-1e9, -1, -1]);

	// Apply
	grid[choice[1]][choice[2]] = 2;
	$('#' + String(3 * choice[1] + choice[2])).html(curSym == 'X' ? 'O' : 'X');
}

// grid, player who has the turn, depth
function dfs(g, p, depth) {
	var tn = check(g);
	var scores = [];

	// If someone won or draw
	if (tn != -1) {
		if (tn == 1) // player won
			return depth - 10;
		else if (tn == 2) // ai won
			return 10 - depth;
		else if (tn == 0)
			return 0;
	}

	for (var i = 0; i < 3; i++)
		for (var j = 0; j < 3; j++)
			if (g[i][j] == 0) {
				g[i][j] = p;
				scores.push(dfs(g, p == 1 ? 2 : 1, depth + 1));
				g[i][j] = 0;
			}

	var ret;
	// Player tries to minimize score
	if (p == 1)
		ret = scores.reduce(function(mn, a) {
			return Math.min(mn, a);
		}, 1e9);
	// AI tries to maximize score
	else
		ret = scores.reduce(function(mx, a) {
			return Math.max(mx, a);
		}, -1e9);
	return ret;
}

// Returns 1 player won, 2 ai won, 0 draw, -1 none yet
function check(g) {
	// Rows
	for (var i = 0; i < 3; i++) {
		if (g[i][0] == g[i][1] && g[i][0] == g[i][2] && g[i][0] != 0)
			return g[i][0];
		if (g[0][i] == g[1][i] && g[0][i] == g[2][i] && g[0][i] != 0)
			return g[0][i];
	}
	// Diagonals
	if (g[1][1] != 0 && (
			g[0][0] == g[1][1] && g[0][0] == g[2][2] ||
			g[0][2] == g[1][1] && g[0][2] == g[2][0]))
		return g[1][1];
	// Draw
	var draw = true;
	for (var i = 0; i < 3 && draw; i++)
		for (var j = 0; j < 3 && draw; j++)
			if (g[i][j] == 0)
				draw = false;
	if (draw)
		return 0;

	return -1;
}

var score = {
	ai: 0,
	player: 0
};

function gameEnded() {
	var tn = check(grid);

	// If someone won or draw
	if (tn != -1) {
		if (tn == 1) {
			$('#won').html('Player Won');
			score.player++;
			$('#playerScore').html(score.player);
		}
		else if (tn == 2) {
			$('#won').html('AI Won');
			score.ai++;
			$('#aiScore').html(score.ai);
		}
		else if (tn == 0) {
			$('#won').html('DRAW');
		}
		gameOn = false;
		return true;
	}
	return false;
}

function reset() {
	grid = [
		[0, 0, 0],
		[0, 0, 0],
		[0, 0, 0]
	];
	for (var i = 0; i < 9; i++)
		$('#' + String(i)).html('');
	$('#won').html('Try to win!');
	gameOn = true;
}

var curSym = 'X';
function switchSym() {
	if (!gameOn) {
		curSym = curSym == 'X' ? 'O' : 'X';
		$('#switch').html('Playing as ' + curSym);
	}
}
