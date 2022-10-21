
import hou

class CameraParm(object):

    def __init__(self):

        self.node   = None
        self.id     = 0

    def setName(self):
        """ Init the camera name if not correct.
        """
        if(self.name == "camera"):
            self.name = "camera%d" % self.id

    def parmNameWithID(self, parmName):
        """ Return the parameter name with the camera id.
        """
        return "%s%d" % (parmName, self.id)

    def getStringParmValue(self, parmName):
        """ Return the string value of a parameter.

        Args:
            parmName (str) : The name of the parameter.
        """
        return self.node.parm(self.parmNameWithID(parmName)).evalAsString()

    def getParmValue(self, parmName, multi=None):
        """ Return the value of a parameter.

        Args:
            parmName    (str)           : The name of the parameter.
            multi       (str or None)   : Set letter to get a value of the vector parameter. 
        """
        if(multi):
            return self.node.parm("%s%d%s" % (parmName, self.id, multi)).eval()
        
        return self.node.parm("%s%d" % (parmName, self.id)).eval() 

    def setParmValue(self, parmName, value, multi=None):
        """ Set the value of a parameter.

        Args:
            parmName    (str)               : The name of the parameter.
            value       (int, float, str)   : The value of the parameter.
            multi       (str or None)       : Set letter to set a value of the vector parameter
        """
        if(multi):
            self.node.parm("%s%d%s" % (parmName, self.id, multi)).set(value)
        else:
            self.node.parm(self.parmNameWithID(parmName)).set(value)

    @property
    def name(self):
        return self.getStringParmValue("camName")

    @name.setter
    def name(self, value):
        self.setParmValue("camName", value)

    @property
    def oldName(self):
        return self.getStringParmValue("camOldName")

    @oldName.setter
    def oldName(self, value):
        self.setParmValue("camOldName", value)

    @property
    def imageWidth(self):
        return self.getParmValue("camImageSize", "x")

    @imageWidth.setter
    def imageWidth(self, value):
        self.setParmValue("camImageSize", value, "x")

    @property
    def imageHeight(self):
        return self.getParmValue("camImageSize", "y")

    @imageHeight.setter
    def imageHeight(self, value):
        self.setParmValue("camImageSize", value, "y")

    @property
    def focal(self):
        return self.getParmValue("camFocal")

    @focal.setter
    def focal(self, value):
        self.setParmValue("camFocal", value)

    @property
    def aperture(self):
        return self.getParmValue("camAperture")
    
    @aperture.setter
    def aperture(self, value):
        self.setParmValue("camAperture", value)

    @property
    def focus(self):
        return self.getParmValue("camFocus")
    
    @focus.setter
    def focus(self, value):
        self.setParmValue("camFocus", value)

    @property
    def assetPivot(self):
        return self.getStringParmValue("ttAssetPivot")
    
    @assetPivot.setter
    def assetPivot(self, value):
        self.setParmValue("ttAssetPivot", value)
    
    @property
    def preset(self):
        return self.getParmValue("ttPreset")
    
    @preset.setter
    def preset(self, value):
        self.setParmValue("ttPreset", value)
    
    @property
    def assetRotationY(self):
        return self.getParmValue("ttAssetRotationY")
    
    @assetRotationY.setter
    def assetRotationY(self, value):
        self.setParmValue("ttAssetRotationY", value)
    
    @property
    def assetRotationX(self):
        return self.getParmValue("ttAssetRotationX")
    
    @assetRotationX.setter
    def assetRotationX(self, value):
        self.setParmValue("ttAssetRotationX", value)
    
    @property
    def hdriRotationY(self):
        return self.getParmValue("ttHDRIRotationY")
    
    @hdriRotationY.setter
    def hdriRotationY(self, value):
        self.setParmValue("ttHDRIRotationY", value)
    
    @property
    def hdriSelect(self):
        return self.getStringParmValue("hdriSelect")
    
    @hdriSelect.setter
    def hdriSelect(self, value):
        self.setParmValue("hdriSelect", value)
    
    @property
    def hdriIntensity(self):
        return self.getParmValue("hrdiIntensity")
    
    @hdriIntensity.setter
    def hdriIntensity(self, value):
        self.setParmValue("hdriIntensity", value)
    
    @property
    def hdriUseBackgroundColor(self):
        return self.getParmValue("hdriUseBGColor")
    
    @hdriUseBackgroundColor.setter
    def hdriUseBackgrounfColor(self, value):
        self.setParmValue("hdriUseBGColor", value)

    @property
    def hdriBackgroundColor(self):
        return self.getParmValue("hdriBGColor")
    
    @hdriBackgroundColor.setter
    def hdriBackgroundColor(self, value):
        self.setParmValue("hdriBGColor", value)

    @property
    def assetSubdivisionType(self):
        return self.getParmValue("assetSubdivType")
    
    @assetSubdivisionType.setter
    def assetSubdivisionType(self, value):
        self.setParmValue("assetSubdivType", value)
    
    @property
    def assetSubdivisionIteration(self):
        return self.getParmValue("assetSubdivIter")
    
    @assetSubdivisionIteration.setter
    def assetSubdivisionIteration(self, value):
        self.setParmValue("assetSubdivIter", value)

    @property
    def shaderPreset(self):
        return self.getParmValue("shaderPreser")
    
    @shaderPreset.setter
    def shaderPreset(self, value):
        self.setParmValue("shaderPreset")

    @property
    def shaderMaterialX(self):
        return self.getStringParmValue("shaderMaterialXFile")
    
    @shaderMaterialX.setter
    def shaderMaterialX(self, value):
        self.setParmValue("shaderMaterialXFile", value)

