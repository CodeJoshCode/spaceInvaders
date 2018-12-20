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

    def show(self,win):
        """show the spaceship in the window"""
        win.erase()

        if(self.currentBullet != None):
            if(self.currentBullet.yPos > 0):
                for x in range(bulletSpeed):
                    self.currentBullet.yPos -= 1
                    # check for collision in enemy array, respond by destroying both bullet and enemy
                    # add points to score on enemy destruction
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



def spaceMain(stdscr):
    curses.curs_set(0) # set invisible cursor
    begin_y = 0
    begin_x = 0
    win = curses.newwin(height, width, begin_y, begin_x) # init window
    win.nodelay(True) # getch() does not block the program
    spaceShip = SpaceShip() #init the space ship
    spaceShip.show(win) #show the space ship

    key = ''
    while key != ord('q'):
        key = win.getch()
        spaceShip.move(key)
        spaceShip.show(win)
        # check for loss via spaceship collision
        # check for win via elimination of enemy array
        time.sleep(.05)


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
