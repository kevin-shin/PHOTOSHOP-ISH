from imageTools import *
import random

#Class Notes
# myFile = pickAFile()
# myFile = "SampleImages/arches.jpg"
# print(myFile)  #daylilies is stored as myFile
#
# myPict = Picture(myFile) #turns the file into a picture object
# print(myPict)
#
# myPict.show() #actually shows the image


pic2 = Picture("SampleImages/mightyMidway.jpg")
numPixels = pic2.getWidth()*pic2.getHeight()
print(numPixels)

pic4 = pic2.copy()
pic4.setColor(4, 4, "Red")
pic4.setColor(8, 8, "Red")

pic4New = pic4
pic4.explore()

def randomBG(w,h):
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    color = (r,g,b)
    newFile = Picture(w,h,color)
    newFile.show()
    input("Press key to exit")
    return newFile

def drawStickFigure():
    pic = Picture(500,500)
    pic.drawOval(100,100,150,150)
    pic.drawLine(125,150,125,250)
    pic.drawLine(125,250, 100,275)
    pic.drawLine(125,250, 150, 275)
    pic.drawLine(125,185,100,160)
    pic.drawLine(125, 185, 150, 160)
    pic.show()
    input("Press key to exit")
    return pic

def changeRed(picture, factor):
    '''turns picture red by a factor, higher factors turn picture entirely red'''
    for (x, y) in picture:
        (red, grn, blu) = picture.getColor(x, y)
        newRed = factor * red
        picture.setColor(x, y, (newRed, grn, blu))

def changeBlue(picture, factor):
    '''turns picture blue by a factor, higher factors turn picture entirely blue'''
    for (x, y) in picture:
        (red, grn, blu) = picture.getColor(x, y)
        newBlue = factor * blu
        picture.setColor(x, y, (red, grn, newBlue))

def removeBlue(picture):
    '''removes blue from a picture'''
    for (x, y) in picture:
        (red, grn, blu) = picture.getColor(x, y)
        picture.setColor(x, y, (red, grn, 0))

def fixGreen(picture, number):
    '''makes all the green values of pixels in the picture input number value'''
    for (x, y) in picture:
        (red, grn, blu) = picture.getColor(x, y)
        newGreen = number
        picture.setColor(x, y, (red, newGreen, blu))
