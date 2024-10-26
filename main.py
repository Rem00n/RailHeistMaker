import pygame,sys,os,math,subprocess,wx,shutil

pygame.init()
clock =  pygame.time.Clock()
WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
pygame.key.set_repeat(300,40)
pygame.display.set_caption('Rail Heist Maker')
MouseX, MouseY = 0,0
prevLmouseclicked, Lmouseclicked = 0,0
prevRmouseclicked, Rmouseclicked = 0,0
prevMmouseclicked, Mmouseclicked = 0,0


CLR_EMPTY = "#000000"
CLR_BTXT = "#FFFFFF"
DIM_BLK = 20
OFF_X,OFF_Y = DIM_BLK*1,DIM_BLK*2

font = pygame.font.SysFont("Arial", DIM_BLK)
fontL = pygame.font.SysFont("Arial", round(DIM_BLK*2))
fontS = pygame.font.SysFont("Arial", round(DIM_BLK*0.8))
numericalButtons = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_KP0]

clock = pygame.time.Clock()



levels = []
selectedLevel = 0


ValidChars = ['x', 'y', 'z', '^', 'w', 'M', '=', '~', '|', '0', '@', 'T', 'P', 'L','H', '-', '+', '8', 'E', 'R', 'B', 'C', 'D', 'I', 'G', 'A', '>', '<', 'K', 'N', 'X', '?', '1', '2', '3', '4', '5', '6', '7', 'Y', 'W', 'V', '$', '%', '&', ':', '*', '!', 'S', 'F', '{', ']', '[', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v']

BGC1 = '#340058'
BGC2 = '#000000'
BGC3 = '#4C0000'


def sine_wave(y_offset, amplitude, frequency, phase_shift, surface, color):
    points = []
    for x in range(surface.get_width()):
        y = y_offset + amplitude * math.sin(frequency * (x + phase_shift))
        points.append((x, y))
    points.append((surface.get_width(), HEIGHT))  
    points.append((0, HEIGHT))      
    pygame.draw.polygon(surface, color, points)


def create_wave_surface(phase_shift, color, amplitude, frequency,h):
    extra_width = WIDTH * 3  
    surface = pygame.Surface((extra_width, HEIGHT), pygame.SRCALPHA)
    sine_wave(HEIGHT * 0.35+h, amplitude, frequency, phase_shift, surface, color)
    return surface

def drawBackground():
    global offset_x_1, offset_x_2
    screen.fill(BGC1)
    delta_time = clock.tick(240) / 1000
    offset_x_1 -= speed_x_1 * delta_time
    if offset_x_1 <= -WIDTH:
        offset_x_1 += WIDTH
    offset_x_2 -= speed_x_2 * delta_time
    if offset_x_2 <= -WIDTH:
        offset_x_2 += WIDTH
    screen.blit(wave_surface_1, (offset_x_1, 0))
    screen.blit(wave_surface_2, (offset_x_2, 0))
    




phase_shift_1 = 0
phase_shift_2 = 100


amplitude = HEIGHT *0.06
frequency = 2 * math.pi / WIDTH * 2
wave_surface_1 = create_wave_surface(phase_shift_1, BGC2, amplitude, frequency,0)
wave_surface_2 = create_wave_surface(phase_shift_2, BGC3, amplitude*0.5, frequency,230)


offset_x_1 = 0
offset_x_2 = 0
speed_x_1 = 50  
speed_x_2 = 150  



sampleTrain = []
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("  T+++++++++++++++P++++                         "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("                                                "));
sampleTrain.append(list("--0====================0E                       "));
sampleTrain.append(list("    8           8                               "));
sampleTrain.append(list("                                                "));

blocksSelectingTrain = [list(' '*48) for i in range(18)]

i,j = 1,1
for b in ValidChars:
	blocksSelectingTrain[i][j] = b
	j += 2
	if j > 30:
		j = 1
		i += 3

blocksInfo = {
	'a': ['alert lawman','looking left'],
	'b': ['alert lawman','looking right'],
	'c': ['unalert lawman','looking left'],
	'd': ['unalert lawman','looking right'],
	'e': ['crouching lawman','looking left'],
	'f': ['crouching lawman','looking right'],
	'g': ['unalert lawman','looking left','aiming up'],
	'h': ['unalert lawman','looking right','aiming up'],
	'i': ['crouching lawman','looking left','aiming down'],
	'j': ['crouching lawman','looking right','aiming down'],
	'k': ['alert lawman','looking left','stairs denier'],
	'l': ['alert lawman','looking right','stairs denier'],
	'm': ['alert lawman','looking left','armored','unused in base game'],
	'n': ['alert lawman','looking right','armored','unused in base game'],
	'o': ['alert lawman','looking left','holding dynamite'],
	'p': ['alert lawman','looking right','holding dynamite'],
	'q': ['unalert lawman','looking left','holding dynamite'],
	'r': ['unalert lawman','looking right','holding dynamite'],
	's': ['alert sheriff','looking left'],
	't': ['alert sheriff','looking right'],
	'u': ['unalert sheriff','looking left'],
	'v': ['unalert sheriff','looking right'],
	'x': ['outlaw','Dodger'],
	'y': ['outlaw','Brand'],
	'z': ['outlaw','Maria'],
	'G': ['unactive gatling','looking right'],
	'A': ['unactive gatling','looking left'],
	'>': ['active gatling','looking right'],
	'<': ['active gatling','looking left'],
	'E': ['end of train','everything to the right',' gets embedded into',' next train (if there is)'],
	'S': ['switch'],
	'F': ['wall wwitch','unused in base game'],
	'!': ['switchable gear (on)','alerts lawmen'],
	'%': ['switchable gear (on)','marks BG start/end'],
	'&': ['switchable gear (on)'],
	':': ['switchable gear (off)','marks BG start/end'],
	'*': ['switchable gear (off)'],
	'@': ['unbreakable','marks BG start/end'],
	'0': ['unbreakable'],
	'=': ['marks BG start/end'],
	'+': ['marks BG start/end'],
	'P': ['ladder top','marks BG start/end'],
	'T': ['ladder top'],
	'L': ['ladder','no platform at top'],
	'H': ['nothing','use L,T, or P for ladders'],	
	'^': ['captured Brand','flip switch to free'],
	'N': ['barrel','contains money'],
	'K': ['barrel','empty'],
	'B': ['crate','empty'],
	'X': ['crate','contains the level\'s',' secret power up'],
	'1': ['crate','contains powerup 1'],
	'2': ['crate','contains powerup 2'],
	'3': ['crate','contains powerup 3'],
	'4': ['crate','contains powerup 4'],
	'5': ['crate','contains powerup 5'],
	'6': ['crate','contains powerup 6'],
	'7': ['crate','contains powerup 7'],
	'8': ['wheels'],
	'W': ['cow','looking left'],
	'Y': ['cow','looking right'],
	'V': ['25% chance to spawn',' a cow if there are',' less than 2 cows'],
	'$': ['money bag'],
	'?': ['crate','contains random powerup','unused in base game'],
	'C': ['chicken'],
	'D': ['dynamite'],
	'I': ['cinder'],
	'R': ['random crate, chicken',' dynamite, cinder, or', ' gatling'],


}







def drawFloor(x,y):
	pygame.draw.rect(screen, '#FEb854', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))				
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.125, DIM_BLK, DIM_BLK*0.75))
def drawFloorVert(x,y):
	pygame.draw.rect(screen, '#FEb854', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))				
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK+DIM_BLK/8, OFF_Y + y*DIM_BLK, DIM_BLK-DIM_BLK/4, DIM_BLK))
def drawStud(x,y):
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#FE48DE', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK),DIM_BLK//6)
def drawJumpThru(x,y):
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK*0.3))
def drawLadderStep(x,y):
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK+DIM_BLK*0, OFF_Y + y*DIM_BLK, DIM_BLK*0.1, DIM_BLK))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK+DIM_BLK*0.9, OFF_Y + y*DIM_BLK, DIM_BLK*0.1, DIM_BLK))	
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0, DIM_BLK, DIM_BLK*0.1))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.33, DIM_BLK, DIM_BLK*0.1))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.67, DIM_BLK, DIM_BLK*0.1))
def drawLadder(x,y):
	drawLadderStep(x,y)
	drawLadderStep(x,y+1)
	drawLadderStep(x,y+2)
	drawLadderStep(x,y+3)
