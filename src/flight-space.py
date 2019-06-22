#! /usr/bin/env python3
import sys

from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#from direct.actor.Model import Model
#from direct.model.Model import Model
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Point3, PandaNode, NodePath, Camera, TextNode


from adsb_interface import ADSBFactory

X_STABLE = 320.0
Y_STABLE = 260.0
MAX_TILT = 30
MAX_LIFT = 20
DEFAULT_HEADING = 180


PLANE_MODEL = './models/plane/boeng707'
ADSB_SOURCE = 'opensky'
#DEFAULT_BOUDNING_BOX = None
DEFAULT_BOUNDING_BOX = [-73.504556, -70.629270, 42.067599, 42.68852]


CAMERA_STATES = ["FOLLOW", "USER"]



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
        plane_scale = 0.07
        self.xPos = 0.0
        self.yPos = 0.0
        self.tilt = 0.0
        self.lift = 0.0
        self.camera_state = "FOLLOW"
        self.adsb = None
        self.adsb_states = None
        self.plane_state = None

        #camera.setPosHpr(0, 0.5, 20, 0, -100, 0) #Vary this

 
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
 

        self.plane = loader.loadModel('./models/plane/boeing707')
        self.plane.setPos(0, 0, 5)
        self.plane.reparentTo(render)
        self.plane.setScale(plane_scale, plane_scale, plane_scale)
        #self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

        # Create a floater object, which lfoats 2 units above the plane
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.plane)
        self.floater.setZ(2.0)



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
        taskMgr.add(self.adsb_task, "adsbTask")

        self.title = addTitle("Danger Plane")
        self.inst1 = addInstructions(0.06, "[ESC]: Quit")
        self.inst2 = addInstructions(0.12, "[Left Arrow]: Rotate Plane Left")
        self.inst3 = addInstructions(0.18, "[Right Arrow]: Rotate Plane Right")
        self.inst4 = addInstructions(0.24, "[Up Arrow]: Moves Plane Down")
        self.inst5 = addInstructions(0.30, "[Down Arrow]: Moves Plane Up")
        self.inst6 = addInstructions(0.36, "[A]: Rotate Camera Left")
        self.inst7 = addInstructions(0.42, "[S]: Rotate Camera Right")
        self.camera.setPos(self.plane.getX(), self.plane.getY() + 10, 2)


        self.text_status = OnscreenText(text="Starting...", style=1, fg=(1, 1, 1, 1), scale=.04,
                        parent=base.a2dBottomLeft, align=TextNode.ALeft,
                        pos=(0.08, 0.09), shadow=(0, 0, 0, 1))


        '''
        self.text_status = TextNode('textStatus')
        self.text_status.setText("Starting...")
        self.text_np = aspect2d.attachNewNode(self.text_status)
        self.text_np.setScale(0.1)
        self.text_np.setX(-0.9)
        self.text_np.setY(-0.9)
        #self.text_np.reparentTo(render)
        #self.text_np.setZ(0.00)
        #self.text_np.setPos(self.floater.getX(), self.floater.getY(), 2)
        print ("Text Position:    %f, %f, %f" % (self.text_np.getX(), self.text_np.getY(), self.text_np.getZ()))
        print ("Plane Position:   %f, %f, %f" % (self.plane.getX(), self.plane.getY(), self.plane.getZ()))
        print ("Floater Position: %f, %f, %f" % (self.floater.getX(), self.floater.getY(), self.floater.getZ()))
        '''


    def setKey(self, key, value):
        self.keyMap[key] = value

    def adsb_task(self, task):
        if self.adsb == None:
            self.adsb = ADSBFactory().open(ADSB_SOURCE)
            if DEFAULT_BOUNDING_BOX is not None:
                self.adsb.set_bounding_box( DEFAULT_BOUNDING_BOX[0],
                                            DEFAULT_BOUNDING_BOX[1],
                                            DEFAULT_BOUNDING_BOX[2],
                                            DEFAULT_BOUNDING_BOX[3],)
                self.adsb.enable_bounding_box(True);

        self.adsb_states = self.adsb.get_states()
        if self.adsb_states is not  None:
            # Update States
            #XXX: Just get the first plane for now
            self.plane_state = self.adsb_states.states[0]
            self.text_status.setText("%s: La: %f, Lo: %f, A: %f, V: %f, H: %f" %
                                        (   self.plane_state.callsign,
                                            self.plane_state.latitude,
                                            self.plane_state.longitude,
                                            self.plane_state.geo_altitude,
                                            self.plane_state.velocity,
                                            self.plane_state.heading))
            self.plane.setPosHpr(self.plane_state.longitude, self.plane_state.latitude, self.plane_state.geo_altitude, self.plane_state.heading, self.lift, self.tilt)


            pass

        return task.cont

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        #if self.keyMap["cam-left"]:
        #    self.camera.setX(self.camera, -20 * dt)
        #if self.keyMap["cam-right"]:
        #    self.camera.setX(self.camera, +20 * dt)

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

        if self.camera_state == "USER":
            pass
        else:
            #Follow the plane
            camvec = self.plane.getPos() - self.camera.getPos()
            camvec.setZ(0)
            camdist = camvec.length()
            camvec.normalize()
            if camdist > 10.0:
                self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
                camdist = 10.0
            if camdist < 5.0:
                self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist))
                camdist = 5.0

            self.camera.setZ(self.plane.getZ() + 2.0)
            self.camera.lookAt(self.floater)

        return task.cont




# Make the Boeing stable on the tilt
    def stabilizeTilt(self):
        if(self.tilt > 0):
            if(self.tilt != 0.0):
                self.tilt = self.tilt - 0.25
        else:
            if(self.tilt != 0.0):
                self.tilt = self.tilt + 0.25
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

# Make the Boeing stable on the lift
    def stabilizeLift(self):
        if(self.lift > 0):
            if(self.lift != 0.0):
                self.lift = self.lift - 0.25
        else:
            if(self.lift != 0.0):
                self.lift = self.lift + 0.25

        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

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
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

# Move the plane left
    def moveLeft(self):
        if(self.tilt <= -MAX_TILT):
            self.tilt = -MAX_TILT
        self.tilt = self.tilt - 0.25
        self.xPos = self.xPos - 0.01
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

# Lift the plane up
    def liftUp(self):
        if(self.lift >= MAX_LIFT):
            self.lift = MAX_LIFT
        self.lift = self.lift + 0.25
        self.yPos = self.yPos + 0.01
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

# Lift the plane down
    def liftDown(self):
        if(self.lift <= -MAX_LIFT):
            self.lift = -MAX_LIFT

        self.lift = self.lift - 0.25
        self.yPos = self.yPos - 0.01
        self.plane.setPosHpr(self.xPos, self.yPos, 0, DEFAULT_HEADING, self.lift, self.tilt)

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


