# PHOTOSHOP-ISH
Python GUI Interface, contains useful photo manipulation functions

Kevin Shin, Arianna Dart, Redi Kurt
Photoshop-ish

MANUAL AND REPORT

User’s Manual											

Our program, Photoshop-ish, allows the user to upload any image from their computer, perform a collection of edits on that photo, and then save the image back to their computer. If the user is interested in having a user-friendly, straightforward program to make basic edits on their photo, our program offers a simplified version of Photoshop which the user might find more intuitive and accessible than a complex photo editing program. This process begins by opening the Python file Final Project Code.py in any Python environment and running the program. imageTools.py must be in the same directory as the Python code. When the user first runs the program, a GUI interface will appear with a default image in place, and the user can press the button “Click Here to Begin” to upload an image file from any location on their computer. Once that is selected, the picture will be displayed on the interface, with a set of buttons on the right-hand side. 

The available tools are as follows:
•	Crop: The user clicks the button and then clicks twice on the image. The first click on the image designates the top left of the area to be cropped, and the second click designates the bottom right of the area to be cropped. The cropped image will then be displayed on the canvas. 
•	Clone: The user clicks the button, and then clicks twice on the image to define an area to clone. As with the crop function, the first click on the image designates the top left of the area to be cropped, and the second click designates the bottom right of the area to be cropped. Then, the user clicks a third time to clone that region onto the original image. The image with the cloned section is displayed on the canvas.
•	Healing Tool: The user clicks the Healing Tool button, and then clicks a point on the image in order to blur a small region around the click. This converts the pixels in the region into same average RGB values. The image with the slight blur is displayed on the canvas.
•	Grayscale, Sepia, and Posterize: The user clicks any of these buttons and then anywhere on the image, and the appropriate filter is applied to the entire image. The filtered image is displayed on the canvas.
•	Reset: The user clicks on the Reset button, and all previous edits are cleared. The original uploaded image is displayed on the canvas.
•	Save: The user clicks on the Reset button and can type in a string to designate the name of the file. The image with the latest edits is saved to the same directory where the Python file is located.
In order to quit the program entirely, the user can click the red button in the top left corner to close the window. 

Report												

Summary
Our program, Photoshop-ish, only contains one file in which we have all of our code. However, in the zip folder there is also the image tools file, and the Sample Image folder which was provided in class. We provide blemish.jpg, a sample image on which we experimented with our functions. The user can import any photo of their choosing. Our program is structured as follows:

Imports: At the top of our python file we have our imports which are “tkinter” and “imageTools”.

GUI Main and importPhoto: Next up, we have our “GUIMain” function which will create a welcome window, with a text label, an image and an import button.  When the user clicks the import button our next function, “importPhoto”, will run. “ImportPhoto” opens another window which allows the user to select an image which they would like to manipulate. After the image is selected, the function closes the previous windows and opens the main window of our function, which contain the main canvas where the selected image is displayed, and all the buttons corresponding to our functions. The main canvas is set to the width of the imported photo. If, however, the height of the photo exceeds 900 pixels or width of the photo exceeds 700 pixels, the “scaleDown” function is called. This function scales the selected image down by half in order to ensure it can be displayed on a normal laptop screen. The canvas is then set to the scaled down image width. 

Click Functions: Afterwards, we have our click functions. Their only job is to set our global variable “whichclick” to a certain value. These are the functions bound to the Buttons in the main window, so that when “whichclick” is set to a value, the coordinates function will only call one of our photo editing functions with the mouse event. We have six click functions: “cropClick”,”healClick”, “cloneClick”, “grayClick”, “sepiaClick” and “posterizeClick”, each corresponding to one of our main image manipulation functions.

Coordinates: Then, we have our “coordinates” function which controls the calls to the functions based on the value of the global variable “whichclick”. This function, depending on that value, takes in mouse events and calls a photo editing function. This function is the one which is bound to our canvas so is essentially the function that acts as the link between the user interface and our program.

Functions: Finally, we have all our individual photo editing functions. The function “cropImage”, crops the part of the image selected by the user, “healingPatch” masks the blemishes by blurring the area selected by the user and then the “cloneFunction” clones the area selected by the user and “copyPicInto” pastes that cloned area into a selected position by the user on the photo. Moreover, in this section we have the three filter functions: “grayscale”, “yellowSepia” and posturize which is divided into two functions “convertTo4” and “posterize64”. These functions apply the respective filter onto the photo in the canvas. 

Reset and Save: Lastly, we have three more functions at the end: “reset”, “savePhoto” and “entryResponse”. “Reset” will undo all the manipulations the user has done on the image and set the picture of the canvas to the original image. “SavePhoto” opens a window that prompts the user to enter a name for their image. This function binds the return key to “entryResponse”, which in turn will take the image currently displayed on the canvas and save it under the name entered by the user.