def drawLadderTop(x,y):
	drawJumpThru(x,y)
	drawLadderStep(x,y)
	drawLadderStep(x,y+1)
	drawLadderStep(x,y+2)
	drawLadderStep(x,y+3)
def drawCrate(x,y):
	pygame.draw.rect(screen, '#E8Ea4a', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#8a6042', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK),DIM_BLK//6)	
def drawStarCrate(x,y):
	pygame.draw.rect(screen, '#E8Ea4a', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#8a6042', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK),DIM_BLK//6)
	screen.blit(font.render('X', True, '#8a6042'), (OFF_X + (x+0.20)*DIM_BLK, OFF_Y + (y-0.1)*DIM_BLK))
def drawBarrel(x,y):
	pygame.draw.circle(screen, '#E8Ea4a', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2)
	pygame.draw.circle(screen, '#8a6042', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2,DIM_BLK//8)
def drawDynamite(x,y):
	pygame.draw.rect(screen, '#E03c32', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#a3a324', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.15, DIM_BLK, DIM_BLK*0.2))
	pygame.draw.rect(screen, '#a3a324', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.65, DIM_BLK, DIM_BLK*0.2))
def drawMoneyBag(x,y):
	pygame.draw.rect(screen, '#E8Ea4a', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#008456', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK),DIM_BLK//6)		
def drawCinder(x,y):
	pygame.draw.rect(screen, '#707070', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
	pygame.draw.rect(screen, '#000000', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.15, DIM_BLK, DIM_BLK*0.2))
	pygame.draw.rect(screen, '#000000', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.65, DIM_BLK, DIM_BLK*0.2))
def drawGatling(x,y):
	pygame.draw.rect(screen, '#8A6042', (OFF_X + (x+0.2)*DIM_BLK, OFF_Y + (y+0.7)*DIM_BLK, DIM_BLK*0.6, DIM_BLK*0.3))
	pygame.draw.rect(screen, '#C8C8C8', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK*0.7))
def drawGear(x,y):
	pygame.draw.circle(screen, '#4430BA', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2)
	pygame.draw.circle(screen, '#FE48DE', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2,DIM_BLK//8)
def drawGearBG(x,y):
	pygame.draw.circle(screen, '#FE48DE', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2,DIM_BLK//8)
def drawWheels(x,y):
	pygame.draw.circle(screen, '#4430BA', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2,DIM_BLK//8)
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x+0.5)*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.35, DIM_BLK, DIM_BLK*0.3))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x+1)*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.35, DIM_BLK, DIM_BLK*0.3))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x+2)*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.35, DIM_BLK, DIM_BLK*0.3))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x+3)*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.35, DIM_BLK, DIM_BLK*0.3))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x+3.5)*DIM_BLK, OFF_Y + y*DIM_BLK+DIM_BLK*0.35, DIM_BLK, DIM_BLK*0.3))
	pygame.draw.circle(screen, '#4430BA', (OFF_X + (x+4)*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2,DIM_BLK//8)
def drawChicken(x,y):
	pygame.draw.circle(screen, '#FFFFFF', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + y*DIM_BLK+DIM_BLK/2),DIM_BLK//2)
def drawSwitch(x,y):
	pygame.draw.rect(screen, '#FEb854', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK*0.2, DIM_BLK))
	pygame.draw.rect(screen, '#4430BA', (OFF_X + (x)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK, DIM_BLK, DIM_BLK*0.5))
def drawCowRight(x,y):
	pygame.draw.ellipse(screen, '#8A6042', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK*3, DIM_BLK*2))
	pygame.draw.circle(screen, '#FFFFFF', (OFF_X + (x+2.5)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK),DIM_BLK//4)
def drawCowLeft(x,y):
	pygame.draw.ellipse(screen, '#8A6042', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK*3, DIM_BLK*2))
	pygame.draw.circle(screen, '#FFFFFF', (OFF_X + (x+0.5)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK),DIM_BLK//4)
def drawMan(x,y,c1,c2,c3,d):
	pygame.draw.rect(screen, c1, (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y-0.5)*DIM_BLK, DIM_BLK*0.2, DIM_BLK*1.5))
	pygame.draw.line(screen, '#ca4a00', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y-0.1)*DIM_BLK), (OFF_X + (x+0.4+0.5-d*1.0)*DIM_BLK, OFF_Y + (y-0.1)*DIM_BLK),round(0.2*DIM_BLK))
	pygame.draw.circle(screen, c2, (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y-1)*DIM_BLK+DIM_BLK/2),DIM_BLK//4)
	pygame.draw.circle(screen, c1, (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y-1)*DIM_BLK+DIM_BLK/2),DIM_BLK//4,DIM_BLK//8)
def drawlawman(x,y,d,a):
	drawMan(x,y,'#a3a324','#FF0000'*a+'#FEb854'*(not a),'#ca4a00',d)
def drawlawmanlup(x,y,d):
	c1,c2,c3 = '#a3a324','#FEb854','#ca4a00'
	pygame.draw.rect(screen, c1, (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y-0.5)*DIM_BLK, DIM_BLK*0.2, DIM_BLK*1.5))
	pygame.draw.line(screen, c3, (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y-0.1)*DIM_BLK), (OFF_X + (x+0.4+0.5-d*1.0)*DIM_BLK, OFF_Y + (y-0.4)*DIM_BLK),round(0.2*DIM_BLK))
	pygame.draw.circle(screen, c2, (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y-1)*DIM_BLK+DIM_BLK/2),DIM_BLK//4)
	pygame.draw.circle(screen, c1, (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y-1)*DIM_BLK+DIM_BLK/2),DIM_BLK//4,DIM_BLK//8)
def drawSheriff(x,y,d,a):
	drawMan(x,y,'#FFFFFF','#FF0000'*a+'#FEb854'*(not a),'#ca4a00',d)	
