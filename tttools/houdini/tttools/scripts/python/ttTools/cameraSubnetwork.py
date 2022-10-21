


import hou

from .cameraParm    import CameraParm


class CameraSubnetwork(object):

    def __init__(self, subnetwork=None):
        
        self.subnetwork = subnetwork

    def camExist(self, name: str):
        """ Check if the camera exist in the subnetwork

        Args:
            name (str) : The name of the camera.
        """
        return self.subnetwork.node(name)

    def addCam(self, name: str):
        pass

    def removeCam(self, name: str):
        pass

    def renameCam(self, name: str, oldName: str):
        pass

    def connectParams(self, camParms: CameraParm):
        """ Connect the camera HDA parameters with the subnetwork camera.

        Args:
            camParms (:class:`CameraParm`) : The camera parameter to connect.
        """
        cam = self.camExist(camParms.name)
        if(cam):
            self.disconnectParams(camParms.name)


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
        pass

    @property
    def cameras(self):
        return [node for node in self.camerasNetwork.children() if node.type().name() == "cam"]