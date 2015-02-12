import maya.cmds as mc

ignoreSg = ['initialParticleSE', 'initialShadingGroup']
ignoreNodes = ['defaultColorMgtGlobals']

#get common maya node types.
mayaNodesDict = dict()
mayaNodesDict["shader"] = mc.listNodeTypes("shader")
mayaNodesDict["texture2D"] = mc.listNodeTypes("texture/2D")
mayaNodesDict["texture3D"] = mc.listNodeTypes("texture/3D")
mayaNodesDict["utility"] = mc.listNodeTypes("utility")
mayaNodesDict["placeTexture"] = ["place2dTexture", "place3dTexture"]
mayaNodesDict["utility"].remove("place2dTexture")
mayaNodesDict["utility"].remove("place3dTexture")

'''
subfixDict = dict()

blendColors
bump2d
bump3d
choice
chooser
clamp
condition
contrast
curveInfo
decomposeMatrix
distanceBetween
doubleShadingSwitch
eulerToQuat
frameCache
gammaCorrect
heightField
hsvToRgb
inverseMatrix
lightInfo
luminance
multDoubleLinear
multMatrix
multiplyDivide
particleSamplerInfo
plusMinusAverage
projection
quadShadingSwitch
quatAdd
quatConjugate
quatInvert
quatNegate
quatNormalize
quatProd
quatSub
quatToEuler
remapColor
remapHsv
remapValue
reverse
rgbToHsv
samplerInfo
setRange
singleShadingSwitch
stencil
surfaceInfo
surfaceLuminance
transposeMatrix
tripleShadingSwitch
unitConversion
uvChooser
vectorProduct
wtAddMatrix
xThinFilmInterference
'''