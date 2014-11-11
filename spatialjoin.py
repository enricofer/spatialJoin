# -*- coding: utf-8 -*-
"""
/***************************************************************************
 spatialJoin
                                 A QGIS plugin
 spatialJoin
                              -------------------
        begin                : 2014-11-11
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from spatialjoindialog import spatialJoinDialog
import os.path


class spatialJoin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'spatialjoin_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = spatialJoinDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/spatialjoin/icon.png"),
            u"spatialJoin", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&spatialJoin", self.action)
        self.dlg.sourceLayerCombo.activated.connect(self.updateAttributeTable)
        self.dlg.buttonBox.accepted.connect(self.applyJoin)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&spatialJoin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def populateComboBox(self,combo,list,predef = '',sort = True):
        #procedure to fill specified combobox with provided list
        combo.clear()
        model=QStandardItemModel(combo)
        for elem in list:
            try:
                item = QStandardItem(unicode(elem))
            except TypeError:
                item = QStandardItem(str(elem))
            model.appendRow(item)
        if sort:
            model.sort(0)
        combo.setModel(model)
        if predef != "":
            combo.insertItem(0,predef)
            combo.setCurrentIndex(0)

    def updateAttributeTable(self):
        if self.dlg.sourceLayerCombo.currentText()[:6] != 'Select' and self.dlg.sourceLayerCombo.currentText() in self.layerSet.keys():
            idx = 0
            fields = [field for field in self.layerSet[self.dlg.sourceLayerCombo.currentText()].pendingFields()]
            self.dlg.attributesTable.clear()
            self.dlg.attributesTable.setRowCount(len(fields))
            self.dlg.attributesTable.setColumnCount(2)
            for field in fields:
                item=QTableWidgetItem()
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                item.setText("")
                #set first column as checkbox
                self.dlg.attributesTable.setItem(idx,0,item)
                #set second colunm as attribute label
                self.dlg.attributesTable.setItem(idx,1,QTableWidgetItem(field.name()))
                idx += 1
            #resize table to contents
            self.dlg.attributesTable.resizeColumnsToContents()
            self.dlg.attributesTable.horizontalHeader().setStretchLastSection(True)

    def getSelFieldList(self):
        res = []
        for idx in range(0,self.dlg.attributesTable.rowCount()):
            if self.dlg.attributesTable.item(idx,0).checkState() == Qt.Checked:
                res.append(self.dlg.attributesTable.item(idx,1).data(Qt.DisplayRole))
        if res == []:
            return None
        else:
            return res


    # run method that performs all the real work
    def run(self):
        self.layerSet = {layer.name():layer for layer in self.iface.legendInterface().layers()}
        self.populateComboBox(self.dlg.destLayerCombo,self.layerSet.keys())
        self.populateComboBox(self.dlg.sourceLayerCombo,self.layerSet.keys(),'Select Layer to spatial join')
        self.populateComboBox(self.dlg.spatialTypeCombo,['nearest','within','contains','crosses','disjoint','equals','intersects','overlaps','touches'],'Select spatial Join type',None)

        # show the dialog
        self.dlg.show()

    def applyJoin(self):
        selectedFields = self.getSelFieldList()
        if selectedFields and self.dlg.destLayerCombo.currentText()[:6] != 'Select' and self.dlg.sourceLayerCombo.currentText()[:6] != 'Select' and self.dlg.spatialTypeCombo.currentText()[:6] != 'Select':
            destLayer = self.layerSet[self.dlg.destLayerCombo.currentText()]
            sourceLayer = self.layerSet[self.dlg.sourceLayerCombo.currentText()]
            sourceLayerFields = [field.name() for field in sourceLayer.pendingFields()]
            destLayerFields = [field.name() for field in destLayer.pendingFields()]
            if not 'sjid' in sourceLayerFields:
                sourceLayer.addExpressionField('$id', QgsField('sjid', QVariant.Int))
                sourceLayer.updateFields()
            if 'sjrif' in destLayerFields:
                destLayer.removeExpressionField(destLayer.pendingFields().fieldNameIndex('sjrif'))
                destLayer.updateFields()
            exp = "geom"+self.dlg.spatialTypeCombo.currentText()+"('"+sourceLayer.name()+"','sjid')"
            destLayer.addExpressionField(exp, QgsField('sjrif', QVariant.Int))
            destLayer.updateFields()
            join = QgsVectorJoinInfo()
            join.targetFieldName = "sjrif"
            join.joinLayerId = sourceLayer.id()
            join.joinFieldName = "sjid"
            join.memoryCache = True
            destLayer.addJoin(join)


