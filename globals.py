import maya.cmds as mc

ignoreSg = ['initialParticleSE', 'initialShadingGroup']
ignoreNodes = ['defaultColorMgtGlobals']

#get common maya node types.
mayaNodesDict = dict()
mayaNodesDict["shader"] = mc.listNodeTypes("shader")
mayaNodesDict["texture2D"] = mc.listNodeTypes("texture/2D")
mayaNodesDict["texture3D"] = mc.listNodeTypes("texture/3D")
mayaNodesDict["utility"] = mc.listNodeTypes("utility")
mayaNodesDict["displacement"] = mc.listNodeTypes("shader/displacement")
mayaNodesDict["volume"] = mc.listNodeTypes("shader/volume")
mayaNodesDict["placeTexture"] = ["place2dTexture", "place3dTexture"]
mayaNodesDict["utility"].remove("place2dTexture")
mayaNodesDict["utility"].remove("place3dTexture")
