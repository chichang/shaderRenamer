#!/usr/bin/python2.6

import os
env = Environment()

initFiles = [
    '__init__.py',
	'shaderRenamerGui.py',
    'shaderRenamerMaya.py',
    ]

# standard install
destInitReleases	= []

# debug install
testLibReleases     = []

#for pyver in ['2.6', '2.7']:
#    destLibReleases.append("/X/tools/python/mrx/pythonlib%s/XAssets" % pyver)
destInitReleases.append("/X/tools/python/users/python2.7/chichang/shaderRenamer")

# standard install
env.Install(destInitReleases, initFiles)

# debug install
#env.Install(testLibReleases, libFiles)
#env.Alias("install-release", [destLibReleases, destUtilReleases])
env.Alias("install-release", [destInitReleases])
#env.Alias("install-debug", [testLibReleases])







