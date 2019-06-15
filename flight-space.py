#! /usr/bin/env python3
import sys

from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#from direct.actor.Model import Model
#from direct.model.Model import Model
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Point3, Camera, TextNode

X_STABLE = 320.0
Y_STABLE = 260.0
MAX_TILT = 30
MAX_LIFT = 20

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)


# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.07,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


 
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        plane_scale = 0.1
        self.xPos = 0.0
        self.yPos = 0.0
        self.tilt = 0.0
        self.lift = 0.0

        camera.setPosHpr(0, 0.5, 20, 0, -100, 0) #Vary this

 
        # Disable the camera trackball controls.
        self.disableMouse()
 
        '''
        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        '''
 
        '''
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        '''
 
        '''
        # Load and transform the panda actor.
        self.airplaneModel = loader.loadModel("models/douglasX")
        #self.airplaneModel.setScale(0.005, 0.005, 0.005)
        self.airplaneModel.setPos(0, 0, 5)
        self.airplaneModel.reparentTo(self.render)
        print ("Type: %s\n" % str(type(self.airplaneModel)))
        #print ("what is this: %s\n" % str(dir(self.airplaneModel)))
        '''

        self.plane = loader.loadModel('./models/plane/boeing707')
        self.plane.setPos(0, 0, 5)
        self.plane.reparentTo(render)
        self.plane.setScale(plane_scale, plane_scale, plane_scale)
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)


        # Add keymappings

        # Key mappings
        '''
        self.accept('escape', sys.exit)
        self.accept(']', self.scaleUp)
        self.accept('[', self.scaleDown)
        self.accept('w', self.liftUp)
        self.accept('s', self.liftDown)
        self.accept('q', self.stabilizeLift)
        self.accept('a', self.moveLeft)
        self.accept('d', self.moveRight)
        self.accept('e', self.stabilizeTilt)
        '''

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0,
            "right": 0,
            "forward": 0,
            "backward": 0,
            "cam-left": 0,
            "cam-right": 0,
        }

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("a", self.setKey, ["cam-left", True])
        self.accept("s", self.setKey, ["cam-right", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])
        self.accept("a-up", self.setKey, ["cam-left", False])
        self.accept("s-up", self.setKey, ["cam-right", False])

        taskMgr.add(self.move, "moveTask")

        self.title = addTitle(
            "Danger Plane")
        self.inst1 = addInstructions(0.06, "[ESC]: Quit")
        self.inst2 = addInstructions(0.12, "[Left Arrow]: Rotate Plane Left")
        self.inst3 = addInstructions(0.18, "[Right Arrow]: Rotate Plane Right")
        self.inst4 = addInstructions(0.24, "[Up Arrow]: Moves Plane Down")
        self.inst5 = addInstructions(0.30, "[Down Arrow]: Moves Plane Up")
        self.inst6 = addInstructions(0.36, "[A]: Rotate Camera Left")
        self.inst7 = addInstructions(0.42, "[S]: Rotate Camera Right")




    def setKey(self, key, value):
        self.keyMap[key] = value

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        if self.keyMap["cam-left"]:
            self.camera.setX(self.camera, -20 * dt)
        if self.keyMap["cam-right"]:
            self.camera.setX(self.camera, +20 * dt)

        # If a move-key is pressed, move ralph in the specified direction.

        if self.keyMap["left"]:
            self.moveLeft()
            #self.ralph.setH(self.ralph.getH() + 300 * dt)
        if self.keyMap["right"]:
            #self.ralph.setH(self.ralph.getH() - 300 * dt)
            self.moveRight()
        if self.keyMap["forward"]:
            #self.ralph.setY(self.ralph, -20 * dt)
            self.liftDown()
        if self.keyMap["backward"]:
            #self.ralph.setY(self.ralph, +10 * dt)
            self.liftUp()

        return task.cont




# Make the Boeing stable on the tilt
    def stabilizeTilt(self):
        if(self.tilt > 0):
            if(self.tilt != 0.0):
                self.tilt = self.tilt - 0.25
        else:
            if(self.tilt != 0.0):
                self.tilt = self.tilt + 0.25
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)

# Make the Boeing stable on the lift
    def stabilizeLift(self):
        if(self.lift > 0):
            if(self.lift != 0.0):
                self.lift = self.lift - 0.25
        else:
            if(self.lift != 0.0):
                self.lift = self.lift + 0.25

        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)

# Zoom into the plane
    def scaleUp(self):
        self.scale = self.scale + 0.005
        self.plane.setScale(self.scale, self.scale, self.scale)

# Zoom out of the plane
    def scaleDown(self):
        self.scale = self.scale - 0.005
        self.plane.setScale(self.scale, self.scale, self.scale)

# Move the plane right
    def moveRight(self):
        if(self.tilt >= MAX_TILT):
            self.tilt = MAX_TILT
        self.xPos = self.xPos + 0.01
        self.tilt = self.tilt + 0.25
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)

# Move the plane left
    def moveLeft(self):
        if(self.tilt <= -MAX_TILT):
            self.tilt = -MAX_TILT
        self.tilt = self.tilt - 0.25
        self.xPos = self.xPos - 0.01
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)

# Lift the plane up
    def liftUp(self):
        if(self.lift >= MAX_LIFT):
            self.lift = MAX_LIFT
        self.lift = self.lift + 0.25
        self.yPos = self.yPos + 0.01
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)

# Lift the plane down
    def liftDown(self):
        if(self.lift <= -MAX_LIFT):
            self.lift = -MAX_LIFT

        self.lift = self.lift - 0.25
        self.yPos = self.yPos - 0.01
        self.plane.setPosHpr(self.xPos, -0.7 + self.yPos, 0, 0, 270 + self.lift, self.tilt)


 
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
 
if __name__ == "__main__":
    print ("Starting");
    app = MyApp()
    app.run()


