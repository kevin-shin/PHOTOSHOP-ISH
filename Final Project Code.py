#PHOTOSHOP-ISH: FINAL PROJECT

#Kevin Shin, Redi Kurt, Arianna Dart
#COMP 123, Beth Ernst


'''

Our goal was to take basic Photoshop functions and illustrate how we could design them in tkinter. We chose the crop, clone, heal functions,
three common filters, and a save function. The program initially opens a welcome window where the user can import any photo on their computer, but
we have additionally provided some photos that the user can edit as well.

Our strategy was to bind each button to a certain value called whichclick to keep track of the function being used by the user.
When the user clicks a button, it will set whichclick to a certain value, which corresponds to a specific "if clause" within our
coordinates function. The coordinates function will only run the if-clause which corresponds to the value whichclick is currently holding,
and call a function which will actually manipulate the function. This function will then replace the image on the screen with the photo
returned by the photoediting function.

Thus, structure of our program is the following:
    1. Imports - we import tkinter and imageTools so we can use them in our program
    2. GUIMain and importPhoto - these are the two functions which import the photo and create the windows we'll be using and
                                 bind the clicks of each button to the appropriate click functions
    3. click Functions - these are the functions mentioned which set the global variable whichclick to a certain value corresponding to
                         the value in the coordinates function.
    4. coordinates - this is the main function which allows us to keep track of what function the user is implementing.
    5. Photoediting Functions - these are the actual functions which manipulate the picture. We designed these functions to directly take in
                                (x,y) values, widths, heights, and other characteristics of the photo, so that we could later simply allow
                                our coordinates function to determine the input coordinates, widths, heights, etc. based on the mouse events.



More specific descriptions of the functions are contained in the manual, as well as doc-strings underneath each function.


Our function is entirely based on the actions of the user. Thus, our tests were done by running our program and checking
the result, that is, seeing that it properly did what we expected it to do. In order to properly specify how we tested the
functions, a main summary of the methods of testing will be provided after each section of the code.

'''


###--------------------------------------IMPORTS--------------------------------------###

from tkinter import *
from imageTools import *

###--------------------------------------GUI MAIN and importPhoto--------------------------------------###

mainWindow = None
welcomeWindow = None
photo = None
whichclick = 0
storedX = None
storedY = None
mainCanvas = None

#this is the picture displayed in the welcome window
displayPic = Picture("screensaver.jpg")
displaytkPic = ImageTk.PhotoImage(displayPic.image)


def GUIMain():
    '''Our GUI function. This function is called when the program is run. It creates a welcome window with a label, image, and import button.'''

    global mainWindow
    global welcomeWindow
    global pic                                    #This global variable is what we're actually editing
    global tkPic                                  #This global variable is what's displayed in canvas

    #this creates our welcome window
    welcomeWindow = Toplevel(root)
    welcomeWindow["bg"] = "white"
    welcomeWindow.title("Welcome to Photoshop-ish")

    #design labels for the window
    welcomeLabel = Label(welcomeWindow)
    welcomeLabel["text"] = "Kevin Shin - Arianna Dart - Redi Kurt" + "\n" + "Core Concepts: COMP 123" + "\n" + "Final Project"
    welcomeLabel["font"] = "Arial 24"
    welcomeLabel["bg"] = "white"
    welcomeLabel.grid(row=0, column=1,pady=(15,5))

    mainLabel = Label(welcomeWindow)
    mainLabel["image"] = displaytkPic
    mainLabel.grid(row=1, column=1,padx=10,pady=8)

    #the import button
    importButton = Button(welcomeWindow)
    importButton["text"] = "Click Here to Begin"
    importButton["font"] = "Arial 12"
    importButton["bg"] = "#997711"
    importButton["fg"] = "blue"
    importButton["command"] = importPhoto
    importButton.grid(row=2, column=1,padx=10,pady=(5,19))


    welcomeWindow.mainloop()


'''
Test: Visual confirmation by testing. GUIMain() opens a welcome window with a label, photo, and button. The button should open 
      a window which prompts the user to pick a photo they wish to manipulate. 
'''



