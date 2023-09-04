from tkinter import *
from tkinter import filedialog 
from tkinter import messagebox
import random

class MineSweeperCell(Label):
    '''represents a MineSweeper cell'''

    def __init__(self, master, coord):
        '''MineSweeperCell(master, coord) -> MineSweeperCell
        creates a new blank MineSweeperCell with (row, column) coord'''
        Label.__init__(self, master, height=1, width=2,text='', \
                       bg='white', font=('Arial', 24))
        self.coord = coord  # (row, column) coordinate tuple
        self.number = 0  # 0 represents an empty cell
        self.Flag = False     # starts as changeable
        self.revealed = False  # starts hidden
        self["relief"] = RAISED 
        self["borderwidth"] = 3
        # set up listeners
        self.bind('<Button-1>', master.show)
        self.bind('<Button-2>', master.Place_Flag)

    def update_display(self):
        '''MineSweeperCell.update_display()
        displays the number in the cell
        displays as:
          empty if its value is 0
          a number if there are mines near the square
          B if the square itself is a mine (self.number = 9)
          F if the player had marked it accordingly'''
        if self.revealed == True:
            self["relief"] = SUNKEN
            self["bg"] = "grey90"
            if self.number == 0:  # cell is empty
                self['text'] = ""
            elif self.number == 9: # cell is a mine
                self["text"] = "B"
                self["fg"] = "orange"
            else:  # cell has a number
                self['text'] = str(self.number)  # display the number
                # set the color
                colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
                self["fg"] = colormap[self.number]
        else: #Square is still hidden           
            if self.Flag == True: #Cell has flag
                self["text"] = "F" 
                self["fg"] = "black"
            else: 
                self["text"] = ""

    def get_coord(self):
        '''MineSweeperCell.get_coord() -> tuple
        returns the (row, column) coordinate of the cell'''
        return self.coord

    def get_number(self):
        '''MineSweeperCell.get_number() -> int
        returns the number in the cell (0 if no mines near, 9 if mine)'''
        return self.number

    def is_Flagged(self):
        '''MineSweeperCell.isFlagged() -> boolean
        returns True if the cell is Flagged False if not'''
        return self.Flag

    def is_revealed(self):
        '''MineSweeperCell.is_revealed() -> boolean
        returns True if the cell is clicked on and is revealed, False if not'''
        return self.revealed

    def set_number(self, number, Flag=False):
        '''MineSweeperCell.set_number(number, Flag (optional))
        sets the number in the cell 
        Flag=True sets the cell to have a Flag'''
        self.number = number
        self.Flag = Flag
        self.hide()  # hide the cell after setting it

    def hide(self):
        '''MineSweeperCell.hide()
        hides a cell'''
        if not self.revealed:
            self.revealed = False
    
    def is_mine(self):
        '''MineSweeperCell.is_mine() -> boolean
        True of the cell is a mine'''
        return self.number == 9

