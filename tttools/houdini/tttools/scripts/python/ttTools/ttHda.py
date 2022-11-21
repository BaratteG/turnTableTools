
import os
import hou

from .hdaParms          import HDAParms
from .cameraParm        import CameraParm
from .cameraSubnetwork  import CameraSubnetwork

class TTHDA(object):

    def __init__(self):
        
        self.node   = None

    def renderLocal(self, node):
        """ Send the local render.
        """
        arnoldRenderNode = node.node("RENDER").node("ARNOLD")
        arnoldRenderNode.parm("execute").pressButton()


    def solveRenderPath(self, node):
        """ Build the render path from the asset infos.
        """
        # Update the current node.
        self.node = node

        pathTemplate  = "<rootPath><project>/assets/<category>/<assetName>/publish/<step>/v<version>/turn/<step>_<assetName>_<task>.<version>.$F4.exr"

        if(self.rootPath != "" and self.project != "" and self.assetName != "" and self.step != ""):

            path    = pathTemplate.replace("<rootPath>", self.rootPath)
            path    = path.replace("<project>", self.project)
            if(self.category != ""):
                path    = path.replace("<category>", self.category)
            else:
                path    = path.replace("/<category>", "")
            path    = path.replace("<assetName>", self.assetName)
            path    = path.replace("<step>", self.step)
            if(self.task != ""):
                path    = path.replace("<task>", self.task)
            else:
                path    = path.replace("_<task>", "")
            path    = path.replace("<version>", "%03d" % self.version)

            self.node.parm("arRenderFolder").set(path)
        
        else:
            self.node.parm("arRenderFolder").set("The Asset Infos Parameters are not correclty setup.")


    def turnTablePresetChanged(self, node):
        """ Update the turn table preset.

        Args:
            node (hou.node) : The current HDA node.
        """
        for hdaCam in self.camerasParms:
            if(hdaCam.preset != hdaCam.oldPreset):
                hdaCam.assetRotationY   = int(hdaCam.preset)
                hdaCam.assetRotationX   = int(hdaCam.preset)
                hdaCam.hdriRotationY    = int(hdaCam.preset)
                hdaCam.oldPreset        = hdaCam.preset

    def getMaxNamingID(self, namingMemory):
        """ Return the max camera auto naming index.
        """
        maxID = 0
        for naming in namingMemory:
            if(naming.find("camera") != -1):
                nameSplit = naming.split("camera")
                if(nameSplit[-1] != ""):
                    nameID = nameSplit[-1]
                    if(int(nameID) > maxID):
                        maxID = int(nameID)
        
        return maxID

    def getAssetInfosFromSG(self, node: hou.Node):
        """ Update the asset infos from shotgrid context.

        Args:
            node (:class:`hou.Node`) : The current HDA node.
        """
        self.node = node

        rootPath    = ""
        project     = ""
        category    = ""
        asset       = ""
        step        = ""
        task        = ""
        user        = ""

        try:
            import  sgtk
            import  os

            engine  = sgtk.platform.current_engine()
            tk      = engine.sgtk
            sg      = engine.shotgun

            try:
                context     = engine.context

                sgStep      = context.step
                sgStep      = sg.find_one("Step", [["id", "is", sgStep["id"]]], ["short_name"])

                sgEntity    = context.entity
                sgEntity    = sg.find_one("Asset", [["id", "is", sgEntity["id"]]], ["sg_asset_type", "code"])

                project     = context.project["name"]
                rootPath    = tk.project_path.split(project)[0]
                category    = sgEntity["sg_asset_type"]
                asset       = sgEntity["code"]
                step        = sgStep["short_name"]
                task        = context.task["name"]
                user        = context.user["name"]

            except:
                warningMsg  = "Not Context Selected !"
                rootPath    = warningMsg
                project     = warningMsg
                category    = warningMsg
                asset       = warningMsg
                step        = warningMsg
                task        = warningMsg
                user        = warningMsg
        except:
            warningMsg  = "ShotGrid Tool Kit not found !"
            rootPath    = warningMsg
            project     = warningMsg
            category    = warningMsg
            asset       = warningMsg
            step        = warningMsg
            task        = warningMsg
            user        = warningMsg

        self.node.parm("rootPath").set(rootPath)
        self.node.parm("project").set(project)
        self.node.parm("assetName").set(asset)
        self.node.parm("category").set(category)
        self.node.parm("step").set(step)
        self.node.parm("task").set(task)
        self.node.parm("userName").set(user)

    def setHDADefaultCameraName(self):
        """ Set the default rename naming.

        Args:
            node (hou.node) : The current HDA node.
        """
        namingMemory    = [hdaCam.name for hdaCam in self.camerasParms]
        startID         = self.getMaxNamingID(namingMemory)+1

        for hdaCam in self.camerasParms:
            if(hdaCam.name == "camera"):
                camName = "camera%d" % startID
                hdaCam.name     = camName
                hdaCam.oldName  = camName
                startID += 1

    def cameraNameChanged(self, node):
        """ Launch when camera name change.

        Args :
            node (hou.Node) : The current HDA node.
        """
        # Update the current node.
        self.node = node
        # Get the cameras subnetwork.
        camNetwork = self.camerasNetwork
        # Update teh cameras subnetwork.
        camNetwork.updateCamerasNaming()    

    def camerasCountChanged(self, node):
        """ Launch when the camera count change.

        Args:
            node (hou.Node) :   The current HDA node.
        """
        # Update the current node.
        self.node = node
        # Set the camera default naming.
        self.setHDADefaultCameraName()
        # Get the cameras subnetwork.
        camNetwork = self.camerasNetwork
        # Update teh cameras subnetwork.
        camNetwork.updateCameras()

    def useMaterialX(self, node):
        """ Launch when select shaders.

        Args :
            node (hou.Node) : The current HDA node.
        """
        # Update the current node.
        self.node = node
        # Get the cameras datas.
        useMaterialX = False
        for camParm in self.camerasParms:
            if(camParm.shaderPreset == 8):
                useMaterialX = True
                break

        # Add expression to the material X node.
        matXNode = self.getMaterialXNode
       
        if(useMaterialX is True):
            matXNode.parm("filename").setExpression("details('../../MIXER/CAM_MIX', 'shaderMaterialX')", language=hou.exprLanguage.Hscript)
        else:
            matXNode.parm("filename").deleteAllKeyframes()

    @property
    def rootPath(self):
        return self.node.parm("rootPath").evalAsString()
    
    @rootPath.setter
    def rootPath(self, value):
        self.node.parm("rootPath").set(value)


    @property
    def project(self):
        return self.node.parm("project").evalAsString()

    @project.setter
    def project(self, value):
        self.node.parm("project").set(value)

    @property
    def category(self):
        return self.node.parm("category").evalAsString()

    @category.setter
    def category(self, value):
        self.node.parm("category").set(value)

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
    def version(self):
        return self.node.parm("version").eval()

    @version.setter
    def version(self, value):
        self.node.parm("version").set(value)

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
        return CameraSubnetwork(subnetwork=self.node.node("CAMERAS"), hdaCameraParms=self.camerasParms)

    @property
    def camerasCount(self):
        return self.node.parm("cameras").eval()
    
    @property
    def camerasParms(self):
        camCount = self.camerasCount
        return [CameraParm(self.node, i) for i in range(camCount)]
    
    @property
    def getMaterialXNode(self):
        return self.node.node("RENDER").node("materialx")
    

    