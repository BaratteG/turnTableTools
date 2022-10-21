
import os
import hou

class HDAParms(object):

    def __init__(self, node=None):

        self.node   = node

        self.bmPreset = {
            "0" : {
                "chromeBallLocationx"   : 0.03,
                "chromeBallLocationy"   : 0.07,
                "chromeBallSize"        : 0.03,
                "blackBallLocationx"    : 0.18,
                "blackBallLocationy"    : 0.07,
                "blackBallSize"         : 0.03,
                "greyBallLocationx"     : 0.13,
                "greyBallLocationy"     : 0.07,
                "greyBallSize"          : 0.03,
                "whiteBallLocationx"    : 0.08,
                "whiteBallLocationy"    : 0.07,
                "whiteBallSize"         : 0.03,
                "macbethLocationx"      : 0.93,
                "macbethLocationy"      : 0.1,
                "macbethSize"           : 0.08
            },
            "1" : {
                "chromeBallLocationx"   : 0.03,
                "chromeBallLocationy"   : 0.95,
                "chromeBallSize"        : 0.03,
                "blackBallLocationx"    : 0.03,
                "blackBallLocationy"    : 0.87,
                "blackBallSize"         : 0.03,
                "greyBallLocationx"     : 0.03,
                "greyBallLocationy"     : 0.79,
                "greyBallSize"          : 0.03,
                "whiteBallLocationx"    : 0.03,
                "whiteBallLocationy"    : 0.71,
                "whiteBallSize"         : 0.03,
                "macbethLocationx"      : 0.07,
                "macbethLocationy"      : 0.1,
                "macbethSize"           : 0.08
            }
        }

        self.arRenderPreset = {
            "1" : {
                "arSampleCamera"        : 3,
                "arSampleDiffuse"       : 2,
                "arSampleSpecular"      : 2,
                "arSampleTransmission"  : 2,
                "arSampleSSS"           : 2,
                "arSampleVolume"        : 2
            },
            "0" : {
                "arSampleCamera"        : 6,
                "arSampleDiffuse"       : 2,
                "arSampleSpecular"      : 3,
                "arSampleTransmission"  : 2,
                "arSampleSSS"           : 5,
                "arSampleVolume"        : 2
            },
            "2" : {
                "arSampleCamera"        : 2,
                "arSampleDiffuse"       : 1,
                "arSampleSpecular"      : 1,
                "arSampleTransmission"  : 1,
                "arSampleSSS"           : 1,
                "arSampleVolume"        : 1
            },
        }

        self.ttPreset = {
            "72" : {
                "assetRotationY" : 72,
                "assetRotationX" : 72,
                "hdriRotationY"  : 72
            },
            "24" : {
                "assetRotationY" : 24,
                "assetRotationX" : 24,
                "hdriRotationY"  : 24
            },
            "12" : {
                "assetRotationY" : 12,
                "assetRotationX" : 12,
                "hdriRotationY"  : 12
            }
        }


    def getAssetParts(self, node: hou.Node):
        """ Get the asset part list from the asset geometry group.

        Args:
            node (:class:`hou.Node`) : The current HDA node.
        """
        # Update the current node.
        self.node = node
        # Get the asset geometry node.
        assetNode = self.node.node("ASSET").node("OUT_FOCUS_CAMERA")
        # Get the asset geometry primitive group list.
        assetGeo = assetNode.geometry()
        if(assetGeo):
            groupList = assetGeo.primGroups()
            # Define the menulist.
            menulist = ["free", "free"]
            for group in groupList:
                menulist.append(group.name())
                menulist.append(group.name())

            return menulist
        
        return ["No Geoemetry", "No Geometry"]

    def getHDRIListFromFolder(self, node: hou.Node):
        """ Get the list of the hdri file in the hdri folder.

        Args:
            node (:class:`hou.Node`) : The current HDA node.
        """
        # Update the current node.
        self.node = node
        # Get the hdri folder.
        hdriFolder = self.node.parm("hdriPath").evalAsString()
        # Check if the folder exist.
        if(os.path.exists(hdriFolder)):
            # Get the hdri file in the folder.
            files = [file for file in os.listdir(hdriFolder) 
                if os.path.isfile(os.path.join(hdriFolder, file)) and
                (file.split(".")[-1] == "hdr" or file.split(".")[-1] == "exr")]
            # Build the menu list array.
            menuList = []
            for file in files:
                menuList.append(file)
                menuList.append(file)
            
            return menuList

        return ["No File", "No File"]

    def applyPreset(self, preset: dict, presetMenu: str):
        """ Apply a preset from the menu parameters value.

        Args:
            preset      (dict)  : The preset to apply.
            presetMenu  (str)   : The menu parameters name.
        """
        # Get the preset to use.
        presetName = self.node.parm(presetMenu).evalAsString()
        # Get the preset and apply to parameters.
        for parmName in preset[presetName]:
            self.node.parm(parmName).set(preset[presetName][parmName])
        
    def applyArnoldRenderPreset(self, node: hou.Node):
        """ Apply the arnold preset.

        Args:
            node      (:class:`hou.Node`)  : The current hda node.
        """
        # update the current node to update the good hda instance.
        self.node = node
        # Apply the preset.
        self.applyPreset(self.arRenderPreset, "arPreset")

    def applyBallsMacbethPreset(self, node: hou.Node):
        """ Apply the balls and macbeth preset.

        Args:
            node      (:class:`hou.Node`)  : The current hda node.
        """
        # update the current node to update the good hda instance.
        self.node = node
        # Apply the preset.
        self.applyPreset(self.bmPreset, "bmPreset")


    def buildUI(self):
        """ Build the HDA UI.
        """

        # Get the hda parm template group.
        ptg = self.node.parmTemplateGroup()

        self.addAssetFolder(ptg)
        self.addCameras(ptg)
        self.addBallsAndMacbeth(ptg)
        self.addHRDITexPath(ptg)
        self.addArnold(ptg)

        self.node.setParmTemplateGroup(ptg)

    def addArnold(self, ptg: hou.ParmTemplateGroup):
        """ Add the asset folder and parameters.

        Args:
            ptg (:class:`hou.ParmTemplateGroup`) : The parameter template to add the folder and parameters.
        """ 
        folder              = hou.FolderParmTemplate("arnoldTab", "Arnold", folder_type=hou.folderType.Tabs)

        presetScript        = "hou.phm().dataUI.applyArnoldRenderPreset(kwargs['node'])"
        preset              = hou.MenuParmTemplate("arPreset", "Preset",
            ("0", "1", "2"), 
            menu_labels=("Hi Quality", "MI Qualtity", "LO Quality"), 
            default_value=1,
            script_callback=presetScript,
            script_callback_language=hou.scriptLanguage.Python)

        renderFolder        = hou.StringParmTemplate("arRenderFolder", "Render Folder", 1, string_type=hou.stringParmType.FileReference)

        sampleFolder        = hou.FolderParmTemplate("arSamplesOpt", "Samples", folder_type=hou.folderType.Simple)
        sCam                = hou.IntParmTemplate("arSampleCamera", "Camera (AA)", 1, default_value=[3], min=0, max=10)
        sDiffuse            = hou.IntParmTemplate("arSampleDiffuse", "Diffuse", 1, default_value=[2], min=0, max=10)
        sSpecular           = hou.IntParmTemplate("arSampleSpecular", "Specular", 1, default_value=[2], min=0, max=10)
        sSSS                = hou.IntParmTemplate("arSampleSSS", "SSS", 1, default_value=[2], min=0, max=10)
        sTransmission       = hou.IntParmTemplate("arSampleTransmission", "Transmission", 1, default_value=[2], min=0, max=10)
        sVolume             = hou.IntParmTemplate("arSampleVolume", "Volume Direct", 1, default_value=[2], min=0, max=10)
        sampleFolder.addParmTemplate(sCam)
        sampleFolder.addParmTemplate(sDiffuse)
        sampleFolder.addParmTemplate(sSpecular)
        sampleFolder.addParmTemplate(sSSS)
        sampleFolder.addParmTemplate(sTransmission)
        sampleFolder.addParmTemplate(sVolume)

        rayFolder           = hou.FolderParmTemplate("arRayDepthOpt", "Ray Depth", folder_type=hou.folderType.Simple)
        rTotal              = hou.IntParmTemplate("arRayTotal", "Total", 1, default_value=[10], min=0, max=30)
        rDiffuse            = hou.IntParmTemplate("arRayDiffuse", "Diffuse", 1, default_value=[1], min=0, max=30)
        rSpecular           = hou.IntParmTemplate("arRaySpecular", "Specular", 1, default_value=[1], min=0, max=30)
        rTransmission       = hou.IntParmTemplate("arRayTransmission", "Transmission", 1, default_value=[8], min=0, max=30)
        rVolume             = hou.IntParmTemplate("arRayVolume", "Volume", 1, default_value=[0], min=0, max=30)
        rTransparency       = hou.IntParmTemplate("arRayTransparency", "Transparency", 1, default_value=[10], min=0, max=30)
        rayFolder.addParmTemplate(rTotal)
        rayFolder.addParmTemplate(rDiffuse)
        rayFolder.addParmTemplate(rSpecular)
        rayFolder.addParmTemplate(rTransmission)
        rayFolder.addParmTemplate(rVolume)
        rayFolder.addParmTemplate(rTransparency)

        folder.addParmTemplate(preset)
        folder.addParmTemplate(renderFolder)
        folder.addParmTemplate(sampleFolder)
        folder.addParmTemplate(rayFolder)

        ptg.addParmTemplate(folder)

    def addBallsAndMacbeth(self, ptg: hou.ParmTemplateGroup):
        """ Add the asset folder and parameters.

        Args:
            ptg (:class:`hou.ParmTemplateGroup`) : The parameter template to add the folder and parameters.
        """
        folder              = hou.FolderParmTemplate("bmTab", "Balls and Macbeth", folder_type=hou.folderType.Tabs)

        presetScript        = "hou.phm().dataUI.applyBallsMacbethPreset(kwargs['node'])"
        preset              = hou.MenuParmTemplate("bmPreset", "Preset",
            ("0", "1"), 
            menu_labels=("horizontal", "vertical"),
            script_callback=presetScript,
            script_callback_language=hou.scriptLanguage.Python)

        chromeBallFolder    = hou.FolderParmTemplate("chromeBallOpt", "Chrome Ball", folder_type=hou.folderType.Simple)
        chromeBallLocation  = hou.FloatParmTemplate("chromeBallLocation", "Screen Location", 2, default_value=[0.03, 0.07])
        chromeBallSize      = hou.FloatParmTemplate("chromeBallSize", "Screen Size", 1, default_value=[0.03])
        chromeBallFolder.addParmTemplate(chromeBallLocation)
        chromeBallFolder.addParmTemplate(chromeBallSize)

        whiteBallFolder    = hou.FolderParmTemplate("whiteBallOpt", "White Ball", folder_type=hou.folderType.Simple)
        whiteBallLocation  = hou.FloatParmTemplate("whiteBallLocation", "Screen Location", 2, default_value=[0.08, 0.07])
        whiteBallSize      = hou.FloatParmTemplate("whiteBallSize", "Screen Size", 1, default_value=[0.03])
        whiteBallFolder.addParmTemplate(whiteBallLocation)
        whiteBallFolder.addParmTemplate(whiteBallSize)

        greyBallFolder    = hou.FolderParmTemplate("greyBallOpt", "Grey Ball", folder_type=hou.folderType.Simple)
        greyBallLocation  = hou.FloatParmTemplate("greyBallLocation", "Screen Location", 2, default_value=[0.13, 0.07])
        greyBallSize      = hou.FloatParmTemplate("greyBallSize", "Screen Size", 1, default_value=[0.03])
        greyBallFolder.addParmTemplate(greyBallLocation)
        greyBallFolder.addParmTemplate(greyBallSize)

        blackBallFolder    = hou.FolderParmTemplate("blackBallOpt", "Black Ball", folder_type=hou.folderType.Simple)
        blackBallLocation  = hou.FloatParmTemplate("blackBallLocation", "Screen Location", 2, default_value=[0.18, 0.07])
        blackBallSize      = hou.FloatParmTemplate("blackBallSize", "Screen Size", 1, default_value=[0.03])
        blackBallFolder.addParmTemplate(blackBallLocation)
        blackBallFolder.addParmTemplate(blackBallSize)

        macbethFolder    = hou.FolderParmTemplate("macbethOpt", "Macbeth", folder_type=hou.folderType.Simple)
        macbethLocation  = hou.FloatParmTemplate("macbethLocation", "Screen Location", 2, default_value=[0.93, 0.01])
        macbethSize      = hou.FloatParmTemplate("macbethSize", "Screen Size", 1, default_value=[0.08])
        macbethFolder.addParmTemplate(macbethLocation)
        macbethFolder.addParmTemplate(macbethSize)

        folder.addParmTemplate(preset)
        folder.addParmTemplate(chromeBallFolder)
        folder.addParmTemplate(whiteBallFolder)
        folder.addParmTemplate(greyBallFolder)
        folder.addParmTemplate(blackBallFolder)
        folder.addParmTemplate(macbethFolder)

        ptg.addParmTemplate(folder)      

    def addAssetFolder(self, ptg: hou.ParmTemplateGroup):
        """ Add the asset folder and parameters.

        Args:
            ptg (:class:`hou.ParmTemplateGroup`) : The parameter template to add the folder and parameters.
        """

        folder      = hou.FolderParmTemplate("assetTab", "Asset", folder_type=hou.folderType.Tabs)
        assetName   = hou.StringParmTemplate("assetName", "Asset Name", 1)
        task        = hou.StringParmTemplate("task", "Task", 1)
        step        = hou.StringParmTemplate("step", "Step", 1)
        geoType     = hou.MenuParmTemplate("geoType", "Type", ("0","1","2","3","4"), menu_labels=("ABC", "OBJ", "BGEO", "VDB", "ASS"))
        geoPath     = hou.StringParmTemplate("geoPath", "Path", 1, string_type=hou.stringParmType.FileReference)

        folder.addParmTemplate(assetName)
        folder.addParmTemplate(step)
        folder.addParmTemplate(task)
        folder.addParmTemplate(geoType)
        folder.addParmTemplate(geoPath)

        ptg.addParmTemplate(folder)
    
    def addHRDITexPath(self, ptg: hou.ParmTemplateGroup):
        """ Add the HDRI and texture path.

        Args:
            ptg (:class:`hou.ParmTemplateGroup`) : The parameter template to add the folder and parameters.
        """

        folder      = hou.FolderParmTemplate("hdriTexTab", "HDRI and Textures Paths", folder_type=hou.folderType.Tabs)
        hdriPath    = hou.StringParmTemplate("hdriPath", "HRDI Folder", 1, string_type=hou.stringParmType.FileReference, default_expression=["$TT_HDRI"])
        texPath     = hou.StringParmTemplate("texPath", "Texture Folder", 1, string_type=hou.stringParmType.FileReference, default_expression=["$TT_TEX"])

        folder.addParmTemplate(hdriPath)
        folder.addParmTemplate(texPath)

        ptg.addParmTemplate(folder)

    def addCamera(self, parent: hou.ParmTemplate):
        """ Add camera folder to multi parms.

        Args:
            ptg (:class:`hou.ParmTemplate`) : The parameter template to add the folder and parameters.
        """
        camFolder       = hou.FolderParmTemplate("cameraOpt#", "Camera", folder_type=hou.folderType.Collapsible)
        camName         = hou.StringParmTemplate("camName#", "Name", 1, default_value=["camera"])
        camImageSize    = hou.FloatParmTemplate("camImageSize#", "Image Size", 2, default_value=[1920, 1080])
        camFocal        = hou.FloatParmTemplate("camFocal#", "Focal", 1, default_value=[50.0], min=0.0, max=1000.0)
        camAperture     = hou.FloatParmTemplate("camAperture#", "Aperture", 1, default_value=[41.4214], min=0.0, max=90.0)
        camFocusScript  = """items = hou.phm().dataUI.getAssetParts(kwargs['node'])\nreturn items"""
        camFocus        = hou.MenuParmTemplate("camFocus#", "Focus", (), item_generator_script=camFocusScript, default_value=1)

        camFolder.addParmTemplate(camName)
        camFolder.addParmTemplate(camImageSize)
        camFolder.addParmTemplate(camFocal)
        camFolder.addParmTemplate(camAperture)
        camFolder.addParmTemplate(camFocus)

        parent.addParmTemplate(camFolder)

    def addTurnTable(self, parent: hou.ParmTemplate):
        """ Add camera folder to multi parms.

        Args:
            ptg (:class:`hou.ParmTemplate`) : The parameter template to add the folder and parameters.
        """ 
        folder              = hou.FolderParmTemplate("turnTableOpt#", "Turn Table", folder_type=hou.folderType.Collapsible)

        assetPivotScript    = """items = hou.phm().dataUI.getAssetParts(kwargs['node'])\nreturn items"""
        assetPivot          = hou.MenuParmTemplate("ttAssetPivot#", "Asset Pivot", (), item_generator_script=assetPivotScript, default_value=1)
        preset              = hou.MenuParmTemplate("ttPreset#", "Preset", ("72", "24", "12"))
        assetRotationY      = hou.IntParmTemplate("ttAssetRotationY#", "Asset Rotation Y", 1, default_value=[72], min=1, max=200)
        assetRotationX      = hou.IntParmTemplate("ttAssetRotationX#", "Asset Rotation X", 1, default_value=[72], min=1, max=200)
        hdriRotationY       = hou.IntParmTemplate("ttHDRIRotationY#", "HDRI Rotation Y", 1, default_value=[72], min=1, max=200)

        folder.addParmTemplate(assetPivot)
        folder.addParmTemplate(preset)
        folder.addParmTemplate(assetRotationY)
        folder.addParmTemplate(assetRotationX)
        folder.addParmTemplate(hdriRotationY)

        parent.addParmTemplate(folder)

    def addHDRI(self, parent: hou.ParmTemplate):
        """ Add camera folder to multi parms.

        Args:
            ptg (:class:`hou.ParmTemplate`) : The parameter template to add the folder and parameters.
        """
        folder          =  hou.FolderParmTemplate("hdriOpt#", "HDRI", folder_type=hou.folderType.Collapsible)

        select          = hou.MenuParmTemplate("hdriSelect#", "Select", (),
            item_generator_script= "items = hou.phm().dataUI.getHDRIListFromFolder(kwargs['node'])\nreturn items")
        intensity       = hou.FloatParmTemplate("hdriIntensity#", "Intensity", 1, default_value=[1.0], min=1, max=20)
        useBGColor      = hou.ToggleParmTemplate("hdriUseBGColor#", "Use Background Color", default_value=True)
        bgColor         = hou.FloatParmTemplate("hdriBGColor#", "Background Color", 3, default_value=[0.18, 0.18, 0.18], 
            look=hou.parmLook.ColorSquare, 
            naming_scheme=hou.parmNamingScheme.RGBA,
            disable_when="{ hdriUseBGColor# == 0 }")

        folder.addParmTemplate(select)
        folder.addParmTemplate(intensity)
        folder.addParmTemplate(useBGColor)
        folder.addParmTemplate(bgColor)

        parent.addParmTemplate(folder)

    def addAsset(self, parent: hou.ParmTemplate):
        """ Add camera folder to multi parms.

        Args:
            ptg (:class:`hou.ParmTemplate`) : The parameter template to add the folder and parameters.
        """
        folder          = hou.FolderParmTemplate("assetOpt#", "Asset", folder_type=hou.folderType.Collapsible)

        subdivFolder    = hou.FolderParmTemplate("assetSubdivOpt#", "Subdivision", folder_type=hou.folderType.Simple)

        subdivType      = hou.MenuParmTemplate("assetSubdivType#", "Type", ("none", "catclark", "linear"), menu_labels=("None", "Catmull-Clark", "Linear"))
        subdivIteration = hou.IntParmTemplate("assetSubdivIter#", "Iteration", 1, default_value=[1], min=0, max=10, disable_when="{ assetSubdivType# == none }")

        subdivFolder.addParmTemplate(subdivType)
        subdivFolder.addParmTemplate(subdivIteration)

        shaderFolder    = hou.FolderParmTemplate("assetShaderOpt#", "Shader", folder_type=hou.folderType.Simple)

        shaderPreset    = hou.MenuParmTemplate("assetShaderPreset#", "Preset", 
            ("0", "1", "2", "3", "4", "5", "6"), 
            menu_labels=("Custom", "Clay", "Chrome", "Black", "Wires", "Glass", "Material X"),
            default_value=1)
        shaderMatX      = hou.StringParmTemplate("assetMaterialXFile#", "Material X File", 1, string_type=hou.stringParmType.FileReference, disable_when="{ assetShaderPreset# != 6 }")

        shaderFolder.addParmTemplate(shaderPreset)
        shaderFolder.addParmTemplate(shaderMatX)

        folder.addParmTemplate(subdivFolder)
        folder.addParmTemplate(shaderFolder)

        parent.addParmTemplate(folder)       

    def addCameras(self, ptg: hou.ParmTemplateGroup):
        """ Add the HDRI and texture path.

        Args:
            ptg (:class:`hou.ParmTemplateGroup`) : The parameter template to add the folder and parameters.
        """
        folder          = hou.FolderParmTemplate("camerasTab", "Cameras", folder_type=hou.folderType.Tabs)
        cameras         = hou.FolderParmTemplate("cameras", "Cameras", folder_type=hou.folderType.MultiparmBlock, tags={"multistartoffset":"0"})

        endSep          = hou.SeparatorParmTemplate("endSep#")

        self.addCamera(cameras)
        self.addTurnTable(cameras)
        self.addHDRI(cameras)
        self.addAsset(cameras)
        cameras.addParmTemplate(endSep)

        folder.addParmTemplate(cameras)

        ptg.addParmTemplate(folder)


