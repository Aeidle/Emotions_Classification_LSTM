import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, bg, fg, text, corner_radius, padding, width, height, command=None, *args, **kwargs):
        tk.Canvas.__init__(self, parent, bg=bg, highlightthickness=0, width=width, height=height, *args, **kwargs)
        
        self.corner_radius = corner_radius
        self.padding = padding
        self.command = command
        
        self.text = self.create_text(padding, padding, anchor=tk.NW, fill=fg, text=text, font=('Arial', 12))
        text_width = self.bbox(self.text)[2] - self.bbox(self.text)[0]
        text_height = self.bbox(self.text)[3] - self.bbox(self.text)[1]
        
        width = text_width + 2*padding
        height = text_height + 2*padding
        
        self.create_rounded_rect(0, 0, width, height, corner_radius, fill=bg, outline=fg)
        
        self.bind("<Button-1>", self._on_click)
        
    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1,
                  x1+r, y1,
                  x2-r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1+r,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True, tags='button')
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