class MineSweeperGrid(Frame):
    '''object for a MineSweeper grid'''

    def __init__(self, master, width, height, numBombs):
        '''MineSweeperGrid(master, width, height, numBombs)
        creates a new blank MineSweeper grid'''
        # initialize a new Frame
        Frame.__init__(self, master, bg='black')
        self.grid()
        
        #Defining attributes
        self.height = height 
        self.width = width
        self.mines = numBombs
        self.lose = False #This is to check if the player has lost or not

        # create labels
        self.mineLabel = Label(self,text=str(self.mines),font=('Arial',18)) #New Label for the mine counter
        self.mineLabel.grid(row=100,column=0,columnspan=100) 
        #We just want the counter to be as low as possible, no matter the grid size. 
        
        # create the cells
        self.cells = {}
        for row in range(height):
            for column in range(width):
                coord = (row, column)
                self.cells[coord] = MineSweeperCell(self, coord)
                # cells go in even-numbered rows/columns of the grid
                self.cells[coord].grid(row=2*row, column=2*column)

        self.generate_mines() #Method made from top-down programming, this adds all the mines or "9"

        #Adding numbers 1-8
        for box in self.cells: 
            coord = box
            adjecent = list(coord) #we make a temporary list of the coord so we can change it
            counter = 0 #Counter to count all the mines
            if self.cells[coord].get_number() == 0: #Square shouldn't be a mine
                if coord[0] > 0: #If square is not on top
                    adjecent[0] = adjecent[0] - 1
                    if self.cells[tuple(adjecent)].get_number() == 9: 
                        counter = counter + 1 #checking square above
                    adjecent[1] = adjecent[1] - 1
                    if coord[1] > 0:#If square is not on left side
                        if self.cells[tuple(adjecent)].get_number() == 9: 
                            counter = counter + 1 #checking square on top left
                    adjecent[1] = adjecent[1] + 2
                    if coord[1] < self.width-1: #If square is not on right side
                        if self.cells[tuple(adjecent)].get_number() == 9:
                            counter = counter + 1 #checking square on top right
                        
                adjecent = list(coord) #Reseting our list
                if coord[0] < self.height-1: #If square is not on the bottom
                    adjecent[0] = adjecent[0] + 1
                    if self.cells[tuple(adjecent)].get_number() == 9:
                        counter = counter + 1 #checking square below
                    adjecent[1] = adjecent[1] - 1
                    if coord[1] > 0: #If square is not on left side
                        if self.cells[tuple(adjecent)].get_number() == 9:
                            counter = counter + 1 #checking square bottom left
                    adjecent[1] = adjecent[1] + 2
                    if coord[1] < self.width-1: #If square is not on right side
                        if self.cells[tuple(adjecent)].get_number() == 9:
                            counter = counter + 1 #checking square bottom right

                adjecent = list(coord) #resetting again
                adjecent[1] = adjecent[1] - 1
                if coord[1] > 0: # if square is not on left side
                    if self.cells[tuple(adjecent)].get_number() == 9:
                            counter = counter + 1 #checking square on left
                
                adjecent[1] = adjecent[1] + 2
                if coord[1] < self.width-1: #If square is on right side
                    if self.cells[tuple(adjecent)].get_number() == 9:
                            counter = counter + 1 #checking square on right
                        
                self.cells[coord].set_number(counter) #We finally set the number on our square to be the counter
        while True: #This picks and marks a random "safe" square with an "X" at the start of the game, to prevent first click deaths
            xbombcor = random.randint(1, self.width-2)
            ybombcor = random.randint(1, self.height-2)
            coord = (ybombcor, xbombcor)
            if self.cells[coord].get_number() == 0:
                self.cells[coord]["fg"] = "lime"
                self.cells[coord]["text"] = "X"
                break

    def show(self, event):
        '''MineSweeperGrid.show(event)
        event handler for mouse left click
        Reveals a square'''
        coords = event.widget.get_coord()
        if not self.cells[coords].Flag: #Nothing happens if the square is Flagged. 
            self.show_coord(coords)     
        if self.check_win() == True: #Checks for a win 
            messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

    def Place_Flag(self, event):
        '''event handler for mouse click
        Places a flag on a square'''

        # only act if the cell is editable and highlighted
        coords = event.widget.get_coord()
        if not self.cells[coords].is_revealed(): #square must be hidden
            if self.cells[coords].Flag: #If statements for the "toggle"
                self.cells[coords].Flag = False
                self.mines = self.mines + 1 #Changing the number of mines
            else:
                self.cells[coords].Flag = True
                self.mines = self.mines - 1 #Lowers the mine counter when a min is "accounted for"
            self.mineLabel["text"] = str(self.mines) #Editing the "mine counter" accordingly
            self.cells[coords].update_display()     

    def check_win(self):
        '''MineSweeperGrid.check_win() -> Boolean
        Returns True if player has won and False if not yet.'''
        win = True #Make the variable True for now
        for coord in self.cells:
            if self.cells[coord].get_number() != 9: 
                if not self.cells[coord].is_revealed(): #Once ANY square that is hidden and not a mine if found,
                    win = False #The player has not won yet.
        return win

    def show_coord(self, coord):
        '''MineSweeperGrid.show_coord(coord)
        reveals the square, with some added functions'''
        coords = tuple(coord) #makes sure the method can handle both list and tuple inputs
        if self.cells[coords].revealed == False: #Makes sure the square has not been already revealed
            self.cells[coords].revealed = True
            self.cells[coords].update_display() #reveals and updates display
            number = self.cells[coords].get_number()
            if number == 0: #If we get a zero, all surronding squares must be revealed.
                adjecent = list(coords) #like the technique done in our _init_ method, we make a temporary list
                if self.cells[coords].get_number() == 0:
                    if coords[0] > 0:
                        adjecent[0] = adjecent[0] - 1
                        self.show_coord(adjecent) #shows square on top
                        adjecent[1] = adjecent[1] - 1
                        if coords[1] > 0:
                            self.show_coord(adjecent) #shows square on top left
                        adjecent[1] = adjecent[1] + 2
                        if coords[1] < self.width-1:
                            self.show_coord(adjecent) #shows square on top right

                    adjecent = list(coords) #reset
                    if coords[0] < self.height-1:
                        adjecent[0] = adjecent[0] + 1 
                        self.show_coord(adjecent) #shows square on bottom
                        adjecent[1] = adjecent[1] - 1
                        if coords[1] > 0:
                            self.show_coord(adjecent) #shows square on bottom left
                        adjecent[1] = adjecent[1] + 2
                        if coords[1] < self.width-1:
                            self.show_coord(adjecent) #shows square on bottom right
                        
                    adjecent = list(coords) #reset
                    adjecent[1] = adjecent[1] - 1
                    if coords[1] > 0:
                        self.show_coord(adjecent) #shows square on left
                    adjecent[1] = adjecent[1] + 2
                    if coords[1] < self.width-1:
                        self.show_coord(adjecent) #shows square on right
            elif self.cells[coords].is_mine(): #if the square was a mine...
                self.boom() #...that takes us to our lose function

    def generate_mines(self):
        '''MineSweeperGrid.generate_mines()
        Generates mines for the start of the game'''
        minesmade = 0 #records the mines made
        while minesmade < self.mines: #This loop breaks once the miens made matches the # of mines requested
            xbombcor = random.randint(0, self.width-1)
            ybombcor = random.randint(0, self.height-1)
            coord = (ybombcor, xbombcor) #random coordinate
            if self.cells[coord].get_number() == 0:
                self.cells[coord].set_number(9) #places mine if the square does not have a mine yet
                minesmade = minesmade + 1 

    def boom(self):
        '''MineSweeperGrid.boom()
        simulates a loss'''
        if self.lose == False:
            messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        self.lose = True #Confirms the player has lost and has seen the message already
        #self.lose is meant to prevent the player from getting the same message over and over as a result of the recursive function
        for coord in self.cells: #revealing all mines
            if self.cells[coord].get_number() == 9:
                self.show_coord(coord)
                self.cells[coord]["bg"] = "red"
            

# main loop for the game
def play_minesweeper(width,height,numBombs):
    '''minesweeper()
    plays minesweeper'''
    root = Tk()
    root.title('MineSweeper')
    sg = MineSweeperGrid(root, width, height, numBombs)
    root.mainloop()

play_minesweeper(25,20,75)
#20,20,50 is my favourite combination
#40,22,250 max
