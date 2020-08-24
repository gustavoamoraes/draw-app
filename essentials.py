import numpy as np
from enum import Enum
import pygame
import math
import random

class Vector2:
	
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def dot(self,other):
		return (self.x * other.x) + (self.y * other.y)
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y)
	def Normalize(self):
		self.x = self.x/self.magnitude()
		self.y = self.y/self.magnitude()
	def normalized(self):
		if self.magnitude() > 1:
			return Vector2(self.x/self.magnitude(),self.y/self.magnitude())
		else:
			return self
	def perpendicular(self):
		t = np.array([[0,-1],[1,0]])
		vec = np.array([self.x,self.y])
		p = t.dot(vec)
		return Vector2(p[0],p[1])
	def __neg__(self):
		return Vector2(-self.x,-self.y)
	def __add__(self, other):
		return Vector2(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return Vector2(self.x-other.x,self.y-other.y)
	def __truediv__(self, n):
		return Vector2(self.x/n,self.y/n)
	def __floordiv__(self, n):
		return Vector2(self.x//n,self.y//n)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __mul__(self, n):
		return Vector2(self.x*n,self.y*n)

	def TupleToVector(tuple):
		return Vector2(tuple[0],tuple[1])
	def Sum(other):
		sum_vec = Vector2(0,0)
		for v in other:
			sum_vec += v
		return sum_vec

	def ToTuple(self):
		return (self.x,self.y)

class Surface:

	def __init__(self,color,rect,position):

		self.color = color
		self.rect = rect
		self.position = position

	def Draw (self,game_screen,gameObject):
		pygame.draw.rect(game_screen,self.color,(((gameObject.transform.position+self.position) - self.rect//2).ToTuple(),self.rect.ToTuple()))

class Button:

	def __init__(self,text_content,button_color,text_color,onClick,button_position,text_position_offset,button_size,font_size):

		self.text_content = text_content
		self.button_color = button_color
		self.active_color = button_color
		self.font_size = font_size
		self.text_position_offset = text_position_offset
		self.text_color = text_color
		self.OnClick = onClick
		self.button_position = button_position
		self.button_size = button_size
		self.render = False
		self.k = 0
		self.isOn = False

	def IsOnButton(self,button_pos,button_size):

		mouse_pos = Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

		if mouse_pos.y < button_pos.y + button_size.y/2 and mouse_pos.y > button_pos.y - button_size.y/2 and mouse_pos.x < button_pos.x + button_size.x/2 and mouse_pos.x > button_pos.x - button_size.x/2:
			return True
		else:
			return False

	def ChangeButtonColor(self,color):
		self.active_color = color

	def Draw (self,game_screen,gameObject):

		screen_button_pos = gameObject.transform.position+self.button_position

		if self.isOn:

			is_realy_on = self.IsOnButton(screen_button_pos,self.button_size)

			if not is_realy_on:
				self.ChangeButtonColor(self.button_color)
				self.DrawButton(gameObject,game_screen,screen_button_pos)
			else:
				self.ChangeButtonColor((self.button_color[0]*0.95,self.button_color[1]*0.95,self.button_color[2]*0.95))
				if pygame.mouse.get_pressed()[0] == 1:
					self.ChangeButtonColor((self.button_color[0]*0.8,self.button_color[1]*0.8,self.button_color[2]*0.8))
					self.OnClick()
				self.DrawButton(gameObject,game_screen,screen_button_pos)

		self.isOn = self.IsOnButton(screen_button_pos,self.button_size)

	def DrawButton(self,gameObject,game_screen,button_pos):

		font = pygame.font.SysFont("arial", self.font_size)
		text = font.render(self.text_content, True, self.text_color)
		text_size = Vector2(text.get_width(),text.get_height())

		Surface(self.active_color,self.button_size,self.button_position).Draw(game_screen,gameObject)
		game_screen.blit(text,((button_pos-text_size/2)+self.text_position_offset).ToTuple())

class Transform:

	def __init__ (self,position,size):

		self.position = position
		self.size = size

	def Translate(self,vector):
		self.position = self.position + vector	

class GameObject:
	def __init__(self,draw_functions,game_instance,name,static):
		self.static = static
		self.transform = Transform(Vector2(0,0),Vector2(1,1))
		self.name = name
		self.draw_functions = draw_functions
		self.game_instance = game_instance
		self.game_instance.game_objects.append(self)