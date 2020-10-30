"""
Import WFDS output files into Paraview easily.
Run from inside the Paraview GUI's Python shell with the appropriate path assigned to 'outputPath'

author: @braddeibert
"""

from paraview.simple import *
import os

def readWFDS(outputPath):
    os.chdir(outputPath)
    contents = os.listdir(".")

    # place all mesh files (.xyz) into a list
    xyzFiles = []
    for item in contents:
        if item[len(item)-4:] == '.xyz':
            xyzFiles.append(item)

    # for each mesh file, find and place all corresponding data files (.q) into a list
    readers = []
    for mesh in xyzFiles:
        qFiles = []
        for item in contents:
            if (item[len(item)-2:] == '.q' and item.find(mesh[:len(mesh)-4]) != -1):
                qFiles.append(outputPath + '/' + item)

        qFiles.sort()

        # read the mesh & data into Paraview using the PLOT3DReader
        reader = PLOT3DReader(FileName=(outputPath + '/' + mesh), QFileName=qFiles, FunctionFileName='')
        readers.append(reader)

    # group all imported meshes
    groupdata = GroupDatasets(Input=readers)

print("*** READ IN WFDS FILES ***\n")
print("readWFDS(your_WFDS_output_directory_here)\nCall readWFDS with the correct path to your WFDS output folder containing .xyz & .q files.\nThe function will read in all mesh & data files using Paraview's PLOT3DReaders. ")
