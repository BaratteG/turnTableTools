#ifndef __CAMERA_MIXER__
#define __CAMERA_MIXER__

#include <ttUtils.h>



void
ballsAndMacbethTransform(
    const int   packedGeoID)
{
    // Get the render cameras datas.
    matrix  camTrans        = optransform("../../RENDER");
    vector2 camImageSize    = chu("../../RENDER/res");
    float   camFocal        = chf("../../RENDER/focal");

    // Get the packed point count of the input geometry.
    int     pointCount      = npoints(packedGeoID);

    // Loop over the points.
    for(int i=0; i<pointCount; i++){
        // Get the packed data.
        string  refName             = point(packedGeoID, "name", i);
        vector  refScreenLocation   = point(packedGeoID, "screenLocation", i);
        float   refScale            = point(packedGeoID, "scale", i);
    }

}


void
groundTransform(
    const   int     mixerGeoID;
    const   int     assetGeoID)
{
    // Get the asset bounding box min and max.
    vector  bbMin, bbMax;
    getbbox(assetGeoID, bbMin, bbMax);
    // Get the asset rotation X to move the ground to avoid the collision with asset
    // during the rotation.
    float   assetAngleX = detail(mixerGeoID, "assetAngleX");
    // Compute the asset size.
    float   assetSize   = length(bbMax - bbMin);
    // Compute the ground size.
    vector  groundSize  = assetSize * 10;
    // Compute the ground position Y.
    float   groundPY    = bbMin.y;
    if(assetAngleX > 0.0 && assetAngleX < 360.0){
        groundPY    = bbMin.y - assetSize * 5;
    }
    // Store the ground data to the detail attribute.
    setdetailattrib(geoself(), "groundSize", groundSize, "set");
    setdetailattrib(geoself(), "groundPosY", groundPY, "set");
}

void
cameraFocus(
    const   int     assetGeoID;
    const   int     mixerGeoID)
{
    // Get the camera datas.
    vector2     camImageSize    = detail(mixerGeoID, "camImageSize");
    float       camFocal        = detail(mixerGeoID, "camFocal");
    float       camApertureX    = detail(mixerGeoID, "camAperture");
    string      camFocus        = detail(mixerGeoID, "camFocus");
    float       camFocusAdjust  = detail(mixerGeoID, "camFocusAdjust");
    // Compute camera aspect ratio and FOVs.
    float       camAspectRatio  = camImageSize.x / camImageSize.y;
    float       camFovX         = degrees(2.0 * atan(camApertureX * 0.5 / camFocal));
    float       camApertureY    = camApertureX * (1.0 / camAspectRatio);
    float       camFovY         = degrees(2.0 * atan(camApertureY * 0.5 / camFocal));
    // Get the asset bounding box.
    vector      bbMin, bbMax;
    getbbox(assetGeoID, camFocus, bbMin, bbMax);
    // Compute the asset center.
    vector      bbCenter        = (bbMax + bbMin) * 0.5;
    // Compute the asset size.
    float       assetSize       = length(bbMax - bbMin);
    assetSize *= camFocusAdjust;
    // Compute the camera position to correctly frame the asset.
    vector      camPos          = bbCenter;
    float       offsetFovX      = (assetSize * 0.5) / tan(radians(camFovX * 0.5));
    camPos.z                    = bbMax.z + offsetFovX;
    float       offsetFovY      = (assetSize * 0.5) / tan(radians(camFovY * 0.5));
    if(offsetFovY > offsetFovX){
        camPos.z = bbMax.z + offsetFovY;
    }
    // Store the position.
    setdetailattrib(geoself(), "camPos", camPos, "set");

    setdetailattrib(geoself(), "temp", assetSize, "set");
}

void
getAssetPivot(
    const   int     assetGeoID;
    const   int     mixerGeoID)
{
    // Get the asset part to use as pivot.
    string  assetPivotGroup     = detail(mixerGeoID, "ttAssetPivot");
    // Get the asset center.
    vector  centerPos           = getbbox_center(assetGeoID, assetPivotGroup);
    // Store the center.
    setdetailattrib(geoself(), "assetPivot", centerPos, "set");
}

void
assetMix()
{
    // Get the hda asset parameters.
    string  assetName   = getStringParm("assetName", 0, 0);
    string  step        = getStringParm("step", 0, 0);
    string  task        = getStringParm("task", 0, 0);
    int     geoType     = getIntParm("geoType", 0, 0);
    string  assetPath   = getStringParm("geoPath", 0, 0);

    // Drive the asset geometry switch.
    int     geoSwitch   = 0;
    if(geoType != 0){
        geoSwitch = 1;
    }

    // Store the parameters in geometry detail.
    setdetailattrib(geoself(), "assetName", assetName, "set");
    setdetailattrib(geoself(), "step", step, "set");
    setdetailattrib(geoself(), "task", task, "set");
    setdetailattrib(geoself(), "geoType", geoType, "set");
    setdetailattrib(geoself(), "assetPath", assetPath, "set");
    setdetailattrib(geoself(), "geoSwtich", geoSwitch, "set");
}