def drawlawmanCrouch(x,y,d):
	pygame.draw.rect(screen, '#a3a324', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y)*DIM_BLK, DIM_BLK*0.2, DIM_BLK))
	pygame.draw.line(screen, '#ca4a00', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK), (OFF_X + (x+0.4+0.5-d*1.0)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK),round(0.2*DIM_BLK))
	pygame.draw.circle(screen, '#FEb854', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y)*DIM_BLK+DIM_BLK/2),DIM_BLK//4)
	pygame.draw.circle(screen, '#a3a324', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y)*DIM_BLK+DIM_BLK/2),DIM_BLK//4,DIM_BLK//8)	
def drawlawmanCrouchldown(x,y,d):
	pygame.draw.rect(screen, '#a3a324', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y)*DIM_BLK, DIM_BLK*0.2, DIM_BLK))
	pygame.draw.line(screen, '#ca4a00', (OFF_X + (x+0.4)*DIM_BLK, OFF_Y + (y+0.5)*DIM_BLK), (OFF_X + (x+0.4+0.5-d*1.0)*DIM_BLK, OFF_Y + (y+0.8)*DIM_BLK),round(0.2*DIM_BLK))
	pygame.draw.circle(screen, '#FEb854', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y)*DIM_BLK+DIM_BLK/2),DIM_BLK//4)
	pygame.draw.circle(screen, '#a3a324', (OFF_X + x*DIM_BLK+DIM_BLK/2, OFF_Y + (y)*DIM_BLK+DIM_BLK/2),DIM_BLK//4,DIM_BLK//8)
def drawDynamiteLawman(x,y,d,a):
	drawMan(x,y,'#a3a324','#FF0000'*a+'#FEb854'*(not a),'#a3a324',d)
	drawDynamite(x,y-1.7)
def drawDodger(x,y):
	drawMan(x,y,'#CA4A00','#FEB854','#991515',0)
def drawBrand(x,y):
	drawMan(x,y,'#8A6042','#FE626E','#861650',0)
def drawMaria(x,y):
	drawMan(x,y,'#006AB4','#8A6042','#FEB854',0)


def drawBlock(block,x,y):
	if block == " ":
		#pygame.draw.rect(screen, CLR_EMPTY, (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))
		pass
	elif block == "=" or block == "~":
		drawFloor(x,y)
	elif block == "|" or block == "~":
		drawFloorVert(x,y)
	elif block == "@" or block == "0":
		drawStud(x,y)
	elif block == "-" or block == "+":
		drawJumpThru(x,y)
	elif block == "L":
		drawLadder(x,y)
	elif block == "P" or block == "T":
		drawLadderTop(x,y)
	elif block == "B" or block == "X":
		drawCrate(x,y)
	elif block in ['1','2','3','4','5','6','7','?']:
		drawStarCrate(x,y)				
	elif block == "K" or block == "N":
		drawBarrel(x,y)				
	elif block == "H":
		pass
	elif block == "D":
		drawDynamite(x,y)
	elif block == "$":
		drawMoneyBag(x,y)
	elif block == "I":
		drawCinder(x,y)
	elif block in ['G','A','>','<']:
		drawGatling(x,y)
	elif block == "%" or block == "&" or block == "!":
		drawGear(x,y)
	elif block == ":" or block == "*":
		drawGearBG(x,y)				
	elif block == "S":
		drawSwitch(x,y)				
	elif block == "8":
		drawWheels(x,y)
	elif block == "C":
		drawChicken(x,y)
	elif block == "Y":
		drawCowRight(x,y)
	elif block == "W":
		drawCowLeft(x,y)
	elif block in ['a','c','k','m']:
		drawlawman(x,y,1,block in ['a','b','k','l','m','n','o','p'])
	elif block in ['b','d','l','n']:
		drawlawman(x,y,0,block in ['a','b','k','l','m','n','o','p'])
	elif block in ['g','h']:
		drawlawmanlup(x,y,block=='g')
	elif block in ['e','f']:
		drawlawmanCrouch(x,y,block=='e')
	elif block in ['i','j']:
		drawlawmanCrouchldown(x,y,block=='i')		
	elif block in ['s','t','u','v']:
		drawSheriff(x,y,block in ['s','u'],block in ['s','t'])			
	elif block in ['o','p','q','r']:
		drawDynamiteLawman(x,y,block in ['o','q'],block in ['a','b','k','l','m','n','o','p'])	
	elif block == 'x':
		drawDodger(x,y)
	elif block == 'y':
		drawBrand(x,y)
	elif block == 'z':
		drawMaria(x,y)
	elif block == 'E':
		screen.blit(font.render('E', True, '#FF0000'), (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK))
		if RUNNING==1 and y<20:
			pygame.draw.line(screen,'#770000',(OFF_X+(x)*DIM_BLK,OFF_Y),(OFF_X+(x)*DIM_BLK,OFF_Y+DIM_BLK*18),1)
	else:
		pygame.draw.rect(screen, '#444444', (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK, DIM_BLK, DIM_BLK))				
	if showText:
		screen.blit(font.render(block, True, CLR_BTXT), (OFF_X + x*DIM_BLK, OFF_Y + y*DIM_BLK))


SETTINGSPATH = os.getcwd()+'/settings'
if not os.path.isfile(os.getcwd()+'/settings'):
	with open(SETTINGSPATH, 'w') as f:
		f.write('{}')

def update_settings(entry, value):
    with open(SETTINGSPATH, 'r') as f:
        settings = eval(f.read())
    settings[entry] = value
    with open(SETTINGSPATH, 'w') as f:
        f.write(str(settings))

def get_value(entry):
    with open(SETTINGSPATH, 'r') as f:
        settings = eval(f.read())
    return settings.get(entry)



DATAWINPATH = get_value('datawinPath')
UTMODCLIPATH = os.getcwd()+'/UTModCli/UndertaleModCli.exe'
GAMECODEFILE = get_value('codeFilePath')

def promptFileSelect(promptText = 'Open', startDir = ''):
	app = wx.App(None)
	dialog = wx.FileDialog(None, promptText,defaultDir=str(startDir))
	if dialog.ShowModal() == wx.ID_OK:
		path = dialog.GetPath()
	else:
		path = None
	dialog.Destroy()
	app.Destroy()
	return path

def firstTimeSetup():
	global DATAWINPATH,GAMECODEFILE
	DATAWINPATH = promptFileSelect('Select Ufo 50\'s data.win file')
	if DATAWINPATH==None:
		return
	#check if it's data.win
	update_settings('datawinPath', DATAWINPATH)
	update_settings('datawinLoaded', 1)

	backupDatawin()

	command = [UTMODCLIPATH,'dump',DATAWINPATH,'-c','gml_Object_o13_Game_Other_21','-o',os.getcwd()]
	x = subprocess.call(command)
	if x != 0:
		return #error
	update_settings('codeFilePath',os.getcwd()+'/CodeEntries'+'/gml_Object_o13_Game_Other_21.gml')
	update_settings('codeFileLoaded',1)
	GAMECODEFILE = get_value('codeFilePath')
	
	if not get_value('baseMissionsExtracted'):
		extractBaseMissions()
		update_settings('baseMissionsExtracted',1)


def loadMissionIntoEditor(new=0):
	global Trains,missionNameBox,missionTextBox,missionTipBox,killMissionButton,timeLimitBox,moneyGoalBox,bulletAmountBox,secretPowerUpButton,starGoalBox,previewYBox,horseButton,horseRiderButton
	if new:
		missionNameBox.text = 'MY LEVEL!'
		missionTextBox.text = 'THIS ONE IS CRAZY!!'
		missionTipBox.text = 'PRESS JUMP BUTTON TO JUMP'
		killMissionButton.num = 0
		timeLimitBox.text = '60'
		moneyGoalBox.text = '4'
		bulletAmountBox.text = '2'
		secretPowerUpButton.num = 0
		starGoalBox.text = '30'
		previewYBox.text = '144'
		horseButton.num = 0
		horseRiderButton.num = 0
		Trains = [[]]
		for t in sampleTrain:
			Trains[0].append(t.copy())
		

	else:
		MissionPath = promptFileSelect('Select Mission',os.getcwd())
		if MissionPath==None:
			return 1
		with open(MissionPath,'r') as f:
			content = f.readlines()
		Trains = []
		for wLine in content:
			line = wLine.split('=')
			match line[0]:
				case 'newLevel.missionName ':
					#print('newLevel.missionName ')
					missionNameBox.text=line[1].split('"')[1]
				case 'newLevel.missionText ':
					#print('newLevel.missionText ')
					missionTextBox.text=line[1].split('"')[1]
				case 'newLevel.missionTip ':
					#print('newLevel.missionTip ')
					missionTipBox.text=line[1].split('"')[1]
				case 'newLevel.killMission ':
					#print('newLevel.killMission ')
					killMissionButton.num = 0 if ('KILL_ANY' in line[1]) else 1 if ('KILL_SHERIFF' in line[1]) else 2
				case 'newLevel.timeLimit ':
					#print('newLevel.timeLimit ')
					timeLimitBox.text=line[1].strip('\'";\n ')
				case 'newLevel.moneyGoal ':
					#print('newLevel.moneyGoal ')
					moneyGoalBox.text=line[1].strip('\'";\n ')
				case 'newLevel.bulletAmount ':
					#print('newLevel.bulletAmount ')
					bulletAmountBox.text =line[1].strip('\'";\n ')
				case 'newLevel.secretPowerUp ':
					#print('newLevel.secretPowerUp ')
					x = line[1].strip('\'"; ')
					secretPowerUpButton.num = x if x.isnumeric() else 0 #WRONG, but i dont know the number to literal mapping of these
				case 'newLevel.starGoal ':
					#print('newLevel.starGoal ')
					starGoalBox.text=line[1].strip('\'";\n ')
				case 'newLevel.previewY ':
					previewYBox.text=line[1].strip('\'";\n ')
				case 'newLevel.horse ':
					#print('newLevel.horse ')
					horseButton.num = 0 if line[1]=='LEFT;' else 1
				case 'newLevel.horseRider ':
					#print('newLevel.horseRider ')
					horseRiderButton.num = 0 if line[1]=='s13_Dodger;' else 1 if line[1]=='s13_Brand;' else 2
				case 'trainLayout ':
					#print('trainLayout')
					Trains.append([])
				case 'trainLayout +':
					#print('trainLayout +')
					x = wLine.split('"')[1]
					#print(x)
					Trains[-1].append(list(x))

	for elem in UI_2:
		elem.refresh() #refreshing the text

	setRunningScreen(1)
	return 0


selectedLevelInFile = [0]
LevelsInFile = [[]]


def backupDatawin():
	DATAWINPATH = get_value('datawinPath')
	if os.path.exists(DATAWINPATH+'.backup'):
		return

	shutil.copy(DATAWINPATH,DATAWINPATH+'.backup')
	print('backup created!')

def insertDatawin():
	genLevelCodeBlock(missionNameBox.text)
	insertMissionToGame(missionNameBox.text,selectedLevelInFile[0],replaceOrInsertButton.num==1)

	command = [UTMODCLIPATH,'replace',DATAWINPATH,'-c',f'gml_Object_o13_Game_Other_21={GAMECODEFILE}','-o',DATAWINPATH]
	x = subprocess.call(command)
	if x==0:
		print("inserted code file into game!")
		return
	print(f"eror!! restore datawin from backup")



def putBlockInTrain(train,pos,c):
	train[pos[1]][pos[0]] = c

levelSavedNotice = 0
def saveCurrentLevelFile():
	genLevelCodeBlock(missionNameBox.text)
	global levelSavedNotice
	levelSavedNotice = 1

def genLevelCodeBlock(missionName):
	getMissionsNames()
	if not os.path.exists(os.getcwd()+'/missions'):
		os.mkdir(os.getcwd()+'/missions')
	filepath = os.getcwd()+f'/missions/{missionName}.txt'


	with open(filepath,'w') as f:
		f.write('newLevel = scr13_CreateLevel(n++);\n')
		f.write(f'newLevel.missionName = "{missionNameBox.text}";\n')
		f.write(f'newLevel.missionText = "{missionTextBox.text}";\n')
		f.write(f'newLevel.missionTip = "{missionTipBox.text}";\n')
		f.write(f'newLevel.killMission = {["KILL_ANY","KILL_SHERIFF","KILL_SWITCH"][killMissionButton.num]};\n')
		f.write(f'newLevel.timeLimit = {timeLimitBox.text};\n')
		f.write(f'newLevel.moneyGoal = {moneyGoalBox.text};\n')
		f.write(f'newLevel.bulletAmount = {bulletAmountBox.text};\n')
		f.write(f'newLevel.secretPowerUp = {secretPowerUpButton.num};\n')
		f.write(f'newLevel.starGoal = {starGoalBox.text};\n')
		f.write(f'newLevel.previewY = {previewYBox.text};\n')
		f.write(f'newLevel.horse = {["LEFT","RIGHT"][horseButton.num]};\n')
		f.write(f'newLevel.horseRider = {["s13_Dodger","s13_Brand","s13_Maria"][horseRiderButton.num]};\n')

		

		for i,train in enumerate(Trains):
			f.write('trainLayout = "";\n')
			for row in train:
				f.write(f'trainLayout += "{"".join(row)}";\n')
			f.write(f'newLevel.map[{i}] = trainLayout;\n')


def getInsertionInfo(names,ind,rep):
	if len(names)==0:
		return ''
	if rep:
		ind = min(ind,len(names)-1)
		ind = max(ind,0)
		return f'replace "{names[ind]}"'
	if ind<=0:
		return f'add before "{names[0]}"'
	if ind>=len(names):
		return f'add after "{names[-1]}"'
	return f'add between "{names[ind-1]}" and "{names[ind]}"'

def getMissionsNames():
	levelsNames = []
	target_file = str(GAMECODEFILE)
	if target_file=='None':
		LevelsInFile[0] = []
		return []
	with open(target_file, 'r') as gf:
		target_content = gf.readlines()  
		for i,line in enumerate(target_content):
			if 'newLevel.missionName' in line:
				if 'scrStringExt' in line:
					levelNum = line.split('"')[1].split('_')[2]
					levelsNames.append('baseMission_'+levelNum)
				else:
					levelsNames.append(line.split('"')[1])

	
	LevelsInFile[0] = levelsNames 
	
	
def extractBaseMissions():
	if not os.path.exists(os.getcwd()+'/base missions'):
		os.mkdir(os.getcwd()+'/base missions')	
	target_file = str(GAMECODEFILE)
	with open(target_file, 'r') as gf:
		prevValidLineInd = -1
		prevValidLineNum = -1
		prevLevelStartLine = 8
		target_content = gf.readlines()  
		levelNum = -1
		for i,line in enumerate(target_content):
			if 'scrStringExt' in line:
				levelNum = int(line.split('"')[1].split('_')[2])
			if 'newLevel.map' in line:
				cartNumber = int(line[line.index('[') + 1:line.index(']')])
				if cartNumber<prevValidLineNum:
					with open(os.getcwd()+f'/base missions/baseMission_{(levelNum-1)}.txt','w') as bf:
						bf.writelines(target_content[prevLevelStartLine:prevValidLineInd+1])
					prevLevelStartLine = prevValidLineInd+1
					prevLine = i-1					
					prevValidLineNum = -1
				else:
					prevValidLineNum = cartNumber
				prevValidLineInd = i

			if 'NUM_LEVELS = n - 1;' in line:
				with open(os.getcwd()+f'/base missions/baseMission_{(levelNum)}.txt','w') as bf:
					bf.writelines(target_content[prevLevelStartLine:i])


def insertMissionToGame(missionName,missionPositon=0,replace=True):

	levelsCount = 0
	target_content = ''
	source_content = ''
	modified_content = ''
	levelsStartLines = [8]
	
	target_file = str(GAMECODEFILE)
	source_file = os.getcwd()+f'/missions/{missionName}.txt'
	with open(target_file, 'r') as gf:
		prevValidLineInd = -1
		prevValidLineNum = -1		
		target_content = gf.readlines()  
		for i,line in enumerate(target_content):
			if 'newLevel.map' in line:
				number = int(line[line.index('[') + 1:line.index(']')])
				if number<=prevValidLineNum:
					levelsStartLines.append(prevValidLineInd+1)
					prevValidLineNum = number
				else:
					prevValidLineNum = number
				prevValidLineInd = i
			if 'NUM_LEVELS = n - 1;' in line:
				levelsStartLines.append(i)


	with open(source_file, 'r') as mf:
		source_content = mf.readlines()  


	if replace:
		if missionPositon+1>=len(levelsStartLines):
			missionPositon = len(levelsStartLines)-2
		line_number = levelsStartLines[missionPositon]
		nextline_number = levelsStartLines[missionPositon+1]		
		modified_content = target_content[:max(line_number,0)] + source_content + target_content[max(nextline_number,0):]
	else:
		line_number = levelsStartLines[missionPositon]
		modified_content = target_content[:line_number] + source_content + target_content[line_number:]

	with open(target_file, 'w') as gf:
		gf.writelines(modified_content)

	print('inserted level into code file!')
	getMissionsNames()



def posToInds(pos):
	return (pos[0]-OFF_X)//DIM_BLK,(pos[1]-OFF_Y)//DIM_BLK


UI_BORDER_RADIUS = 3
UI_BORDER_DEPTH = 1
UI_BORDER_COLOR = '#CCCCCC'
UI_BUTTON_COLOR = "#111111"
UI_BUTTON_HCOLOR = "#333333"
UI_BUTTON_CCOLOR = '#000000'
class InputBox:
	def __init__(self, x, y, w, h, text="", numsOnly = False):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = "#777777"
		self.text = text
		self.txt_surface = font.render(text, True, "#000000")
		self.active = False
		self.numsOnly = numsOnly

	def clicked(self, mx=MouseX, my=MouseY):

		if (
			self.rect.x <= mx <= self.rect.x + self.rect.w
			and self.rect.y <= my <= self.rect.y + self.rect.h
		):
			self.active = not self.active
		else:
			self.active = False

		self.color = "#CCCCCC" if self.active else "#777777"

	def Typing(self, event):
		if self.active:

			if event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
				if len(self.text) == 0 and self.numsOnly:
					self.text = "0"

			elif self.numsOnly:
				if event.key in numericalButtons:
					if self.text[0] == "0":
						self.text = event.unicode
					else:
						self.text += event.unicode
			else:
				self.text += event.unicode

		self.refresh()
	def draw(self):
		pygame.draw.rect(screen, self.color, self.rect,0,UI_BORDER_RADIUS)
		pygame.draw.rect(screen, UI_BORDER_COLOR, self.rect,UI_BORDER_DEPTH,UI_BORDER_RADIUS)
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.rect.h/5))
		width = max(200, self.txt_surface.get_width() + 10)
		self.rect.w = width
	def refresh(self):
		# Re-render the text.
		self.txt_surface = font.render(self.text, True, "#000000")		


