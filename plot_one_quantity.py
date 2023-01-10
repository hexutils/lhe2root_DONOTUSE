import argparse
import lhe2root_methods

def ran(s):
    """A function to define the range format for this program

    Arguments:
        s -- The range in question

    Raises:
        argparse.ArgumentTypeError: Raises an error if formatted incorrectly

    Returns:
        two floats for the range bounds
    """
    try:
        left, right = map(float, s.split(','))
        return (left, right)
    except:
        raise argparse.ArgumentTypeError("Ranges must be of form 'left, right'!")

parser = argparse.ArgumentParser()

parser.add_argument('filenames',nargs='+',
                    help="The file you want to plot")

parser.add_argument('-v','--value',default='M4L', choices=list(lhe2root_methods.beautified_title.keys()),
                    help="The attributes you want to plot.")

parser.add_argument('-r','--range', default=(6,9), type=ran,
                    help='The ranges for your attributes. Enclose your ranges with quotes and a leading space i.e. " -3.14,3.14"')

parser.add_argument('-n', '--nbins', type=int, default=100,
                    help="The number of bins you want")

parser.add_argument('-l', '--labels', nargs="+", type=str, default=None,
                    help="The legend label for each filename")

parser.add_argument('-no', '--norm', action="store_true",
                    help="Option to normalize the area of the histogram to 1")

parser.add_argument('-t', '--title', default="",
                    help="Optional Figure Title")

args = parser.parse_args()



if __name__ == "__main__":
    
    lhe2root_methods.plot_one_quantity(args.filenames, args.value, args.range, args.nbins, args.labels, args.norm, args.title)