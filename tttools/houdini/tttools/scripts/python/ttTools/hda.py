
import os
import hou

from .hdaParms      import HDAParms
from .cameraParm    import CameraParm

class HDA(object):

    def __init__(self):
        
        self.node   = None


    def getCamerasList(self, node):
        """ Get the list of cameras from the hda parameters.

        Args:
            node (:class:`hou.Node`) :  The current HDA node.
        
        Returns:
            dict : The cameras list of the HDA.
        """
        camCount    = node.parm("cameras").eval()
        cameras     = {}

        for i in range(camCount):
            camDict = {}
            camDict["parmID"]   = i
            camDict["oldName"]  = node.parm("")

    def getCamerasNodes(self, camSubnet):
        """ Get the cameras node from the cameras subnetwork.

        Args:
            camSubnet (:class:`hou.Node`) :  The HDA cameras subnetwork.
        
        Returns:
            list(:class:`hou.Node`) : The list of cameras node in the cameras subnetwork.
        """
        return [node for node in camSubnet.children() if node.type().name() == "cam"]

    @property
    def assetName(self):
        return self.node.parm("assetName").evalAsString()

    @assetName.setter
    def assetName(self, value):
        self.node.parm("assetName").set(value)

    @property
    def step(self):
        return self.node.parm("step").evalAsString()

    @step.setter
    def step(self, value):
        self.node.parm("step").set(value)
    
    @property
    def task(self):
        return self.node.parm("task").evalAsString()

    @task.setter
    def task(self, value):
        self.node.parm("task").set(value)
    
    @property
    def user(self):
        return self.node.parm("user").evalAsString()
    
    @user.setter
    def user(self, value):
        self.node.parm("user").set(value)
    
    @property
    def geometryType(self):
        return self.node.parm("geoTypes").eval()
    
    @geometryType.setter
    def geometryType(self, value):
        self.node.parm("geoTypes").set(value)
    
    @property
    def geometryPath(self):
        return self.node.parm("geoPath").evalAsString()
    
    @geometryPath.setter
    def geometryPath(self, value):
        self.node.parm("geoPath").set(value)

    @property
    def camerasNetwork(self):
        self.node.node("CAMERAS")

    @property
    def subNetworkCameras(self):
        return [node for node in self.camerasNetwork.children() if node.type().name() == "cam"]

    @property
    def camerasCount(self):
        return self.node.parm("cameras").eval()
    
    @property
    def camerasParms(self):
        camCount = self.camerasCount
        return [CameraParm(self.node, i) for i in range(camCount)]
    

    