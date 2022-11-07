


import hou

from .cameraParm    import CameraParm


class CameraSubnetwork(object):

    def __init__(self, subnetwork=None, hdaCameraParms=None):
        
        self.subnetwork     = subnetwork
        self.hdaCameras     = hdaCameraParms

    def camExist(self, name: str):
        """ Check if the camera exist in the subnetwork

        Args:
            name (str) : The name of the camera.
        """
        return self.subnetwork.node(name)

    def addCam(self, camParm: CameraParm):
        """ Add the camera in the camera subnetwork.

        Args:
           camParm    (:class:`CameraParm`) :     The node camera parameter.

        Returns:
            hou.Node : The camera node.

        """
        cam = self.camExist(camParm.name)
        if not(cam):
            cam = self.subnetwork.createNode("cam", node_name=camParm.name)
            self.connectParams(camParm)
            self.subnetwork.layoutChildren()
        
        return cam

    def removeCam(self, name: str):
        """ Remove the camera from the subnetwork.

        Args:
            name (str) :    The name of the camera to remove.
        """
        cam = self.camExist(name)
        cam.destroy()

        self.subnetwork.layoutChildren()

    def renameCam(self, name: str, oldName: str):
        """ Rename the camera with old name to name.

        Args:
            name    (str)   : The name of the camera.
            oldName (str)   : The old camera name.
        """
        cam = self.camExist(oldName)
        cam.setName(name)

        return cam

    def updateCam(self, camParm: CameraParm):
        """ Update the camera of the subnetwork with the hda camera parameters.

        Args:
            camParm (:class:`CameraParm`) :     The hda camera parameters.
        """
        cam = self.camExist(camParm.oldName)
        if(cam):
            self.renameCam(camParm.name, camParm.oldName)
            self.disconnectParams(camParm.name)
            self.connectParams(camParm)

    def connectParams(self, camParm: CameraParm):
        """ Connect the camera HDA parameters with the subnetwork camera.

        Args:
            camParm (:class:`CameraParm`) : The camera parameter to connect.
        """
        cam = self.camExist(camParm.name)
        if(cam):
            self.disconnectParams(camParm.name)
            cam.parm("resx").set(camParm.getParm("camImageSize", "x"))
            cam.parm("resy").set(camParm.getParm("camImageSize", "y"))
            cam.parm("focal").set(camParm.getParm("camFocal"))
            cam.parm("aperture").set(camParm.getParm("camAperture"))


    def disconnectParams(self, camName: str):
        """ Disconnect the camera HDA parameters.
        
        Args:
            camName (str) : The name of the camera.
        """
        cam = self.camExist(camName)
        if(cam):
            cam.parm("resx").deleteAllKeyframes()
            cam.parm("resy").deleteAllKeyframes()
            cam.parm("focal").deleteAllKeyframes()
            cam.parm("aperture").deleteAllKeyframes()

    def updateCameras(self):
        """ Update the subnetwork cameras from the hda cameras.
        """

        if(len(self.hdaCameras) > len(self.cameras)):
            # The hda camera count grow.
            for hdaCam in self.hdaCameras:
                self.addCam(hdaCam)

        elif(len(self.hdaCameras) < len(self.cameras)):
            # The hda camera count skrink
            for cam in self.cameras:
                hdaExist = False
                for hdaCam in self.hdaCameras:
                    if(cam.name() == hdaCam.name):
                        hdaExist = True
                        self.connectParams(hdaCam)
                        break
                if(hdaExist == False):
                    self.removeCam(cam.name())

    def updateCamerasNaming(self):
        """ Update the camera naming of the subnetwork with the hda camaras parms.
        """
        for cam in self.cameras:
            for hdaCam in self.hdaCameras:
                if(cam.name() == hdaCam.oldName):
                    if(hdaCam.name != hdaCam.oldName):
                        self.renameCam(hdaCam.name, hdaCam.oldName)
                        hdaCam.oldName = hdaCam.name
                        break



    @property
    def cameras(self):
        return [node for node in self.subnetwork.children() if node.type().name() == "cam"]