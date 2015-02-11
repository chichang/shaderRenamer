#!/usr/bin/python2.6
import os
env = Environment()


package_files = [
    '__init__.py',
    'shaderRenamerGui.py',
    'shaderRenamerMaya.py',
    'utils.py',
    'globals.py',
    'logger.py',
    ]

supported_maya_versions = ['2014', '2015']


destMayaReleases = []


for mayaver in supported_maya_versions:
    destMayaReleases.append("/X/tools/maya/python/%s-x64/shaderRenamer" % mayaver)


# standard install
env.Install(destMayaReleases, package_files)


# release install
env.Alias("install-release", [destMayaReleases,])
