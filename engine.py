from essentials import *
import pygame, sys
from pygame.locals import *
import types

class Instance:

	#Start
	def __init__ (self,name,resolution,background_color):

		#Start
		pygame.init()

		self.screen = pygame.display.set_mode(resolution)

		#Title
		pygame.display.set_caption(name)

		#Game clock
		self.game_clock = pygame.time.Clock()

		#Time per frame
		self.delta_time = 0

		#Initializing array
		self.game_objects = []

		#Background color
		self.screen.fill(background_color)

	#Start game
	def Start(self,game_objects,update_method,to_draw_every_frame):

		self.game_objects = game_objects
		self.Update = types.MethodType(update_method,self)
		self.to_draw_every_frame = to_draw_every_frame

		for obj in self.game_objects:
			for draw_func in obj.draw_functions:
				if type(draw_func) == Button:
					print("draw")
					draw_func.DrawButton(obj,self.screen,obj.transform.position+draw_func.button_position)
		self.Loop()

	#Background stuff
	def Loop(self):

		while True:

			#Frame rate
			self.game_clock.tick(120)

			pygame.display.update()

			for obj in self.game_objects:
				for draw_func in obj.draw_functions:
					if type(draw_func) in self.to_draw_every_frame:
						draw_func.Draw(self.screen,obj)

			#Game inputs
			self.keys = pygame.key.get_pressed()

			if self.game_clock.get_fps() > 0:
				self.delta_time = 1/self.game_clock.get_fps()

			self.Update()

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)

	def DrawOnScene (self,funcs,obj):
		for draw_func in funcs:
				draw_func.Draw(self.screen,obj)