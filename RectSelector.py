# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:31:09 2020

@author: Josh Levitt
From https://matplotlib.org/examples/widgets/rectangle_selector.html
"""

from __future__ import print_function
"""
Do a mouseclick somewhere, move the mouse to some destination, release
the button.  This class gives click- and release-events and also draws
a line or a box from the click-point to the actual mouseposition
(within the same axes) until the button is released.  Within the
method 'self.ignore()' it is checked whether the button from eventpress
and eventrelease are the same.

"""
from matplotlib.widgets import RectangleSelector, AxesWidget
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import lines

# adapted from https://stackoverflow.com/questions/34517484/persistent-rectangle-selector
class PersistRectangleSelector(RectangleSelector):
    #Taken from matplotlib source code
    def release(self, event):
        """on button release event"""
        if self.eventpress is None or self.ignore(event):
            return
        # make the box/line invisible again
        self.to_draw.set_visible(True) # this is the key line I changed: False --> True. Basically makes the rectangle stay instead of disappearing
        self.canvas.draw()
        # release coordinates, button, ...
        self.eventrelease = event

        if self.spancoords == 'data':
            xmin, ymin = self.eventpress.xdata, self.eventpress.ydata
            xmax, ymax = self.eventrelease.xdata, self.eventrelease.ydata
            # calculate dimensions of box or line get values in the right
            # order
        elif self.spancoords == 'pixels':
            xmin, ymin = self.eventpress.x, self.eventpress.y
            xmax, ymax = self.eventrelease.x, self.eventrelease.y
        else:
            raise ValueError('spancoords must be "data" or "pixels"')

        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin

        spanx = xmax - xmin
        spany = ymax - ymin
        xproblems = self.minspanx is not None and spanx < self.minspanx
        yproblems = self.minspany is not None and spany < self.minspany

        if (((self.drawtype == 'box') or (self.drawtype == 'line')) and
                (xproblems or yproblems)):
            # check if drawn distance (if it exists) is not too small in
            # neither x nor y-direction
            return

        self.onselect(self.eventpress, self.eventrelease)
                                              # call desired function 
        self.eventpress = None                # reset the variables to their
        self.eventrelease = None              # inital values
        return False
        
    # I copied a bunch of these functions directly from my matplotlib source folder for debugging purposes. basically they 
    # make the rectangle selector work properly
        
    def __init__(self, ax, onselect, drawtype='box',
                 minspanx=None, minspany=None, useblit=False,
                 lineprops=None, rectprops=None, spancoords='data',
                 button=None):

        """
        Create a selector in *ax*.  When a selection is made, clear
        the span and call onselect with::

          onselect(pos_1, pos_2)

        and clear the drawn box/line. The ``pos_1`` and ``pos_2`` are
        arrays of length 2 containing the x- and y-coordinate.

        If *minspanx* is not *None* then events smaller than *minspanx*
        in x direction are ignored (it's the same for y).

        The rectangle is drawn with *rectprops*; default::

          rectprops = dict(facecolor='red', edgecolor = 'black',
                           alpha=0.5, fill=False)

        The line is drawn with *lineprops*; default::

          lineprops = dict(color='black', linestyle='-',
                           linewidth = 2, alpha=0.5)

        Use *drawtype* if you want the mouse to draw a line,
        a box or nothing between click and actual position by setting

        ``drawtype = 'line'``, ``drawtype='box'`` or ``drawtype = 'none'``.

        *spancoords* is one of 'data' or 'pixels'.  If 'data', *minspanx*
        and *minspanx* will be interpreted in the same coordinates as
        the x and y axis. If 'pixels', they are in pixels.

        *button* is a list of integers indicating which mouse buttons should
        be used for rectangle selection.  You can also specify a single
        integer if only a single button is desired.  Default is *None*,
        which does not limit which button can be used.

        Note, typically:
         1 = left mouse button
         2 = center mouse button (scroll wheel)
         3 = right mouse button
        """
        AxesWidget.__init__(self, ax)

        self.visible = True
        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('button_press_event', self.press)
        self.connect_event('button_release_event', self.release)
        self.connect_event('draw_event', self.update_background)

        self.active = True                    # for activation / deactivation
        self.to_draw = None
        self.background = None

        if drawtype == 'none':
            drawtype = 'line'                        # draw a line but make it
            self.visible = False                     # invisible

        if drawtype == 'box':
            if rectprops is None:
                rectprops = dict(facecolor='white', edgecolor='black',
                                 alpha=0.5, fill=False)
            self.rectprops = rectprops
            self.to_draw = patches.Rectangle((0, 0),
                                     0, 1, visible=False, **self.rectprops)
            self.ax.add_patch(self.to_draw)
        if drawtype == 'line':
            if lineprops is None:
                lineprops = dict(color='black', linestyle='-',
                                 linewidth=2, alpha=0.5)
            self.lineprops = lineprops
            self.to_draw = lines.Line2D([0, 0], [0, 0], visible=False,
                                  **self.lineprops)
            self.ax.add_line(self.to_draw)

        self.onselect = onselect
        self.useblit = useblit and self.canvas.supports_blit
        self.minspanx = minspanx
        self.minspany = minspany

        if button is None or isinstance(button, list):
            self.validButtons = button
        elif isinstance(button, int):
            self.validButtons = [button]

        assert(spancoords in ('data', 'pixels'))

        self.spancoords = spancoords
        self.drawtype = drawtype
        # will save the data (position at mouseclick)
        self.eventpress = None
        # will save the data (pos. at mouserelease)
        self.eventrelease = None
        
    def update(self):
        """draw using newfangled blit or oldfangled draw depending on
        useblit

        """
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.to_draw)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False

    def onmove(self, event):
        """on motion notify event if box/line is wanted"""
        if self.eventpress is None or self.ignore(event):
            return
        x, y = event.xdata, event.ydata             # actual position (with
                                                   #   (button still pressed)
        
        if self.drawtype == 'box':
            minx, maxx = self.eventpress.xdata, x  # click-x and actual mouse-x
            miny, maxy = self.eventpress.ydata, y  # click-y and actual mouse-y
            if minx > maxx:
                minx, maxx = maxx, minx  # get them in the right order
            if miny > maxy:
                miny, maxy = maxy, miny
            self.to_draw.set_x(minx)             # set lower left of box
            self.to_draw.set_y(miny)
            self.to_draw.set_width(maxx - minx)  # set width and height of box
            self.to_draw.set_height(maxy - miny)
            self.update()
            self.canvas.draw() # I added this line. it fixes some bugs, but slows performance :/ -Josh
            return False
        if self.drawtype == 'line':
            self.to_draw.set_data([self.eventpress.xdata, x],
                                  [self.eventpress.ydata, y])
            self.update()
            return False
            
    def update_background(self, event):
        """force an update of the background"""
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)


def line_select_callback(eclick, erelease, parent = None):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    print("%3.2f --> %3.2f" % (x1, x2))
    if parent: # set coords field in our ui
        parent.Coords = (x1, y1, x2, y2)


#unused function
def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

'''
fig, current_ax = plt.subplots()                 # make a new plotting range
N = 100000                                       # If N is large one can see
x = np.linspace(0.0, 10.0, N)                    # improvement by use blitting!

plt.plot(x, +np.sin(.2*np.pi*x), lw=3.5, c='b', alpha=.7)  # plot something
plt.plot(x, +np.cos(.2*np.pi*x), lw=3.5, c='r', alpha=.5)
plt.plot(x, -np.sin(.2*np.pi*x), lw=3.5, c='g', alpha=.3)

print("\n      click  -->  release")

# drawtype is 'box' or 'line' or 'none'
toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels')
plt.connect('key_press_event', toggle_selector)
plt.show()
'''