
import maya.cmds as mc
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
	logger.debug("root shader for searching connections: " + root)

	#I am afraied of while loops... so lets set a max for now and break when done.
	for l in range(0, MAX_SEARCH_LEVEL):
		#print "searching level: " + str(l)
		#print "next level nodes: ", nextLevel

		if len(nextLevel) == 0:
			#print "no more nodes to search."
			break
		
		for i in nextLevel:
			#print "getting connections for: " + i

			try:
				nextLevel.remove(i)
			except ValueError:
				pass

			#print "next level nodes: ", nextLevel

			conectedNodes = mc.listConnections(i, sh=True, s=True, d=False)
			#print conectedNodes

			try:
				conectedNodes = list(set(conectedNodes))
				#print i + " : ", conectedNodes
				nextLevel += conectedNodes
	
			except:
				#print "nothing connected to : " + i
				continue
                        
			allNodes += conectedNodes
			
			nextLevel = list(set(nextLevel))

		#print "searching next level for connections: ", nextLevel, "\n"
		#
		conectedNodes=[]
	
	#print allNodes
	return allNodes


#allNodes = getUpstreamNodes("UHAUL_metal_A_shad")