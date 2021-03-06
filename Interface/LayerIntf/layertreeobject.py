#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4083: * @file layertreeobject.py
#@@first

#
# Copyright (c) 2010 Matteo Boscolo
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
# This  module provide all the global variable to be used from the pythoncad Application
#
#
# This Class define a QTreeWidget implementation for showing the layer structure
#




#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4084: ** <<declarations>> (layertreeobject)
import sys
#if sys.version_info <(2, 7):
#    import sip
#    sip.setapi('QString', 2)
#    sip.setapi('QVariant', 2)

from PyQt4                              import QtCore, QtGui

from Kernel.initsetting                 import MAIN_LAYER
from Kernel.layer                       import Layer
from Kernel.exception                   import PythonCadWarning
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4085: ** class LayerItem
class LayerItem(QtGui.QTreeWidgetItem):
    """
        Single item
    """
    #@+others
    #@+node:1.20130426141258.4086: *3* __init__
    def __init__(self, kernelItem,type=0, id=None, active=True):
        super(LayerItem, self).__init__(type)
        self._kernelItem=kernelItem
        self._id=id
        self.setText(0, self.name)
        self.setActive(active)
        self.setVisible(kernelItem.Visible)
    #@+node:1.20130426141258.4087: *3* setActive
    def setActive(self, activate):
        """
            overwrite the set active property
        """
        self.setExpanded(True)
        if activate:
            self.setBackgroundColor(0, QtCore.Qt.lightGray)
        else:
            self.setBackgroundColor(0, QtCore.Qt.white)
    #@+node:1.20130426141258.4088: *3* setVisible
    def setVisible(self, activate):        
        if activate:
            self.setText(1, "Visible")    
        else:
            self.setText(1, "Hide")
    #@+node:1.20130426141258.4089: *3* name
    @property
    def name(self):
        """
            get the layer name
        """
        return self._kernelItem.name
    #@+node:1.20130426141258.4090: *3* id
    @property
    def id(self):
        """
            Get the id of the layer
        """
        return self._id
    #@-others
