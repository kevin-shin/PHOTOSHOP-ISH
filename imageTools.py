"""=====================================================
imageTools.py

This is a modification/implementation of the functions and data types
from Mark Guzdial's Media Computation project, taken from the implementation
for Myro in C Python

Revision 2:  
* Some bug fixes
* Removed the alpha component of colors
* Added the ImageWindow class to let us handle displayed images a little better, now we can hide and reshow them. 
* Added the explore method and function, which opens the image in an external viewer, etc.
* Added a setAllPixels function that changes all pixels to be a single color

Revision 3: (Summer 2016)
A major change to simplify the form of things...
* Remove pixel objects and color objects. Colors are just tuples of (r, g, b) values, or color strings.
* Merge GraphicsObj class back into Picture, as Pixel and Color classes are going away
* Created PictureIterator class to allow looping over (x, y) coordinates in the image

"""

from __future__ import print_function

import sys
import math

versionInfo = sys.version_info[0]
if versionInfo >= 3:
    import tkinter as tk
    import tkinter.colorchooser as tkColorChooser
    import tkinter.filedialog as tkFileDialog
    import tkinter.simpledialog as tkSimpleDialog
else:
    import Tkinter as tk
    import tkColorChooser
    import tkFileDialog
try: 	 
    import PIL.Image as Image
    import PIL.ImageColor as ImageColor
    import PIL.ImageDraw as ImageDraw
    import PIL.ImageFont as ImageFont
    import PIL.ImageTk as ImageTk
except: 	 
    print("WARNING: PIL modules not found; you must install the Python Imaging Library", file=sys.stderr)


root = tk.Tk()
root.withdraw()


def globalUpdate():
    global root
    root.update_idletasks()
    root.update()


# ==============================================================

