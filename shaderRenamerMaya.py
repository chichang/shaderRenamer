
'''
http://srinikom.github.io/pyside-docs/PySide/QtGui/QStandardItem.html
http://srinikom.github.io/pyside-docs/PySide/QtGui/QStandardItemModel.html
http://srinikom.github.io/pyside-docs/PySide/QtGui/QListView.html
http://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
'''

'''
TODO:
current default mode is lookdev. which assumes current scene only have one asset.
adding in lighting mode which just do general naming convention checking and operates
naming and asset string checking on only selected
'''
import sys
import os
import re
#import logging
import maya.cmds as mc
from functools import partial
from PySide import QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
import shiboken
from shaderRenamerGui import Ui_shaderRenamerGUI
from globals import *
import logger
reload(logger)
import utils
reload(utils)

#simple logger
# logger = logging.getLogger('shaderRenamer')
# logger.setLevel(logging.DEBUG)

logger = logger.getLogger()


def maya_main_window():
	#Get the maya main window as a QMainWindow instance
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget)
	else:
		logger.warning("now window found.")


# class MouseEventFilter(QtCore.QObject):
#     def eventFilter(self, obj, event):
#         if event.type() == QtCore.QEvent.KeyPress:
#             return True
#         return False


class ShaderRenamerWindow(QtGui.QMainWindow, Ui_shaderRenamerGUI):

	def __init__(self, parent=maya_main_window()):
		#init
		super(ShaderRenamerWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("Shader Renamer")
		logger.info("setting up ui...")

		DEFAULT_ASSET_STRING = "asset"
		DEFAULT_VARIATION_STRING = "A"
		self.INFO_CLEAN = ""
		#self.INFO_DIRTY = "Please rename shader: (ASSET)_(shader)_(variation)_shad"
		self.INFO_DIRTY = "shader Name invalid. please rename."
		self.INFO_NAMING = "shader Name already exist."
		self.INIT_INDEX = "2"

		self.ASSET = ""
		self.VARIATION = ""
		self.VARIATION_STR_INDEX = -2
		DEFAULT_VARIATION_STRING = "A"

		#set models
		self.shaderModel = ShadersItemModel()
		self.shaderModel.setSortRole(QtCore.Qt.ToolTipRole)
		self.shadersListView.setModel(self.shaderModel)
		
		self.dependencyModel = DependenciesItemModel()
		self.dependencyModel.setSortRole(QtCore.Qt.ToolTipRole)
		self.dependenciesListView.setModel(self.dependencyModel)

		#selection mode
		self.geoAssignedListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.shadersListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.dependenciesListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		#self.shadersListView.setStyleSheet("background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #25262d, stop: 0.7 #242424 );")


		#find asset if not use shot name
		rcnulls = self.getAssetInScene()
		if rcnulls:
			if len(rcnulls) != 0:
				logger.warning("found more than one asset in the scene. use the first one.")
				#assume we only have one asset in the scene for now
				assetName = mc.getAttr(rcnulls[0]+".assetString")
		else:
			#use the shot name
			try:
				shot = os.getenv("SHOT")
				if shot:
					assetName = shot
				else:
					logger.warning("can not get shot. use default name")
					assetName = DEFAULT_ASSET_STRING

			except:
				logger.error("error getting shot. use default name")
				assetName = DEFAULT_ASSET_STRING


		#fill this in when adding variation support
		variationName = DEFAULT_VARIATION_STRING

		#set initial values
		logger.info("assigning initial values.")
		self.assetLineEdit.setText(assetName)
		self.ASSET = assetName
		self.variationLineEdit.setText(variationName)
		self.VARIATION = variationName

		#rx = QtCore.QRegExp("-?\\d{1,3}")
		#validator = QtGui.QRegExpValidator(rx, self)
		#self.shaderNameLineEdit.setValidator(validator)

		activePallet = QtGui.QPalette()
		activePallet.setColor(QtGui.QPalette.Text, QtCore.Qt.lightGray)
		activePallet.setColor(QtGui.QPalette.Background, QtCore.Qt.darkGray)

		disablePallet = QtGui.QPalette()
		disablePallet.setColor(QtGui.QPalette.Text, QtCore.Qt.gray)

		self.assetLineEdit.setPalette(disablePallet)
		self.variationLineEdit.setPalette(disablePallet)
		self.shaderNameLineEdit.setPalette(activePallet)


		#signals.
		self.renameButton.clicked.connect(self.rename)
		self.setNameButton.clicked.connect(self.setSelectedNames)
		self.setNodeNameButton.clicked.connect(self.setSelectedNodeNames)
		self.cancel_Button.clicked.connect(self.close)
		self.refreshButton.clicked.connect(self.refresh)
		self.assetLineEdit.textEdited.connect(self.assetNameChanged)
		self.assetLineEdit.editingFinished.connect(self.assetNameFinished)
		self.variationLineEdit.textChanged.connect(self.variationChanged)

		#self.shaderNameLineEdit.returnPressed.connect(self.setSelectedNames)
		self.shadersListView.clicked[QtCore.QModelIndex].connect(partial(self.itemClicked, "shaderView"))
		self.dependenciesListView.clicked[QtCore.QModelIndex].connect(partial(self.itemClicked, "dependencyView"))

		self.geoAssignedListWidget.clicked.connect(self.selectGeo)
		self.shaderModel.dataChanged.connect(self.nameChanged)
		self.dependencyModel.dataChanged.connect(self.nodeNameChanged)

		#init the shader list
		self.refresh()


	def refresh(self):
		#refresh the shaders list and the dependencies list
		logger.info("refreshing shaders and dependencies list.")
		self.shaderModel.clear()
		self.shadersToLoad, self.geoConnections, self.shaderDependencies = self.getAllShaders()

		row = 0
		#load the shaders into list view
		for shader in self.shadersToLoad.keys():
			print shader
			item = ShaderItem(shader)
			item.validateName(self.assetLineEdit.text(), self.variationLineEdit.text())
			self.shaderModel.setItem(row, 0, item)
			self.shaderModel.sort(QtCore.Qt.DisplayRole)
			#model.clicked[row].connect(self.clicked)
			row += 1

		row = 0
		#load the shaders into list view
		filteredChildList = self.filterAllDependencies()
		#print "filtered childs to add: ", filteredChildList
		#message = '%s:%s' % (i, filteredChildList[i].items())
		#logger.debug("filtered childs to add: " + message)
		for node in filteredChildList:

			#ignore nodes
			if node in ignoreNodes:
				continue

			item = DependencieItem(node)
			item.validateName(self.assetLineEdit.text(), self.variationLineEdit.text())
			self.dependencyModel.setItem(row, 0, item)
			self.dependencyModel.sort(QtCore.Qt.DisplayRole)
			#model.clicked[row].connect(self.clicked)
			row += 1

	def filterAllDependencies(self):
		#return the dependency list for adding to list view.
		nodesToAdd = []
		for shader in self.shaderDependencies.keys():
			nodesToAdd += self.shaderDependencies[shader]
		#blast same nodes
		nodesToAdd = list(set(nodesToAdd))
		return nodesToAdd



	def getAllShaders(self):
		#returns all shaders in the scene. that's connected to a shading group.
		#ignoreSg = ['initialParticleSE', 'initialShadingGroup']
		readonlySg = mc.ls(readOnly=True)

		shadingGroups = mc.ls(type="shadingEngine")
		#stores shaders and coresponding shading groups
		allShaders = dict()
		#stores sading group and connected geo
		allMeshConnections = dict()
		#stores all the child nodes for the shader
		allDependencies = dict()

		logger.info("getting all shaders in the scene.")
		for sg in shadingGroups:
			if sg not in readonlySg:
				if sg not in ignoreSg:
					#TODO: add in displacement, volume and other renderer specific inputs
					#for now just get the surface shader
					connectedShader = mc.connectionInfo(sg+".surfaceShader", sfd=True)

					#get surface shader
					if connectedShader:
						print sg, connectedShader
						connectedShader = connectedShader.split(".")[0]
						allDependencies[connectedShader] = utils.getUpstreamNodes(connectedShader)
						allShaders[connectedShader] = sg

					#get displacement shader
					connectedDisp = mc.connectionInfo(sg+".displacementShader", sfd=True)
					if connectedDisp:
						connectedDisp = connectedDisp.split(".")[0]
						allDependencies[connectedDisp] = utils.getUpstreamNodes(connectedDisp)
						allShaders[connectedDisp] = sg

					#get volume shader
					connectedVolum = mc.connectionInfo(sg+".volumeShader", sfd=True)
					if connectedVolum:
						connectedVolum = connectedVolum.split(".")[0]
						allDependencies[connectedVolum] = utils.getUpstreamNodes(connectedVolum)
						allShaders[connectedVolum] = sg

					if connectedShader == "":
						logger.warning("no surface shader connected to : " + sg)
						continue
					print allShaders
					#print "connectedShader: ", connectedShader
					logger.debug("getting shaders geo connection and dependencies.")
					allMeshConnections[connectedShader] = mc.listConnections(sg, s=True, sh=True, type="mesh")
					#allDependencies[connectedShader] = utils.getUpstreamNodes(connectedShader)

		print allShaders, allMeshConnections, allDependencies
		return allShaders, allMeshConnections, allDependencies



	def getAssetInScene(self):
		#getting the asset. assuming we are only lookdeving one asset for now.
		try:
			rcnulls = mc.ls(type="rigCenterNode")
			return rcnulls
		except:
			logger.error("node type rigCenterNode not exist")
			return None

	def assetNameFinished(self):
		#print "asset name edit done."
		#set text color back to valid
		cleanEntries = self.getCleanEntry()
		#for i in cleanEntries:
			#i.setTextColor("valid")

	def itemHasAssetString(self,item):
		#return if asset name string data is initialized on the item.
		if item.assetString:
			return True
		else:
			return False


	def assetNameChanged(self):
		#asset name changed
		#update all clean entries with new asset name
		newAssetName = self.assetLineEdit.text()
		cleanEntries = self.getCleanEntry()

		if newAssetName == "":
			logger.debug("no asset name found.")
			return

		for i in cleanEntries:
			#shaderName = i.text()
			self.updateAssetString(i, self.ASSET, newAssetName)
		#set new asset name to current asset name
		self.ASSET = newAssetName
		self.validateAllShaders()

	def updateAssetString(self, item, oldAssetName, newAssetName):
		#set update asset name on item
		oldShaderName = item.text()

		#smart update. if found this item has name string data.
		if self.itemHasAssetString(item):
			newShaderName = "_".join([newAssetName, item.nodeString, item.variationString, item.subfixString])
			item.assetString = newAssetName
		else:
			#TODO: fill this with a better function to parse out the asset name.
			newShaderName = oldShaderName.replace(oldAssetName, newAssetName)


		logger.debug("asset name updated new shader name: " + newShaderName)
		item.setText(newShaderName)


		#update asset string

	def variationChanged(self):
		#variation changed
		#update all clean entries with new asset name
		newVariation = self.variationLineEdit.text()
		cleanEntries = self.getCleanEntry()

		if newVariation == "":
			logger.debug("no variation name found.")
			return

		for i in cleanEntries:
			#shaderName = i.text()
			self.updateVariationString(i, self.VARIATION, newVariation)

		self.VARIATION = newVariation
		self.validateAllShaders()


	def updateVariationString(self, item, oldVariation, newVariation):
		oldShaderName = item.text()

		#smart update. if found this item has name string data.
		if self.itemHasAssetString(item):
			newShaderName = "_".join([item.assetString, item.nodeString, newVariation, item.subfixString])
			item.variationString = newVariation
		else:
			#ok, so the -2 element will be the variation.
			#TODO: fill this with a better function to parse out the asset name.
			nameList = oldShaderName.split("_")
			nameList.pop(self.VARIATION_STR_INDEX)
			nameList.insert(self.VARIATION_STR_INDEX+1, newVariation)
			#print nameList
			newShaderName = "_".join(nameList)

		logger.debug("variation updated new shader name: " + newShaderName)
		item.setText(newShaderName)



	def getCleanEntry(self):
		#retruns a list of clean entries
		cleanEntries = []

		#get clean entries from shader view
		numShaders = self.shaderModel.rowCount()
		for i in range(0, numShaders):
			item = self.shaderModel.item(i)
			logger.debug(item.text() + " is clean: " + str(item.clean))
			if item.clean:
				cleanEntries.append(item)

		#get clean entries from dependency view
		numShaders = self.dependencyModel.rowCount()
		for i in range(0, numShaders):
			item = self.dependencyModel.item(i)
			logger.debug(item.text() + " is clean: " + str(item.clean))
			if item.clean:
				cleanEntries.append(item)

		return cleanEntries


	def validateAllShaders(self):
		#validate all shader names based on current settings
		logger.debug("validating all shader names.")
		#shaderView
		numShaders = self.shaderModel.rowCount()
		self.shaderModel.blockSignals(True)
		for i in range(0, numShaders):
			item = self.shaderModel.item(i)
			item.validateName(self.assetLineEdit.text(),self.variationLineEdit.text())
		self.shaderModel.blockSignals(False)

		#dependency view
		numShaders = self.dependencyModel.rowCount()
		self.dependencyModel.blockSignals(True)
		for i in range(0, numShaders):
			item = self.dependencyModel.item(i)
			item.validateName(self.assetLineEdit.text(),self.variationLineEdit.text())
		self.dependencyModel.blockSignals(False)
		#refresh view
		#self.shadersListView.refresh()


	def nameChanged(self, index):
		#new shader name entered. check if it's valid
		#re chek
		item = self.shaderModel.item(index.row())
		numShaders = self.shaderModel.rowCount()
		changedItemRow = item.index().row()
		#block signals until functions is done
		self.shaderModel.blockSignals(True)
		item.validateName(self.assetLineEdit.text(), self.variationLineEdit.text())
		self.shaderModel.blockSignals(False)

	def nodeNameChanged(self, index):
		#new node name entered. check if it's valid
		#re chek
		item = self.dependencyModel.item(index.row())
		numShaders = self.dependencyModel.rowCount()
		changedItemRow = item.index().row()
		#block signals until functions is done
		self.dependencyModel.blockSignals(True)
		item.validateName(self.assetLineEdit.text(), self.variationLineEdit.text())
		self.dependencyModel.blockSignals(False)



	def setSelectedNames(self):
		#set the name for selected shaders
		logger.info("set name for selected shaders.")
		selectedIndexes = self.shadersListView.selectedIndexes()
		for i in selectedIndexes:
			self.currentIndex = i
			self.setName(self.currentIndex, "shaderView")

	def setSelectedNodeNames(self):
		#set the name for selected nodes
		logger.info("set name for selected node.")
		selectedIndexes = self.dependenciesListView.selectedIndexes()
		for i in selectedIndexes:
			self.currentIndex = i
			self.setNodeName(self.currentIndex, "dependencyView")


	def setName(self, selectedIndex, view):
		logger.info("set name for shader")
		#selectedIndex = self.shadersListView.selectedIndexes()[0].row()
		selectedItem = self.shaderModel.item(selectedIndex.row())
		if self.buildItemName(selectedItem, subfix=selectedItem.subfixString):
			numShaders = self.shaderModel.rowCount()
			#check if there are shaders named the same
			for i in range(0, numShaders):
				#item = self.shaderModel.item(i)
				#print "checking " + self.shaderNameToSet
				#print "against: " + self.shaderModel.item(i).text()
				if self.shaderNameToSet == self.shaderModel.item(i).text():
					logger.debug("name clash, incrementing name " + self.shaderNameToSet)
					self.shaderNamePlusPlus(self.shaderNameLineEdit.text(), view)
					return
			#set the name
			selectedItem.setText(self.shaderNameToSet)


	def setNodeName(self, selectedIndex, view):
		logger.info("set name for node")
		#selectedIndex = self.shadersListView.selectedIndexes()[0].row()
		selectedItem = self.dependencyModel.item(selectedIndex.row())
		nodeType = selectedItem.nodeType
		#print "nodeType: ", nodeType
		if self.buildItemName(selectedItem, subfix=selectedItem.subfixString):
			#print self.shaderNameToSet
			numShaders = self.dependencyModel.rowCount()
			#check if there are shaders named the same
			for i in range(0, numShaders):
				#item = self.shaderModel.item(i)
				#print "checking " + self.shaderNameToSet
				#print "against: " + self.dependencyModel.item(i).text()
				if self.shaderNameToSet == self.dependencyModel.item(i).text():
					logger.debug("name clash, incrementing name " + self.shaderNameToSet)
					self.shaderNamePlusPlus(self.shaderNameLineEdit.text(), view)
					return
			#set the name
			selectedItem.setText(self.shaderNameToSet)


	def shaderNamePlusPlus(self, name, view):
		#add one to shader name
		re1='.*?'	# Non-greedy match on filler
		re2='(\\d+)'	# Integer Number 1
		re3='($)'
		rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
		m = rg.search(name)
		if m:
			num=m.group(1)
			#print "("+num+")"+"\n"
			newName = name.replace(str(num), "")
			newNum = int(num)+1
			#print newName, newNum
			newName = newName + str(newNum)#.zfill(2)
			#print "set shader name to :" + newName
			self.shaderNameLineEdit.setText(newName)
			if view == "shaderView":
				self.setName(self.currentIndex, view)
			elif view == "dependencyView":
				self.setNodeName(self.currentIndex, view)
		else:
			name = name+self.INIT_INDEX
			self.shaderNameLineEdit.setText(name)
			if view == "shaderView":
				self.setName(self.currentIndex, view)
			elif view == "dependencyView":
				self.setNodeName(self.currentIndex, view)


	def buildItemName(self, item, subfix):
		#return the full name to set for the shader and nodes item based on current settings.
		assetString = self.assetLineEdit.text()
		#print assetString
		if assetString == "":
			self.statusBar.showMessage("no asset name found.")
			return False

		nodeString = self.shaderNameLineEdit.text()
		#print nodeString
		if nodeString == "":
			self.statusBar.showMessage("no shader string found.")
			return False

		variationString = self.variationLineEdit.text()
		if variationString == "":
			self.statusBar.showMessage("no variation name found.")
			return False

		#store the setting in the item
		item.assetString = assetString
		item.nodeString = nodeString
		item.variationString = variationString

		#subfix = self.subfixLabel.text()
		self.shaderNameToSet = "_".join([assetString, nodeString, variationString, subfix])
		return True


	def itemClicked(self, view, index):
		#item clicked in the shader view
		if view == "shaderView":
			item = self.shaderModel.itemFromIndex(index)
			mc.select(item.oldName)
			self.shaderTypeLabel.setText(item.nodeType)
			# print index.row()
			# print self.shaderModel.itemData(index)
			# print item.toolTip()
			shader = item.oldName

			self.geoAssignedListWidget.clear()
			assignedGeo = self.geoConnections[shader]
			if assignedGeo:
				for geo in assignedGeo:
					self.geoAssignedListWidget.addItem(geo)

		if view == "dependencyView":
			self.geoAssignedListWidget.clear()
			item = self.dependencyModel.itemFromIndex(index)
			mc.select(item.oldName)
			self.nodeTypeLabel.setText(item.nodeType)
			# print index.row()
			# print self.shaderModel.itemData(index)
			# print item.toolTip()

		#set info based on item state
		if item.clean:
			self.statusBar.showMessage(self.INFO_CLEAN)
		else:
			self.statusBar.showMessage(self.INFO_DIRTY)


		#load name into node string field
		#if the item was set before use the seted data
		if item.nodeString:
			logger.debug("using node string on item.")
			newName = item.nodeString
		else:
			logger.debug("parsing node string...")
			newName = self.parseShaderName(item.text(), item.subfixString)
		self.shaderNameLineEdit.setText(newName)


	def parseShaderName(self, name, subfixString):
		#before comming up with a betterway to track shader strings
		#try the best to parse out the shader string in the full shader name.
		#TODO: Kill subfixLabel
		import unicodedata
		nameList = name.split("_")

		#if nameList[-1] == self.subfixLabel.text()[1:]:
		if nameList[-1] == subfixString:
			#print self.subfixLabel.text()[1:]
			nameList.pop()
			nameList.pop()

		upper = []
		for i in nameList:
			unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			if i.isupper() == True:
				upper.append(i)

		nameList =[item for item in nameList if item not in upper]
		return "_".join(nameList)


	def selectGeo(self,index):
		#select geo in maya scene.
		mc.select(clear=True)
		selectedItems = self.getAllSelectedGeo()
		for i in selectedItems:
			#row = index.row()
			#shape = self.geoAssignedListWidget.item(row).text()
			shape = i.text()
			transform = mc.listRelatives(shape, p=True, type="transform")
			mc.select(transform, add=True)


	def getAllSelectedGeo(self):
		#returns all hilighted geo in the geo list widget.
		selectedItems = self.geoAssignedListWidget.selectedItems()
		return selectedItems


	def rename(self):
		#do the rename.

		logger.info("renaming shaders.")
		numShaders = self.shaderModel.rowCount()
		for i in range(0, numShaders):
			item = self.shaderModel.item(i)
			originalShaderName = item.oldName
			newShaderName = item.text()

			originalSGName = self.shadersToLoad[originalShaderName]
			newSGName = newShaderName + "SG"

			if originalShaderName != newShaderName:
				#rename shader
				logger.debug(originalShaderName + " => " + newShaderName)
				mc.rename(originalShaderName, newShaderName)

			#rename the shading group
			self.renameShadingGroup(originalSGName, newSGName)


		logger.info("renaming dependency nodes.")
		numNodes = self.dependencyModel.rowCount()
		for i in range(0, numNodes):
			item = self.dependencyModel.item(i)
			originalNodeName = item.oldName
			newNodeName = item.text()
			if originalNodeName != newNodeName:
				#rename shader
				logger.debug(originalNodeName + " => " + newNodeName)
				mc.rename(originalNodeName, newNodeName)

		#done
		mc.warning("rename shaders succesful.")

		#close or refresh?
		#self.close()
		self.refresh()


	def renameShadingGroup(self, oldName, newName):
		#rename the shading group to match shader
		if oldName != newName:
			mc.rename(oldName, newName)
			logger.debug("renaming shading group.")
			logger.info(oldName + " => " + newName)



class ShadingNodeItem(QtGui.QStandardItem):
	#mother class for all standard items
	def __init__(self, name):
		super(ShadingNodeItem, self).__init__()
		self.setText(name)
		#self.setEditable(False)
		self.clean = False
		self.oldName = name
		self.nodeType = mc.nodeType(self.oldName)
		self.setToolTip(self.nodeType)

		self.assetString = None
		self.nodeString = None
		self.variationString = None

		self.DEFAULT_ICON = QtGui.QIcon(os.getenv("MAYA_LOCATION")+"/icons/fpe_okPaths.png")
		self.WARNING_ICON = QtGui.QIcon(os.getenv("MAYA_LOCATION")+"/icons/fpe_someBrokenPaths.png")

		self.setIcon(self.WARNING_ICON)

	def validateName(self, asset, variation):
		#print "validating shader name ..."

		if utils.validShaderName(asset, variation, self.text()):
			#print "good shader name"
			self.setIcon(self.DEFAULT_ICON)
			self.clean = True
			#self.setTextColor("valid")

		else:
			logger.debug("bad name: " + self.text())
			self.setIcon(self.WARNING_ICON)
			self.clean = False


	def setTextColor(self, color="default"):
		#set text color
		if color == "default":
			#self.setData(9,0)
			pass
		elif color == "valid":
			pass
			#self.setData(QtGui.QColor("#3d8a3d"),QtCore.Qt.TextColorRole)
			#self.setData(QtGui.QColor("#cae3c3"),QtCore.Qt.TextColorRole)
		elif color == "editing":
			#self.setData(QtGui.QColor("#bde8b1"),QtCore.Qt.TextColorRole)
			pass
		# elif color == "warning":
		#self.setData(QtGui.QColor("#FF333D"),QtCore.Qt.TextColorRole)
		#self.setData(QtGui.QColor("#FF333D"),QtCore.Qt.BackgroundColorRole)

	def setBackgroundColor(self):
		#TODO: define the colors some where
		#set background color :)
		if self.nodeType in mayaNodesDict["shader"]:
			color = "#383838"
		elif self.nodeType in mayaNodesDict["texture2D"]:
			#give file nodes it's own color
			if self.nodeType == "file":
				color = "#2b458b"
			else:
				color = "#2d5867"
		elif self.nodeType in mayaNodesDict["texture3D"]:
			color = "#2c003a"
		elif self.nodeType in mayaNodesDict["utility"]:
			color = "#1e2e4d"
		elif self.nodeType in mayaNodesDict["placeTexture"]:
			color = "#654433"
		else:
			color = "#653359"
		self.setData(QtGui.QColor(color),QtCore.Qt.BackgroundColorRole)


#item for shader items.
class ShaderItem(ShadingNodeItem):
	def __init__(self, shaderName):
		ShadingNodeItem.__init__(self, shaderName)

		self.subfixString = "shad"
		self.setBackgroundColor()

#item for all dependency items
class DependencieItem(ShadingNodeItem):
	def __init__(self, nodeName):
		ShadingNodeItem.__init__(self, nodeName)

		self.nodeType = mc.nodeType(self.oldName)
		self.subfixString = self.nodeType
		self.setBackgroundColor()




class ParentItem(QtGui.QStandardItem):
	#mother class for all standard items
	def __init__(self, name):
		super(ShadingNodeItem, self).__init__()
		self.setText(name)
		#self.setEditable(False)




class ShadersItemModel(QtGui.QStandardItemModel):
	def __init__(self):
		super(ShadersItemModel, self).__init__()
		logger.debug("shader view model created.")

class DependenciesItemModel(QtGui.QStandardItemModel):
	def __init__(self):
		super(DependenciesItemModel, self).__init__()
		logger.debug("dependencies model view created.")


def main(debug=False):
	#launch shader renamer
	global win
	try:
		win.close()
	except:
		pass
	win = ShaderRenamerWindow()
	win.show()
	return

if __name__ == "__main__":
	pass
	# import sys
	# sys.path.insert(0,"/USERS/chichang/workspace/shaderRenamer")
	# import shaderRenamerMaya
	# reload(shaderRenamerMaya)
	# shadrenamer = shaderRenamerMaya.ShaderRenamerWindow()
	# shadrenamer.show()
