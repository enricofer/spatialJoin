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
from qgis.core import QgsRelation, QgsProject
from qgis.utils import plugins
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from spatialjoindialog import spatialJoinDialog
import os.path
import uuid

class trace:
    """
    class for tracing debug infos
    """

    def __init__(self):
        self.trace = False

    def ce(self,string):
        if self.trace:
            s = repr(string).decode('utf8')
            print(s)

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
        self.tra = trace()

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
        self.dlg.joinLayerCombo.activated.connect(self.updateAttributeTable)
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
            for row in range (0,combo.count()):
                if combo.itemText(row) == predef:
                    pos = row
            try:
                combo.setCurrentIndex(pos)
            except:
                combo.insertItem(0,predef)
                combo.setCurrentIndex(0)

    def updateAttributeTable(self):
        if self.dlg.joinLayerCombo.currentText()[:6] != 'Select' and self.dlg.joinLayerCombo.currentText() in self.layerSet.keys():
            idx = 0
            fields = [field for field in self.layerSet[self.dlg.joinLayerCombo.currentText()].pendingFields()]
            self.dlg.attributesTable.clear()
            self.dlg.attributesTable.setRowCount(len(fields))
            self.dlg.attributesTable.setColumnCount(2)
            for field in fields:
                item=QTableWidgetItem()
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                item.setText("")
                #set first column as checkbox
                if field.name()[0:5] != 'sjrif':
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
        if not 'refFunctions' in plugins:
            QMessageBox.critical(None, "Plugin Dependency:", "Plugin 'refFunctions' is needed.\nInstall it from Qgis repository before performing spatial joins")
            return
        self.layerSet = {}
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                self.layerSet[layer.name()]=layer
        self.dlg.attributesTable.clear()
        self.dlg.progressBar.reset()
        if self.iface.legendInterface().currentLayer():
            cLayerName = self.iface.legendInterface().currentLayer().name()
        else:
            cLayerName = ""
        self.populateComboBox(self.dlg.targetLayerCombo,self.layerSet.keys(),cLayerName)
        self.populateComboBox(self.dlg.joinLayerCombo,self.layerSet.keys(),'Select Layer to spatial join')
        self.populateComboBox(self.dlg.spatialTypeCombo,['nearest','within','contains','crosses','disjoint','equals','intersects','overlaps','touches'],'Select spatial Join type',None)
        # show the dialog
        self.dlg.show()

    def applyJoin(self):
        self.dlg.show()
        selectedFields = self.getSelFieldList() or []
        if self.dlg.targetLayerCombo.currentText()[:6] != 'Select' and self.dlg.joinLayerCombo.currentText()[:6] != 'Select' and self.dlg.spatialTypeCombo.currentText()[:6] != 'Select':
            targetLayer = self.layerSet[self.dlg.targetLayerCombo.currentText()]
            joinLayer = self.layerSet[self.dlg.joinLayerCombo.currentText()]
            joinLayerFields = [field.name() for field in joinLayer.pendingFields()]
            #targetLayerFields = [field.name() for field in targetLayer.pendingFields()]
            targetLayerFields = []
            for field in targetLayer.pendingFields():
                if field.name()[0:7] == 'spjoin_':
                    idx = targetLayer.pendingFields().fieldNameIndex(field.name())
                    self.tra.ce("removing:"+field.name()+str(idx))
                    targetLayer.dataProvider().deleteAttributes([idx])
                    targetLayer.removeExpressionField(idx)
                else:
                    targetLayerFields.append(field.name())
            self.tra.ce(targetLayerFields)
            targetLayer.updateFields()
            joinField = 'spjoin_rif'
            exp = "geom"+self.dlg.spatialTypeCombo.currentText()+"('"+joinLayer.name()+"','$id')"
            self.tra.ce( exp)
            #add a rif field if build relation requested
            if self.dlg.checkBuildRelation.checkState() == Qt.Checked:
                #joinLayer.addExpressionField('$id', QgsField('spjoin_rif', QVariant.Int))
                joinLayer.dataProvider().addAttributes([QgsField(joinField, QVariant.Int)])
                #joinLayer.updateFields()
                idx = joinLayer.dataProvider().fields().fieldNameIndex(joinField)
                expObj = QgsExpression('$id')
                changes = {}
                for feature in joinLayer.getFeatures():
                    value = expObj.evaluate(feature)
                    #joinLayer.dataProvider().changeAttributeValues({feature.id():{idx:value}})
                    changes[feature.id()] = {idx:value}
                joinLayer.dataProvider().changeAttributeValues(changes)
            if self.dlg.checkDynamicJoin.checkState() == Qt.Checked:
                targetLayer.addExpressionField(exp, QgsField(joinField, QVariant.Int))
            else:
                #Create static rif field
                targetLayer.dataProvider().addAttributes([QgsField(joinField, QVariant.Int)])
                #targetLayer.updateFields()
                F = [field.name() for field in targetLayer.dataProvider().fields()]
                self.tra.ce(F)
                #Compile spatial expression to get feature rifs
                expObj = QgsExpression(exp)
                expObj.prepare(targetLayer.pendingFields())
                idx = targetLayer.dataProvider().fields().fieldNameIndex(joinField)
                self.tra.ce( "new " + joinField + str(idx))
                changes = {}
                #init progress bar
                self.dlg.progressBar.setMinimum(0)
                self.dlg.progressBar.setMaximum(targetLayer.featureCount())
                #cicle into feature to build mod vector
                for count, feature in enumerate(targetLayer.getFeatures()):
                    self.dlg.progressBar.setValue(count)
                    value = expObj.evaluate(feature)
                    changes[feature.id()] = {idx:value}
                self.tra.ce(changes)
                #apply mod vector
                targetLayer.dataProvider().changeAttributeValues(changes)
            targetLayer.updateFields()
            #build expression fields to connect to join field rif
            for f in selectedFields:
                fieldType = joinLayer.pendingFields().field(f).type()
                exp = """dbvaluebyid('%s','%s',"%s")""" %(joinLayer.name(),f,joinField)
                self.tra.ce(exp)
                targetLayer.addExpressionField(exp, QgsField('spjoin_'+f, fieldType))
            targetLayer.updateFields()
            if self.dlg.checkBuildRelation.checkState() == Qt.Checked:
                jRel = 	QgsRelation()
                jRel.setRelationId(targetLayer.name()+"_"+str(uuid.uuid1()))
                jRel.setRelationName("%s_%s-rif_%s" % (targetLayer.name(),self.dlg.spatialTypeCombo.currentText(),joinLayer.name()))
                jRel.setReferencedLayer(joinLayer.id())
                jRel.setReferencingLayer(targetLayer.id())
                jRel.addFieldPair('spjoin_rif','spjoin_rif')
                QgsProject.instance().relationManager().addRelation(jRel)
            self.dlg.hide()


