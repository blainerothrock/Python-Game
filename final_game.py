#final game code
#spaceinvaders.py




import math, random
from livewires import games, color

games.init(screen_width = 640, screen_height = 480, fps = 100)
		
class Ship(games.Sprite):

	image = games.load_image("ship.bmp")
	
	INSTANCE = "ship"
	
	def __init__(self, game, x, y, invaders):
		super(Ship,self).__init__(image = Ship.image, x = x, y = y)
		self.game = game
		self.missile_wait = 0
		self.is_fired = False
		self.missile = "normal"
		self.invaders = invaders
		
		self.health = games.Text(value = 100,
					size = 40,
				color = color.red,
				top = 50,
				right = games.screen.width - 10,
				is_collideable = False)
		games.screen.add(self.health)
		
		self.AP = games.Text(value = 10,
							 size = 25,
							 color = color.blue,
							 top = 5,
							 left = games.screen.width - 630,
							 is_collideable = False)
		games.screen.add(self.AP)
		
		self.L = games.Text(value = 5,
							size = 25,
							color = color.green,
							top = 5,
							left = games.screen.width - 595,
							is_collideable = False)
		games.screen.add(self.L)
		
	def update(self):
		super(Ship, self).update()
		
		if self.missile_wait > 0:
			self.missile_wait -= 1
			
		if games.keyboard.is_pressed(games.K_LEFT):
			self.x -= 5
		if games.keyboard.is_pressed(games.K_RIGHT):
			self.x += 5 
			
		if games.keyboard.is_pressed(games.K_z):
			self.missile = "normal"
		if games.keyboard.is_pressed(games.K_x):
			if self.AP.value == 0:
				self.missile = "normal"
			else:
				self.missile = "armorpiercing"
		if games.keyboard.is_pressed(games.K_c) and self.game.level < 10:
			if self.L.value == 0:
				self.missile = "normal"
			else:
				self.missile = "lightning"
			
		if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0 and self.is_fired == False:
			self.is_fired = True
			if self.missile == "normal":
				new_missile = Missile(self, self.x, self.y, "normal_missile.bmp", 1)
				games.screen.add(new_missile)
			if self.missile == "armorpiercing":
				new_missile = Missile(self, self.x, self.y, "armorpiercing_missile.bmp", 5)
				games.screen.add(new_missile)
				if self.AP.value > 0:
					self.AP.value -= 1
				else:
					new_missile = Missile(self, self.x, self.y, "normal_missile.bmp", 1)
					games.screen.add(new_missile)
			if self.missile == "lightning":
				new_missile = Missile(self, self.x, self.y, "lightning_missile.bmp", 100)
				games.screen.add(new_missile)
				if self.L.value > 0:
					self.L.value -= 1
				else:
					new_missile = Missile(self, self.x, self.y, "normal_missile.bmp", 1)
					games.screen.add(new_missile)
					
		if self.health.value <= 0:
			self.die()
		
		if self.overlapping_sprites:
			for sprite in self.overlapping_sprites:
				if sprite.INSTANCE == "invader":
					self.health.value -= 50
					sprite.die()
					
		xmin = games.screen.width + 1
		xmax = -1
		
		for invader in self.invaders:
			if invader.x < xmin:
				xmin = invader.x
			if invader.x > xmax:
				xmax = invader.x
		
		if xmin < 10 or xmax > games.screen.width-10:
			for invader in self.invaders:
				invader.dx = -invader.dx
				invader.y += 10
				
		if self.game.invaders == []:
			self.game.next_level()

	def missile_died(self):
		self.is_fired = False
			
	def die(self):
		self.destroy
		self.game.end()
			
