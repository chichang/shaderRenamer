
import maya.cmds as mc
import re
import logger
reload(logger)

logger = logger.getLogger()

def getUpstreamNodes(root):
	#pass in a node. returns all upstream nodes.

	MAX_SEARCH_LEVEL = 50

	allNodes = []
	#start with the root
	conectedNodes=[]

	nextLevel = [root]
	logger.warning("root shader for searching connections: " + root)

	#I am afraied of while loops... so lets set a max for now and break when done.
	for l in range(0, MAX_SEARCH_LEVEL):
		logger.warning("searching level: " + str(l))
		#print "next level nodes: ", nextLevel
		if len(nextLevel) == 0:
			logger.warning("no more nodes to search.")
			break
		
		for i in nextLevel:
			logger.warning("getting connections for: " + i)

			try:
				nextLevel.remove(i)
			except ValueError:
				pass

			#print "next level nodes: ", nextLevel

			conectedNodes = mc.listConnections(i, sh=True, s=True, d=False)
			#print conectedNodes

			try:
				conectedNodes = list(set(conectedNodes))
				logger.warning(i + " connected nodes: ")
				for i in conectedNodes:
					logger.warning(i)
				nextLevel += conectedNodes
	
			except:
				logger.debug("nothing connected to : " + i)
				continue
                        
			allNodes += conectedNodes
			
			nextLevel = list(set(nextLevel))

		logger.warning(i + " searching next level nodes: ")
		for i in nextLevel:
			logger.warning(i)

		conectedNodes=[]
	
	#print allNodes
	return allNodes


#allNodes = getUpstreamNodes("UHAUL_metal_A_shad")



def validShaderName(assetName, variationName, shaderName):
    #TODO: pass node type into reg7.
    #print "checking shader name: "+ shaderName

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='('+variationName+')' # Word 2
    re6='(_)'   # Any Single Character 3
    re7='.*?'   # Word 3
    re8='($)'

    rg1 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m1 = rg1.search(shaderName)

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='('+variationName+')' # Word 2
    re6='(_)'   # Any Single Character 3
    #re7='((?:[a-z][a-z]+))'    # Word 3
    re7='.*?'   # Word 3
    re8='($)'

    rg2 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m2 = rg2.search(shaderName)

    #print m1, m2

    if m1 or m2:
        word1=m2.group(1)
        c1=m2.group(2)
        c2=m2.group(3)
        word2=m2.group(4)
        c3=m2.group(5)
        word3=m2.group(6)
        return True
    else:
        return False
