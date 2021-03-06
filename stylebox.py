#!env/bin/python

import abc # abstract base class
import numpy as np

from overrides import overrides

def rescale(x, from_lo, from_hi, to_lo, to_hi):
    # y = yi + (yf-yi)/(xf-xi)*(x-xi)
    y = to_lo + (to_hi-to_lo)/(from_hi-from_lo)*(x-from_lo)
    return y


class Scatter:
    def __init__(self, x_domain=[-np.inf, np.inf], y_domain=[-np.inf, np.inf]):
        
        if not(len(x_domain) == len(y_domain) == 2):
            raise ValueError
        
        self.x_domain = x_domain
        self.y_domain = y_domain
        
        x_lo, x_hi = x_domain
        y_lo, y_hi = y_domain
        
        self.x_lo, self.x_hi = x_domain
        self.y_lo, self.y_hi = y_domain
        
        self.x_range = x_hi-x_lo
        self.y_range = y_hi-y_lo
        
        self.x = []
        self.y = []
        
    
    def add_point(self, x: float, y: float) -> bool:
        in_range = (self.x_lo <= x <= self.x_hi) and (self.y_lo <= y <= self.y_hi)
        if in_range:
            self.x.append(x)
            self.y.append(y)
        
        return in_range


class StyleBox(Scatter):
    
    def set_gridlines(self, nx:int, ny:int=None):
        
        ny = nx if ny is None else ny
        
        # make sure `nx`, `ny` are non-negative
        nx, ny = max(0, nx), max(0, ny)
        # TODO handle case when domain is (semi) infinite
        dx, dy = self.x_range/(nx+1), self.y_range/(ny+1)
        
        # generate a list of coordinates for the gridlines
        xi = np.arange(self.x_lo + dx, self.x_hi, dx) # x-coords, vertical gridlines
        yi = np.arange(self.y_lo + dy, self.y_hi, dy) # y-coords, horizontal gridlines
        
        self.grid_xi, self.grid_yi = list(xi), list(yi)


class StyleBoxBuilder(metaclass=abc.ABCMeta):
    
    def __init__(self, x_domain, y_domain, size, color='None'):
        self.size = size
        self.color = color
        self.stylebox = StyleBox(x_domain, y_domain)
    
    def grid(self, nx: int, ny: int):
        # SVG box size is always 300
        self.stylebox.set_gridlines(nx, ny)
        return self
    
    def point(self, x: float, y: float):
        # SVG box size is always 300
        self.stylebox.add_point(x, y)
        return self
    
    @abc.abstractmethod
    def build(self):
        pass


class SVGStyleBoxBuilder(StyleBoxBuilder):
    
    VERT_GRIDLINE_TEMPLATE = '<path id="vgridline-{vid}" d="m{x:.3f} 0.0v300"/>\n' # SVG box size is always 300
    HORZ_GRIDLINE_TEMPLATE = '<path id="hgridline-{hid}" d="m0.0 {y:.3f}h300"/>\n' # SVG box size is always 300
    
    CIRC_TEMPLATE = '<circle id="{pid}" cx="{x:.3f}" cy="{y:.3f}" r="15" fill="{color}"/>\n' # Circle radius is always 15
    
    
    def x_to_box_coords(self, x):
        return rescale(x, self.stylebox.x_lo, self.stylebox.x_hi, 0.0, 300.0)
    
    def y_to_box_coords(self, y):
        return rescale(y, self.stylebox.y_lo, self.stylebox.y_hi, 0.0, 300.0)
        
    def build(self):
        
        # Concatenate gridline <path /> statements
        vert = '\n'.join([self.VERT_GRIDLINE_TEMPLATE.format(vid=vid, x=self.x_to_box_coords(x)) \
                            for vid,x in enumerate(self.stylebox.grid_xi)])
        horz = '\n'.join([self.HORZ_GRIDLINE_TEMPLATE.format(hid=hid, y=self.y_to_box_coords(y)) \
                            for hid,y in enumerate(self.stylebox.grid_yi)])
        
        # Group all gridlines
        self.grid = '<g id="gridlines">\n' + vert + horz + '</g>\n'
        
        self.axes = '<rect id="axes" stroke-opacity="1.0" height="297.50" width="297.50" y="2.5" x="2.5"/>\n'
        
        points = '\n'.join([self.CIRC_TEMPLATE.format(pid=pid, x=self.x_to_box_coords(x), y=self.y_to_box_coords(y), color=self.color) \
            for pid,x,y in zip(range(len(self.stylebox.x)), self.stylebox.x, self.stylebox.y)])
        self.points = '<g id="points">\n' + points + '</g>\n'
        
        self.box = '<g id="box" stroke="{color}" stroke-width="5" fill="none">\n'.format(color=self.color) + \
                   self.axes + self.grid + self.points + '</g>\n'
        
        self.layer = '<g id="layer1">\n' + self.box + '</g>\n'
        
        self.svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg id="svg2" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.w3.org/2000/svg" height="{size}" width="{size}" version="1.1" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" viewBox="0 0 302.5 302.5">\n""".format(size=self.size) + self.layer + '</svg>\n'
        
        return self.svg


class HTMLStyleBoxBuilder(StyleBoxBuilder):

    HTML_TEMPLATE = """
    <div class="stylebox" style="position: relative; width: 50px; height: 50px;">
        <table class="grid" style="position: absolute; border-collapse: collapse; border-color:#000000; overflow:hidden; width:50px; height:50px; border: 1px;">
            <tr>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
            </tr>
            <tr>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
            </tr>
            <tr>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
                <td class="cell" style="border-style:solid; padding: 0px; margin: 0px;"></td>
            </tr>
        </table>
        <div class="circle" style="position: absolute; width: 10px; height: 10px; background-color: black; border-radius: 50%; left: {x}%; top: {y}%; transform: translate(-50%, -50%);"/>
    <div>