class Missile(games.Sprite):

	sound = games.load_sound("Missile.wav")
	INSTANCE = "missile"
	
	LIFETIME = 50

	def __init__(self, ship, ship_x, ship_y, image, damage):
		Missile.sound.play()
		x = ship_x
		y = ship_y - 25
		dy = -8
		dx = 0
		pic = games.load_image(image)
		self.damage = damage
		self.ship = ship
		
		super(Missile, self).__init__(image = pic,
						x = x, y = y,
						dx = dx, dy = dy,
											)
		
	def update(self):
		
		self.LIFETIME -= 1
		if self.LIFETIME == 0:
			self.die()
			
		if self.overlapping_sprites:
			for sprite in self.overlapping_sprites:
				if sprite.INSTANCE == "invader":
					if sprite.health < self.damage:
						sprite.die()
						self.damage -= sprite.health
					if sprite.health == self.damage:
						sprite.die()
						self.die()
					if sprite.health > self.damage:
						sprite.health -= self.damage
						self.die()
				if sprite.INSTANCE == "invader_missile":
					sprite.destroy
					self.damage -= 1
	def die(self):

		self.ship.missile_died()
		self.destroy()
	
class Invader_Missile(games.Sprite):

	INSTANCE = "invader_missile"

	power = ("health+", "heath++", "health-", "armorper+", "light+")

	LIFETIME = 40

	def __init__(self, invader, invader_x, invader_y, image, damage):
			x = invader_x
			y = invader_y - 25
			dy = 1
			dx = 0
			pic = games.load_image(image)
			self.damage = damage
			self.invader = invader
					
			super(Invader_Missile, self).__init__(image = pic,
												x = x, y = y,
												dx = dx, dy = dy)
											
	def update(self):
		
		self.LIFETIME -= 1
		if self.LIFETIME == 0:
			self.destroy
			
		if self.overlapping_sprites:
			for sprite in self.overlapping_sprites:
				if sprite.INSTANCE == "ship":
					self.destroy()
					sprite.health.value -= self.damage
	
class Power_Up(games.Sprite):

	INSTANCE = "power_up"
	
	def __init__(self, invader, invader_x, invader_y, image, type):
		x = invader_x
		y = invader_y
		pic = games.load_image(image)
		dy = 1.5
		dx = 0
		self.type = type
		
		super(Power_Up, self).__init__(image = pic,
									   x = x, y = y,
									   dx = dx, dy = dy)
									   
		games.screen.add(self)
									   
	def update(self):
		
		if self.y == 0:
			self.destroy()
		
		if self.overlapping_sprites:
			for sprite in self.overlapping_sprites:
				if sprite.INSTANCE == "ship":
					if self.type == "health+":
						if sprite.health.value > 50:
							sprite.health.value = 100
							self.destroy()
						else:
							sprite.health.value = Ship.health * 2
							self.destroy()
					if self.type == "health++":
						sprite.health.value = 100
						self.destroy()
					if self.type == "armor+":
						sprite.AP.value += 10
						self.destroy()
					if self.type == "light+":
						sprite.L.value += 5
						self.destroy()
					if self.type == "health-":
						sprite.health.value -= 20
						self.destroy()

class Invader1(games.Sprite):

	INSTANCE = "invader"

	health = 1
	image = games.load_image("invader1.bmp") 
	
	def __init__(self, game, x, y):
		
		super(Invader1, self).__init__(image = Invader1.image,
					  x = x, y = y,
									  is_collideable = True,
					  dx = 1,
					  dy = 0)
		self.game = game
		
	def update(self):
	
		fire_missile = random.randrange(10000)
		
		if fire_missile == 0:
			new_missile = Invader_Missile(self, self.x, self.y, "invader_missile1.bmp", 5)
			games.screen.add(new_missile)
		
	def die(self):
	
		explosion = Explosion(self.x, self.y)
		games.screen.add(explosion)
	
		drop_power_up = random.randrange(15)
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
	
		self.destroy()
		self.game.delete(self)
		
		self.game.score.value += 10
		self.game.score.right = games.screen.width - 10
		
class Invader2(games.Sprite):

	INSTANCE = "invader"

	health = 3
	image = games.load_image("invader2.bmp") 
	
	def __init__(self, game, x, y):
		
		super(Invader2, self).__init__(image = Invader2.image,
					  x = x, y = y,
									  is_collideable = True,
					  dx = 1,
					  dy = 0)
		self.game = game
		
	def update(self):
	
		fire_missile = random.randrange(10000)
		
		if fire_missile == 0:
			new_missile = Invader_Missile(self, self.x, self.y, "invader_missile2.bmp", 20)
			games.screen.add(new_missile)
		
	def die(self):
	
		explosion = Explosion(self.x, self.y)
		games.screen.add(explosion)
	
		drop_power_up = random.randrange(15)
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
	
		self.destroy()
		self.game.delete(self)
		
		self.game.score.value += 10
		self.game.score.right = games.screen.width - 10
		
