#ifndef __TURN_TABLE_UTILITY__
#define __TURN_TABLE_UTILITY__



struct HDAParameters{

    string  hdaRelativePath = "../../";
    int     camID           = 0;
    
    vector2 camImageSize;
    float   camFocal;
    float   camAperture;
    
    string  focusPart;

    string  ttAssetPivot;
    int     ttAssetRotationX;
    int     ttAssetRotationY;
    int     ttHDRIRotationY;

    string  hdriPaht;
    string  hdriFile;
    float   hdriIntensity;
    int     hdriUseBGColor;
    vector  hdriBGColor;

    string  subdivType;
    int     subdivIteration;

    int     shaderPreset;
    string  shaderMaterialX;

    int
    getIntParm(
        string  parmName)
    {
        return chi(concat(this.hdaRelativePath, parmName, itoa(this.camID)));
    }

    float
    getFloatParm(
        string parmName)
    {
        return chf(concat(this.hdaRelativePath, parmName, itoa(this.camID)));
    }

    vector2
    getVector2Parm(
        string parmName)
    {
        return chu(concat(this.hdaRelativePath, parmName, itoa(this.camID)));
    }

    vector
    getVector3Parm(
        string parmName)
    {
        return chv(concat(this.hdaRelativePath, parmName, itoa(this.camID)));
    }

    string
    getStringParm(
        string parmName)
    {
        return chs(concat(this.hdaRelativePath, parmName, itoa(this.camID)));
    }

    int
    getCameraFrames()
    {
        int assetRotationX  = this->getIntParm("camAssetAxisX");
        int assetRotationY  = this->getIntParm("camAssetAxisY");
        int hdriRotationX   = this->getIntParm("camHDRIAxisY");

        return assetRotationX + assetRotationY + hdriRotationX;
    }

    void 
    getHDAParameters(
        int camID)
    {
        this.camID              = camID;
        this.camImageSize       = this->getVector2Parm("camImageSize");
        this.camFocal           = this->getFloatParm("camFocal");
        this.camAperture        = this->getFloatParm("camAperture");
        this.focusPart          = this->getStringParm("camFocus");
        this.ttAssetPivot       = this->getStringParm("camFocusAssetPivot");
        this.ttAssetRotationX   = this->getIntParm("camAssetAxisX");
        this.ttAssetRotationY   = this->getIntParm("camAssetAxisY");
        this.ttHDRIRotationY    = this->getIntParm("camHDRIAxisY");
        this.hdriFile           = this->getStringParm("camHDRISelect");
        this.hdriUseBGColor     = this->getIntParm("camHDRIUseBgColor");
        this.hdriBGColor        = this->getVector3Parm("camHDRIbgColor");
        this.hdriIntensity      = this->getFloatParm("camHDRIIntensity");
        this.subdivType         = this->getStringParm("camSubdivType");
        this.subdivIteration    = this->getIntParm("camSubdivIter");
        this.shaderPreset       = this->getIntParm("camShaderPreset");
        this.shaderMaterialX    = this->getStringParm("camShaderMaterialX");
    }

    void
    updateDetailAttributes()
    {
        setdetailattrib(geoself(), "camImageSize", this.camImageSize, "set");
        setdetailattrib(geoself(), "camFocal", this.camFocal, "set");
        setdetailattrib(geoself(), "camAperture", this.camAperture, "set");
        setdetailattrib(geoself(), "focusPart", this.focusPart, "set");
        setdetailattrib(geoself(), "ttAssetPivot", this.ttAssetPivot, "set");
        setdetailattrib(geoself(), "ttAssetRotationX", this.ttAssetRotationX, "set");
        setdetailattrib(geoself(), "ttAssetRotationY", this.ttAssetRotationY, "set");
        setdetailattrib(geoself(), "ttHDRIRotationY", this.ttHDRIRotationY, "set");
        setdetailattrib(geoself(), "hdriFile", this.hdriFile, "set");
        setdetailattrib(geoself(), "hdriUseBGColor", this.hdriUseBGColor, "set");
        setdetailattrib(geoself(), "hdriBGColor", this.hdriBGColor, "set");
        setdetailattrib(geoself(), "hdriIntensity", this.hdriIntensity, "set");
        setdetailattrib(geoself(), "subdivType", this.subdivType, "set");
        setdetailattrib(geoself(), "subdivIteration", this.subdivIteration, "set");
        setdetailattrib(geoself(), "shaderPreset", this.shaderPreset, "set");
        setdetailattrib(geoself(), "shaderMaterialX", this.shaderMaterialX, "set");

    }

    void
    camMixer(
        float frame)
    {
        // Get the camera count.
        int cameraCount = chi(concat(this.hdaRelativePath, "cameras"));
        // Check if there are some cameras.
        if(cameraCount > 0){
            // Init the hda parameters.
            this->getHDAParameters(0);
            // Init the cumul of all camera frames.
            int allCameraFrames = 0;
            // Loop over the cameras.
            for(int i=0; i<cameraCount; i++){
                // Update the camera ID.
                this.camID = i;
                // Get the camera frames.
                int camFrames   = this->getCameraFrames();
                int camEndFrame = allCameraFrames + camFrames;

                // Check if the current time match with the current cameras.
                // We use the current camera setup to drive the turn table setup.
                if(frame > allCameraFrames && frame <= camEndFrame){
                    this->getHDAParameters(this.camID);
                    break;
                }

                allCameraFrames += camFrames;
            }

            // Update the camera mixer detail attributes.
           this->updateDetailAttributes();

        }
        
    }

};

#endif