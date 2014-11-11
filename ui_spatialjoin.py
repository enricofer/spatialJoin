# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_spatialjoin.ui'
#
# Created: Tue Nov 11 15:57:43 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_spatialJoin(object):
    def setupUi(self, spatialJoin):
        spatialJoin.setObjectName(_fromUtf8("spatialJoin"))
        spatialJoin.resize(256, 398)
        self.verticalLayout = QtGui.QVBoxLayout(spatialJoin)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(spatialJoin)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.destLayerCombo = QtGui.QComboBox(spatialJoin)
        self.destLayerCombo.setObjectName(_fromUtf8("destLayerCombo"))
        self.verticalLayout.addWidget(self.destLayerCombo)
        self.label_3 = QtGui.QLabel(spatialJoin)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.spatialTypeCombo = QtGui.QComboBox(spatialJoin)
        self.spatialTypeCombo.setObjectName(_fromUtf8("spatialTypeCombo"))
        self.verticalLayout.addWidget(self.spatialTypeCombo)
        self.label_2 = QtGui.QLabel(spatialJoin)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.sourceLayerCombo = QtGui.QComboBox(spatialJoin)
        self.sourceLayerCombo.setObjectName(_fromUtf8("sourceLayerCombo"))
        self.verticalLayout.addWidget(self.sourceLayerCombo)
        self.label_4 = QtGui.QLabel(spatialJoin)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.attributesTable = QtGui.QTableWidget(spatialJoin)
        self.attributesTable.setShowGrid(False)
        self.attributesTable.setObjectName(_fromUtf8("attributesTable"))
        self.attributesTable.setColumnCount(0)
        self.attributesTable.setRowCount(0)
        self.attributesTable.horizontalHeader().setVisible(False)
        self.attributesTable.verticalHeader().setVisible(False)
        self.attributesTable.verticalHeader().setDefaultSectionSize(20)
        self.attributesTable.verticalHeader().setMinimumSectionSize(15)
        self.verticalLayout.addWidget(self.attributesTable)
        self.buttonBox = QtGui.QDialogButtonBox(spatialJoin)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(spatialJoin)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), spatialJoin.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), spatialJoin.reject)
        QtCore.QMetaObject.connectSlotsByName(spatialJoin)

    def retranslateUi(self, spatialJoin):
        spatialJoin.setWindowTitle(QtGui.QApplication.translate("spatialJoin", "spatialJoin", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("spatialJoin", "Destination Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("spatialJoin", "Spatial join type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("spatialJoin", "Layer to Join", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("spatialJoin", "Attributes to join", None, QtGui.QApplication.UnicodeUTF8))

