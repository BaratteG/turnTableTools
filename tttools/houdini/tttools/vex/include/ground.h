#ifndef __GROUND__
#define __GROUND__

#include <ttUtils.h>

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

#endif
