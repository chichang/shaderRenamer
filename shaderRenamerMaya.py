#!/usr/bin/python2.6


'''
#!/usr/bin/python2.6
import sys
sys.path.insert(0,"/USERS/chichang/workspace/shaderRenamer")
import shaderRenamerMaya
reload(shaderRenamerMaya)
shadrenamer = shaderRenamerMaya.shaderRenamerWindow()
shadrenamer.show()

http://srinikom.github.io/pyside-docs/PySide/QtGui/QStandardItem.html
http://srinikom.github.io/pyside-docs/PySide/QtGui/QStandardItemModel.html
http://srinikom.github.io/pyside-docs/PySide/QtGui/QListView.html

http://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
'''

import sys
import os
import re
import maya.cmds as mc
from PySide import QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
import shiboken
from shaderRenamerGui import Ui_shaderRenamerGUI

def maya_main_window():
	#Get the maya main window as a QMainWindow instance
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


class shaderRenamerWindow(QtGui.QMainWindow, Ui_shaderRenamerGUI):

	def __init__(self, parent=maya_main_window()):
		#super
		'''Mandatory initialization of the class.'''
		super(shaderRenamerWindow, self).__init__(parent)
		self.setupUi(self)
		print "setting up ui."

		DEFAULT_ASSET_STRING = ""
		DEFAULT_VARIATION_STRING = ""

		self.INFO_CLEAN = ""
		self.INFO_DIRTY = "Please rename shader: (ASSET)_(shader)_(variation)_shad"

		self.cancel_Button.clicked.connect(self.close)
		self.renameButton.clicked.connect(self.rename)
		self.shadersListView.clicked[QtCore.QModelIndex].connect(self.itemClicked)
		#self.shadersListView.dataChanged[QtCore.QModelIndex].connect(self.dataChanged)
		#self.shadersListView.entered[QtCore.QModelIndex].connect(self.entered)


		self.geoAssignedListWidget.clicked.connect(self.selectGeo)

		#find asset if not use shot name
		rcnulls = self.getAssetInScene()
		if rcnulls:
			if len(rcnulls) != 0:
				#assume we only have one asset in the scene for now
				assetName = mc.getAttr(rcnulls[0]+".assetString")
		else:
			#use the shot
			try:
				shot = os.getenv("SHOT")
				assetName = shot
			except:
				print "error getting shot. use default name"
				assetName = DEFAULT_ASSET_STRING

		#fill this in when adding variation support
		variationName = DEFAULT_VARIATION_STRING

		self.assetLineEdit.setText(assetName)
		self.variationLineEdit.setText(variationName)

		#Disable for now
		disablePallet = QtGui.QPalette()
		#disablePallet.setColor(QtGui.QPalette.Base, QtCore.Qt.darkGray)
		disablePallet.setColor(QtGui.QPalette.Text, QtCore.Qt.gray)
		self.assetLineEdit.setPalette(disablePallet)
		self.variationLineEdit.setPalette(disablePallet)
		self.assetLineEdit.setReadOnly(True)
		self.variationLineEdit.setReadOnly(True)


		self.model = shadersItemModel()
		self.shadersListView.setModel(self.model)


		self.shadersToLoad, self.geoConnections = self.getAllShaders()
		row = 0
		for shader in self.shadersToLoad.keys():
			item = shaderItem(shader)
			item.validateName(self.assetLineEdit.text())

			self.model.setItem(row, 0, item)
			#model.clicked[row].connect(self.clicked)
			row += 1

		#not Item Changed find name changed??
		#self.model.itemChanged.connect(self.nameChanged)
		self.model.dataChanged.connect(self.nameChanged)


	def getAllShaders(self):
		#returns all shaders in the scene. that's connected to a shading group.
		print "getting all shaders in the scene."
		shadingGroups = mc.ls(type="shadingEngine")

		#get shaders and coresponding shading groups
		allShaders = dict()
		#get sading group and connected geo
		allMeshConnections = dict()

		ignorSg = ['initialParticleSE', 'initialShadingGroup']
		for sg in shadingGroups:
			if sg not in ignorSg:
				connectedShader = mc.connectionInfo(sg+".surfaceShader", sfd=True)
				connectedShader = connectedShader.split(".")[0]

				allShaders[connectedShader] = sg
				allMeshConnections[connectedShader] = mc.listConnections(sg, s=True, sh=True, type="mesh")

		print allShaders, allMeshConnections
		return allShaders, allMeshConnections


	def getAssetInScene(self):
		#getting the asset. assuming we are only lookdeving one asset for now.
		try:
			rcnulls = mc.ls(type="rigCenterNode")
			return rcnulls
		except:
			print "node type rigCenterNode not exsist"
			return None


	def rename(self):
		#do the rename.
		print "rename shaders."
		numShaders = self.model.rowCount()
		for i in range(0, numShaders):
			item = self.model.item(i)

			originalShaderName = item.oldName
			newShaderName = item.text()

			originalSGName = self.shadersToLoad[originalShaderName]
			newSGName = newShaderName + "SG"

			if originalShaderName != newShaderName:
				#rename shader
				print originalShaderName + " => " + newShaderName
				mc.rename(originalShaderName, newShaderName)

			else:
				newShaderName = originalShaderName


			#rename the shading group
			self.renameShadingGroup(originalSGName, newSGName)

			#done
			self.close()


	def renameShadingGroup(self, oldName, newName):
		#rename the shading group to match shader
		if oldName != newName:
			mc.rename(oldName, newName)
			print "renaming shading group:"
			print oldName + " => " + newName


	#def nameChanged(self, item):
	def nameChanged(self, index):
		#new shader name entered. check if it's valid
		#re chek

		item = self.model.item(index.row())


		numShaders = self.model.rowCount()
		changedItemRow = item.index().row()

		## check if there are shaders named the same

		#for i in range(0, numShaders):

			#if i == changedItemRow:
				#continue

			#print "checking " + item.text()
			#print "against: " + self.model.item(i).text()

			#if item.text() == self.model.item(i).text():
				#set to dirty
				#item.nameClash()
				#return

		#nothing name the same.
		#item.nameResolved()

		#block signals until functions is done
		self.model.blockSignals(True)
		item.validateName(self.assetLineEdit.text())
		self.model.blockSignals(False)




	def itemClicked(self, index):
		item = self.model.itemFromIndex(index)
		#self.model.itemData(index)
		print index.row()
		print self.model.itemData(index)
		#self.model.setData("d", 222)
		# Do stuff with the item ...
		shader = item.oldName

		self.geoAssignedListWidget.clear()
		assignedGeo = self.geoConnections[shader]
		if assignedGeo:
			for geo in assignedGeo:
				self.geoAssignedListWidget.addItem(geo)

		if item.clean:
			self.infoLabel.setText(self.INFO_CLEAN)
		else:
			self.infoLabel.setText(self.INFO_DIRTY)




	def selectGeo(self,index):
		row = index.row()
		shape = self.geoAssignedListWidget.item(row).text()
		transform = mc.listRelatives(shape, p=True, type="transform")
		mc.select(clear=True)
		mc.select(transform)