def importPhoto():
    '''The function corresponding to the import Button on the welcome window. This function will allow the user to pick a photo they wish to edit.
    Then, it will create the main window of our function, which contains the main canvas in which the edited photo will be displayed, and all the
    buttons corresponding to our functions.'''

    global mainWindow
    global welcomeWindow
    global whichclick
    global mainCanvas
    global pic
    global resetPic
    global tkPic
    global scaledPic

    #allows the user to pick a file, then turns the photo into a tkImage, one which we need to actually display the photo in tkinter
    pic = Picture(pickAFile())

    #this is to control when pictures are too big for the screen
    if pic.getWidth() > 900 or pic.getHeight() > 700:
        scaledPic = scaleDown(pic)
        pic = scaledPic

    resetPic = pic.copy()
    tkPic = ImageTk.PhotoImage(pic.image)


    #main window and canvas
    mainWindow = Toplevel(root)
    mainWindow.title("Photoshop-ish: COMP 123")

    mainCanvas = Canvas(mainWindow, width=pic.getWidth(),height=pic.getHeight())
    mainCanvas.bind("<Button-1>", coordinates)
    mainCanvas.grid(row=1, column=1, padx=30,pady=30)
    mainCanvas.create_image(0,0,image=tkPic, anchor=NW)

    #frame to hold the buttons
    Frame1 = Frame(mainWindow)
    Frame1["bg"] = "white"
    Frame1.grid(row=1, column=2)

    #buttons corresponding to the functions
    cropButton = Button(Frame1)
    cropButton["text"] = "Crop"
    cropButton["font"] = "Arial 12"
    cropButton["bg"] = "#997711"
    cropButton["fg"] = "blue"
    cropButton["command"] = cropClick
    cropButton.grid(row=1, column=1)

    cloneButton = Button(Frame1)
    cloneButton["text"] = "Clone"
    cloneButton["font"] = "Arial 12"
    cloneButton["bg"] = "#997711"
    cloneButton["fg"] = "blue"
    cloneButton["command"] = cloneClick
    cloneButton.grid(row=2, column=1)

    healButton = Button(Frame1)
    healButton["text"] = "Healing Tool"
    healButton["font"] = "Arial 12"
    healButton["bg"] = "#997711"
    healButton["fg"] = "blue"
    healButton["command"] = healClick
    healButton.grid(row=3, column=1)

    grayButton = Button(Frame1)
    grayButton["text"] = "Grayscale"
    grayButton["font"] = "Arial 12"
    grayButton["bg"] = "#997711"
    grayButton["fg"] = "blue"
    grayButton["command"] = grayClick
    grayButton.grid(row=4, column=1)

    sepiaButton = Button(Frame1)
    sepiaButton["text"] = "Sepia"
    sepiaButton["font"] = "Arial 12"
    sepiaButton["bg"] = "#997711"
    sepiaButton["fg"] = "blue"
    sepiaButton["command"] = sepiaClick
    sepiaButton.grid(row=5, column=1)

    posterizeButton = Button(Frame1)
    posterizeButton["text"] = "Posterize"
    posterizeButton["font"] = "Arial 12"
    posterizeButton["bg"] = "#997711"
    posterizeButton["fg"] = "blue"
    posterizeButton["command"] = posterizeClick
    posterizeButton.grid(row=6, column=1)

    resetButton = Button(Frame1)
    resetButton["text"] = "Reset"
    resetButton["font"] = "Arial 12"
    resetButton["bg"] = "#997711"
    resetButton["fg"] = "blue"
    resetButton["command"] = reset
    resetButton.grid(row=7, column=1)

    saveButton = Button(Frame1)
    saveButton["text"] = "Save"
    saveButton["font"] = "Arial 12"
    saveButton["bg"] = "#997711"
    saveButton["fg"] = "blue"
    saveButton["command"] = savePhoto
    saveButton.grid(row=8, column=1)

    #closes the welcome window, since it's no longer needed
    welcomeWindow.destroy()

    mainWindow.mainloop()

'''
Test: Visual confirmation by testing. importPhoto() opens a window with the photo that was imported, chosen by the user, and a frame which
holds our 8 buttons. The welcome window should be closed.
'''




##---------------------------CLICK FUNCTIONS--------------------------------##

'''
The following are the click functions. Their only job is to set our global variable whichclick to a certain value. These are the functions
bound to the Buttons in the main window, so that when whichclick is set to a value, the coordinates function will only call one of our
photoediting functions with the mouse event. 

'''

def cropClick():
    global whichclick
    whichclick = 1

def healClick():
    global whichclick
    whichclick = 11

def cloneClick():
    global whichclick
    whichclick = 21

def grayClick():
    global whichclick
    whichclick = 31

def sepiaClick():
    global whichclick
    whichclick = 41

