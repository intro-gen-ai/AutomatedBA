
import os
import sys
from pathlib import Path

# This check ensures that the following code block runs only when the script is executed directly
if __name__ == '__main__':
    # Get the absolute path to the directory containing cmdline.py
    current_dir = Path(__file__).parent.absolute()

    # Get the project root directory by going up two levels from the current directory
    # Adjust the number of parents based on your project structure
    project_root = current_dir.parent.parent

    # Add the project root directory to sys.path
    sys.path.insert(0, str(project_root))


import argparse
from src.util import ControlDict
from src.core.driver import layoutProcess




def parse_arguments():
    parser = argparse.ArgumentParser(description='Import sets of integers using tags e, m, p, s.')

    # Define the arguments for each tag with the expected type as a list of integers
    parser.add_argument('-e', '--e_set', nargs='+', type=int, default=[], help='Set of integers for encoding options')
    parser.add_argument('-m', '--m_set', nargs='+', type=int, default=[], help='Set of integers for model options')
    parser.add_argument('-p', '--p_set', nargs='+', type=int, default=[], help='Set of integers for prompt options')
    parser.add_argument('-i', '--i_set', nargs='+', type=int, default=[], help='Set of integers for instruction options')
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
    # - uncomment to run easily from vscode for testing. Change below to get the inputs you want
    m_set = set()
    m_set.add(1)
    s_set = set()
    s_set.add(1)
    
    layoutProcess(e_set, m_set, p_set, i_set, s_set)

if __name__ == "__main__":
    main()
