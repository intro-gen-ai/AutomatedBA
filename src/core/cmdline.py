
import os
import sys
# Add the parent directory of the current file to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
print(current_dir)

import argparse
from converter import ControlDict
from driver import layoutProcess




def parse_arguments():
    parser = argparse.ArgumentParser(description='Import sets of integers using tags e, m, p, s.')

    # Define the arguments for each tag with the expected type as a list of integers
    parser.add_argument('-e', '--e_set', nargs='+', type=int, default=[], help='Set of integers for encoding options')
    parser.add_argument('-m', '--m_set', nargs='+', type=int, default=[], help='Set of integers for model options')
    parser.add_argument('-p', '--p_set', nargs='+', type=int, default=[], help='Set of integers for prompt options')
    parser.add_argument('-i', '--i_set', nargs='+', type=int, default=[], help='Set of integers for prompt options')
    parser.add_argument('-s', '--s_set', nargs='+', type=int, default=[], help='Set of integers for semantics layer options')

    # Parse the arguments
    args = parser.parse_args()

    return args

def main():
    # Parse the command line arguments
    args = parse_arguments()

    # Extract the sets of integers for each tag
    e_set = args.e_set
    m_set = args.m_set
    p_set = args.p_set
    i_set = args.i_set
    s_set = args.s_set
    
    x = ControlDict()
    x.mode = 0

    my_set = set()
    my_set.add(1)

    layoutProcess(e_set, my_set, p_set, i_set, s_set)

if __name__ == "__main__":
    main()
