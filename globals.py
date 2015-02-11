import maya.cmds as mc

ignorSg = ['initialParticleSE', 'initialShadingGroup']

#get common maya node types.
mayaNodesDict = dict()
mayaNodesDict["shader"] = mc.listNodeTypes("shader")
mayaNodesDict["texture2D"] = mc.listNodeTypes("texture/2D")
mayaNodesDict["texture3D"] = mc.listNodeTypes("texture/3D")
mayaNodesDict["utility"] = mc.listNodeTypes("utility")
mayaNodesDict["placeTexture"] = ["place2dTexture", "place3dTexture"]
mayaNodesDict["utility"].remove("place2dTexture")
mayaNodesDict["utility"].remove("place3dTexture")
