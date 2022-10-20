#ifndef __ASSET_MIX__
#define __ASSET_MIX__

#include <ttUtils.h>




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



#endif