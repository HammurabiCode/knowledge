# AcDbRegion

AcDbRegion::getAreaProp Function 

```
virtual Acad::ErrorStatus
getAreaProp(
const AcGePoint3d& origin,
const AcGeVector3d& xAxis,
const AcGeVector3d& yAxis,
double& perimeter,
double& area,
AcGePoint2d& centroid,
double momInertia[2],
double& prodInertia,
double prinMoments[2],
AcGeVector2d prinAxes[2],
double radiiGyration[2],
AcGePoint2d& extentsLow,
AcGePoint2d& extentsHigh) const;
```

origin: Input origin of the region 

xAxis: Input X axis of the region 

yAxis: Input Y axis of the region 

perimeter: Returns perimeter of the region 周长

area: Returns area of the region 面积

centroid: Returns centroid of the region 质心，二维的点，位于“由前3个参数确定的平面”上。

momInertia[2]: Returns moment of inertia of the region 惯性矩，转动惯量

prodInertia: Returns product of inertia of the region 惯性积

prinMoments[2]: Returns principal moments of the region 主矩

prinAxes[2]: Returns principle axes of the region 主轴

radiiGyration[2]: Returns radii of gyration of the region 回转半径

extentsLow: Returns minimum extents point of the region 

extentsHigh: Returns maximum extents point of the region 


This function calculates the area properties of the region. All the values are in the World Coordinate System (WCS). The function validates the origin, xAxis, and yAxis parameters to ensure that the axes are of unit length and are perpendicular to each other, and that the axes and the origin lie in the same plane as the region.

Returns Acad::eOk if successful.

If there is an error in the ShapeManager modeler, then Acad::eGeneralModelingFailure is returned.