struct CameraParm{
    string      name;
    vector2     imageSize;
    float       focal;
    float       aperture;
    string      focus;
    float       focusAdjust;
}

void
getCameraParm(
    const   int         camID;
    export CameraParm   camParm)
{
    camParm.name        = getStringParm("camName", camID, 1);
    camParm.imageSize   = getVector2Parm("camImageSize", camID, 1);
    camParm.focal       = getFloatParm("camFocal", camID, 1);
    camParm.aperture    = getFloatParm("camAperture", camID, 1);
    camParm.focus       = getStringParm("camFocus", camID, 1);
    camParm.focusAdjust = getFloatParm("camFocusAdjust", camID, 1);
}

void
storeCameraParm(
    const CameraParm    camParm)
{
    setdetailattrib(geoself(), "camName", camParm.name, "set");
    setdetailattrib(geoself(), "camImageSize", camParm.imageSize, "set");
    setdetailattrib(geoself(), "camFocal", camParm.focal, "set");
    setdetailattrib(geoself(), "camAperture", camParm.aperture, "set");
    setdetailattrib(geoself(), "camFocus", camParm.focus, "set");
    setdetailattrib(geoself(), "camFocusAdjust", camParm.focusAdjust, "set");
}

struct TurnTableParm{
    string      assetPivot;
    int         assetRotationX;
    int         assetRotationY;
    int         hdriRotationY;
    int         frameCount;
    float       assetAngleX;
    float       assetAngleY;
    float       hdriAngleY;
}

void
getTurnTableParm(
    const   int             camID;
    export  TurnTableParm   ttParm)
{
    ttParm.assetPivot       = getStringParm("ttAssetPivot", camID, 1);
    ttParm.assetRotationX   = getIntParm("ttAssetRotationX", camID, 1);
    ttParm.assetRotationY   = getIntParm("ttAssetRotationY", camID, 1);
    ttParm.hdriRotationY    = getIntParm("ttHDRIRotationY", camID, 1);
    ttParm.frameCount       = ttParm.assetRotationX + ttParm.assetRotationY + ttParm.hdriRotationY;
}

void
storeTurnTableParm(
    const TurnTableParm ttParm)
{
    setdetailattrib(geoself(), "ttAssetPivot", ttParm.assetPivot, "set");
    setdetailattrib(geoself(), "ttAssetRotationX", ttParm.assetRotationX, "set");
    setdetailattrib(geoself(), "ttAssetRotationY", ttParm.assetRotationY, "set");
    setdetailattrib(geoself(), "ttHDRIRotationY", ttParm.hdriRotationY, "set");
    setdetailattrib(geoself(), "assetAngleX", ttParm.assetAngleX, "set");
    setdetailattrib(geoself(), "assetAngleY", ttParm.assetAngleY, "set");
    setdetailattrib(geoself(), "hdriAngleY", ttParm.hdriAngleY, "set");
}

struct HDRIParm{
    string  path;
    float   intensity;
    int     useBGColor;
    vector  bgColor;
}

void
getHDRIParm(
    const   string      hdriFolder;
    const   int         camID;
    export  HDRIParm    hdriParm)
{
    hdriParm.path       = concat(hdriFolder, "/", getStringParm("hdriSelect", camID, 1));
    hdriParm.intensity  = getFloatParm("hdriIntensity", camID, 1);
    hdriParm.useBGColor = getIntParm("hdriUseBGColor", camID, 1);
    hdriParm.bgColor    = getVectorParm("hdriBGColor", camID, 1);
}

void
storeHDRIParm(
    const HDRIParm  hdriParm)
{
    setdetailattrib(geoself(), "hdriFile", hdriParm.path, "set");
    setdetailattrib(geoself(), "hdriIntensity", hdriParm.intensity, "set");
    setdetailattrib(geoself(), "hdriUseBGColor", hdriParm.useBGColor, "set");
    setdetailattrib(geoself(), "hdriBGColor", hdriParm.bgColor, "set");
}

struct SubdivParm{
    string  type;
    int     iteration;
}

void
getSubdivParm(
    const   int         camID;
    export  SubdivParm  subParm)
{
    subParm.type        = getStringParm("assetSubdivType", camID, 1);
    subParm.iteration   = getIntParm("assetSubdivIter", camID, 1);
}

void
storeSubdivParm(
    const SubdivParm    subParm)
{
    setdetailattrib(geoself(), "subdivType", subParm.type, "set");
    setdetailattrib(geoself(), "subdivIteration", subParm.iteration, "set");
}

struct ShaderParm{
    int     preset;
    string  materialX;
}

void
getShaderParm(
    const   int         camID;
    export  ShaderParm  shdParm)
{
    shdParm.preset       = getIntParm("assetShaderPreset", camID, 1);
    shdParm.materialX    = getStringParm("assetMaterialXFile", camID, 1);
}