class FlipButton:
	def __init__(self, rect, startNum=0,numsLen=2,texts=[]):
		self.rect = pygame.Rect(rect) 
		self.color = UI_BUTTON_COLOR
		self.hoverColor = UI_BUTTON_HCOLOR 
		self.num = startNum
		self.currentColor = self.color 
		self.numsLen=numsLen
		self.texts = texts
		self.txt_surface = font.render("", True, "#000000")
		if len(self.texts)>self.num:
			self.txt_surface = font.render(self.texts[self.num], True, "#FFFFFF")		

	def draw(self):
		pygame.draw.rect(screen, self.currentColor, self.rect,0,UI_BORDER_RADIUS)
		pygame.draw.rect(screen, UI_BORDER_COLOR, self.rect,UI_BORDER_DEPTH,UI_BORDER_RADIUS)
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.rect.h/6))

		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.currentColor = self.hoverColor
			if pygame.mouse.get_pressed()[0]:
				self.currentColor = UI_BUTTON_CCOLOR			
		else:
			self.currentColor = self.color		

	def clicked(self, mx=MouseX, my=MouseY):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.num = (self.num+1)%self.numsLen
		if len(self.texts)>self.num:
			self.refresh()	
	def refresh(self):
		self.txt_surface = font.render(self.texts[self.num], True, "#FFFFFF")				

