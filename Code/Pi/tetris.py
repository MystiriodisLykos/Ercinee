from random import randrange as rand
# from gpiozero import Button
import sys
import time
import driver

# control buttons
# b1 = Button(11)
# b2 = Button(9)
# b3 = Button(10)
# b4 = Button(22)

driver.setup()

cols = 10
rows = 20

shapes = [
	[[1, 1, 1], [0, 1, 0]],
	[[0, 1, 1], [1, 1, 0]],
	[[1, 1, 0], [0, 1, 1]],
	[[1, 0, 0], [1, 1, 1]],
	[[0, 0, 1], [1, 1, 1]],
	[[1, 1, 1, 1]],
	[[1, 1], [1, 1]]
]

line_cleared_scores = [100, 300, 500, 800]
line_clears_awarded = [1, 3, 5, 8]


def rotate_clockwise(shape):
	return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[cy + off_y][cx + off_x]:
					return True
			except IndexError:
				return True
	return False


def remove_row(board, row):
	del board[row]
	return [[0 for i in range(cols)]] + board


def join_matrixes(mat1, mat2, mat2_off):
	off_x, off_y = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy + off_y - 1][cx + off_x] += val
	return mat1


def new_board():
	board = [[0 for x in range(cols)] for y in range(rows)]
	board += [[1 for x in range(cols)]]
	return board


def add_boards(b1, b2):
	new = new_board()
	for i in range(len(b1) - 1):
		for j in range(len(b1[0])):
			new[i][j] = b1[i][j] + b2[i][j]
	return new


def print_board(b):
	print()
	print('Board:')
	for i in range(len(b)-1):
		print(b[i])


class Tetris(object):
	def __init__(self):
		self.next_stone = shapes[rand(len(shapes))]
		self.board = new_board()
		self.new_stone()
		self.level = 1
		self.score = 0
		self.time1 = time.time()
		self.b2b = False
		self.cleared_lines = 0
		self.lines_to_level_up = 5


	def new_stone(self):
		self.stone = self.next_stone[:]
		self.next_stone = shapes[rand(len(shapes))]
		self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)
		self.stone_y = 0

		if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
			self.quit()


	def move(self, delta_x):
		new_x = self.stone_x + delta_x
		if new_x < 0:
			new_x = 0
		if new_x > cols - len(self.stone[0]):
			new_x = cols - len(self.stone[0])
		if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
			self.stone_x = new_x

	def quit(self):
		print('Game Over')
		print('Score:', self.score)
		time.sleep(4)
		driver.tear_down()
		sys.exit()

	def drop(self, soft=False):
		self.time1 = time.time()
		self.score += 1 if soft else 0
		self.stone_y += 1
		if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
			self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
			self.new_stone()
			cur_cleared_lines = 0
			while True:
				for i, row in enumerate(self.board[:-1]):
					if 0 not in row:
						self.board = remove_row(self.board, i)
						cur_cleared_lines += 1
						break
				break

			if cur_cleared_lines > 0:
				self.score += int(line_cleared_scores[cur_cleared_lines - 1] * self.level)
				self.cleared_lines += line_clears_awarded[cur_cleared_lines - 1]

			# check for level up
			if self.cleared_lines + cur_cleared_lines > self.lines_to_level_up:
				self.cleared_lines = (self.cleared_lines + cur_cleared_lines) % self.lines_to_level_up
				self.lines_to_level_up += 5
				self.level += 1

			# check for back-to-back tetris scoring
			if cur_cleared_lines == 4:
				if self.b2b:
					self.score += int(line_cleared_scores[cur_cleared_lines - 1] * self.level * .5)
				self.b2b = True
			elif cur_cleared_lines != 0:
				self.b2b = False


	def rotate_stone(self):
		new_stone = rotate_clockwise(self.stone)
		if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
			self.stone = new_stone

	def run(self):
		while 1:
			tot_board = new_board()
			for i in range(len(self.stone)):
				tot_board[self.stone_y + i][self.stone_x:self.stone_x + len(self.stone[i])] = self.stone[i]
			added_boards = add_boards(self.board, tot_board)
			leds = [(i, j) for j in range(len(added_boards) - 1) for i in range(len(added_boards[j])) if
					added_boards[j][i] > 0]

			# illuminate list of leds
			driver.leds_lumos(leds)

			# controls
			# if b1.is_pressed:
			# 	self.move(1)
			# elif b2.is_pressed:
			# 	self.move(-1)
			# elif b3.is_pressed:
			# 	self.rotate_stone()
			# elif b4.is_pressed:
			# 	self.drop(True)


			# increase game speed according to level - rate according to Commodore 64 Tetris
			if time.time() - self.time1 < (0.8 - ((self.level - 1) * 0.007))**(self.level - 1):
				time.sleep(.005)
				drop_qued = False
			else:
				drop_qued = True

			# drop and print board
			if drop_qued:
				self.drop()
				print_board(added_boards)
				print('Leds:', leds)


if __name__ == '__main__':
	Tetris().run()
