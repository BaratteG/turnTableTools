#ifndef __ASSET_PIVOT__
#define __ASSET_PIVOT__

#include <ttUtils.h>

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


#endif