class AddButton:
	def __init__(self, rect,text):
		self.rect = pygame.Rect(rect) 
		self.color = UI_BUTTON_COLOR
		self.hoverColor = UI_BUTTON_HCOLOR 
		self.currentColor = self.color 
		self.txt_surface = font.render(text, True, "#FFFFFF")
	def draw(self):
		pygame.draw.rect(screen, self.currentColor, self.rect,0,UI_BORDER_RADIUS)
		pygame.draw.rect(screen, UI_BORDER_COLOR, self.rect,UI_BORDER_DEPTH,UI_BORDER_RADIUS)
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.rect.h/6))

		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.currentColor = self.hoverColor
			if pygame.mouse.get_pressed()[0]:
				self.currentColor = UI_BUTTON_CCOLOR
		else:
			self.currentColor = self.color		

	def clicked(self, mx, my,arr,num):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			arr[0] += num
	def refresh(self):
		self.txt_surface = font.render(self.texts[self.num], True, "#FFFFFF")				

class FuncButton:
	def __init__(self, rect,text,func,arg=None,font=font):
		self.rect = pygame.Rect(rect) 
		self.color = UI_BUTTON_COLOR
		self.hoverColor = UI_BUTTON_HCOLOR
		self.currentColor = self.color 
		self.txt_surface = font.render(text, True, "#FFFFFF")
		self.func = func
		self.arg = arg
	def draw(self):
		pygame.draw.rect(screen, self.currentColor, self.rect,0,UI_BORDER_RADIUS)
		pygame.draw.rect(screen, UI_BORDER_COLOR, self.rect,UI_BORDER_DEPTH,UI_BORDER_RADIUS)
		screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.rect.h/6))

		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.currentColor = self.hoverColor
			if pygame.mouse.get_pressed()[0]:
				self.currentColor = UI_BUTTON_CCOLOR
		else:
			self.currentColor = self.color		

	def clicked(self, mx, my):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			if self.arg != None:
				self.func(self.arg)
			else:
				self.func()
	def refresh(self):
		pass				


