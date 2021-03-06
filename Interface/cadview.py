#@+leo-ver=5-thin
#@+node:1.20130426141258.3560: * @file cadview.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3561: ** <<declarations>> (cadview)
import math
from PyQt4 import QtCore, QtGui

from Interface.Entity.base import *
from Interface.Preview.base import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3562: ** class CadView
class CadView(QtGui.QGraphicsView):
    #@+others
    #@+node:1.20130426141258.3563: *3* __init__
    def __init__(self, scene, parent=None):
        super(CadView, self).__init__(scene, parent)
        self.scaleFactor=1
        self.controlPress=False
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

        #handle mouse midbutton pan and zoom
        scene.fireZoomFit+=self.fit
        scene.firePan+=self.Pan
        self.firstPanPoint=QtCore.QPointF()
    #@+node:1.20130426141258.3564: *3* Pan
    def Pan(self, panActive, eventPoint):

        if panActive==True:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.firstPanPoint=eventPoint
        elif panActive==False:
            self.firstPanPoint=None
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        else:
            if self.controlPress==False:
                c=QtCore.QPoint((self.width()/2-10), (self.height()/2-10))
                cOnScene=self.mapToScene(c)
                vector=self.firstPanPoint-eventPoint
                newC=cOnScene+vector
                self.centerOn(newC)
    #@+node:1.20130426141258.3565: *3* wheelEvent
    def wheelEvent(self, event):
        #get the center of the view in scene coordinates
        c=QtCore.QPoint((self.width()/2.0)-10, (self.height()/2.0)-10)
        cOnScene=self.mapToScene(c)
        #get the mouse position in scene coordinates
        pOnView=event.pos()
        pOnScene=self.mapToScene(pOnView)
        #old command
        self.scaleFactor=math.pow(2.0,event.delta() / 240.0)
        self.scaleView(self.scaleFactor)
#       self.updateShape()  <<<prova


        #get the modified position due to occurred zoom
        newPOnScene=self.mapToScene(pOnView)
        #get the vector to move the modified position in the old position
        vector=pOnScene-newPOnScene
        #set a new center to maintain mouse position referred to the scene
        newC=cOnScene+vector
        self.centerOn(newC)
        #self.scaleFactor=math.pow(2.0,-event.delta() / 240.0)
        #self.scaleView(self.scaleFactor)
        self.updateShape()   # <<<prova
    #@+node:1.20130426141258.3566: *3* keyPressEvent
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Control:
            self.controlPress=True
            self.scene().isInPan=True
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(CadView, self).keyPressEvent(event)
    #@+node:1.20130426141258.3567: *3* keyReleaseEvent
    def keyReleaseEvent(self, event):
        self.controlPress=False
        self.scene().isInPan=False
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        super(CadView, self).keyReleaseEvent(event)
    #@+node:1.20130426141258.3568: *3* fit
    def fit(self):
        """
            fit all the item in the view
        """
        boundingRectangle=[item.boundingRect() for item in list(self.scene().items()) if isinstance(item, BaseEntity)]
        qRect=None
        for bound in boundingRectangle:
            if not qRect:
                qRect=bound
            else:
                qRect=qRect.unite(bound)
        if qRect:
            self.zoomWindows(qRect)
            self.updateShape()
    #@+node:1.20130426141258.3569: *3* centerOnSelection
    def centerOnSelection(self):
        """
            center the view on selected item
        """
        #TODO: if the item is in the border the centerOn will not work propely
        #more info at :http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qgraphicsview.html#ViewportAnchor-enum
        for item in self.scene().selectedItems():
            self.centerOn(item)
            return
    #@+node:1.20130426141258.3570: *3* zoomWindows
    def zoomWindows(self, qRect):
        """
            perform a windows zoom
        """
        zb=self.scaleFactor
        qRect.setX(qRect.x()-zb)
        qRect.setY(qRect.y()-zb)
        qRect.setWidth(qRect.width()+zb)
        qRect.setHeight(qRect.height()+zb)
        self.fitInView(qRect,1) # KeepAspectRatioByExpanding
        self.updateShape()
    #@+node:1.20130426141258.3571: *3* scaleView
    def scaleView(self, factor):
        self.scale(factor, factor)
    #@+node:1.20130426141258.3572: *3* updateShape
    def updateShape(self):
        """
            update the item shape tickness
        """
        matrixScaleFactor=self.matrix().m11()
        if matrixScaleFactor<0.001:
            matrixScaleFactor=0.001
        val=(1.0/matrixScaleFactor)*10
        BaseEntity.shapeSize=val
        PreviewBase.shapeSize=val
    #@-others
#@-others
#@-leo
