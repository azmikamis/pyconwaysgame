import itertools
from Tkinter import Tk, Label, Frame, Button, BOTTOM, LEFT

class Board(object):
    def __init__(self, parent, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.cells = []
        self.livecells = set()
        self.createcells(parent)

    def createcells(self, parent):
        for column in range(self.sizex):
            rowcells = []
            for row in range(self.sizey):
                cell = Label(parent, relief="raised", width=2,
                          borderwidth=1, bg="white")
                cell.grid(row=row, column=column)
                cell.bind("<Button-1>", self.toggle)
                rowcells.append(cell)
            self.cells.append(rowcells)

    def toggle(self, event):
        grid_info = event.widget.grid_info()
        col = int(grid_info["column"])
        row = int(grid_info["row"])
        if (col, row) in self.livecells:
            self.livecells.remove((col, row))
            self.colourcells([(col, row)], "white")
        else:
            self.livecells.add((col, row))
            self.colourcells([(col, row)], "black")

    def advance(self, livecells=None):
        if livecells is not None:
            self.livecells = livecells
            self.colourcells(self.livecells, "black")
        else:
            self.colourcells(self.livecells, "white")
            newlivecells = set()
            recalc = self.livecells | \
                     set(
                        itertools.chain(
                            *map(self.neighbours, self.livecells)
                        )
                     )
            for point in recalc:
                count = sum(
                            (neighbour in self.livecells)
                            for neighbour in self.neighbours(point)
                        )
                if count == 3 or (count == 2 and point in self.livecells):
                    newlivecells.add(point)
            self.livecells = newlivecells
            self.colourcells(self.livecells, "black")

    def neighbours(self, point):
        col, row = point

        leftcol = (col == 0 and [self.sizex-1] or [col-1])[0]
        rightcol = (col == self.sizex-1 and [0] or [col+1])[0]

        toprow = (row == 0 and [self.sizey-1] or [row-1])[0]
        bottomrow = (row == self.sizey-1 and [0] or [row+1])[0]

        yield rightcol, row
        yield leftcol, row
        yield col, bottomrow
        yield col, toprow
        yield rightcol, bottomrow
        yield rightcol, toprow
        yield leftcol, bottomrow
        yield leftcol, toprow

    def colourcells(self, cells, colour):
        for (col, row) in cells:
            self.cells[col][row]["bg"] = colour

    def clear(self):
        self.colourcells(self.livecells, "white")
        self.livecells.clear()

def main():
    root = Tk()
    frame = Frame(root)
    frame.pack()
    board = Board(frame, 25, 25)
    #blinker = set([(9, 11), (10, 11), (11, 11)])
    #glider = set([(10, 9), (11, 10), (9, 11), (10, 11), (11, 11)])
    #board.advance(glider)
    bottomframe = Frame(root)
    bottomframe.pack(side=BOTTOM)
    buttonstep = Button(bottomframe, text="Step", command=board.advance)
    buttonstep.pack(side=LEFT)
    buttonclear = Button(bottomframe, text="Clear", command=board.clear)
    buttonclear.pack(side=LEFT, after=buttonstep)
    root.mainloop()

if __name__ == "__main__":
    main()
