# -*- coding: utf-8 -*-                                       

# Form implementation generated from reading ui file 'shaderRenamerGui2.ui'
#                                                                          
# Created: Thu Feb  5 12:50:08 2015                                        
#      by: pyside-uic 0.2.15 running on PySide 1.2.1                       
#                                                                          
# WARNING! All changes made in this file will be lost!                     

from PySide import QtCore, QtGui

class Ui_shaderRenamerGUI(object):
    def setupUi(self, shaderRenamerGUI):
        shaderRenamerGUI.setObjectName("shaderRenamerGUI")
        shaderRenamerGUI.setEnabled(True)                 
        shaderRenamerGUI.resize(444, 584)                 
        shaderRenamerGUI.setStyleSheet("")                
        self.centralwidget = QtGui.QWidget(shaderRenamerGUI)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)                                                      
        sizePolicy.setVerticalStretch(0)                                                        
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())       
        self.centralwidget.setSizePolicy(sizePolicy)                                            
        self.centralwidget.setObjectName("centralwidget")                                       
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)                               
        self.gridLayout_2.setObjectName("gridLayout_2")                                         
        self.mid_HBoxLayout = QtGui.QHBoxLayout()                                               
        self.mid_HBoxLayout.setObjectName("mid_HBoxLayout")                                     
        self.midLeft_GridLayout = QtGui.QGridLayout()                                           
        self.midLeft_GridLayout.setObjectName("midLeft_GridLayout")                             
        self.shadersListView = QtGui.QListView(self.centralwidget)                              
        self.shadersListView.setEnabled(True)                                                   
        self.shadersListView.setObjectName("shadersListView")                                   
        self.midLeft_GridLayout.addWidget(self.shadersListView, 0, 0, 1, 1)                     
        self.mid_HBoxLayout.addLayout(self.midLeft_GridLayout)                                  
        self.gridLayout_2.addLayout(self.mid_HBoxLayout, 2, 0, 1, 1)                            
        self.bottom_VBoxLayout = QtGui.QVBoxLayout()                                            
        self.bottom_VBoxLayout.setObjectName("bottom_VBoxLayout")                               
        self.assignedGeoLable = QtGui.QLabel(self.centralwidget)                                
        self.assignedGeoLable.setObjectName("assignedGeoLable")                                 
        self.bottom_VBoxLayout.addWidget(self.assignedGeoLable)                                 
        self.geoAssignedListWidget = QtGui.QListWidget(self.centralwidget)                      
        self.geoAssignedListWidget.setObjectName("geoAssignedListWidget")                       
        self.bottom_VBoxLayout.addWidget(self.geoAssignedListWidget)                            
        self.exportButton_HBoxLayout = QtGui.QHBoxLayout()                                      
        self.exportButton_HBoxLayout.setObjectName("exportButton_HBoxLayout")                   
        self.cancel_Button = QtGui.QPushButton(self.centralwidget)                              
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)    
        sizePolicy.setHorizontalStretch(0)                                                      
        sizePolicy.setVerticalStretch(0)                                                        
        sizePolicy.setHeightForWidth(self.cancel_Button.sizePolicy().hasHeightForWidth())
        self.cancel_Button.setSizePolicy(sizePolicy)
        self.cancel_Button.setMinimumSize(QtCore.QSize(0, 45))
        self.cancel_Button.setObjectName("cancel_Button")
        self.exportButton_HBoxLayout.addWidget(self.cancel_Button)
        self.renameButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.renameButton.sizePolicy().hasHeightForWidth())
        self.renameButton.setSizePolicy(sizePolicy)
        self.renameButton.setMinimumSize(QtCore.QSize(0, 45))
        self.renameButton.setStyleSheet("QPushButton{background-color: rgb(150, 200, 150);}")
        self.renameButton.setObjectName("renameButton")
        self.exportButton_HBoxLayout.addWidget(self.renameButton)
        self.bottom_VBoxLayout.addLayout(self.exportButton_HBoxLayout)
        self.gridLayout_2.addLayout(self.bottom_VBoxLayout, 4, 0, 1, 1)
        self.top_GridLayout = QtGui.QGridLayout()
        self.top_GridLayout.setObjectName("top_GridLayout")
        self.assetLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.assetLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.assetLineEdit.setText("")
        self.assetLineEdit.setObjectName("assetLineEdit")
        self.top_GridLayout.addWidget(self.assetLineEdit, 1, 0, 1, 1)
        self.variationLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.variationLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.variationLineEdit.setObjectName("variationLineEdit")
        self.top_GridLayout.addWidget(self.variationLineEdit, 1, 1, 1, 1)
        self.shadersLable = QtGui.QLabel(self.centralwidget)
        self.shadersLable.setObjectName("shadersLable")
        self.top_GridLayout.addWidget(self.shadersLable, 2, 0, 1, 1)
        self.assetLabel = QtGui.QLabel(self.centralwidget)
        self.assetLabel.setObjectName("assetLabel")
        self.top_GridLayout.addWidget(self.assetLabel, 0, 0, 1, 1)
        self.variationLable = QtGui.QLabel(self.centralwidget)
        self.variationLable.setObjectName("variationLable")
        self.top_GridLayout.addWidget(self.variationLable, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.top_GridLayout, 0, 0, 2, 1)
        self.infoLabel = QtGui.QLabel(self.centralwidget)
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout_2.addWidget(self.infoLabel, 5, 0, 1, 1)
        shaderRenamerGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(shaderRenamerGUI)
        QtCore.QMetaObject.connectSlotsByName(shaderRenamerGUI)

    def retranslateUi(self, shaderRenamerGUI):
        shaderRenamerGUI.setWindowTitle(QtGui.QApplication.translate("shaderRenamerGUI", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.assignedGeoLable.setText(QtGui.QApplication.translate("shaderRenamerGUI", "geo assigned:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_Button.setText(QtGui.QApplication.translate("shaderRenamerGUI", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.renameButton.setText(QtGui.QApplication.translate("shaderRenamerGUI", "Rename Shaders", None, QtGui.QApplication.UnicodeUTF8))
        self.shadersLable.setText(QtGui.QApplication.translate("shaderRenamerGUI", "shaders:", None, QtGui.QApplication.UnicodeUTF8))
        self.assetLabel.setText(QtGui.QApplication.translate("shaderRenamerGUI", "Asset:", None, QtGui.QApplication.UnicodeUTF8))
        self.variationLable.setText(QtGui.QApplication.translate("shaderRenamerGUI", "Variation:", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("shaderRenamerGUI", "info", None, QtGui.QApplication.UnicodeUTF8))