def posterizeClick():
    global whichclick
    whichclick = 51



'''
Test: the only purpose of these functions is to control our global variable. We know these functions are correct when the proper photo-editing
function is called by a mouse event. However, we also had print(whichclick) underneath each click. As such, clicking the corresponding button
printed the value of whichclick which was assigned by that click function.
'''



###--------------------------------------COORDINATES--------------------------------------###

def coordinates(event):
    '''Our function which controls the calls to the functions based on the current value of whichclick. Recall that clicking a button will
    set the value of whichclick to a certain number. This function, depending on that value, takes in mouse events and calls a photoediting
    function.'''

    global mainCanvas
    global storedX
    global storedY
    global whichclick
    global pic
    global smallPic

    #values in these if clause correspond to cropClick. Notice that the first click stores the mouse position and sets whichclick to 2.
    #Now that whihclick is set to 2, when the user clicks again, we compute the width and height of the area encompassed by those two
    #clicks, and call cropImage. We then set whichclick to 0 to reset our value.
    if whichclick == 1:
        storedX = event.x
        storedY = event.y
        whichclick = 2
    elif whichclick == 2:
        width = abs(storedX - event.x)
        height = abs(storedY - event.y)
        cropImage(pic,storedX,storedY,width,height)
        whichclick = 0

    #values in this if clause correspond to healClick. The user clicks an area, and healingPatch is called in a 20 pixel diameter around the
    #mouse click position.
    elif whichclick == 11:
        healingPatch(pic,event.x,event.y,20)

    #values in this if clause correspond to cloneClick. The first click stores the mouse position and sets the whichclick to 22. Upon the user's
    #second click, we computer the width and height of the region specified by those two clicks, call cloneFunction, and set whichclick to 23.
    #Upon the third click, copyPicInto is called, which takes the returned photo of cloneFunction, puts it into our original image,
    #and displays it into the canvas.
    elif whichclick == 21:
        storedX = event.x
        storedY = event.y
        whichclick = 22
    elif whichclick == 22:
        width = abs(storedX - event.x)
        height = abs(storedY - event.y)
        cloneFunction(pic, storedX, storedY, width, height)
        whichclick = 23
    elif whichclick == 23:
        copyPicInto(smallPic, pic, event.x, event.y)

    #values correspond to the grayscale function. Upon the user's click, the grayscale filter will be applied.
    elif whichclick == 31:
        grayscale(pic)
        whichclick = 0

    #values correspond to the sepia function. Upon the user's click, the sepia filter will be applied.
    elif whichclick == 41:
        yellowSepia(pic)
        whichclick = 0

    #values correspond to the posterize function. Upon the user's click, the posterize filter will be applied.
    elif whichclick == 51:
        posterize64(pic)
        whichclick = 0

'''
Test: Visual confirmation by testing. Since the purpose of this function is just to call the photo-editing functions, if clicking a button
calls a function and we know what the photo is supposed to look like after this edit, we know that coordinates has the proper if statements.

'''

###--------------------------------------FUNCTIONS--------------------------------------###


'''
This section contains all of the functions which actually manipulate the picture in the way we want. The structure of the functions is essentially
the same - we delete what's currently on the main canvas, make a copy of the image, manipulate it in the way we want, set our global variable 
"pic" to this new photo, make it a tkImage, then put the picture on our canvas. 
'''

##---------CROP---------##
def cropImage(sourceImage,ulx,uly,w,h):
    '''Takes in a picture, coordinates of the upper left corner (ulx, uly), and a width and height. The function returns a picture
    that starts at the inputted upper left corner with the added width and height, and sets this image to the canvas.'''
    global pic
    global mainCanvas
    global tkPic
    mainCanvas.delete("all")
    newPic = Picture(w,h)
    for x in range(w):
        for y in range(h):
             a = ulx+x
             b = uly+y
             if a < pic.getWidth() or b < pic.getHeight() or a > 0 or b > 0:
                 color = sourceImage.getColor(a, b)
                 newPic.setColor(x,y, color)
    pic = newPic
    tkPic = ImageTk.PhotoImage(pic.image)
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)