class Picture:
    """A picture object represents an image, keeping track of the size, source, and pixel values
    of an image"""
     
     
    def __init__(self, *args):
        """
        Takes one to three args to make a picture. Allows for any other number but raises an error.
        makePicture(filename) - reads picture from a file
        makePicture(width, height) - creates a new blank picture with given size and color white
        makePicture(width, height, color) - creates a new picture with given size and input color
        """
        self.width = 0
        self.height = 0
        self.image = None
        self.filename = '<none>'
        self.mode = "RGB"
        self.tkImage = None
        self.dispWindow = None
        self.drawObj = None
      
        if len(args) == 1:
            filename = args[0]
            if isinstance(filename, str):
                self.image = Image.open(filename)
                self.filename = filename
                self._configureImage()
            else:
                raise TypeError("Picture: single input must be a filename, given: " + str(filename))
        elif len(args) == 2:
            wid = args[0]
            hgt = args[1]
            try:
                self._checkNumeric(wid, "__init__")  # will raise an exception if values are not numeric
                self._checkNumeric(hgt, "__init__")
                self.width = wid
                self.height = hgt
                self.image = Image.new(self.mode, (wid, hgt), (255, 255, 255))
                self._configureImage()
            except TypeError:
                raise TypeError("Picture: two inputs must be numeric, given: " + str(wid) + " and " + str(hgt))
        elif len(args) == 3:
            wid = args[0]
            hgt = args[1]
            color = args[2]
            try:
                self._checkNumeric(wid, "__init__")  # will raise an exception if values are not numeric
                self._checkNumeric(hgt, "__init__")
            except TypeError:
                raise TypeError("Picture: first two inputs must be numeric, given: " + str(wid) + " and " + str(hgt))
            try:
                self._checkColor(color, "__init__")
            except TypeError:
                raise TypeError("Picture: third input must be a valid color, given: " + str(color))
            self.width = wid
            self.hgt = hgt
            self.image = Image.new(self.mode, (wid, hgt), color)
            self._configureImage()
        else:
            raise TypeError("Picture: wrong number of arguments (must take 1, 2, or 3 inputs)")
      

    def _configureImage(self):
        """ Assumes an Image object has been created in self.image, and sets the other instance
        variables appropriately."""
        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")
        self.pixels = self.image.load()
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        if self.pixels is None:
            raise RuntimeError("Picture: image loading failed")
   
   
    def copy(self):
        """Makes and returns a new picture that is a copy of this one."""
        newPic = Picture(self.width, self.height)
        newPic.filename = self.filename
        newPic.image = self.image.copy()
        newPic._configureImage()
        return newPic
      
      
    def setAllPixels(self, color):
        """Takes in a color and sets every pixel to have the input color."""
        if self._checkColor(color, "setAllPixels"):  # raises exception if color is invalid
            for (x, y) in self:
                self.setColor(x, y, color)
 
         
    def getWidth(self):
        """Returns the width of the image in the Picture"""
        return self.width
   
    def getHeight(self):
        """Returns the height of the image in the Picture"""
        return self.height


    def getColor(self, x, y):
        """Takes in the column (x) and row (y) position of a pixel, and returns the
        Color of the pixel at that location"""
        if self._checkRange(x, y, "getColor"):
            retval = self.pixels[x, y]
            return retval[:3]


    def setColor(self, x, y, newColor):
        """Given the (x, y) location of a pixel, and a new Color object, it changes
        the pixel at that location to have the new color.  No return value"""
        self._checkRange(x, y, "setColor")
        self._checkColor(newColor, "setColor")
        if isinstance(newColor, str):
            try:
                newColor = ImageColor.getrgb(newColor)
            except ValueError as vErr:
                raise ValueError("(Picture) setColor: " + str(vErr))
        else:
            newColor = tuple([self._convertRange(val) for val in newColor])
        self.pixels[x, y] = newColor


    def save(self, filename):
        """Given a string filename, write this picture to that file"""
        if isinstance(filename, str):
            self.image.save(filename)
        else:
            raise TypeError("(Picture) save: expected a string as input, giveN: " + str(filename))
      
      
    def show(self):
        """Create a Toplevel widget to display the picture, if one doesn't already exist,
        and display the picture data in it"""
        if self.dispWindow is None:
            self.dispWindow = ImageWindow(self.image, self.width, self.height, self.filename)
        else:
            self.dispWindow.update(self.image)


    def hide(self):
        """Close the window displaying this picture"""
        if self.dispWindow is None:
            return
        else:
            self.dispWindow.close()
         
      
    def explore(self):
        self.image.show()
      

    # -------------------------------------------------------
    # Drawing methods
   
    def drawLine(self, x0, y0, x1, y1, color=(0, 0, 0), width=1):
        """Draws a line from (x0, y0) to (x1, y1) of input color and width.
        Default values for color and width are black and one pixel wide."""
        # Check input types
        self._checkRange(x0, y0, "drawLine")
        self._checkRange(x1, y1, "drawLine")
        self._checkColor(color, "drawLine")
        self._checkNumeric(width, "drawLine")
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.line([(x0, y0), (x1, y1)], color, width)


    def drawRectangle(self, x0, y0, x1, y1, outlineColor=(0, 0, 0), fillColor=None):
        """Draws a rectangle (x0, y0) to (x1, y1) (excluding (x1, y1)) with a given outline
        color, and an optional fill color."""
        # Check input types
        self._checkRange(x0, y0, "drawRectangle")
        self._checkRange(x1, y1, "drawRectangle")
        self._checkColor(outlineColor, "drawRectangle")
        if not (fillColor is None):
            self._checkColor(fillColor, "drawRectangle")
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.rectangle([(x0, y0), (x1, y1)], fillColor, outlineColor)


    def drawOval(self, x0, y0, x1, y1, outlineColor=(0, 0, 0), fillColor=None):
        """Draws an oval/ellipse inside a bounding rectangle with corners
        (x0, y0) to (x1, y1) (excluding (x1, y1)) with a given outline
        color, and an optional fill color."""
        # Check input types
        self._checkRange(x0, y0, "drawOval")
        self._checkRange(x1, y1, "drawOval")
        self._checkColor(outlineColor, "drawOval")
        if not (fillColor is None):
            self._checkColor(fillColor, "drawOval")
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.ellipse([(x0, y0), (x1, y1)], fillColor, outlineColor)

  
    def drawArc(self, x0, y0, x1, y1, startAngle=0, endAngle=180, style='arc', outlineColor=(0, 0, 0), fillColor=None):
        """Draws an arc, a chord inside a bounding rectangle with corners
        (x0, y0) to (x1, y1) (excluding (x1, y1)) It starts with startAngle and ends with endAngle,
        and has an optional fill color. Note that 3 o'clock is 0 degrees, and degrees increase clockwise."""
        # Check input types
        self._checkRange(x0, y0, "drawArc")
        self._checkRange(x1, y1, "drawArc")
        self._checkNumeric(startAngle, "drawArc")
        self._checkNumeric(endAngle, "drawArc")
        self._checkColor(outlineColor, "drawArc")
        if not (fillColor is None):
            self._checkColor(fillColor, "drawArc")
        if not isinstance(style, str):
            raise TypeError("(Picture) drawArc: style must be a string ('arc', 'chord', or 'pie'), given: " + str(style))
        if style not in {'arc', 'chord', 'pie'}:
            raise ValueError("(Picture) drawArc: style must be one of 'arc', 'chord', or 'pie', given: " + str(style))
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        if style == 'arc':
            self.drawObj.arc([(x0, y0), (x1, y1)], startAngle, endAngle, outlineColor)
        elif style == 'chord':
            self.drawObj.chord([(x0, y0), (x1, y1)], startAngle, endAngle, fillColor, outlineColor)
        elif style == 'pie':
            self.drawObj.pieslice([(x0, y0), (x1, y1)], startAngle, endAngle, fillColor, outlineColor)


    def drawPolygon(self, pointList, outlineColor=(0, 0, 0), fillColor=None):
        """Draws a closed polygon given a list of points, with an input
        outline color and optional fill color."""
        # Check input types
        if isinstance(pointList[0], tuple):
            for (x, y) in pointList:
                self._checkRange(x, y, "drawPolygon")
        else:
            for i in range(0, len(pointList) - 1, 2):
                x = pointList[i]
                y = pointList[i+1]
                self._checkRange(x, y, "drawPolygon")
        self._checkColor(outlineColor, "drawPolygon")
        if not (fillColor is None):
            self._checkColor(fillColor, "drawPolygon")
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.polygon(pointList, fillColor, outlineColor)
  
  
  
    def drawPoints(self, pointList, color=(0, 0, 0)):
        """Draws separate points with the given color (black by default)."""
        # Check input types
        if isinstance(pointList[0], tuple):
            for (x, y) in pointList:
                self._checkRange(x, y, "drawPoints")
        else:
            for i in range(0, len(pointList) - 1, 2):
                x = pointList[i]
                y = pointList[i+1]
                self._checkRange(x, y, "drawPoints")
        self._checkColor(color, "drawPoints")
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.point(pointList, color)
      
      
      
    def drawText(self, x0, y0, text, color=(0, 0, 0), font=None):
        """Draws given text with given font and color, black by default."""
        # Check input types
        self._checkRange(x0, y0, "drawText")
        self._checkColor(color, "drawText")
        if not isinstance(text, str):
            text = str(text)
        # If all inputs okay, do drawing
        if self.drawObj is None:
            self.drawObj = ImageDraw.Draw(self.image)
        self.drawObj.text((x0, y0), text, color, font)
      
      
      
    # -------------------------------------------------------
    # Utility methods


    def __repr__(self):
        """Takes no inputs, and produces a string that accurately describes the picture object"""
        return "<Picture instance ({:d} x {:d})>".format(self.width, self.height)
   
    def __iter__(self):
        return PictureIterator(self.width, self.height)
   
   
    def _convertRange(self, val):
        """Takes in a value, and converts it to be an integer between 0 and 255"""
        self._checkNumeric(val, "_convertRange")
        return int(max(min(val, 255), 0))


    def _checkRange(self, x, y, funcName):
        """Check whether the input values are valid indices to pixels in this image.
        If they are, then return True, otherwise raise an exception that describes
        what is wrong"""
        errHeader = "(Picture) " + funcName + ": "
        self._checkNumeric(x, funcName)
        self._checkNumeric(y, funcName)
        if (0 <= x < self.width) and (0 <= y < self.height):
            return True
        else:
            if x < 0:
                errStr = "input x value out of bounds: {:d} < 0".format(x)
            elif x >= self.width:
                errStr = "input x value out of bounds: {:d} >= {:d}".format(x, self.width)
            elif y < 0:
                errStr = "input y value out of bounds: {:d} < 0".format(y)
            elif y >= self.height:
                errStr = "input y value out of bounds: {:d} >= {:d}".format(y, self.height)
            else:
                errStr = "Weird unknown error, contact developers"
            raise ValueError(errHeader + errStr)
      
      


    def _checkNumeric(self, value, funcName):
        """Takes in a value, and checks if it is one of the valid numeric types,
        int, float, or long, and returns True or False"""
        if isinstance(value, int) or isinstance(value, float):
            return True
        else:
            raise TypeError("(Picture) " + funcName + ": expected value to be a number, given: " + str(value))
   
   
    def _checkColor(self, value, funcName):
        """Given a value, this function checks to see if it is a list or tuple three long, where
        each value in the triple is an integer between 0 and 255"""
        errHeader = "(Picture) " + funcName + ": "
        if isinstance(value, str):
            try:
                ImageColor.getrgb(value)
                return True
            except ValueError as vErr:
                raise ValueError(errHeader + str(vErr))
        elif not (isinstance(value, tuple)):
            raise TypeError(errHeader + "Color must be tuple or string, not " + str(value) + " of type " + str(type(value)))
        elif (len(value) == 3) and \
                all([self._checkNumeric(x, funcName) for x in value]):
            return True
        else:
            raise ValueError(errHeader + "Invalid color tuple: " + str(value))
 
 
 