class Invader3(games.Sprite):

	INSTANCE = "invader"

	health = 5
	image = games.load_image("invader3.bmp") 
	
	def __init__(self, game, x, y):
		
		super(Invader3, self).__init__(image = Invader3.image,
					  x = x, y = y,
									  is_collideable = True,
					  dx = 1,
					  dy = 0)
		self.game = game
		
	def update(self):
	
		fire_missile = random.randrange(1000)
		
		if fire_missile == 0:
			new_missile = Invader_Missile(self, self.x, self.y, "invader_missile2.bmp", 25)
			games.screen.add(new_missile)
		
	def die(self):
	
		explosion = Explosion(self.x, self.y)
		games.screen.add(explosion)
	
		drop_power_up = random.randrange(10)
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
	
		self.destroy()
		self.game.delete(self)
		
		self.game.score.value += 10
		self.game.score.right = games.screen.width - 10
		
class Invader4(games.Sprite):

	INSTANCE = "invader"

	health = 50
	image = games.load_image("invader4.bmp") 
	
	def __init__(self, game, x, y):
		
		super(Invader4, self).__init__(image = Invader4.image,
					  x = x, y = y,
									  is_collideable = True,
					  dx = 1,
					  dy = 0)
		self.game = game
		
	def update(self):
	
		fire_missile = random.randrange(400)
		
		if fire_missile == 0:
			new_missile = Invader_Missile(self, self.x, self.y, "armorpiercing_missile.bmp", 50)
			games.screen.add(new_missile)
		
	def die(self):
	
		explosion = Explosion(self.x, self.y)
		games.screen.add(explosion)
	
		drop_power_up = 0
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
	
		self.destroy()
		self.game.delete(self)
		
		self.game.score.value += 10
		self.game.score.right = games.screen.width - 10
		
class Boss(games.Sprite):

	INSTANCE = "invader"

	health = 150
	image = games.load_image("boss.bmp") 
	
	def __init__(self, game, x, y):
		
		super(Boss, self).__init__(image = Boss.image,
					  x = x, y = y,
									  is_collideable = True,
					  dx = 1,
					  dy = 0)
		self.game = game
		
	def update(self):
	
		fire_missile = random.randrange(100)
		
		if fire_missile == 0:
			new_missile = Invader_Missile(self, self.x, self.y, "lightning_missile.bmp", 25)
			games.screen.add(new_missile)
			
		drop_power_up = random.randrange(10000)
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
		
	def die(self):
	
		explosion = Explosion(self.x, self.y)
		games.screen.add(explosion)
	
		drop_power_up = 0
			
		if drop_power_up == 0:
			which_power = random.randrange(5)
			if which_power == 0:
				Power_Up(self, self.x, self.y, "health+.bmp", "health+")
			if which_power == 1:
				Power_Up(self, self.x, self.y, "health++.bmp", "health++")
			if which_power == 2:
				Power_Up(self, self.x, self.y, "ap_pu.bmp", "armor+")
			if which_power == 3:
				Power_Up(self, self.x, self.y, "l_pu.bmp", "light+")
			if which_power == 4:
				Power_Up(self, self.x, self.y, "health-.bmp", "health-")
	
		self.destroy()
		self.game.delete(self)
		
		self.game.score.value += 10
		self.game.score.right = games.screen.width - 10
		
class Explosion(games.Animation):
    """ Explosion animation. """
    sound = games.load_sound("explosion.wav")
    images = ["explosion1.bmp",
              "explosion2.bmp"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images = Explosion.images,
                                        x = x, y = y,
                                        repeat_interval = 4, n_repeats = 1,
                                        is_collideable = False)
					
