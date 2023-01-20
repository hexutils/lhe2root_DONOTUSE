import argparse
import lhefile_methods


parser = argparse.ArgumentParser()

parser.add_argument('filenames', type=str, nargs= "+",
                    help="The files you are slicing")

parser.add_argument('-n', '--num', type=int, required=True,
                    help="The number of events you would like")

args = parser.parse_args()


if __name__ == '__main__':
    for file in args.filenames:
        to_write = lhefile_methods.cut_down_to_size(file, args.num)
        
        filename = file.split('/')[-1]
        filepath = "/".join(file.split('/')[:-1])
        # print(filepath, filename)
        
        outfile = filepath + '/' + str(args.num) + "_SLICED" + filename
        with open(outfile, 'w+') as f:
            f.write(to_write)
            
        print("Dumped to", outfile)