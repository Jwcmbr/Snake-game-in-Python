from scene import *
from random import randrange

DELTA = 0.1


class MyScene(Scene):
	def setup(self):
		self.first = True
		self.newgame()

	def newgame(self):
		self.w = int((self.size.w - 60) / 20)
		self.h = int((self.size.h - 50) / 20)
		self.grid = [[None for x in range(self.w)] for y in range(self.h)]

		self.headx, self.heady = self.w // 2, self.h // 2 - 4
		self.tailx, self.taily = self.headx, self.heady - 0

		self.grid[self.heady][self.headx] = 'H'
		self.grid[self.taily][self.tailx] = (0, 1)

		self.dx = 0
		self.dy = 1
		self.dchanged = False

		self.tp = 0

		self.alive = False
		self.score = 0
		self.hiscore = 150

		try:
			self.highscore = int(open('snakehi.txt').read())
		except:
			pass

		for i in range(6):
			self.spawn_food()

	def stop(self):
		open('snakehi.txt', 'w').write(str(self.hiscore))

	def did_change_size(self):
		pass

	def update(self):
		pass

	def spawn_food(self):
		for i in range(12):
			x = randrange(self.w)
			y = randrange(self.h)
			if not self.grid[y][x]:
				self.grid[y][x] = 'F'
				return

	def draw(self):
		t = self.t
		if t > self.tp + DELTA:
			self.tp = self.t
			self.onestep()

		translate(self.size.w / 2, 15)
		text('SCORE: %s   HIGHSCORE: %s' % (self.score, self.hiscore))
		translate(-self.size.w / 2, -15)

		if not self.alive:
			translate(self.size.w / 2, self.size.h / 2)
			t = 'Snake Game by Jerome' if self.first else 'Oops try again'
			text(t, font_size=30)
			translate(-self.size.w / 2, -self.size.h / 2)

		no_fill()
		stroke(300, 300, 300)
		stroke_weight(2)
		translate((self.size.w - 20 * self.w) // 2, 30)
		rect(-1, -1, 20 * self.w + 2, 20 * self.h + 2)

		fill(300, 300, 300)
		no_stroke()
		for row in self.grid:
			for cell in row:
				if cell == 'F':
					rect(5, 5, 10, 10)
				elif cell == 'H':
					rect(1, 1, 18, 18)
				elif cell:
					x, y = 2, 3
					xx, yy = 14, 14
					rect(x, y, xx, yy)
				translate(20, 0)
			translate(-20 * self.w, 20)

	def onestep(self):
		if not self.alive:
			return

		self.grid[self.heady][self.headx] = (self.dx, self.dy)

		self.headx += self.dx
		self.heady += self.dy

		if not (0 <= self.headx < self.w) or \
			not (0 <= self.heady < self.h) or \
			self.grid[self.heady][self.headx] not in (None, 'F'):
			if self.score > self.hiscore:
				self.hiscore = self.score
			self.alive = False
			self.stop()
			return

		ate_food = self.grid[self.heady][self.headx] == 'F'

		if not ate_food:
			tdx, tdy = self.grid[self.taily][self.tailx]
			self.grid[self.taily][self.tailx] = None
			self.tailx += tdx
			self.taily += tdy

		self.grid[self.heady][self.headx] = 'H'

		self.dchanged = False

		if ate_food:
			self.spawn_food()
			self.score += 10

	def touch_began(self, touch):
		if not self.alive:
			if self.first:
				self.first = False
			else:
				self.newgame()
			self.alive = True
			return

		if self.dchanged:
			return

		x, y = touch.location
		x //= 20
		y //= 20
		if self.dx == 0:

			self.dy = 0
			self.dx = 1 if x > self.headx else -1
		elif self.dy == 0:

			self.dx = 0
			self.dy = 1 if y > self.heady else -1
		self.dchanged = True

	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass


if __name__ == '__main__':
	run(MyScene(), show_fps=False)

