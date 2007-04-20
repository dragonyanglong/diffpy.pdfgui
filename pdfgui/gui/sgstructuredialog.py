#!/usr/bin/env python
########################################################################
#
# PDFgui            by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################

# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4 on Mon Oct 30 11:01:37 2006

import wx
from copy import copy
import math
from diffpy.Structure import SpaceGroups
from diffpy.pdfgui.control.controlerrors import *
from pdfpanel import PDFPanel

class SGStructureDialog(wx.Dialog, PDFPanel):
    def __init__(self, *args, **kwds):
        PDFPanel.__init__(self)
        # begin wxGlade: SGStructureDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.sizer_2_staticbox = wx.StaticBox(self, -1, "Space Group Expansion")
        self.numConstrainedLabel = wx.StaticText(self, -1, "")
        self.sgLabel = wx.StaticText(self, -1, "Space Group")
        self.sgComboBox = wx.ComboBox(self, -1, choices=["P1"], style=wx.CB_DROPDOWN)
        self.offsetLabel = wx.StaticText(self, -1, "Origin Offset")
        self.offsetTextCtrlX = wx.TextCtrl(self, -1, "0", style=wx.TE_PROCESS_ENTER)
        self.offsetTextCtrlY = wx.TextCtrl(self, -1, "0", style=wx.TE_PROCESS_ENTER)
        self.offsetTextCtrlZ = wx.TextCtrl(self, -1, "0", style=wx.TE_PROCESS_ENTER)
        self.static_line_1 = wx.StaticLine(self, -1)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.okButton = wx.Button(self, wx.ID_OK, "OK")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.onSGTextEnter, self.sgComboBox)
        self.Bind(wx.EVT_COMBOBOX, self.onSGSelect, self.sgComboBox)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOXTextEnter, self.offsetTextCtrlX)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOYTextEnter, self.offsetTextCtrlY)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOZTextEnter, self.offsetTextCtrlZ)
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
        # end wxGlade
        self.__customProperties()

    def __set_properties(self):
        # begin wxGlade: SGStructureDialog.__set_properties
        self.SetTitle("Space Group Expansion")
        self.sgComboBox.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SGStructureDialog.__do_layout
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.VERTICAL)
        sizer_4_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.numConstrainedLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_3.Add(self.sgLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_3.Add(self.sgComboBox, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.offsetLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.offsetTextCtrlX, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.offsetTextCtrlY, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.offsetTextCtrlZ, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_2.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_4_copy.Add((0, 0), 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_4_copy.Add(self.cancelButton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_4_copy.Add(self.okButton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(sizer_4_copy, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        sizer_2.SetSizeHints(self)
        self.Layout()
        # end wxGlade


    ###########################################################################

    def __customProperties(self):
        """Set the custom properties."""
        # Get the available space group names and add them to the ComboBox
        self.sgComboBox.Clear()
        sgnames = [(sg.number, sg.short_name) for sg in\
                SpaceGroups.SpaceGroupList]
        sgnames.sort()
        for (number, name) in sgnames[:230]:
            self.sgComboBox.Append(name)
        self.sgComboBox.SetValue('P1')

        self.spacegroup = SpaceGroups.GetSpaceGroup('P1')
        self.offset = [0,0,0]
        self.structure = None
        self.indices = []

        self.textCtrls = [self.offsetTextCtrlX, self.offsetTextCtrlY,
                self.offsetTextCtrlZ]

        # Set the focus events.
        for textctrl in self.textCtrls:
            textctrl.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus) 
        self.sgComboBox.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus) 
        return

    def setStructure(self, structure):
        """Set the structure and update the dialog."""
        self.structure = structure
        self.updateWidgets()
        return

    def getSpaceGroup(self):
        """Get the current space group."""
        return self.spacegroup

    def getOffset(self):
        """Get the offset."""
        return self.offset

    def updateWidgets(self):
        """Update the widgets."""
        # Update space group
        sgname = self.sgComboBox.GetValue()
        try:
            sgname = int(sgname)
        except ValueError:
            pass
        self.spacegroup = SpaceGroups.GetSpaceGroup(sgname)
        self.sgComboBox.SetValue(self.spacegroup.short_name)

        # Update offset
        for i in range(3):
            textctrl = self.textCtrls[i]
            val = textctrl.GetValue()
            # make sure the value is meaningful
            try:
                val = float(eval("1.0*"+val, dict(math.__dict__)))
            except (NameError, TypeError, SyntaxError):
                val = 0
            textctrl.SetValue("%s"%val)
            self.offset[i] = val
        
        # Check the space group
        error = ""
        if sgname != self.spacegroup.short_name and \
            sgname != self.spacegroup.number:
            error = "Space group %s does not exist." % sgname

        # find how many new atoms would be generated
        from diffpy.Structure.SymmetryUtilities import ExpandAsymmetricUnit
        corepos = [ self.structure[i].xyz for i in self.indices ]
        symposeps = self.structure.symposeps
        eau = ExpandAsymmetricUnit(self.spacegroup, corepos,
                sgoffset=self.offset, eps=symposeps)
        newsize = sum(eau.multiplicity)
        s = ""
        if len(self.indices) != 1:
            s = "s"
        message = "%i atom%s selected.  Expanding to %i positions." %\
                (len(self.indices), s, newsize)
        self.numConstrainedLabel.SetLabel(message)

        # Raise an error if we had to change the space group
        if error:
            raise ControlValueError(error);
        return

    ### Events
    def onKillFocus(self, event):
        """Check value of widgets and update the dialog message."""
        self.updateWidgets()
        return

    def onSGTextEnter(self, event): # wxGlade: SGStructureDialog.<event_handler>
        self.updateWidgets()
        self.onOk(None)
        return

    def onSGSelect(self, event): # wxGlade: SGStructureDialog.<event_handler>
        self.updateWidgets()
        return

    def onOXTextEnter(self, event): # wxGlade: SGStructureDialog.<event_handler>
        self.updateWidgets()
        self.onOk(None)
        return

    def onOYTextEnter(self, event): # wxGlade: SGStructureDialog.<event_handler>
        self.updateWidgets()
        self.onOk(None)
        return

    def onOZTextEnter(self, event): # wxGlade: SGStructureDialog.<event_handler>
        self.updateWidgets()
        self.onOk(None)
        return

    def onOk(self, event): # wxGlade: SGStructureDialog.<event_handler>
        # check to see if the space group is consistant
        if not self.structure.isSpaceGroupPossible(self.spacegroup):
            message =  "The chosen space group is not consistent\n"
            message += "with the lattice parameters.\n"
            message += "Would you like to proceed anyways?"
            d = wx.MessageDialog( self, message, 
                    "Inconsistent space group", wx.YES_NO)
            code = d.ShowModal()
            if code == wx.ID_YES:
                self.EndModal(wx.ID_OK)
        else:
            self.EndModal(wx.ID_OK)
        return

    def onCancel(self, event): # wxGlade: SGStructureDialog.<event_handler>
        event.Skip()
        return

__id__ = "$Id$"

# end of class SGStructureDialog
