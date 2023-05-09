import random
from time import sleep
from pimoroni import Button
from picographics import PicoGraphics
from picographics import DISPLAY_PICO_DISPLAY
from picographics import PEN_P8

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type = PEN_P8, rotate = 180)
display.set_backlight(0.85)
display.set_font("serif")

buttonB = Button(13) # Fire button
right = Button(14) # Right button
left = Button(15) # Left button

white = display.create_pen(255, 255, 255)
black = display.create_pen(0, 0, 0)
blue = display.create_pen(65, 105, 225)
grey = display.create_pen(128, 128, 128)
purple = display.create_pen(255, 0, 255)
yellow = display.create_pen(255, 255, 0)
green = display.create_pen(0, 255, 0)
red = display.create_pen(255, 0, 0)

width, height = display.get_bounds()

# Initialise variables
cirles = ""
circles = []
wall = ""
shooter = ""

spritex = 5
spritey = 5
circlecountx = 6
circlecounty = 7
circlesSpacingx = 9
circlesSpacingy = 6
addY = 12 # Pixels of movement sideways, per turn on cirles (make faster when difficulty is higher)

loopCount = 0
score = 0
difficulty = 1
shooterPos = 40
middleOfShooter = 25
shotX = 250       
shotY = shooterPos + middleOfShooter 
shooterSpeed = 4          


class Circles(object):
    
    def __init__(self, type, x, y):
        self.visible = True
        self.type = type
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
    
def create_circle(type, x, y):
    circle = Circles(type, x, y)
    return circle

def define_circles():
    type = "circles" 
    for x in range (1, circlecountx + 1):
        for y in range (1, circlecounty + 1):
            xval = 210 - ((x * (spritex + circlesSpacingx)) - spritex)
            yval = (y * (spritey + circlesSpacingy)) - spritey
            circles.append(create_circle(type, xval, yval))

# Setting circles back to original position
def reset_circles(visibility): 
    x = 1
    y = 1
    for c in circles:
        if visibility:
            c.visible = True
        c.x = c.origx
        c.y = c.origy
            
def draw_circle(circle_type, pen, x, y):
    cur_x = x
    cur_y = y
    new_x = x + 10;
    new_y = y + 0;
    display.set_pen(black)
    display.circle(cur_x, cur_y, 6) #x, y and radius
    display.set_pen(pen)
    display.circle(new_x, new_y, 6) #x, y and radius
    
def draw_shooter(shooter_type, pen, x, y):
    cur_x = x
    cur_y = y
    new_x = x
    new_y = y+15;
    display.set_pen(black)
    display.rectangle(cur_x, cur_y, 20, 20)
    display.set_pen(pen)
    display.rectangle(new_x, new_y, 20, 20)

# Creating the walls at the bottom of the display
def walls(wall_type, pen, x, y):
    display.set_pen(pen)
    display.rectangle(x, y, 20, 30)

def clear():
    display.set_pen(black)
    display.clear()
    display.update()

# Clearing display
clear()
sleep(1)
clear()
sleep(1)

# Creating the circles
define_circles()

# Main game loop
while True:
    loopCount = loopCount + 1
    
    display.set_pen(black)
    display.clear()
    
    if loopCount > 16 - difficulty:         
        dropdown = False
        # Rest loop
        loopCount = 0             
        for c in circles:
            # Check if we need to move circles
            if c.visible == True: 
                if c.y + addY > 125 or c.y + addY < 1: # Checking if there are any circles at the edge of the screen
                    if c.x - 3 < 90:                   # If circles are at the bottom, reset their position to the top
                        reset_circles(False)
                        dropdown = False
                    dropdown = True
        # Moving the circles down if they reach the top
        if dropdown == True: 
            addY = addY * - 1
            for c in circles:
                c.x = c.x - 12 # Number of pixels to move them down by
        else:
            for c in circles:
                c.y = c.y + addY
                
    if left.read():
        if shooterPos > -15:
            shooterPos = shooterPos - 3  # Number of pixels to move left
    
    if right.read():
        if shooterPos < 98:
            shooterPos = shooterPos + 3  # Number of pixels to move right
    shotX = shotX + shooterSpeed 
    foundVisible = False

                    
    # Loop through all cicles and detect if they have been hit
    for c in circles:
        if shotX >= c.x and c.visible == True:
            # TODO: may need to change based on config of cicles
            if shotX - 4 <= c.x + 8:        
                if shotY > c.y:
                    if shotY <= c.y + 10:   
                        c.visible = False  
                        score = score + 10
                        # Reset the shot
                        shotX = 250               
                        shotY = shooterPos + middleOfShooter
                        
        if c.visible == True:
            foundVisible = True
            draw_circle(circles, white, c.x, c.y)

    if shotX > 240:
        if buttonB.read():
            shotX = 40
            shotY = shooterPos + middleOfShooter
        else:
            shotX = 250
  
    # Once all of the circles have gone, increase difficulty level and rest the circles
    if foundVisible == False:
            if difficulty < 10:
                difficulty = difficulty + 1
            reset_circles(True)
    
    # Drawing the red block
    draw_shooter(shooter, red, 20, int(shooterPos)) 
    
    # Drawing the shot: length of 5
    display.line(shotX, shotY, shotX - 5, shotY) 

    # Creating the walls
    walls(wall, grey, 55, 10)
    walls(wall, grey, 55, 55)
    walls(wall, grey, 55, 100)

    # Showing the scoring on the display
    display.set_pen(blue)
    display.text("["+str(difficulty)+"] score:"+str(score), 8, 5, angle=90, scale=0.5)

    # Colours change once the circles have been cleared
    if difficulty == 1:
        invader_colour = white
    elif difficulty == 2:
        invader_colour = green
    elif difficulty == 3:
        invader_colour = purple
    else:
        invader_colour = white
                  
    display.update()
    sleep(0.001)