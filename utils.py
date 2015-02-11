import maya.cmds as mc


def getUpstreamNodes(root):
    #pass in a node. returns all upstream nodes.
    
    MAX_SEARCH_LEVEL = 50

    allNodes = []
    #start with the root
    conectedNodes=[]

    nextLevel = [root]

    #I am afraied of while loops... so lets set a max for now and break when done.
    for l in range(0, MAX_SEARCH_LEVEL):
        print "searching level: " + str(l)
        
        if len(nextLevel) == 0:
            print "no more nodes to search."
            break
        
        for i in nextLevel:

            nextLevel.remove(i)
            print "getting connections for: " + i

            conectedNodes = mc.listConnections(i, sh=True, s=True, d=False)
            #print conectedNodes

            try:
                conectedNodes = list(set(conectedNodes))
                print i + " : ", conectedNodes
                nextLevel += conectedNodes
    
            except:
                print "nothing connected to : " + i
                continue

            allNodes += conectedNodes
            
            nextLevel = list(set(nextLevel))
    
        print "searching next level for connections: ", nextLevel, "\n"
        #
        conectedNodes=[]
    
    print allNodes
    return allNodes


# allNodes = getUpstreamNodes("plastic_01")
# mc.select(clear=True)
# for i in allNodes:
#     print i
#     mc.select(i, add=True)