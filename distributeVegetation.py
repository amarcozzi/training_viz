"""
    This script takes in a blender2FDS input file with &TREE lines.
    It will load in the input file, and modify the &TREE line to create a runnable
    WFDS LS4 simulation

"""
import sys
import numpy as np


def meters(feet):
    return feet / 3.281


def modify_tree(filein, fileout):
    # parse through the lines in the input file
    for line in filein:
        # look for the &TREE designator
        if '&TREE' in line:     # This can be expanded for different vegetation definitions in the future
            line_without_tree = line.split('&TREE')[1]
            line_with_id, line_with_coords = line_without_tree.split("XYZ")
            line_coords = line_with_coords.replace('/','').strip()

            # First get the tree ID and give it a part_id, then give it a label with the unique
            # tree_id int variable
            # The part_id will be 'needles' in this primitive first version
            tree_id = int(line_with_id.split('ID=')[1].replace('\'',''))   # Grab the Tree ID number and make it an int
            line_part_id = ' PART_ID = \'needles\','     # Give the &TREE the part_id needles (can be changed later)
            line_label = ' LABEL = \'Tree_%d\' / \n' % tree_id  # Give the &TREE the label tree_(tree_id), change later!
            line_fuel_geom = ', FUEL_GEOM = \'CONE\','       # Give the &TREE a cone shape
            line_output_tree = "OUTPUT_TREE = .FALSE., "

            # Calculate crown width, crown base height and tree height
            # Future versions will read in crown width from the shape-file, and calculate the others based on that
            # For now I'm going to randomly draw values with a normal distribution
            # The crown_width data comes from the shape-file
            # crown_width
            crown_width_mean = 6.1311
            crown_width_stdev = 1.8356
            crown_width = crown_width_mean + np.random.normal() * crown_width_stdev
            line_crown_width = " CROWN_WIDTH = %.2f," % crown_width
            # crown base height
            crown_base_height_mean = 1.5
            crown_base_height_stdev = .35
            crown_base_height = crown_base_height_mean + np.random.normal() * crown_base_height_stdev
            line_crown_base_height = " CROWN_BASE_HEIGHT = %.2f" % crown_base_height
            # tree height
            tree_height_mean = 10
            tree_height_stdev = 2.5
            tree_height = tree_height_mean + np.random.normal() * tree_height_stdev
            line_tree_height = " TREE_HEIGHT = %.2f, " % tree_height

            # Put the whole thing back together!
            line = "&TREE" + line_part_id + " XYZ" + line_coords + line_fuel_geom + line_crown_width + line_crown_base_height \
                    + line_tree_height + line_output_tree + line_label

        fileout.write(str(line))

if __name__ == '__main__':

    # pass the inputfile through the command line
    if len(sys.argv) > 1:
        input = sys.argv[1]
    # name the input file in the script
    else:
        input = "input_test.fds"

    filename, extension = input.split('.')      # get the input file name / file extension from the input
    with open(input, "r") as filein:
        with open(filename + "_trees." + extension, 'w') as fileout:
            modify_tree(filein, fileout)