##-------------HEAL--------------##
def healingPatch(sourceImage, x, y, r):
    '''Takes in an image, an x and y value, and a diameter. This function computes the average RGB values of the square region with
    side length r, centered at the inputted (x,y) coordinate. The function replaces the values inside this region with the average RGB value,
    and makes a copy of the original picture with this modification. The function then puts this picture onto the canvas.'''
    global pic
    global mainCanvas
    global tkPic

    mainCanvas.delete("all")
    newPic5 = sourceImage.copy()
    totalRed = 0
    totalGreen = 0
    totalBlue = 0
    for i in range(x-r//2,x+r//2):
        for j in range(y-r//2,y+r//2):
            if i >= pic.getWidth() or j >= pic.getHeight() or i < 0 or j < 0:
                continue
            colorTuple = newPic5.getColor(i,j)
            totalRed = totalRed + colorTuple[0]
            totalGreen = totalGreen + colorTuple[1]
            totalBlue = totalBlue + colorTuple[2]
    avgRed = totalRed//(r**2)
    avgGreen = totalGreen//(r**2)
    avgBlue = totalBlue//(r**2)
    for i in range(x-r//2,x+r//2):
        for j in range(y-r//2,y+r//2):
            if i >= pic.getWidth() or j >= pic.getHeight() or i < 0 or j < 0:
                continue
            newPic5.setColor(i, j, (avgRed, avgGreen, avgBlue))
    pic = newPic5  # Set newPic to pic - this updates the global variable
    tkPic = ImageTk.PhotoImage(pic.image)  # Set pic to tkPic in order to display on canvas
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)


##-----------CLONE--------------##
def cloneFunction(sourceImage,ulx,uly,w,h):
    '''This function takes an image, values for the upper left corner (ulx, uly), and a width and height. The function returns a cropped picture
    which starts at (ulx, uly) and is w in width and h in height.'''
    global mainCanvas
    global pic
    global smallPic

    smallPic = Picture(w,h)
    for x in range(w):
        for y in range(h):
            a = ulx+x
            b = uly+y
            color = sourceImage.getColor(a, b)
            smallPic.setColor(x,y, color)
    return smallPic


def copyPicInto(smallPic,bigPic,startX,startY):
    '''This function takes smallPic, the cropped picture returned in cloneFunction above, bigPic, another picture, and x and y values startX
    and startY. The function copies smallPic into bigPic, starting with the coordinate defined as (startX,startY). The function then sets
    this new picture onto the canvas.'''
    global mainCanvas
    global pic
    global tkPic

    w1 = smallPic.getWidth()
    h1 = smallPic.getHeight()
    newPic = bigPic.copy()
    for x in range(w1):
        for y in range(h1):
            color = smallPic.getColor(x, y)
            a = x + startX
            b = y + startY
            if a >= pic.getWidth() or b >= pic.getHeight() or x < 0 or y < 0:
                continue
            newPic.setColor(a, b, color)
    pic = newPic
    tkPic = ImageTk.PhotoImage(pic.image)  # Set pic to tkPic in order to display on canvas
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)


##---------------GRAYSCALE---------------##
def grayscale(sourceImage):
    '''Takes in an image, and loops over the pixels in the image. The function computes a lumin value based on the RGB values of the pixel,
    and sets each pixel to this value. The result is a picture that is in grayscale. The function then sets the image in the canvas to this image.'''
    global mainCanvas
    global pic
    global tkPic

    mainCanvas.delete("all")
    newPic = sourceImage.copy()
    for (x, y) in newPic:
        (r, g, b) = newPic.getColor(x, y)
        lumin = (r * 0.299) + (g * 0.587) + (b * 0.114)
        newPic.setColor(x, y, (lumin, lumin, lumin))
    pic = newPic
    tkPic = ImageTk.PhotoImage(pic.image)  # Set pic to tkPic in order to display on canvas
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)



##---------------SEPIA---------------##
def yellowSepia(sourceImage):
    '''Takes in an image, and loops over the pixels in the image. For each pixel, it computes a new RGB value and sets the pixel to this color.
    The result is a picture in sepia. The function then sets the image in the canvas to this image.'''
    global mainCanvas
    global pic
    global tkPic

    newPic = sourceImage.copy()
    for (x, y) in newPic:
        (origRed, origGreen, origBlue) = newPic.getColor(x, y)
        newRed = (0.393 * origRed) + (0.769 * origGreen) + (0.189 * origBlue)
        newGreen = (0.349 * origRed) + (0.686 * origGreen) + (0.168 * origBlue)
        newBlue = (0.272 * origRed) + (0.534 * origGreen) + (0.131 * origBlue)
        newPic.setColor(x, y, (newRed, newGreen, newBlue))
    pic = newPic
    tkPic = ImageTk.PhotoImage(pic.image)  # Set pic to tkPic in order to display on canvas
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)


