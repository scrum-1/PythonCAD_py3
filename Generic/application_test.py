#@+leo-ver=5-thin
#@+node:1.20130426141258.2498: * @file application_test.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2499: ** <<declarations>> (application_test)
import sympy            as mainSympy
import sympy.geometry   as geoSympy

from Kernel.GeoEntity.point         import Point
from Kernel.GeoEntity.segment       import Segment
from Kernel.GeoEntity.arc           import Arc
from Kernel.GeoEntity.ellipse       import Ellipse
from Kernel.GeoEntity.cline         import CLine

from Kernel.GeoUtil.intersection    import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2500: ** testSympySegment
def testSympySegment():
    print("++ Sympy Segment ++")
    p1=Point(0, 1)
    p2=Point(10, 20)
    arg={"SEGMENT_0":p1, "SEGMENT_1":p2}
    seg=Segment(arg)
    symSeg=seg.getSympy()
    print(symSeg)
    p3=Point(30, 40)
    arg1={"SEGMENT_0":p1, "SEGMENT_1":p3}
    seg1=Segment(arg1)
    seg1.setFromSympy(symSeg)
    print("Segment ", seg1)
    print("-- Sympy Segment --")
#@+node:1.20130426141258.2501: ** testSympyCline
def testSympyCline():
    print("++ Sympy CLine ++")
    p1=Point(0, 1)
    p2=Point(10, 20)
    arg={"CLINE_0":p1, "CLINE_1":p2}
    seg=CLine(arg)
    symSeg=seg.getSympy()
    print(symSeg)
    p3=Point(30, 40)
    arg1={"CLINE_0":p1, "CLINE_1":p3}
    seg1=CLine(arg1)
    seg1.setFromSympy(symSeg)
    print("CLine ", seg1)
    print("-- Sympy CLine --")
#@+node:1.20130426141258.2502: ** testSympyCircle
def testSympyCircle():
    print("++ Sympy Arc ++")
    p1=Point(0, 1)
    arg={"ARC_0":p1, "ARC_1":5, "ARC_2":0, "ARC_3":6.2831}
    arc=Arc(arg)
    sympCircle=arc.getSympy()
    print("sympCircle", sympCircle)
    sympCircel=geoSympy.Circle(geoSympy.Point(10, 10), 10)
    arc.setFromSympy(sympCircel)
    print("Pythonca Arc ", arc)
    print("-- Sympy Arc --")
#@+node:1.20130426141258.2503: ** testSympyEllipse
def testSympyEllipse():
    print("++ Sympy Ellipse ++")
    p1=Point(0, 1)
    arg={"ELLIPSE_0":p1, "ELLIPSE_1":100, "ELLIPSE_2":50}
    eli=Ellipse(arg)
    sympEli=eli.getSympy()
    print("sympEllipse", sympEli)
    sympEli1=geoSympy.Ellipse(geoSympy.Point(10, 10), 300, 200)
    eli.setFromSympy(sympEli1)
    print("Pythonca Ellipse ", eli)
    print("-- Sympy Ellipse --")
#@+node:1.20130426141258.2504: ** TestSympy
def TestSympy():
    testSympySegment()
    testSympyCline()
    testSympyCircle()
    testSympyEllipse()
#@+node:1.20130426141258.2505: ** segment_segmet
#*****************************************************************
#Test Intersection
#*****************************************************************
def segment_segmet():
    print("++ segment_segmet ++")
    p1=Point(0,0)
    p2=Point(0, 1)
    arg={"SEGMENT_0":p1, "SEGMENT_1":p2}
    seg1=Segment(arg)
    p3=Point(0, 0)
    p4=Point(-1,0)
    arg={"SEGMENT_0":p3, "SEGMENT_1":p4}
    seg2=Segment(arg)

    print(find_intersections(seg1, seg2))
    print("-- segment_segmet --")
#@+node:1.20130426141258.2506: ** segment_cline
def segment_cline():
    print("++ segment_cline ++")
    p1=Point(0,0)
    p2=Point(0, 1)
    arg={"CLINE_0":p1, "CLINE_1":p2}
    seg1=CLine(arg)
    p3=Point(0, 0)
    p4=Point(-1,0)
    arg={"SEGMENT_0":p3, "SEGMENT_1":p4}
    seg2=Segment(arg)

    print(find_intersections(seg1, seg2))
    print("-- segment_cline --")
#@+node:1.20130426141258.2507: ** segment_circle
def segment_circle():
    print("++ segment_circle ++")
    p1=Point(0, 0)
    arg={"ARC_0":p1, "ARC_1":5, "ARC_2":0, "ARC_3":6.2831}
    arc=Arc(arg)
    p2=Point(0, 0)
    p3=Point(-1,0)
    arg={"CLINE_0":p2, "CLINE_1":p3}
    seg1=CLine(arg)
    print(find_intersections(arc, seg1))
    print("-- segment_circle --")
#@+node:1.20130426141258.2508: ** segment_ellipse
def segment_ellipse():
    print("++ segment_ellipse ++")
    p1=Point(0, 0)
    arg={"ELLIPSE_0":p1, "ELLIPSE_1":300, "ELLIPSE_2":100}
    eli=Ellipse(arg)
    p2=Point(0, 0)
    p3=Point(-1,0)
    arg={"CLINE_0":p2, "CLINE_1":p3}
    seg1=CLine(arg)
    print(find_intersections(eli, seg1))
    print("-- segment_ellipse --")
#@+node:1.20130426141258.2509: ** TestIntersection
def TestIntersection():
    segment_segmet()
    segment_cline()
    segment_circle()
    segment_ellipse()
#@-others
from application import Application

a=Application()
print("stored file")
for f in a.getRecentFiles:
    print("File :", str(f))

print("available command")
for c in a.getCommandList():
    print("Command:", str(c))

TestSympy()
TestIntersection()

doc=a.openDocument(a.getRecentFiles[0])
a.saveAs(r"C:\temp\test.dxf")
#@-leo
