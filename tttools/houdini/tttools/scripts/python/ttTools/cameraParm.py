
import hou

class CameraParm(object):

    def __init__(self):

        self.node   = None
        self.id     = 0

    @property
    def name(self):
        return self.node.parm("camName%d" % self.id).evalAsString()

    @name.setter
    def name(self, value):
        self.node.parm("camName%d" % self.id).set(value)

    @property
    def imageWidth(self):
        return self.node.parm("camImageSize%dx" % self.id).eval()

    @imageWidth.setter
    def imageWidth(self, value):
        self.node.parm("camImageSize%dx" % self.id).set(value)

    @property
    def imageHeight(self):
        return self.node.parm("camImageSize%dy" % self.id).eval()

    @imageHeight.setter
    def imageHeight(self, value):
        self.node.parm("camImageSize%dy" % self.id).set(value)

    @property
    def focal(self):
        return self.node.parm("camFocal%d" % self.id).eval()

    @focal.setter
    def focal(self, value):
        self.node.parm("camFocal%d" % self.id).set(value)

    @property
    def aperture(self):
        return self.node.parm("camAperture%d" % self.id).eval()
    
    @aperture.setter
    def aperture(self, value):
        self.node.parm("camAperture%d" % self.id).set(value)

    @property
    def focusPart(self):
        return self.node.parm("camFocus%d" % self.id).evalAsString()
    
    @focusPart.setter
    def focusPart(self, value):
        self.node.parm("camFocus%d" % self.id).set(value)

    @property
    def assetPivot(self, value):
        return self.node.parm("camFocusAssetPivot%d" % self.id).evalAsString()
