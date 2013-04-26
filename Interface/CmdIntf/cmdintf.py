#@+leo-ver=5-thin
#@+node:1.20130426141258.3705: * @file cmdintf.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3706: ** <<declarations>> (cmdintf)
import os
import sys

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui

from Interface.CmdIntf.cmdcategory  import CmdCategory
from Interface.CmdIntf.cmdaction    import CmdAction
from Interface.CmdIntf.cmdlinedock  import CmdLineDock
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3707: ** class CmdIntf
class CmdIntf(object):
    '''
    Future implementation:
        Dynamic read menu, toolbars and panels from a cui/xml definition file.
    Current implementation:
        Create static menu, toolbars and palettes.
    '''
    #@+others
    #@+node:1.20130426141258.3708: *3* __init__
    def __init__(self, parent):
        # parent is the main_window object
        self.__main_window = parent
        # command line window
        self.__edit_ctrl = CmdLineDock('Command', self.__main_window)
        # dictionary with file action objects
        self.__actions = {}
        # categories in which commands are stored
        self.__category = CmdCategory(self.__main_window) 
        # icons search path
        self.__icon_dir = os.path.join(os.getcwd(), 'icons')
        #add custom event
        return
    #@+node:1.20130426141258.3709: *3* commandLine
    #-------- properties -----------#
    @property
    def commandLine(self):
        """
            Get the command line dock window
        """
        return self.__edit_ctrl
    #@+node:1.20130426141258.3710: *3* FunctionHandler
    @property
    def FunctionHandler(self):
        """
            Get the function handler object
        """
        return self.__edit_ctrl.FunctionHandler
    #@+node:1.20130426141258.3711: *3* Category
    @property 
    def Category(self):
        """
            Get the category enumerator object
        """
        return self.__category   
    #@+node:1.20130426141258.3712: *3* _actionHandler
    #-------- properties -----------#
    @QtCore.pyqtSlot(str)
    def _actionHandler(self, expression):
        '''
        Callback function for all QAction objects.
        1) Look up command in the dictionary.
        2) Execute command by calling the FunctionHandler.Evaluate member.
        '''
        # evaluate command
        if len(expression) > 0:
            # command is found, evaluate it
            self.__edit_ctrl.FunctionHandler.evaluate(expression)
        return
    #@+node:1.20130426141258.3713: *3* _getIcon
    def _getIcon(self, cmd):
        '''
        Create an QIcon object based on the command name.
        The name of the icon is ':/images/' + cmd + '.png'.
        If the cmd = 'Open', the name of the icon is ':/images/Open.png'.
        '''
        icon_name = cmd + '.png'
        icon_path = os.path.join(self.__icon_dir, icon_name)
        # check if icon exist
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            return icon
        # icon not found, don't use an icon, return None
        return None
    #@+node:1.20130426141258.3714: *3* registerCommand
    def registerCommand(self, category_enum, cmd, text=None, callback=None):
        '''
        Register a command with it's call-back in the command table.
        Commands are executed by a call to the evaluate function.
        params:
            category_enum: enumerated attribute value of CmdCategory
            cmd: command name
            text: menu entry text 
            callback: call-back function
        '''
        # get the menu for this category
        menu = self.__category.getMenu(category_enum)
        # get the tool-bar for this category
        toolbar = self.__category.getToolbar(category_enum)
        # Check for the special separator name: '-'
        # A separator is not a command, it defines an separator in the menu and tool-bar.
        if cmd == '-':
            # add a separator to the menu
            if not menu is None:
                menu.addSeparator()
#            # add a separator to the tool-bar
            if not toolbar is None:
                toolbar.addSeparator()
        elif cmd=='>':
            #add subMenu
            pass
        else:
            # register the command with the function handler
            self.__edit_ctrl.FunctionHandler.registerCommand(cmd, callback)
            # get an icon for command, needed for tool-bar
            icon = self._getIcon(cmd)
            # create action object for this command
            action = CmdAction(cmd, icon, text, self.__main_window, self.__edit_ctrl.FunctionHandler)
            #action.callback = self._actionHandler
            # add it to the action table for fast lookup
            self.__actions[cmd] = action
            # add action to menu
            if not menu is None:
                menu.addAction(action)
            # add action to tool-bar only if an icon if found
            if (not toolbar is None) and (not icon is None):
                toolbar.addAction(action)
        return
    #@+node:1.20130426141258.3715: *3* evaluate
    def evaluate(self, expression):
        '''
        Looks up the expression from the command table.
        If a command is found, it's callback function is called.
        If it is not a command the expression is evaluated.
        Return: command exit, the evaluated expression or "*error*"
        '''    
        self.__edit_ctrl.FunctionHandler.evaluate(expression)
        return
    #@+node:1.20130426141258.3716: *3* evaluateInnerCommand
    def evaluateInnerCommand(self, kernelCommand, selectedItems):
        '''
            evaluate a kernel command
        '''
        self.__edit_ctrl.FunctionHandler.evaluateInnerCommand(kernelCommand, selectedItems)
    #@+node:1.20130426141258.3717: *3* evaluateMouseImput
    def evaluateMouseImput(self,view,event):
        '''
            get imput from viewport
        '''
        self.__edit_ctrl.FunctionHandler.evaluateMouseImput(event)
    #@+node:1.20130426141258.3718: *3* resetCommand
    def resetCommand(self):
        """
            reset the active command 
        """
        self.__edit_ctrl.FunctionHandler.resetCommand()
    #@+node:1.20130426141258.3719: *3* hideAction
    def hideAction(self, name):
        """
            hide the name action
        """
        if name in self.__actions:
            self.__actions[name].hide()
    #@+node:1.20130426141258.3720: *3* showAction
    def showAction(self, name):
        """
            show the name action
        """
        if name in self.__actions:
            self.__actions[name].show()
    #@+node:1.20130426141258.3721: *3* setVisible
    def setVisible(self, name, value):
        """
            set the action name to visible value
        """
        if name in self.__actions:
            if value:
                self.__actions[name].show()
            else:
                self.__actions[name].hide()
    #@+node:1.20130426141258.3722: *3* updateText
    def updateText(self, name, text):
        """
            update the label text
        """
        if name in self.__actions:
            self.__actions[name].setText(text)
    #@-others
#@-others
#@-leo