"""

    def x_to_box_coords(self, x):
        return rescale(x, self.stylebox.x_lo, self.stylebox.x_hi, 0.0, 100.0)
    
    def y_to_box_coords(self, y):
        return rescale(y, self.stylebox.y_lo, self.stylebox.y_hi, 0.0, 100.0)
    
    def build(self):
        # TODO make use of all points
        return self.HTML_TEMPLATE.format(x=self.x_to_box_coords(self.stylebox.x[-1]), y=self.y_to_box_coords(self.stylebox.y[-1]))


class PNGStyleBoxBuilder(StyleBoxBuilder):
    pass


class ASCIIStyleBoxBuilder(StyleBoxBuilder):

    def x_to_box_coords(self, x):
        return round(rescale(x, self.stylebox.x_lo, self.stylebox.x_hi, 0.0, self.size-1))
    
    def y_to_box_coords(self, y):
        return round(rescale(y, self.stylebox.y_lo, self.stylebox.y_hi, 0.0, self.size-1))
    
    @overrides
    def grid(self, nx:int, ny:int=None):
        # N gridlines are possible only if size-1 is divisible by N+1.
        # e.g. for 1 gridline, (size-1) must be divisible by 2
        #      for 2 gridlines, (size-1) must be divisible by 3
        
        nx = nx if ((self.size-1) % (nx+1))==0 else 0
        if ny is None:
            ny = nx
        else:
            ny = ny if ((self.size-1) % (ny+1))==0 else 0
        
        # make sure `nx`, `ny` are non-negative
        nx, ny = max(0, nx), max(0, ny)
        
        xi = np.arange(0,self.size,self.size//(nx+1))[1:-1]
        yi = np.arange(0,self.size,self.size//(ny+1))[1:-1]
        
        self.stylebox.grid_xi, self.stylebox.grid_yi = list(xi), list(yi)
        
        return self

    def build(self):
    
        # Generate the "wireframe"
        top = ['┌'] + ['─']*(self.size-2) + ['┐']
        sides = ['│'] + [' ']*(self.size-2) + ['│']
        bottom = ['└'] + ['─']*(self.size-2) + ['┘']
        
        box = [sides.copy() for i in range(self.size-2)]
        box.insert(0, top)
        box.append(bottom)
        
        # Add gridlines
        for ix in self.stylebox.grid_xi:
            box[0][ix] = '┬' # top
            box[-1][ix] = '┴' # bottom
            
            for iy in range(1, self.size-1):
                box[iy][ix] = '│'
        
        for iy in self.stylebox.grid_yi:
            box[iy][0] = '├'
            box[iy][-1] = '┤'
            
            for ix in range(1, self.size-1):
                box[iy][ix] = '─' #if ix not in self.stylebox.grid_xi else '┼'
        
        for ix in self.stylebox.grid_xi:
            for iy in self.stylebox.grid_yi:
                box[iy][ix] = '┼'
            
        
        # Add point
        if len(self.stylebox.x):
            ix = self.x_to_box_coords(self.stylebox.x[-1])
            iy = self.y_to_box_coords(self.stylebox.y[-1])
            box[iy][ix] = '*'
        
        return '\n'.join([''.join(line) for line in box])
        

class StyleBoxBuilderDirector:
    pass

#with open("/tmp/direct.svg", "w") as svg_file:
#    svg_file.write(SVGStyleBoxBuilder([0, 1], [0, 1], size=50, color="#000000").grid(2,2).point(0.5,0.5).point(0.5,0.4).point(0.4,0.5).build())

#print(ASCIIStyleBoxBuilder([0,1],[0,1], size=7).grid(1).point(0.25,0.75).build())