class shaderItem(QtGui.QStandardItem):
	def __init__(self, shaderName):
		super(shaderItem, self).__init__()
		
		self.setText(shaderName)

		self.clean = True
		self.oldName = shaderName

		self.DEFAULT_ICON = QtGui.QIcon("/mnt/X/tools/binlinux/aw/maya2014-x64_sp1/icons/fpe_okPaths.png")
		self.WARNING_ICON = QtGui.QIcon("/mnt/X/tools/binlinux/aw/maya2014-x64_sp1/icons/fpe_someBrokenPaths.png")
		
		self.setIcon(self.DEFAULT_ICON)


	def validateName(self, asset):
		print "validating shader name ..."

		if validShaderName(asset, self.text()):
			print "good shader name"
			self.setIcon(self.DEFAULT_ICON)
			self.clean = True
		else:
			print "bad shader name"
			self.setIcon(self.WARNING_ICON)
			self.clean = False







	def nameClash(self):
		#name clash
		print "name clash!!"
		self.clean = False
		print self.clean
		self.setIcon(self.WARNING_ICON)

	def nameResolved(self):
		#name clash
		self.clean = True
		print "name ok."
		print self.clean
		#self.setIcon(self.DEFAULT_ICON)






class shadersItemModel(QtGui.QStandardItemModel):
	def __init__(self):
		super(shadersItemModel, self).__init__()
		print "model view created!"
















def validShaderName(assetName, shaderName):

    print "checking shader name: "+ shaderName

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='((?:[a-z][a-z]+))' # Word 2
    re6='(_)'   # Any Single Character 3
    re7='(shad)'    # Word 3
    re8='($)'
    
    rg1 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m1 = rg1.search(shaderName)

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='((?:[a-z]+))' # Word 2
    re6='(_)'   # Any Single Character 3
    re7='(shad)'    # Word 3
    re8='($)'

    rg2 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m2 = rg2.search(shaderName)
    
    print m1, m2

    if m1 or m2:
        word1=m2.group(1)
        c1=m2.group(2)
        c2=m2.group(3)
        word2=m2.group(4)
        c3=m2.group(5)
        word3=m2.group(6)
        #print "("+word1+")"+"("+c1+")"+"("+c2+")"+"("+word2+")"+"("+c3+")"+"("+word3+")"+"\n"
        #print "valid shader name:  " + shaderName
        return True
        
    else:
        print "invalid shader name!! :  " + shaderName
        return False





	# To edit the data behind the name, I'll add a method within my QListWidget that creates a custom editing environment:

	# def edit_items(self):
	#     dialog = MyQDialog(self.parent())
	#     table = QTableWidget(self.count(),2,dialog)
	#     for row in range(0, self.count()):
	#         spec = repr(self.item(row).data(32).toPyObject())
	#         name = self.item(row).text()
	#         spec_item = QTableWidgetItem(spec)
	#         name_item = QTableWidgetItem(name)
	#         table.setItem(row,0,name_item)
	#         table.setItem(row,1,spec_item)
	#     layout = QHBoxLayout()
	#     layout.addStrut(550)
	#     layout.addWidget(table)
	#     dialog.setLayout(layout)
	#     dialog.show()