import curses
import time




height = 20
width = 60
left_buffer_x = 15
bulletSpeed = 2

class SpaceShip:
    """A spaceship is defined by position and graphic and hitpoints"""
    def __init__(self):
        self.score = 0
        self.leftPos = int((width-left_buffer_x)/2)
        self.currentBullet = None

    def show(self,win,invader_list):
        """show the spaceship in the window"""
        win.erase()

        if(self.currentBullet != None):
            if(self.currentBullet.yPos > 0):
                for x in range(bulletSpeed):
                    self.currentBullet.yPos -= 1
                    # check for collision in enemy array, respond by destroying both bullet and enemy
                    for counter,invader in enumerate(invader_list):
                        if invader.isCollision(self.currentBullet.yPos,self.currentBullet.xPos-1):
                            invader_list.pop(counter)
                            win.addstr(self.currentBullet.yPos, self.currentBullet.xPos-1, " * ")
                            win.addstr(self.currentBullet.yPos-1, self.currentBullet.xPos-1, "* *")
                            win.addstr(self.currentBullet.yPos+1, self.currentBullet.xPos-1, "* *")
                            self.score += 10
                            self.currentBullet.__del__
                            self.currentBullet = None
                            break
                # add points to score on enemy destruction
                if self.currentBullet != None:
                    self.currentBullet.show(win)
            else:
                self.currentBullet.__del__
                self.currentBullet = None
                win.erase()

        # display score
        # -------------
        win.addstr(0,0,"score: " + str(self.score))
        # display spaceShip
        # -------------
        win.addstr((height-1),self.leftPos,"-^-")

        win.refresh()

    def move(self,key):
        #Go right
        if(key == 100 and self.leftPos < (width-4)):
            self.leftPos += 1
        #Go Left
        if(key == 97 and self.leftPos > left_buffer_x):
            self.leftPos -= 1
        #SPACEBAR shoot 32
        if(key == 32 and self.currentBullet == None):
            self.currentBullet = Bullet(self.leftPos+1)

        #TODO: redo entire workflow. Bullets should be in charge of shooting themselves.
        # Perhaps somekind of drawing handler should handle redrawing after every event
        # collisions should result in the position being filled with asterisk * for explosion, hangs for a second or two
        # enemies should fire bullets
        # good job tho
        
    
class Bullet:
    """A bullet will fly into the enemy ships"""

    def __del__(self):
        #probably put into log?
        print()
    
    def __init__(self, xPosition):
        self.xPos =  xPosition
        self.yPos = (height-2)
    
    def show(self,win):
        """show the bullet in the window"""
        # display bullet
        # -------------
        win.addstr(self.yPos,self.xPos,"+")
        win.refresh()


class Invader:
    """Enemy ships"""

    def __init__(self, yPosition, xPosition):
        self.xPos =  xPosition
        self.yPos = yPosition

    def show1(self,win):
        """show the invader in the window"""

        # display invader
        # -------------
        win.addstr(self.yPos, self.xPos,"-o-")

        win.refresh()

    def show2(self,win):
        """show the invader in the window"""

        # display invader
        # -------------
        win.addstr(self.yPos, self.xPos,"-0-")

        win.refresh()

    def isCollision(self,yPos, xPos):
        """detect collision on this object"""
        if xPos == self.xPos and yPos == self.yPos:
            return True
        else:
            return False



def spaceMain(stdscr):
    curses.curs_set(0) # set invisible cursor
    begin_y = 0
    begin_x = 0
    invader_list = []
    win = curses.newwin(height, width, begin_y, begin_x) # init window
    win.nodelay(True) # getch() does not block the program
    spaceShip = SpaceShip() #init the space ship
    spaceShip.show(win,invader_list) #show the space ship

    # create array of invaders
    for x in range(11):
        for y in range(6):
            invader_list.append(Invader(2*(y+1),(4*x)+left_buffer_x))
    # loop through and show invaders
    for invader in invader_list:
        invader.show1(win)

    key = ''
    while key != ord('q'):
        key = win.getch()
        spaceShip.move(key)
        spaceShip.show(win, invader_list)
        for invader in invader_list:
            invader.show1(win)
        # loop through and show invaders
        # check for loss via spaceship collision
        # check for win via elimination of enemy array
        time.sleep(.1)
        for invader in invader_list:
            invader.show2(win)
        time.sleep(.1)

if __name__ == '__main__':
    # Initialize curses
    stdscr = curses.initscr()

    # set settings to make more user/dev friendly
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.wrapper(spaceMain)

    # return terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    # close curses, return to regular terminal
    curses.endwin()
