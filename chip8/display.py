import tkinter as tk

keymap = {
    '1': 0x1,
    '2': 0x2,
    '3': 0x3,
    '4': 0xC,
    'q': 0x4,
    'w': 0x5,
    'e': 0x6,
    'r': 0xD,
    'a': 0x7,
    's': 0x8,
    'd': 0x9,
    'f': 0xE,
    'z': 0xA,
    'x': 0x0,
    'c': 0xB,
    'v': 0xF,
}

class Display:
    cols = 64
    rows = 32
    scale = 15

    pixels = [0b0 for i in range(cols * rows)]

    root = tk.Tk()
    root.geometry(f'{cols*scale}x{rows*scale}')

    canvas = tk.Canvas(root, width=cols*scale, height=rows*scale)

    canvas.pack()

    def __init__(self, keyboard):
        self.shapes = [
            self.canvas.create_rectangle(x*self.scale, y*self.scale, (x+1)*self.scale, (y+1)*self.scale, fill='black')
            for y in range(self.rows)
            for x in range(self.cols)
        ]

        self.keyboard = keyboard
        self.root.bind('<KeyPress>', self.keypress)
        self.root.bind('<KeyRelease>', self.keyrelease)

    def keypress(self, event):
        self.keyboard(keymap[event.keysym], True)

    def keyrelease(self, event):
        self.keyboard(keymap[event.keysym], False)

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
