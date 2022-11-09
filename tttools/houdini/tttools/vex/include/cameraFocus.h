#ifndef __CAMERA_FOCUS__
#define __CAMERA_FOCUS__

#include <ttUtils.h>

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
    assetSize *= 0.6;
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



#endif