void
storeShaderParm(
    const ShaderParm shdParm)
{
    setdetailattrib(geoself(), "shaderPreset", shdParm.preset, "set");
    setdetailattrib(geoself(), "shaderMaterialX", shdParm.materialX, "set");
}

void
assetAngleY(
    const   float         frame;
    const   float         timeOffset;
    export  TurnTableParm ttParm)
{
    float startFrame    = timeOffset;
    float endFrame      = startFrame + ttParm.assetRotationY;
    if(startFrame != endFrame){
        ttParm.assetAngleY =  clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
    }else{
        ttParm.assetAngleY = 0.0;
    }
}

void
assetAngleX(
    const   float         frame;
    const   float         timeOffset;
    export  TurnTableParm ttParm)
{
    float   startFrame  = timeOffset + ttParm.assetRotationY;
    float   endFrame    = startFrame + ttParm.assetRotationX;
    if(startFrame != endFrame){
        ttParm.assetAngleX = clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
    }else{
        ttParm.assetAngleX = 0.0;
    }
}

void
hdriAngleY(
    const   float         frame;
    const   float         timeOffset;
    export  TurnTableParm ttParm)
{
    float   startFrame  = timeOffset + ttParm.assetRotationY + ttParm.assetRotationX;
    float   endFrame    = startFrame + ttParm.hdriRotationY;
    if(startFrame != endFrame){
        ttParm.hdriAngleY = clamp(fit(frame, startFrame, endFrame, 0.0, 360.0), 0.0, 360.0);
    }else{
        ttParm.hdriAngleY = 0.0;
    }
}


void
cameraParmMixer(
    float frame)
{
    // Get the hda main parameters.
    string  hdriPath        = getStringParm("hdriPath", 0, 0);
    int     cameraCount     = getIntParm("cameras", 0, 0);

    if(cameraCount > 0){
        // Get the camera parameters.
        CameraParm      camParm;
        TurnTableParm   ttParm;
        HDRIParm        hdriParm;
        SubdivParm      subParm;
        ShaderParm      shdParm;

        getCameraParm(0, camParm);
        getTurnTableParm(0, ttParm);
        getHDRIParm(hdriPath, 0, hdriParm);
        getSubdivParm(0, subParm);
        getShaderParm(0, shdParm);

        // Init the frame counter.
        // Use to setup the render frames range.
        int frameCounter = 0;


        // Loop over the cameras to mix the parameters.
        for(int i=0; i<cameraCount; i++){

            // Update the turn table paramter to mix the parameter of the cameras.
            getTurnTableParm(i, ttParm);

            // Define the current camera range.
            int     startFrame  = frameCounter;
            int     endFrame    = startFrame + ttParm.frameCount;

            // If the current time is in the range of the current cameras.
            // We use the current camera parameters.
            if(frame > startFrame && frame <= endFrame){
                getCameraParm(i, camParm);
                getHDRIParm(hdriPath, i, hdriParm);
                getSubdivParm(i, subParm);
                getShaderParm(i, shdParm);
                assetAngleY(frame, startFrame, ttParm);
                assetAngleX(frame, startFrame, ttParm);
                hdriAngleY(frame, startFrame, ttParm);
                break;
            }

            frameCounter = endFrame;
        }

        // Store the mixed parameters.
        storeCameraParm(camParm);
        storeTurnTableParm(ttParm);
        storeHDRIParm(hdriParm);
        storeSubdivParm(subParm);
        storeShaderParm(shdParm);
    
        // Get all frame to do the turn table.
        int endFrame = 0;
        for(int i=0; i<cameraCount; i++){
            getTurnTableParm(i, ttParm);
            endFrame += ttParm.frameCount;
        }

        setdetailattrib(geoself(), "endFrame", endFrame, "set");

    }

}



void
cameraMixer(
    int     mixerGeoID)
{
    // By default we use the transformation of the auto focus camera.
    matrix camTrans         = optransform("../../AUTO_FOCUS_CAM");
    // Get the camera name from the camera mixer parameters.
    string currentCamera    = detail(mixerGeoID, "camName");
    // Get the camera focus.
    string focusCamera      = detail(mixerGeoID, "camFocus");

    // Check if we use the autoFocus cameras trans or the current camera transform.
    if(focusCamera == "free"){
        camTrans = optransform(concat("../../CAMERAS/", currentCamera));
    }
    
    // Split the camera transform to drive the render camera.
    vector camPos   = cracktransform(0, 0, 0, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);
    vector camRot   = cracktransform(0, 0, 1, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);
    vector camScl   = cracktransform(0, 0, 2, {0.0,0.0,0.0}, {0.0,0.0,0.0}, camTrans);

    setdetailattrib(geoself(), "camPosition", camPos, "set");
    setdetailattrib(geoself(), "camRotation", camRot, "set");
    setdetailattrib(geoself(), "camScale", camScl, "set");

}


#endif