class Game(object):

	starty = 0
	startx = 0
	
	def __init__(self):
		self.sound = games.load_sound("level.wav")
		self.invaders = []
		self.level = 1
		
		self.score = games.Text(value = 0,
					size = 30,
				color = color.white,
				top = 5,
				right = games.screen.width - 10,
				is_collideable = False)
		games.screen.add(self.score)
		
		self.level1()
			
		self.ship = Ship(game = self,
			 x = games.screen.width/2,
			 y = games.screen.height - 25, invaders = self.invaders)
		games.screen.add(self.ship)
	
	def play(self):
	
		games.music.load("theme.mid")
		games.music.play(-1)
        
		background_image = games.load_image("background.bmp")
		games.screen.background = background_image
		
		
#		games.screen.add(Invader(game = self, x = games.screen.width/2, y = games.screen.height/2))
		games.screen.mainloop()
		
	def delete(self, obj):
		for ele in self.invaders:
			if ele == obj:
				self.invaders.remove(obj)
		
		
	def next_level(self):
	
		games.music.load("Vocalish 004.wav")
		games.music.play(1)
	
		if self.level == 1:
			self.level2()
			self.level += 1
		elif self.level == 2:
			self.level3()
			self.level += 1
		elif self.level == 3:
			self.level4()
			self.level += 1
		elif self.level == 4:
			self.level5()
			self.level += 1
		elif self.level == 5:
			self.level6()
			self.level += 1
		elif self.level == 6:
			self.level7()
			self.level += 1
		elif self.level == 7:
			self.level8()
			self.level += 1
		elif self.level == 8:
			self.level9()
			self.level += 1
		elif self.level == 9:
			self.level10()
			self.level += 1
		elif self.level == 10:
			self.level1()
			self.level = 1
		
			
			
	def level1(self):
	
		message = games.Message(value = "level 1",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
		
		y = 0
		
		for col in range(5):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	def level2(self):
	
		message = games.Message(value = "level 2",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
	
		y = 0
		
		for col in range(5):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	
	def level3(self):
	
		message = games.Message(value = "level 3",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
		
		y = 0
		for col in range(1):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader2(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(4):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1

				
	def level4(self):
	
		message = games.Message(value = "level 4",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
	 
		y = 0
		for col in range(2):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader2(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(3):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	def level5(self):
	
		message = games.Message(value = "level 5",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
		
		y = 0
		for col in range(1):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader3(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(2):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader2(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
		for col in range(2):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	def level6(self):
	
		message = games.Message(value = "level 6",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
		
		y = 0
		for col in range(1):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader3(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(3):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader2(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
		for col in range(1):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	def level7(self):
	
		message = games.Message(value = "level 7",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
			
		y = 0
		for col in range(2):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader3(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(3):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader1(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
	def level8(self):
	
		message = games.Message(value = "level 8",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
	
		y = 0
		for col in range(2):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader3(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
		for col in range(3):
			row_y = 50 * y + 50
			y += 1
			x = 0
			for row in range(10):
				invader = Invader2(game = self, x = 40 * x + 50, y = row_y)
				self.invaders.append(invader)
				games.screen.add(invader)
				x += 1
				
	def level9(self):
	
		message = games.Message(value = "level 9",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
	 
		invader1 = Invader4(game = self, x = 50, y = 50)
		invader2 = Invader4(game = self, x = 200, y = 50)
		invader3 = Invader4(game = self, x = 350, y = 50)
		
		self.invaders.append(invader1)
		games.screen.add(invader1)
		self.invaders.append(invader2)
		games.screen.add(invader2)
		self.invaders.append(invader3)
		games.screen.add(invader3)
		
	def level10(self):
	
		message = games.Message(value = "level 10",
					size = 90,
					color = color.green,
					x = games.screen.width/2,
					y = 400,
					lifetime = 5 * games.screen.fps,
					is_collideable = False)
		games.screen.add(message)
	 
		boss = Boss(game = self, x = 40, y = 50)
		
		self.invaders.append(boss)
		games.screen.add(boss)
		
	
	def end(self):
		
		end_message = games.Message(value = "Game Over",
					size = 90,
					color = color.red,
					x = games.screen.width/2,
					y = games.screen.height/2,
					lifetime = 5 * games.screen.fps,
									after_death = games.screen.quit,
					is_collideable = False)
		games.screen.add(end_message)
		
def main():
	final = Game()
	final.play()
	
main()
		
		
		
	
		