##---------------POSTERIZE---------------##
def convertTo4(n):
    '''Takes in an integer, and depending on the value of this integer, returns another integer, specified by a, b, c, d. These are values
    computed by dividing the 256 available values of red, green, and blue into 4, then taking the median value of each region.'''
    a = 32
    b = 96
    c = 160
    d = 223
    if n <= 64:
        return a
    elif 64 < n <= 128:
        return b
    elif 128 < n <= 191:
        return c
    elif 191 < n <= 255:
        return d

def posterize64(sourceImage):
    '''Takes in an image, and loops over the pixels in the image. For each pixel, it takes the integer returned by convertTo4 of each RGB value, and
    sets the pixels of the copy of this picture into this new RGB value. The result is a posterized picture. The function then replaces the picture
    on the canvas to this picture.'''
    global mainCanvas
    global pic
    global tkPic

    newPic = sourceImage.copy()
    for (x,y) in newPic:
        (r, g, b) = newPic.getColor(x, y)
        r1 = convertTo4(r)
        g1 = convertTo4(g)
        b1 = convertTo4(b)
        newPic.setColor(x,y,(r1,g1,b1))
    pic = newPic
    tkPic = ImageTk.PhotoImage(pic.image)
    mainCanvas.create_image(0, 0, image=tkPic, anchor=NW)

##---------------RESET---------------##
def reset():
    '''resetPic is a global variable that is a copy of the original pic uploaded. When called, it will set the picture of the canvas to the original
    image.'''
    global pic
    global tkPic
    global resetPic

    pic = resetPic
    tkPic = ImageTk.PhotoImage(pic.image)
    mainCanvas.create_image(0,0,image=tkPic, anchor=NW)


##---------------SAVE---------------##
def savePhoto():
    '''Opens a window which prompts the user to enter a name for their image. This function binds the return key to entryResponse, the following
    function.'''
    global pic
    global saveWindow
    global saveEntry

    saveWindow = Toplevel(mainWindow)
    saveWindow.title("Save")

    saveLabel = Label(saveWindow, anchor="w")
    saveLabel["text"] = "Choose a name for your file:"
    saveLabel["font"] = "Arial 14"
    saveLabel["bg"] = "white"
    saveLabel.grid(row=0, column=1,pady=(15,5))

    saveEntry = Entry(saveWindow, bg = 'white', bd = 0.5, font = "Arial 14",
                justify = CENTER, width=40)
    saveEntry.grid(row=2,column=1,padx=10,pady=(0,15))
    saveEntry.bind("<Return>",entryResponse)

def entryResponse(event):
    '''Takes in an event, in this case the pressing of the Return key by the user. When the Return key is pressed, this function will
    take the picture currently on the canvas and save this image under the name entered by the user in saveWindow.'''
    global saveText

    if event.keysym == "Return": # examples of how to check what key
        saveText = saveEntry.get() + ".jpg"

    pic.save(saveText)
    saveWindow.destroy()


##-------------------SCALE DOWN-------------------##

def scaleDown(pic):
    '''Takes in a picture and returns a copy of the picture half in height and width.'''
    newPic = Picture(math.ceil(pic.getWidth()/2),math.ceil(pic.getHeight()/2))
    for x in range(math.ceil(pic.getWidth()/2)):
        for y in range(math.ceil(pic.getHeight()/2)):
            a = 2*x
            b = 2*y
            color = pic.getColor(a, b)
            newPic.setColor(x,y, color)
    return newPic


'''Test: Visual confirmation by testing. Each of these functions were developed originally just using imageTools. As such, we were able to test
that they worked by writing a version of this function that would show a copy of the new photo. After we confirmed visually that all of these
functions returned and showed the proper edited photo, we changed our function to set this returned image to the canvas rather than show it. As such,
a visual confirmation of the result would mean that when the user clicked the canvas, the photo would be replaced by a photo we knew each of these 
functions returned. All of the functions passed the visual tests.

The reset function was tested independently. We made a range of edits onto our photo, then clicked reset after each edit, making sure that 
the canvas would change the image to our original image. reset passed all of our tests, and works for every photo-editing function.


The save function was also tested independently. After the user inputs the name of the file into the saveWindow, we should expect to see the photo
on the canvas saved with the name as the string inputted by the user. save passed the test.'''


GUIMain()