class TextBox:
	def __init__(self,text,font,color,x,y):
		self.x = x
		self.y = y
		self.txt_surface = font.render(text, True, color)
	def draw(self):
		screen.blit(self.txt_surface, (self.x, self.y))
	def clicked(self,mx,my):
		pass


# missionName = "MY LEVEL"
# missionText = "THEY CANT KEEP GETTING AWAY WITH IT!"
# missionTip = "GET CREATIVE!"
# killMission = 0  #0 is KILL_ANY, 1 is KILL_SHERIFF
# timeLimit = 72 
# moneyGoal = 4 
# bulletAmount = 2 
# secretPowerUp = 0  # from 0 to 7 inclusive
# starGoal = 30 
# previewY = 144 
# horse = 0  #0 is LEFT, 1 is RIGHT
# horseRider = 0 #0 Dodger, 1 Brand, 2 Maria

def addTrain(n):
	preAddTrainButton.num=0
	preAddTrainButton.refresh()
	x = []
	for t in sampleTrain:
		x.append(t.copy())
	if n==0:
		Trains.insert(TrainIndex[0], x)

	if n==1:
		Trains.insert(TrainIndex[0]+1,x)


def removeTrain():
	preRmvTrainButton.num=0
	preRmvTrainButton.refresh()
	if len(Trains)==1:
		print("cant remove only train!")
		return
	Trains.pop(TrainIndex[0])
	if TrainIndex[0]>0:
		TrainIndex[0] -= 1
	else:
		pass


def setRunningScreen(n):
	global RUNNING
	if RUNNING==11 and n==11:
		n=1
	RUNNING = n

	match n:
		case 0:
			pass
		case 1:
			pass
		case 2:
			pass
		case 3:
			getMissionsNames()

def loadAndInsert():
	getMissionsNames()
	x = loadMissionIntoEditor()
	setRunningScreen(0)
	if x: ##user cancelled file selection
		return 
	
	replaceOrInsertButton.num=0
	if quickInsertPositionButton.num==0:
		selectedLevelInFile[0] = 0
	else:
		selectedLevelInFile[0] = len(LevelsInFile[0])
	insertDatawin()

preRmvTrainButton = FlipButton((320,HEIGHT-95,60,30),0,2,['-train','sure?'])
preAddTrainButton = FlipButton((470,HEIGHT-95,60,30),0,2,['+train','where?'])
addTrainButton0 = FuncButton((460,HEIGHT-60,40,30),'left',addTrain,0)
addTrainButton1 = FuncButton((510,HEIGHT-60,40,30),'right',addTrain,1)
rmvTrainButton = FuncButton((320,HEIGHT-60,40,30),'yes',removeTrain)
prevTrainButton = AddButton((385,HEIGHT-60,30,30),'<-')
nextTrainButton = AddButton((425,HEIGHT-60,30,30),'->')


blockSelectButton = FuncButton((10,HEIGHT-95,80,30),'blocks (Tab)',setRunningScreen,11,fontS)

saveLevelButton = FuncButton((570,HEIGHT-60,50,30),'save',saveCurrentLevelFile)
LevelSettingsButton = FuncButton((570,HEIGHT-95,140,30),'mission settings',setRunningScreen,2)
InsertLevelButton = FuncButton((630,HEIGHT-60,150,30),'insert into game...',setRunningScreen,3)




UI_1 = [nextTrainButton,prevTrainButton,preAddTrainButton,preRmvTrainButton,saveLevelButton,InsertLevelButton,LevelSettingsButton,blockSelectButton]


X = 200
Y = 50
H = 40
missionNameBox = InputBox(X,Y,100,H,"MY LEVEL");Y = Y+42
missionTextBox = InputBox(X,Y,100,H,"MY TEXT");Y = Y+42
missionTipBox = InputBox(X,Y,100,H,"MY TIP");Y = Y+42
killMissionButton = FlipButton((X,Y,100,H),0,3,["normal","kill sheriff",'rescue (flip switch)']);Y = Y+42
timeLimitBox = InputBox(X,Y,100,H,"72",True);Y = Y+42
moneyGoalBox = InputBox(X,Y,100,H,"4",True);Y = Y+42
bulletAmountBox = InputBox(X,Y,100,H,"2",True);Y = Y+42
secretPowerUpButton = FlipButton((X,Y,100,H),0,8,["0","1","2","3","4","5","6","7"]);Y = Y+42
starGoalBox = InputBox(X,Y,100,H,"72",True);Y = Y+42
previewYBox = InputBox(X,Y,100,H,"144",True);Y = Y+42
horseButton = FlipButton((X,Y,100,H),0,2,["Left","Right"]);Y = Y+42
horseRiderButton = FlipButton((X,Y,100,H),0,3,["Dodger","Brand","Maria"]);Y = Y+42

backToEditorButton = FuncButton((WIDTH-X,510,80,40),"Back",setRunningScreen,1)
UI_2 = [missionNameBox,missionTextBox,missionTipBox,killMissionButton,timeLimitBox,moneyGoalBox,bulletAmountBox,secretPowerUpButton,starGoalBox,previewYBox,horseButton,horseRiderButton,backToEditorButton]



replaceOrInsertButton = FlipButton((130,130,100,H),0,2,["Add","Replace"]);
levelUpButton = AddButton((230,175,40,H),'^')
levelmaxButton = AddButton((180,175,40,H),'^^^')
levelDownButton = AddButton((280,175,40,H),'v')
levelminButton = AddButton((330,175,40,H),'vvv')
InsertButton = FuncButton((20,245,100,40),'Insert',insertDatawin)
UI_3 = [replaceOrInsertButton,levelUpButton,levelDownButton,InsertButton,backToEditorButton,levelmaxButton,levelminButton]


