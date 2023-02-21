import os
import argparse
import lhe_constants
import lhe2root_methods

exceptions = { #There is no reason to store LHE files in the pycache folder. Use this to hardcode other exceptions in
    '__pycache__',
}
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('argument', type=str,
                        choices=lhe_constants.lhe_2_root_options,
                        help="The argument to be passed to LHE2ROOT.py")

    parser.add_argument('-c',"--clean", action='store_true',
                        help="remove all produced ROOT files and re-create them")

    parser.add_argument('-cd', '--currentDirectory', type=str, default=os.getcwd(),
                        help="The directory you would like to recurse down from")

    parser.add_argument('-o', '--output', type=str, default='./',
                        help="The directory you would like to output to")

    parser.add_argument('-e','--exceptions', nargs='*',
                        help="Any folder exceptions you want to make to conversion. Useful if you have different argument types for LHE files",
                        default=[])

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Option to make the process verbose")

    parser.add_argument('-w', '--write', default="CrossSections.csv",
                        help='Option to write out cross sections to the file named here. Enter "" if you do not want a file written.')

    args = parser.parse_args()
    
    
    current_directory = args.currentDirectory
    exceptions = set(args.exceptions).union(exceptions)
    
    if not lhe2root_methods.check_for_MELA():
        raise FileNotFoundError("MELA path not found!")
    
    file_cross_sections = lhe2root_methods.recursively_convert(current_directory=current_directory, output_directory=args.output, 
                                                                argument=args.argument, verbose=args.verbose, 
                                                                exceptions=exceptions, write=args.write)