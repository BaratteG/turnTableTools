#ifndef __T_T_UTILS__
#define __T_T_UTILS__

#define HDA_PATH "../../"

string
getStringParm(
    const string  parmName;
    const int     parmID;
    const int     useID)
{
    if(useID){
        return chs(concat(HDA_PATH, parmName, itoa(parmID)));
    }

    return chs(concat(HDA_PATH, parmName));
}

int
getIntParm(
    const string  parmName;
    const int     parmID;
    const int     useID)
{
    if(useID){
        return chi(concat(HDA_PATH, parmName, itoa(parmID)));
    }

    return chi(concat(HDA_PATH, parmName));
}

float
getFloatParm(
    const string    parmName;
    const int       parmID;
    const int       useID)
{
    if(useID){
        return chf(concat(HDA_PATH, parmName, itoa(parmID)));
    }

    return chf(concat(HDA_PATH, parmName));
}

vector2
getVector2Parm(
    const string    parmName;
    const int       parmID;
    const int       useID)
{
    if(useID){
        return chu(concat(HDA_PATH, parmName, itoa(parmID)));
    }

    return chu(concat(HDA_PATH, parmName, itoa(parmID)));
}

vector
getVectorParm(
    const string    parmName;
    const int       parmID;
    const int       useID)
{
    if(useID){
        return chv(concat(HDA_PATH, parmName, itoa(parmID)));
    }

    return chv(concat(HDA_PATH, parmName, itoa(parmID)));
}



#endif