logoText = TextBox("Rail Heist Maker",fontL,'#FFFFFF',50,50)
SetupReadyText = TextBox("Ready!",font,'#44FF44',150,135)
SetupNotReadyText = TextBox("<-- Select UFO 50's data.win file to start making levels!",font,'#FF4444',150,135)
SetupButton = FuncButton((50,130,70,40),"Setup",firstTimeSetup)



returnToEditorButton = FuncButton((50,190,80,40),"Return",setRunningScreen,1)
newMissionButton = FuncButton((50,260,140,40),"New Mission",loadMissionIntoEditor,1)
LoadMissionButton = FuncButton((50,330,140,40),"Load Mission",loadMissionIntoEditor)
loadAndInsertButton = FuncButton((50,400,140,40),"Load & Insert",loadAndInsert)
inPositionText = TextBox("in position:",font,'#FFFFFF',195,405)
quickInsertPositionButton = FlipButton((280,400,100,40),0,2,["before first","after last"])
UI_0 = [SetupButton,logoText,loadAndInsertButton,quickInsertPositionButton,inPositionText]


def nothing():
	pass



Trains = []

TrainIndex = [0]

text1 = ""
MENU_1 = False

selectedChar = ''
infoChar = ''
showText = False
selectedCharValid = False

RUNNING = 0

selected_block_ind =[]