# ==============================================================

class ImageWindow:
  
    """An ImageWindow is a toplevel window for displaying an image."""
  
    def __init__(self, displayImage, wid, hgt, title = "Image", autoflush = True):
        self.master = None
        self.tkImage = None
        self.imageLabel = None
        self.closed = True
        self.width = wid
        self.height = hgt
        self.title = title
        self.autoflush = autoflush
        self.openWindow(displayImage)
      
      
    def openWindow(self, displayImage):
        self.master = tk.Toplevel(root,
                                  width=self.width,
                                  height=self.height,
                                  bg="gray")
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.bind("Button-1", self.__autoflush)
        self.tkImage = ImageTk.PhotoImage(displayImage)
        self.imageLabel = tk.Label(self.master, image=self.tkImage, bg="gray")
        self.imageLabel.pack()
        self.master.title(self.title)
        self.master.resizable(False, False)
        self.closed = False
        self.master.lift()
        if self.autoflush:
            self.__autoflush()
       
      
    def update(self, displayImage):
        if self.closed:
            self.openWindow(displayImage)
        else:
            self.tkImage = ImageTk.PhotoImage(displayImage)
            self.imageLabel["image"] = self.tkImage
            if self.autoflush:
                self.__autoflush()
         
         
    def close(self):
        """Close the window"""
        if self.closed:
            return
        self.closed = True
        self.master.destroy()
        # self.__autoflush()
  
  
    def isClosed(self):
        return self.closed
  
  
    def isOpen(self):
        return not self.closed
  
  
    def __autoflush(self, optEvent=None):
        if self.autoflush:
            globalUpdate()
  

