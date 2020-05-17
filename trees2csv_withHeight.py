"""
Python script to create a .csv file containing WFDS tree data for visualization in Paraview

Requires a WFDS input file in the arguments

author: @braddeibert
"""

import os, sys, csv

#function below for retrieving tree coordinates
def getCenter(inputLine):
    if inputLine.find("XB") != -1:                      #RECTANGLE geometry
        inputLine = inputLine.split("XB=")
        inputLine = (inputLine[1]).split(",")

        output = [inputLine[0], inputLine[2], inputLine[4]]
        output.append(1)
        output = tuple(map(float, output))

        return output

    else:                                               #CONE, FRUSTUM, or CYLINDER type geometry
        inputLine = inputLine.split("XYZ=")
        inputLine = (inputLine[1]).split(",")

        output = inputLine[0:3]
        output.append(1)
        output = tuple(map(float, output))

        return output


if len(sys.argv) != 2:
    print('Please pass in a single valid WFDS input file. \nex: python3 trees2csv.py your_input_file_here.fds\n')
else:
    f = open(sys.argv[1])
    c = csv.writer(open('treeDataTest.csv', 'w'))
    c.writerow(['x', 'y', 'z', 'treeHeight'])

    #array to track tree locations (x, y)
    treeLocations = []

    #array to store trees. written to csv at end
    trees = []

    #tree counter for array accessing
    ctr = 0

    for line in f:
        if line[:5] == '&TREE':
            
            #get tree coordinates
            tree = getCenter(line)  

            if (tree[:2] in treeLocations):
                print("stacked coordinates")

                #get appropriate tree index
                treeNum = treeLocations.index(tree[:2])

                #increment tree height value in array
                treeData = list(trees[treeNum])
                treeData[3] += 1
                trees[treeNum] = tuple(treeData)

            else:
                #add tree data to array
                trees.append(tree)

                #add x,y coordinates of new tree to array, increment counter
                treeLocations.append(tree[:2])
                ctr += 1

            
    for tree in trees:
        #write the tree data to a csv file
        c.writerow(tree)
