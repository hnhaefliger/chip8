import tkinter as tk

class Display:
    cols = 64
    rows = 32
    scale = 15

    pixels = [0b0 for i in range(cols * rows)]

    root = tk.Tk()
    root.geometry(f'{cols*scale}x{rows*scale}')

    canvas = tk.Canvas(root, width=cols*scale, height=rows*scale)

    canvas.pack()

    def __init__(self):
        self.shapes = [
            self.canvas.create_rectangle(x*self.scale, y*self.scale, (x+1)*self.scale, (y+1)*self.scale, fill='black')
            for y in range(self.rows)
            for x in range(self.cols)
        ]

    def mainloop(self):
        self.paint()
        self.root.after(1, self.mainloop)

    def set_pixel(self, x, y):
        self.pixels[y * self.cols + x] ^= 1

        return not(self.pixels[y * self.cols + x])

    def clear(self):
        self.pixels = [0b0 for i in range(self.cols * self.rows)]


    def paint(self):
        for x in range(self.cols):
            for y in range(self.rows):
                self.canvas.itemconfig(self.shapes[y * self.cols + x], fill='white' if self.pixels[y * self.cols + x] else 'black')


    def draw(self, x, y, height):
        collision = False

        for x in range(x, x+8):
            for y in range(y, y+height):
                if self.set_pixel(x, y):
                    collision = True

        return collision