# ==============================================================

class PictureIterator:
    """An iterator for positions in an image. It loops over columns and
    rows, returning an (x, y) tuple each time."""

    def __init__(self, wid, hgt):
        """Sets up bounds and starting values"""
        self.width = wid
        self.height = hgt
        self.x = 0
        self.y = 0
      
    def __iter__(self):
        """By def, should return itself"""
        return self
   
    def __next__(self):
        """Returns current (x, y) coordinates, and then updates to the next
        coordinate. Resets if goes past end of current column. """
        if (self.x >= self.width):
            raise StopIteration
        else:
            res = (self.x, self.y)
            self.y += 1
            if self.y >= self.height:
                self.x += 1
                self.y = 0
            return res


# ==============================================================
# Below this are helpful functions


def pickAFile():
    """Creates a dialog window for selecting a file.  Returns a string which is the filename, returning
    an empty string if no file was selected"""
    globalUpdate()
    result = tkFileDialog.askopenfilename() # filetypes = [('image file', '*.jpg'), ('image file', '*.jpeg')])
    if result is None:
        print("Warning: no file selected, returning an empty string")
        return ""
    else:
        return result


def pickAFont():
    """Creates a dialog window for selecting a font. User must know where to find the fonts, and must choose only
    .ttf files. Then it asks for the point size, and finally builds and returns the font object."""
    globalUpdate()
    filename = tkFileDialog.askopenfilename(title = "Select font file", filetypes = [('truetype font', '*.ttf')])
    if filename is None:
        print("Warning: no file selected, returning None")
        return None
    fontSize = tkSimpleDialog.askinteger("Font size", "Enter font size")
    if not (fontSize is None):
        fontSize = int(fontSize)
    else:
        fontSize = 12
    newFont = ImageFont.truetype(filename, fontSize)
    return newFont
   

def distance(color1, color2):
    """Given two colors objects, this computes the distance between the colors, assuming
    that each color is a point in three-dimensional state, and using a 3D version of the
    Pythagorean theorem to compute distance."""
    (r1, g1, b1) = makeRGBTuple(color1)
    (r2, g2, b2) = makeRGBTuple(color2)
    dist = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return dist


def makeRGBTuple(value):
    """Takes in a representation of a color, and converts it to be a tuple. It raises
    an error if it cannot be converted to a tuple, or if it does not have the right content."""
    errHeader = "distance: "
    if isinstance(value, str):
        try:
            tup = ImageColor.getrgb(value)
            return tup
        except ValueError as vErr:
            raise ValueError(errHeader + str(vErr))
    elif not (isinstance(value, tuple)):
        raise TypeError(errHeader + "Color must be tuple or string, not " + str(value) + " of type " + str(type(value)))
    elif len(value) == 3 and \
            all([((isinstance(x, int) or isinstance(x, float)) and (0 <= x <= 255)) for x in value]):
        return value
    else:
        raise ValueError(errHeader + "Invalid color tuple: " + str(value))



