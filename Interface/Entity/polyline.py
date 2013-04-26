#@+leo-ver=5-thin
#@+node:1.20130426141258.4056: * @file polyline.py
#
# Copyright (c) ,2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# qt arc class
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4057: ** <<declarations>> (polyline)
from Interface.Entity.base import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4058: ** class Polyline
class Polyline(BaseEntity):
    """
        this class define the polyline object 
    """
    #@+others
    #@+node:1.20130426141258.4059: *3* __init__
    def __init__(self, entity):
        super(Polyline, self).__init__(entity)
        self.qtPoints=self.getQtPointF()
        return
    #@+node:1.20130426141258.4060: *3* getQtPointF
    def getQtPointF(self):
        qtPoints=[]
        geoPolyline=self.geoItem
        for p in geoPolyline.points():
            x, y=p.getCoords()
            qtPointf=QtCore.QPointF(x, y*-1.0 )
            qtPoints.append(qtPointf)
        return qtPoints
    #@+node:1.20130426141258.4061: *3* drawShape
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        painterPath.moveTo(self.qtPoints[0])
        for i in range(1,len(self.qtPoints)):
            painterPath.lineTo(self.qtPoints[i])    
    #@+node:1.20130426141258.4062: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        """
            overloading of the paint method
        """
        #Create poliline Object
        pol=QtGui.QPolygonF(self.qtPoints)
        painter.drawPolyline(pol)
        #painter.drawRect(self.boundingRect())
    #@-others
#@-others
#@-leo