#@+node:1.20130426141258.4091: ** class LayerTreeObject
class LayerTreeObject(QtGui.QTreeWidget):
    """
        Python
        CAD Layer tree Structure
    """
    #@+others
    #@+node:1.20130426141258.4092: *3* __init__
    def __init__(self, parent, document):
        super(LayerTreeObject, self).__init__(parent)
        self._document=document
        self._document.getTreeLayer.setCurrentEvent=self.updateTreeStructure
        self._document.getTreeLayer.deleteEvent=self.updateTreeStructure
        self._document.getTreeLayer.insertEvent=self.updateTreeStructure
        self._document.getTreeLayer.update=self.updateTreeStructure
        self.setColumnCount(2)
        self.setHeaderLabels(("Layer Name ", "Visible"))
        self.TopLevelItem=None
        self.setSortingEnabled(True)
        self.populateStructure()
    #@+node:1.20130426141258.4093: *3* itemDoubleClicked
    def itemDoubleClicked(self, qTreeWidgetItem ,column):
        return QtGui.QTreeWidget.itemDoubleClicked(self, qTreeWidgetItem, column)   
    #@+node:1.20130426141258.4094: *3* updateTreeStructure
    #
    # Manage event
    #
    def updateTreeStructure(self, layer):
        """
            update the tree structure
        """
        self.populateStructure()
    #@+node:1.20130426141258.4095: *3* populateStructure
    def populateStructure(self):
        """
            populate the tree view structure
        """
        self.clear()
        layerTreeStructure=self._document.getTreeLayer.getLayerTree()
        activeLayer=self._document.getTreeLayer.getActiveLater()
        def populateChild(layers, parentItem, activeLayerId):
            for key in layers:
                c, childs=layers[key]
                if key==activeLayerId:
                    parent=LayerItem(c, id=key, active=True)
                else:
                    parent=LayerItem(c, id=key, active=False)
                self.expandItem(parent)
                if parentItem==None:
                    self.addTopLevelItem(parent)
                    self.TopLevelItem=parent
                else:
                    parentItem.addChild(parent)
                if childs!=None:
                    populateChild(childs,parent,activeLayerId)
        populateChild(layerTreeStructure, None, activeLayerId=activeLayer.getId())
        if self.TopLevelItem!= None:
            self.expandItem(self.TopLevelItem)
    #@+node:1.20130426141258.4096: *3* contextMenuEvent
    def contextMenuEvent(self, event):
        """
            context menu event remapped
        """
        contexMenu=QtGui.QMenu(self)
        # Create Actions
        addAction=QtGui.QAction("Add Child", self, triggered=self._addChild)
        removeAction=QtGui.QAction("Remove", self, triggered=self._remove)
        renameAction=QtGui.QAction("Rename", self, triggered=self._rename)
        hideAction=QtGui.QAction("Hide", self, triggered=self._hide)
        showAction=QtGui.QAction("Show", self, triggered=self._show)
        setCurrentAction=QtGui.QAction("Set Current", self, triggered=self._setCurrent)
        #TODO : propertyAction=QtGui.QAction("Property", self, triggered=self._property)
        #
        contexMenu.addAction(addAction)
        contexMenu.addAction(removeAction)
        contexMenu.addAction(renameAction)
        contexMenu.addAction(hideAction)
        contexMenu.addAction(showAction)
        contexMenu.addAction(setCurrentAction)
        #contexMenu.addAction(propertyAction)
        #
        contexMenu.exec_(event.globalPos())
        del(contexMenu)
    #@+node:1.20130426141258.4097: *3* _addChild
    def _addChild(self):
        """
            Add a child layer
        """
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
                                                'Enter Layer Name :')
        if ok:
            layerName=text
            parentLayer=self._document.getTreeLayer.getActiveLater()
            newLayer=self._document.saveEntity(Layer(layerName))
            self._document.getTreeLayer.insert(newLayer, parentLayer)
    #@+node:1.20130426141258.4098: *3* _remove
    def _remove(self):
        """
            Remove the selected layer
        """
        if self.currentIterfaceTreeObject.name==MAIN_LAYER:
            print("Put on popUp Unable to delate the main layer ")
            return
        layerId=self.currentIterfaceTreeObject.id      
        self._document.getTreeLayer.delete(layerId)
    #@+node:1.20130426141258.4099: *3* _rename
    def _rename(self): 
        """
            rename the current layer
        """   
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
                                                'Enter Layer Name :')
        if ok:
            layerId=self.currentIterfaceTreeObject.id  
            self._document.getTreeLayer.rename(layerId, text)
    #@+node:1.20130426141258.4100: *3* _hide
    def _hide(self):
        """
            Hide the selected layer
        """
        try:
            layerId=self.currentIterfaceTreeObject.id  
            self._document.getTreeLayer.Hide(layerId)
        except PythonCadWarning as e:
            QtGui.QMessageBox.information(self, 
                                                "PythonCad -Warning", 
                                                str(e) , 
                                                QtGui.QMessageBox.Ok)
    #@+node:1.20130426141258.4101: *3* _show
    def _show(self):
        """
            Show the selected layer
        """
        try:
            layerId=self.currentIterfaceTreeObject.id 
            self._document.getTreeLayer.Hide(layerId, False) 
        except PythonCadWarning as e:
            QtGui.QMessageBox.information(self, 
                                                "PythonCad -Warning", 
                                                str(e) , 
                                                QtGui.QMessageBox.Ok)
    #@+node:1.20130426141258.4102: *3* _setCurrent
    def _setCurrent(self):
        """
            set the current layer
        """
        cito=self.currentIterfaceTreeObject
        if cito!=None:
            self._document.getTreeLayer.setActiveLayer(cito.id)
            #cito.setActive(True)
    #@+node:1.20130426141258.4103: *3* _property
    def _property(self):
        """
            Show the layer property dialog
        """
        pass
    #@+node:1.20130426141258.4104: *3* currentIterfaceTreeObject
    @property
    def currentIterfaceTreeObject(self):
        """
            return the current interface tree Object
        """
        exitLayer=None
        for item in self.selectedItems():
            if(item.id!=None):
                exitLayer=item           
            break
        return exitLayer
    #@-others
#@-others
#@-leo
