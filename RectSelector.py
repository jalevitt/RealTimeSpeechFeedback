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
from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches


# adapted from https://stackoverflow.com/questions/34517484/persistent-rectangle-selector
class PersistRectangleSelector(RectangleSelector):
    #Taken from matplotlib source code
    def release(self, event):
        """on button release event"""
        if self.eventpress is None or self.ignore(event):
            return
        # make the box/line invisible again
        self.to_draw.set_visible(True)
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


def line_select_callback(eclick, erelease, parent = None):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    print("%3.2f --> %3.2f" % (x1, x2))
    if parent:
        parent.Coords = (x1, y1, x2, y2)



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