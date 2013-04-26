#@+leo-ver=5-thin
#@+node:1.20130426141258.3013: * @file relationdb.py
#encoding: utf-8
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
# This module provide basic operation for the Relation in the pythoncad database
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3014: ** <<declarations>> (relationdb)
import pickle as pickle

from Kernel.entity          import Entity
from Kernel.Db.basedb       import BaseDb
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3015: ** class RelationDb
class RelationDb(BaseDb):
    """
        this class provide the besic operation for the relation
    """
    #@+others
    #@+node:1.20130426141258.3016: *3* __init__
    def __init__(self,dbConnection=None):
        BaseDb.__init__(self)
        if dbConnection is None:
            self.createConnection()
        else:
            self.setConnection(dbConnection)

        _sqlCheck="""select * from sqlite_master where name like 'pycadrel'"""
        _table=self.makeSelect(_sqlCheck).fetchone()
        if _table is None:
            _sqlCreation="""CREATE TABLE pycadrel(
                    "pycad_id" INTEGER PRIMARY KEY,
                    "pycad_parent_id" INTEGER,
                    "pycad_child_id" INTEGER
                    )"""
            self.makeUpdateInsert(_sqlCreation)
    #@+node:1.20130426141258.3017: *3* saveRelation
    def saveRelation(self,parentEntObj,childEntObj):
        """
            This method save the Relation in the db
            TODO  : THE RELATION MAST BE UNIVOC ...
        """
        _parentEntityId=parentEntObj.getId()
        _childEntityId=childEntObj.getId()
        _sqlInsert="""INSERT INTO pycadrel (
                      pycad_parent_id,
                      pycad_child_id
                      ) VALUES
                      (%s,"%s")"""%(
                    str(_parentEntityId),
                    str(_childEntityId))
        self.makeUpdateInsert(_sqlInsert)
    #@+node:1.20130426141258.3018: *3* getChildrenIds
    def getChildrenIds(self,entityParentId):
        """
            Get the children id of a relation
        """
        _outObj=[]
        _sqlGet="""SELECT pycad_child_id
                FROM pycadrel
                WHERE pycad_parent_id=%s"""%str(entityParentId)
        _rows=self.makeSelect(_sqlGet)
        _dbEntRow=self.makeSelect(_sqlGet)
        if _dbEntRow is not None:
            for _row in _dbEntRow:
                _outObj.append(_row[0])
        return _outObj
    #@+node:1.20130426141258.3019: *3* getAllChildrenType
    def getAllChildrenType(self, parent, childrenType=None):
        """
            get all the children entity of type childrenType
        """
        _outObj=[]
        if not childrenType:
            childrenType='%'
        if childrenType=='ALL':
            childrenType='%' # TODO : controllare questa select pycad_id,
        _sqlSelect="""SELECT 
                            pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_object_style,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible,
                            pycad_id
                            FROM pycadent
                            WHERE pycad_entity_id IN
                                (
                                    SELECT pycad_child_id
                                    FROM pycadrel
                                    WHERE pycad_parent_id =%s
                                )
                            AND pycad_id IN (
                                SELECT max(pycad_id) 
                                FROM pycadent  
                                WHERE pycad_undo_visible=1  
                                GROUP BY pycad_entity_id ORDER BY pycad_id)
                            AND pycad_entity_state NOT LIKE "DELETE"
                            AND pycad_object_type LIKE '%s'
                            AND pycad_undo_visible=1
                            """%(str(parent.getId()), str(childrenType))
        _dbEntRow=self.makeSelect(_sqlSelect)
        for _row in _dbEntRow:
            _style=pickle.loads(_row[3])
            _dumpObj=pickle.loads(_row[2])
            _objEnt=Entity(_row[1],_dumpObj,_style,_row[0])
            _objEnt.state=_row[4]
            _objEnt.index=_row[5]
            _objEnt.visible=_row[6]
            _objEnt.updateBBox()
            _outObj.append(_objEnt)

        return _outObj
    #@+node:1.20130426141258.3020: *3* getParentEnt
    def getParentEnt(self,entity):
        """
            get the parent entity
            TODO: To be tested
        """
        _sqlSelect="""SELECT pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_object_style,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                            FROM pycadent
                            WHERE pycad_entity_id IN
                                (
                                    SELECT pycad_parent_id
                                    FROM pycadrel
                                    WHERE pycad_child_id =%s
                                )
                            AND pycad_entity_state NOT LIKE "DELETE"
                            AND pycad_object_type LIKE '%s'
                            AND pycad_undo_visible=1
                            """%(str(entity.getId()), str(entity.eType))

        _dbEntRow=self.makeSelect(_sqlSelect)
        for _row in _dbEntRow:
            _style=pickle.loads(_row[3])
            _dumpObj=pickle.loads(_row[2])
            _objEnt=Entity(_row[1],_dumpObj,_style,_row[0])
            _objEnt.state=_row[4]
            _objEnt.index=_row[5]
            _objEnt.visible=_row[6]
            _objEnt.updateBBox()
            return _objEnt
        return None
    #@+node:1.20130426141258.3021: *3* deleteFromParent
    def deleteFromParent(self,entityObj):
        """
            Delete the entity from db
        """
        _entityId=entityObj.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_parent_id='%s'"""%str(_entityId)
        self.makeUpdateInsert(_sqlDelete)
    #@+node:1.20130426141258.3022: *3* deleteFromChild
    def deleteFromChild(self,entityObj):
        """
            Delete the entity from db
        """
        _entityId=entityObj.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_child_id='%s'"""%str(_entityId)
        self.makeUpdateInsert(_sqlDelete)
    #@+node:1.20130426141258.3023: *3* deleteRelation
    def deleteRelation(self,entityObjParent,entityObjChild):
        """
            delete the relation from parent and child
        """
        _parentId=entityObjParent.getId()
        _childId=entityObjChild.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_parent_id='%s' and pycad_child_id='%s'and """%(str(_parentId),str(_childId))
        self.makeUpdateInsert(_sqlDelete)
    #@+node:1.20130426141258.3024: *3* relationExsist
    def relationExsist(self, parentId, childId):
        """
            check if the given parent child id exsist or not
        """
        _sqlSelect="""SELECT COUNT(*)
                    FROM pycadrel
                    WHERE pycad_parent_id='%s' and pycad_child_id='%s'
                    """%(str(parentId),str(childId))
        res=self.fetchOneRow(_sqlSelect)
        return res
    #@-others
#@-others
"""
    TODO TEST deleteFromChild
    TODO TEST deleteRelation
"""
#@-leo