while True:

	MouseX, MouseY = pygame.mouse.get_pos()
	#screen.blit(font.render(str([MouseX,MouseY]+selectedLevelInFile+[selected_block_ind]),True,'#00FF00'),(10,10))
	prevLmouseclicked = Lmouseclicked
	prevRmouseclicked = Rmouseclicked
	prevMmouseclicked = Mmouseclicked

	selected_block_pos = ((MouseX)//DIM_BLK)*DIM_BLK,((MouseY)//DIM_BLK)*DIM_BLK
	selected_block_ind = posToInds((MouseX,MouseY))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_F8]:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			Lmouseclicked = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			Lmouseclicked = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
			Mmouseclicked = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
			Mmouseclicked = False			
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			Rmouseclicked = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
			Rmouseclicked = False


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if RUNNING!=1 and len(Trains)>0: 
					setRunningScreen(1)
				else:
					setRunningScreen(0)
			if event.key == pygame.K_TAB:
				if RUNNING==1:
					setRunningScreen(11)
				elif RUNNING==11:
					setRunningScreen(1)
			if event.key == pygame.K_F5:
				loadMissionIntoEditor()





		if RUNNING==0:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				for elem in UI_0:
					elem.clicked(MouseX,MouseY)
				if get_value('datawinLoaded') and get_value('codeFileLoaded'):
					newMissionButton.clicked(MouseX,MouseY)
					LoadMissionButton.clicked(MouseX,MouseY)
				if len(Trains)>0:
					returnToEditorButton.clicked(MouseX,MouseY)
		elif RUNNING==1:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				
				nextTrainButton.clicked(MouseX,MouseY,TrainIndex,1)
				prevTrainButton.clicked(MouseX,MouseY,TrainIndex,-1)
				TrainIndex[0] = max(TrainIndex[0],0)
				TrainIndex[0] = min(TrainIndex[0],len(Trains)-1)

				preAddTrainButton.clicked(MouseX,MouseY)
				preRmvTrainButton.clicked(MouseX,MouseY)

				if preAddTrainButton.num==1:
					addTrainButton0.clicked(MouseX,MouseY)
					addTrainButton1.clicked(MouseX,MouseY)
				if preRmvTrainButton.num==1:
					rmvTrainButton.clicked(MouseX,MouseY)			

				LevelSettingsButton.clicked(MouseX,MouseY)
				saveLevelButton.clicked(MouseX,MouseY)
				InsertLevelButton.clicked(MouseX,MouseY)
				blockSelectButton.clicked(MouseX,MouseY)

			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_LALT:
					showText=not showText
				elif event.key==pygame.K_LEFT:
					if pygame.key.get_pressed()[pygame.K_LSHIFT]:
						TrainIndex[0] = max(TrainIndex[0]-1,0)

					else:
						OFF_X -= DIM_BLK
				elif event.key==pygame.K_RIGHT:
					if pygame.key.get_pressed()[pygame.K_LSHIFT]:
						TrainIndex[0] = min(TrainIndex[0]+1,len(Trains)-1)

					else:					
						OFF_X += DIM_BLK			
				elif event.key==pygame.K_UP:
					if pygame.key.get_pressed()[pygame.K_LSHIFT]:
						DIM_BLK += 5

					else:					
						OFF_Y -= DIM_BLK
				elif event.key==pygame.K_DOWN:
					if pygame.key.get_pressed()[pygame.K_LSHIFT]:
						DIM_BLK = max(DIM_BLK-5,10)

					else:									
						OFF_Y += DIM_BLK
				elif event.key in [pygame.K_LSHIFT,pygame.K_TAB]:
					pass

				else:
					selectedChar = event.unicode
		elif RUNNING==11:
			if event.type==pygame.MOUSEBUTTONUP:
				blockSelectButton.clicked(MouseX,MouseY)		
		elif RUNNING==2:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				for elem in UI_2:
					elem.clicked(MouseX,MouseY)

			if event.type == pygame.KEYDOWN:
				for elem in UI_2:
					if type(elem)==InputBox:
						elem.Typing(event)
			


		elif RUNNING==3:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				replaceOrInsertButton.clicked(MouseX,MouseY)
				levelUpButton.clicked(MouseX,MouseY,selectedLevelInFile,1)
				levelDownButton.clicked(MouseX,MouseY,selectedLevelInFile,-1)
				levelmaxButton.clicked(MouseX,MouseY,selectedLevelInFile,99)
				levelminButton.clicked(MouseX,MouseY,selectedLevelInFile,-99)				
				InsertButton.clicked(MouseX,MouseY)
				backToEditorButton.clicked(MouseX,MouseY)




			#print("".join([str(int(pygame.key.get_pressed()[x])) for x in range(512)]))

		

	if RUNNING==0:
		for elem in UI_0:
			elem.draw()
			if get_value('datawinLoaded') and get_value('codeFileLoaded'):
				newMissionButton.draw()
				LoadMissionButton.draw()
			if len(Trains)>0:
				returnToEditorButton.draw()
		

		if (get_value('datawinLoaded') and get_value('codeFileLoaded')):
			SetupReadyText.draw()
		else:
			SetupNotReadyText.draw()

	elif RUNNING==1:
		pygame.draw.rect(screen, '#000010', (OFF_X , OFF_Y, DIM_BLK*48, DIM_BLK*18))
		for y,row in enumerate(Trains[TrainIndex[0]]):
			for x,block in enumerate(row):
				drawBlock(block,x,y)


		
		selectionValid = False		
		selectedCharValid = False

		if 0<=selected_block_ind[0]<48 and 0<=selected_block_ind[1]<18:
			selectionValid = True
			pygame.draw.rect(screen, '#FF0000', (selected_block_ind[0]*DIM_BLK+OFF_X, selected_block_ind[1]*DIM_BLK+OFF_Y, DIM_BLK, DIM_BLK),DIM_BLK//10)
			screen.blit(font.render(str(selected_block_ind),True,'#00FF00'),(100,HEIGHT-90))
		else:
			screen.blit(font.render(str(selected_block_ind),True,'#FF0000'),(100,HEIGHT-90))



		pygame.draw.rect(screen, (0,0,0), (0, HEIGHT-100, WIDTH, 100)) #bottom bar
		pygame.draw.line(screen,'#FFFFFF',(0,HEIGHT-100),(WIDTH,HEIGHT-100),2) #top border		
		pygame.draw.line(screen,'#FFFFFF',(315,HEIGHT-100),(315,HEIGHT),2) #seperator 1
		pygame.draw.line(screen,'#FFFFFF',(560,HEIGHT-100),(560,HEIGHT),2) #seperator 2


		if selectedChar in ValidChars:
			selectedCharValid=True
			screen.blit(font.render(selectedChar,True,'#00FF00'),(100,HEIGHT-70))
			t1 = posToInds((20,HEIGHT-30))
			drawBlock(selectedChar,t1[0],t1[1])
		else:
			screen.blit(font.render(selectedChar,True,'#FF0000'),(100,HEIGHT-70))
		


		screen.blit(fontS.render("block info:",True,'#FFFFFF'),(100,HEIGHT-90))
		if selectedChar in blocksInfo:
			Y=HEIGHT-90
			for t in blocksInfo[selectedChar]:
				screen.blit(fontS.render(' - '+t,True,'#FFFFFF'),(165,Y))
				Y+=15
		


		if selectionValid :
			if Mmouseclicked:
				selectedChar=Trains[TrainIndex[0]][selected_block_ind[1]][selected_block_ind[0]]
			if selectedCharValid and Lmouseclicked:
				putBlockInTrain(Trains[TrainIndex[0]],selected_block_ind,selectedChar)
			if Rmouseclicked:
				putBlockInTrain(Trains[TrainIndex[0]],selected_block_ind,' ')

		screen.blit(font.render(f"Train #{TrainIndex[0]+1}/{len(Trains)}",True,'#FFFFFF'),(390,HEIGHT-90))
		for elem in UI_1:
			elem.draw()
		if preAddTrainButton.num==1:
			addTrainButton0.draw()
			addTrainButton1.draw()
		if preRmvTrainButton.num==1:
			rmvTrainButton.draw()


		if levelSavedNotice > 0:
			screen.blit(fontS.render(f"saved level '{missionNameBox.text}'!",True,(round(levelSavedNotice*0x44),round(levelSavedNotice*0xFF),round(levelSavedNotice*0x44))),(575,575))
			levelSavedNotice -= clock.tick(240)/1000


		# pygame.draw.rect(screen,'#000000',(580,0,WIDTH-580,HEIGHT))
		# bx,by=600,30
		# for block in ValidChars:
		# 	t1 = posToInds((bx,by))
		# 	drawBlock(block,t1[0],t1[1])
		# 	by += 40
		# 	if by>30*16:
		# 		by=30
		# 		bx += 60

	if RUNNING == 11:

		pygame.draw.rect(screen, '#000010', (OFF_X , OFF_Y, DIM_BLK*48, DIM_BLK*18))
		for y,row in enumerate(blocksSelectingTrain):
			for x,block in enumerate(row):
				drawBlock(block,x,y)


		pygame.draw.rect(screen, (0,0,0), (0, HEIGHT-100, WIDTH, 100)) #bottom bar
		pygame.draw.line(screen,'#FFFFFF',(0,HEIGHT-100),(WIDTH,HEIGHT-100),2) #top border
		pygame.draw.line(screen,'#FFFFFF',(315,HEIGHT-100),(315,HEIGHT),2) #seperator 1
		pygame.draw.line(screen,'#FFFFFF',(560,HEIGHT-100),(560,HEIGHT),2) #seperator 2

		blockSelectButton.draw()

		selectionValid = False
		if 0<=selected_block_ind[0]<48 and 0<=selected_block_ind[1]<18:
			selectionValid = True
			pygame.draw.rect(screen, '#FF0000', (selected_block_ind[0]*DIM_BLK+OFF_X, selected_block_ind[1]*DIM_BLK+OFF_Y, DIM_BLK, DIM_BLK),DIM_BLK//10)


		if selectedChar in ValidChars:
			selectedCharValid=True
			t1 = posToInds((20,HEIGHT-30))
			drawBlock(selectedChar,t1[0],t1[1])

		




		if selectionValid:
			infoChar=blocksSelectingTrain[selected_block_ind[1]][selected_block_ind[0]]
		
		screen.blit(font.render(infoChar,True,'#00FF00'),(100,HEIGHT-70))
		screen.blit(fontS.render("block info:",True,'#FFFFFF'),(100,HEIGHT-90))
		if infoChar in blocksInfo:
			Y=HEIGHT-90
			for t in blocksInfo[infoChar]:
				screen.blit(fontS.render(' - '+t,True,'#FFFFFF'),(165,Y))
				Y+=15


		if Lmouseclicked and (infoChar in ValidChars):
			selectedChar = infoChar

		


	elif RUNNING==2:
		Y=50
		screen.blit(font.render("Mission Name:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Mission Text:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Mission Tip:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Mission Type:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Time Limit:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Money Goal:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Bullet Amount:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Secret PowerUp:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Time Star Goal:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Preview Y-Level:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Horse:",True,'#FFFFFF'),(20,Y));Y = Y+42
		screen.blit(font.render("Horse Rider:",True,'#FFFFFF'),(20,Y));Y = Y+42

		for elem in UI_2:
			elem.draw()
	elif RUNNING==3:
		Y=50
		screen.blit(font.render(f"Insert Current Level: {missionNameBox.text}",True,'#FFFFFF'),(20,Y));Y = Y+42
		if (get_value('datawinLoaded') and get_value('codeFileLoaded')):
			screen.blit(font.render("Ready! =)",True,'#00FF00'),(20,Y));Y = Y+42
			screen.blit(font.render("insertion type: ",True,'#FFFFFF'),(20,Y));Y = Y+42
			screen.blit(font.render(f"insertion position: {selectedLevelInFile[0]} ",True,'#FFFFFF'),(20,Y))
			screen.blit(font.render(getInsertionInfo(LevelsInFile[0],selectedLevelInFile[0],replaceOrInsertButton.num),True,'#FFFFFF'),(380,Y));Y = Y+42
			for elem in UI_3:
				elem.draw()

			if (selectedLevelInFile[0]<0):
				selectedLevelInFile[0]=0
			if (selectedLevelInFile[0]>len(LevelsInFile[0])):
				selectedLevelInFile[0]=len(LevelsInFile[0])			

			screen.blit(font.render("Levels in game: ",True,'#FFFFFF'),(20,350))
			bx,by = 10,380
			for name in LevelsInFile[0]:
				screen.blit(fontS.render(name+'',True,'#FFFFFF'),(bx,by))
				bx += 160
				if bx>WIDTH-100:
					bx = 10
					by += 20
		else:
			screen.blit(font.render("Not Ready! load data.win by pressing F5 or from the menu",True,'#FF0000'),(20,Y));Y = Y+42


		
	


			
	pygame.display.update()
	drawBackground()
