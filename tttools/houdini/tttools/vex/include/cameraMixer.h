#ifndef __CAMERA_MIXER__
#define __CAMERA_MIXER__

struct CameraMixer{

    string  hdaRelativePath = "../../";
    int     camID           = 0;
    
    string  camName;
    vector2 camImageSize;
    float   camFocal;
    float   camAperture;
    
    string  focusPart;

    string  ttAssetPivot;
    int     ttAssetRotationX;
    int     ttAssetRotationY;
    int     ttHDRIRotationY;

    float   ttAssetAngleX   = 0.0;
    float   ttAssetAngleY   = 0.0;
    float   ttHDRIAngleY    = 0.0;

    string  hdriPaht;
    string  hdriFile;
    float   hdriIntensity;
    int     hdriUseBGColor;
    vector  hdriBGColor;

    string  subdivType;
    int     subdivIteration;

    int     shaderPreset;
    string  shaderMaterialX;

    string  hdriFolder;

    vector  camPosition;
    vector  camRotation;
    vector  camScale;

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
    assetAngleY(
        float   frame;
        float   timeOffset)
    {
        float startFrame    = timeOffset;
        float endFrame      = startFrame + this.ttAssetRotationY;
        if(startFrame != endFrame){
            this.ttAssetAngleY  =  clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
        }else{
            this.ttAssetAngleY = 0.0;
        }
    }

    void
    assetAngleX(
        float   frame;
        float   timeOffset)
    {
        float   startFrame  = timeOffset + this.ttAssetRotationY;
        float   endFrame    = startFrame + this.ttAssetRotationX;
        if(startFrame != endFrame){
            this.ttAssetAngleX  = clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
        }else{
            this.ttAssetAngleX = 0.0;
        }
    }

    void
    hdriAngleY(
        float   frame;
        float   timeOffset)
    {
        float   startFrame  = timeOffset + this.ttAssetRotationY + this.ttAssetRotationX;
        float   endFrame    = startFrame + this.ttHDRIRotationY;
        if(startFrame != endFrame){
            this.ttHDRIAngleY   = clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
        }else{
            this.ttHDRIAngleY = 0.0;
        }
    }

    void 
    getHDAParameters(
        int camID)
    {
        this.camID              = camID;
        this.camName            = this->getStringParm("camName");
        this.camImageSize       = this->getVector2Parm("camImageSize");
        this.camFocal           = this->getFloatParm("camFocal");
        this.camAperture        = this->getFloatParm("camAperture");
        this.focusPart          = this->getStringParm("camFocus");
        this.ttAssetPivot       = this->getStringParm("camFocusAssetPivot");
        this.ttAssetRotationX   = this->getIntParm("camAssetAxisX");
        this.ttAssetRotationY   = this->getIntParm("camAssetAxisY");
        this.ttHDRIRotationY    = this->getIntParm("camHDRIAxisY");
        this.hdriFile           = concat(this.hdriFolder, '/', this->getStringParm("camHDRISelect"));
        this.hdriUseBGColor     = this->getIntParm("camHRDIUseBGColor");
        this.hdriBGColor        = this->getVector3Parm("camHDRIBGColor");
        this.hdriIntensity      = this->getFloatParm("camHRDIIntensity");
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
        setdetailattrib(geoself(), "ttAssetAngleX", this.ttAssetAngleX, "set");
        setdetailattrib(geoself(), "ttAssetAngleY", this.ttAssetAngleY, "set");
        setdetailattrib(geoself(), "ttHDRIAngleY", this.ttHDRIAngleY, "set");
    }

    void
    mixCamTransform(
        float frame)
    {
        // Get the auto focus cam.
        matrix autoFocusTrans   = optransform("../../autoFocus");
        matrix camTrans         = autoFocusTrans;
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

                    if(this.focusPart != "free"){
                        camTrans = autoFocusTrans;
                    }else{
                        camTrans = optransform(concat("../../CAMERAS/", this.camName));
                    }

                    break;
                }

                allCameraFrames += camFrames;
            }

            this.camPosition    = cracktransform(0, 0, 0, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);
            this.camRotation    = cracktransform(0, 0, 1, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);
            this.camScale       = cracktransform(0, 0, 2, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);

            setdetailattrib(geoself(), "camPosition", this.camPosition, "set");
            setdetailattrib(geoself(), "camRotation", this.camRotation, "set");
            setdetailattrib(geoself(), "camScale", this.camScale, "set");
        }
    }

    void
    mix(
        float frame)
    {
        // Get the hdri folder.
        this.hdriFolder = chs(concat(this.hdaRelativePath, "hdriPath"));
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
                    this->assetAngleY(frame, allCameraFrames);
                    this->assetAngleX(frame, allCameraFrames);
                    this->hdriAngleY(frame, allCameraFrames);
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