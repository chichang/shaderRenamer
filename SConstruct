#!/usr/bin/python2.6
import os
env = Environment()


package_files = [
    'shaderRenamerGui.py',
    'shaderRenamerMaya.py',
    ]

supported_maya_versions = ['2014', '2015']


destMayaReleases = []


for mayaver in supported_maya_versions:
    destMayaReleases.append("/X/tools/maya/python/%s-x64" % mayaver)


# standard install
env.Install(destMayaReleases, package_files)


# release install
env.Alias("install-release", [destMayaReleases,])
