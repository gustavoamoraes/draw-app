from engine import *
import image_test

screen_size = Vector2(800,800)
bg_color = (0,0,0)
tools_bar_color = (230,230,230)
game = Instance("A-Star",screen_size.ToTuple(),tools_bar_color)

grid_space = Vector2(800,700)

grid_width = 800
grid_size = grid_space.x/grid_width
grid_height = int(grid_space.y/grid_size)
surface_color = (0,0,0)
grid_line_width = 0


cells = [[(255,255,255) for n in range(grid_width)] for i in range(grid_height)]
cells_father = GameObject([],game,"Cells",False)

game.DrawOnScene([Surface(tools_bar_color,Vector2(screen_size.x,screen_size.y-grid_space.y),Vector2(screen_size.x/2,(grid_space.y+screen_size.y)/2))],cells_father)

painted_cells = []

def ChangeColor (color):

	global surface_color
	surface_color = color

def CleanDrawing():
	global cells
	game.DrawOnScene([Surface((255,255,255),grid_space+Vector2(1,1),grid_space/2)],cells_father)
	cells = [[(255,255,255) for n in range(grid_width)] for i in range(grid_height)]
CleanDrawing()

def SaveImage():
	image_test.CreateImage(cells)

color_buttons = []
buttons = []
color_buttons.append(Button("",(255,127,39),(255,255,255),lambda: ChangeColor((255,127,39)),Vector2(-15,0),Vector2(0,0),Vector2(25,25),30))
color_buttons.append(Button("",(237, 25, 36),(255,255,255),lambda: ChangeColor((237, 25, 36)),Vector2(15,0),Vector2(0,0),Vector2(25,25),30))
color_buttons.append(Button("",(255, 249, 151),(255,255,255),lambda: ChangeColor((255, 249, 151)),Vector2(45,0),Vector2(0,0),Vector2(25,25),30))
color_buttons.append(Button("",(34, 177, 76),(255,255,255),lambda: ChangeColor((34, 177, 76)),Vector2(75,0),Vector2(0,0),Vector2(25,25),30))
color_buttons.append(Button("",(0, 162, 232),(255,255,255),lambda: ChangeColor((0, 162, 232)),Vector2(105,0),Vector2(0,0),Vector2(25,25),30))
color_buttons.append(Button("",(0, 0, 0),(255,255,255),lambda: ChangeColor((0, 0, 0)),Vector2(135,0),Vector2(0,0),Vector2(25,25),30))

buttons.append(Button("Save Image!",(224, 120, 96),(255,255,255),SaveImage,Vector2(0,0),Vector2(0,0),Vector2(200,30),15))
buttons.append(Button("Clean",(224, 120, 96),(255,255,255),CleanDrawing,Vector2(250,0),Vector2(0,0),Vector2(200,30),15))

buttons_father = GameObject(buttons,game,"Buttons",False)
colors_father = GameObject(color_buttons,game,"Buttons",False)
colors_father.transform.position = Vector2(550,750)
buttons_father.transform.position = Vector2(150,750)

last_mouse_pos = Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

mouse_pos = Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
mouse_cell_indexes = Vector2(int(mouse_pos.x//grid_size),int(mouse_pos.y//grid_size))+Vector2(1,1)

last_pos = mouse_cell_indexes
current = Vector2(0,0)

def Update(self):

	global last_pos
	global current

	mouse_pos = Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
	mouse_cell_indexes = Vector2(int(mouse_pos.x//grid_size),int(mouse_pos.y//grid_size))+Vector2(1,1)
	mouse_cell_position = Vector2(mouse_cell_indexes.x*grid_size,mouse_cell_indexes.y*grid_size)

	#for button in colors_father.draw_functions:
	#	self.DrawOnScene([button],colors_father)

	if mouse_cell_position.y <= grid_space.y and mouse_cell_position.x <= grid_space.x:
		if pygame.mouse.get_pressed()[0] == 1:

			#if cells[mouse_cell_indexes.x-1][mouse_cell_indexes.y-1] == None:

				diff =  (mouse_pos-last_pos)

				current_cell = last_pos

				if diff == Vector2(0,0):

					newCell = Surface(surface_color,Vector2(grid_size-grid_line_width,grid_size-grid_line_width),Vector2(mouse_cell_indexes.x*grid_size,mouse_cell_indexes.y*grid_size) - Vector2(grid_size,grid_size)/2)

					cells[mouse_cell_indexes.y-1][mouse_cell_indexes.x-1] = surface_color

					self.DrawOnScene([newCell],cells_father)

				while current_cell != mouse_pos:
					
					draw_point = Vector2(int(current_cell.x//grid_size),int(current_cell.y//grid_size))+Vector2(1,1)

					if draw_point.x < grid_width+1 and draw_point.y < grid_height+1 and draw_point.x > 0 and draw_point.y+1 > 0:

						newCell = Surface(surface_color,Vector2(grid_size-grid_line_width,grid_size-grid_line_width),Vector2(draw_point.x*grid_size,draw_point.y*grid_size) - Vector2(grid_size,grid_size)/2)
						cells[draw_point.y-1][draw_point.x-1] = surface_color

						self.DrawOnScene([newCell],cells_father)

					current_cell += diff/512
			
		if pygame.mouse.get_pressed()[2] == 1:
			if cells[mouse_cell_indexes.y-1][mouse_cell_indexes.x-1] != None:
				self.DrawOnScene([Surface((255,255,255),Vector2(grid_size-grid_line_width,grid_size-grid_line_width),mouse_cell_position - Vector2(grid_size,grid_size)/2)],cells_father)
				cells[mouse_cell_indexes.y-1][mouse_cell_indexes.x-1] = (255,255,255)

	last_pos = mouse_pos

game.Start(game.game_objects,Update,[Button])